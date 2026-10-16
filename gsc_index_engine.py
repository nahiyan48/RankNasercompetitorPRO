#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console Official URL Inspection & Live Diagnosis Engine
Complies with Google Search Console URL Inspection API specifications.
Database: SQLite (sites, urls, inspections, findings, history, quotas)
"""

import os
import sys
import re
import json
import gzip
import time
import sqlite3
import urllib.request
import urllib.error
import urllib.parse
import math
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    BeautifulSoup = None

try:
    from google.oauth2 import service_account
    import google.auth.transport.requests
    HAS_GOOGLE_AUTH = True
except ImportError:
    service_account = None
    HAS_GOOGLE_AUTH = False

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsc_index_data.db")

# Exact Google Coverage State Mappings & Bengali Actionable Solutions (Section 8)
COVERAGE_STATE_MAP = {
    "Crawled - currently not indexed": {
        "reason_bn": "Google পেজটি ক্রল করে দেখেছে, কিন্তু কনটেন্ট কোয়ালিটি বা ভ্যালু যথেষ্ট মনে করেনি।",
        "solution_bn": "কনটেন্ট ইউনিক ও বিস্তারিত করুন, ২৫০০+ শব্দের EEAT গাইড যুক্ত করুন, সাইটের অন্য পেজ থেকে ইন্টারনাল লিঙ্ক দিন এবং থিন (thin) পেজ মার্জ করুন।"
    },
    "Discovered - currently not indexed": {
        "reason_bn": "Google URL টি সম্পর্কে জানে, কিন্তু ক্রল বাজেট বা সার্ভার লোডের কারণে এখনো ক্রল করেনি।",
        "solution_bn": "শক্তিশালী ইনবাউন্ড ইন্টারনাল লিঙ্ক তৈরি করুন, সার্ভার রেসপন্স স্পিড (TTFB) ঠিক করুন এবং XML সাইটম্যাপ আপডেট রাখুন।"
    },
    "URL is unknown to Google": {
        "reason_bn": "Google এই পেজটা চেনেই না (সার্চ ইনডেক্সে কোনো তথ্য নেই)।",
        "solution_bn": "পেজটি sitemap.xml-এ যোগ করুন, হোমপেজ/ক্যাটাগরি থেকে ইন্টারনাল লিঙ্ক দিন এবং Search Console-এ Request Indexing করুন।"
    },
    "Excluded by 'noindex' tag": {
        "reason_bn": "পেজের মেটা ট্যাগ বা X-Robots-Tag হেডারে 'noindex' দেওয়া আছে।",
        "solution_bn": "HTML-এর <meta name='robots' content='noindex'> অথবা সার্ভার হেডারের X-Robots-Tag থেকে noindex সরিয়ে ফেলুন।"
    },
    "Excluded by \u2018noindex\u2019 tag": {
        "reason_bn": "পেজের মেটা ট্যাগ বা X-Robots-Tag হেডারে 'noindex' দেওয়া আছে।",
        "solution_bn": "HTML-এর <meta name='robots' content='noindex'> অথবা সার্ভার হেডারের X-Robots-Tag থেকে noindex সরিয়ে ফেলুন।"
    },
    "Blocked by robots.txt": {
        "reason_bn": "robots.txt ফাইলের Disallow নির্দেশের কারণে Googlebot পেজে ঢুকতে পারছে না।",
        "solution_bn": "robots.txt ফাইলে গিয়ে সংশ্লিষ্ট URL বা ডিরেক্টরি থেকে Disallow রুল তুলে Allow রুল সেট করুন।"
    },
    "Not found (404)": {
        "reason_bn": "পেজটি সার্ভারে পাওয়া যায়নি (Broken 404 Error)।",
        "solution_bn": "পেজটি পুনরায় তৈরি করুন অথবা প্রাসঙ্গিক ক্যাটাগরি পেজে 301 Permanent Redirect সেট করুন এবং সাইটম্যাপ থেকে লিঙ্ক মুছুন।"
    },
    "Soft 404": {
        "reason_bn": "সার্ভার 200 OK দিচ্ছে কিন্তু পেজ খালি বা 'Page Not Found' জাতীয় ফাঁকা কন্টেন্ট দেখাচ্ছে।",
        "solution_bn": "আসল ও তথ্যবহুল কনটেন্ট যোগ করুন অথবা পেজটি সত্যিই না থাকলে সরাসরি 404 বা 410 Gone স্ট্যাটাস কোড প্রদান করুন।"
    },
    "Page with redirect": {
        "reason_bn": "URL টি অন্য কোনো পেজে রিডাইরেক্ট করে।",
        "solution_bn": "সাইটম্যাপ এবং অভ্যন্তরীণ লিঙ্কিংয়ে সরাসরি ফাইনাল ডেস্টিনেশন URL ব্যবহার করুন। রিডাইরেক্ট চেইন বন্ধ করুন।"
    },
    "Duplicate without user-selected canonical": {
        "reason_bn": "পেজের কনটেন্ট অন্য পেজের মতো ডুপ্লিকেট, কিন্তু কোনো canonical ট্যাগ দেওয়া নেই।",
        "solution_bn": "পেজের <head>-এ নিজের URL দিয়ে Self-referencing Canonical ট্যাগ যুক্ত করুন।"
    },
    "Duplicate, Google chose different canonical": {
        "reason_bn": "ইউজার এক URL ক্যানোনিকাল দিয়েছে, কিন্তু Google অন্য শক্তিশালী URL-কে আসল ক্যানোনিকাল ধরেছে।",
        "solution_bn": "আপনার ক্যানোনিকাল ট্যাগ এবং ইন্টারনাল অ্যাঙ্কর লিঙ্ক একই অভিন্ন URL-এ পয়েন্ট করুন এবং কনটেন্টকে আরও ইউনিক করুন।"
    },
    "Server error (5xx)": {
        "reason_bn": "Googlebot ভিজিট করার সময় সার্ভার ক্র্যাশ বা 500/502/503 ইন্টারনাল সার্ভার এরর দিয়েছে।",
        "solution_bn": "ওয়েব হোস্টিং সার্ভার কনফিগারেশন, PHP/Python এরর লগ এবং ডেটাবেস কানেকশন টাইমআউট ঠিক করুন।"
    },
    "Blocked due to access forbidden (403)": {
        "reason_bn": "Googlebot কে ফায়ারওয়াল বা সিকিউরিটি পলিসি দিয়ে ব্লক করা হয়েছে (403 Forbidden)।",
        "solution_bn": "Cloudflare / ModSecurity ফায়ারওয়ালে Googlebot IP এবং User-Agent কে Whitelist করুন।"
    },
    "Blocked due to unauthorized request (401)": {
        "reason_bn": "পেজে লগইন বা পাসওয়ার্ড প্রটেকশন (Basic Auth) রয়েছে।",
        "solution_bn": "পাবলিক পেজ হলে লগইন অথেনটিকেশন রিমুভ করুন যাতে সার্চ ইঞ্জিন ক্রল করতে পারে।"
    }
}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes SQLite schema for Google Search Console Index Engine"""
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property TEXT UNIQUE,
        property_type TEXT,
        sitemap_url TEXT,
        service_account_email TEXT,
        service_account_json TEXT,
        connected_at TEXT,
        last_check_at TEXT,
        total_urls INTEGER DEFAULT 0,
        indexed_count INTEGER DEFAULT 0,
        non_indexed_count INTEGER DEFAULT 0,
        unchecked_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active'
    );

    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER,
        url TEXT UNIQUE,
        source TEXT,
        first_seen TEXT,
        last_inspected_at TEXT,
        verdict TEXT DEFAULT 'UNCHECKED',
        coverage_state TEXT DEFAULT 'Not Inspected',
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url_id INTEGER,
        verdict TEXT,
        coverage_state TEXT,
        robots_txt_state TEXT,
        indexing_state TEXT,
        page_fetch_state TEXT,
        google_canonical TEXT,
        user_canonical TEXT,
        last_crawl_time TEXT,
        crawled_as TEXT,
        raw_json TEXT,
        checked_at TEXT,
        FOREIGN KEY(url_id) REFERENCES urls(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url_id INTEGER,
        check_name TEXT,
        result TEXT,
        message TEXT,
        checked_at TEXT,
        FOREIGN KEY(url_id) REFERENCES urls(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site_id INTEGER,
        date TEXT,
        total_urls INTEGER,
        indexed_count INTEGER,
        non_indexed_count INTEGER,
        unchecked_count INTEGER,
        snapshot_json TEXT,
        created_at TEXT,
        FOREIGN KEY(site_id) REFERENCES sites(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS quotas (
        property TEXT PRIMARY KEY,
        date TEXT,
        calls_count INTEGER DEFAULT 0,
        last_reset TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_urls_site_id ON urls(site_id);
    CREATE INDEX IF NOT EXISTS idx_urls_verdict ON urls(site_id, verdict);
    CREATE INDEX IF NOT EXISTS idx_urls_coverage ON urls(site_id, coverage_state);
    CREATE INDEX IF NOT EXISTS idx_inspections_url_id ON inspections(url_id);
    """)
    conn.commit()
    conn.close()


init_db()


class GSCIndexEngine:
    """Core Google Search Console URL Inspection & Live Diagnosis Engine"""

    def __init__(self):
        init_db()

    # -------------------------------------------------------------------------
    # 1. SITE & CREDENTIAL MANAGEMENT
    # -------------------------------------------------------------------------

    def get_service_account_token(self, sa_info: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """Generates Google OAuth2 Bearer Access Token for Service Account"""
        if not HAS_GOOGLE_AUTH:
            return None, "google.oauth2 library is not installed on system."
        try:
            scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
            creds = service_account.Credentials.from_service_account_info(sa_info, scopes=scopes)
            req = google.auth.transport.requests.Request()
            creds.refresh(req)
            return creds.token, None
        except Exception as e:
            return None, str(e)

    def test_connection(self, property_id: str, sa_json_data: Any) -> Dict[str, Any]:
        """Tests GSC Service Account connectivity and permissions for property"""
        try:
            if isinstance(sa_json_data, str):
                sa_info = json.loads(sa_json_data)
            else:
                sa_info = sa_json_data

            client_email = sa_info.get("client_email", "")
            if not client_email:
                return {
                    "success": False,
                    "message": "Service Account JSON-এ কোনো 'client_email' পাওয়া যায়নি।"
                }

            token, err = self.get_service_account_token(sa_info)
            if not token:
                return {
                    "success": False,
                    "client_email": client_email,
                    "message": f"Google Token জেনারেট ব্যর্থ হয়েছে: {err}"
                }

            # Attempt a live inspection test call on root URL of property
            test_url = property_id
            if test_url.startswith("sc-domain:"):
                domain = test_url.replace("sc-domain:", "").strip()
                test_url = f"https://{domain}/"

            if not test_url.endswith("/"):
                test_url += "/"

            api_endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "inspectionUrl": test_url,
                "siteUrl": property_id
            }

            resp = requests.post(api_endpoint, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200:
                return {
                    "success": True,
                    "client_email": client_email,
                    "message": f"Search Console সফলভাবে কানেক্ট হয়েছে! ({client_email} ইউজার হিসেবে ভেরিফাইড)"
                }
            elif resp.status_code == 403:
                return {
                    "success": False,
                    "client_email": client_email,
                    "status_code": 403,
                    "message": f"Search Console-এ এই ইমেইলকে ইউজার হিসেবে যোগ করুন: {client_email} (Settings > Users & permissions > Add user > Permission: Restricted or Full)"
                }
            else:
                err_text = resp.text
                try:
                    err_json = resp.json()
                    err_text = err_json.get("error", {}).get("message", err_text)
                except Exception:
                    pass
                return {
                    "success": False,
                    "client_email": client_email,
                    "status_code": resp.status_code,
                    "message": f"Google API রেসপন্স এরর ({resp.status_code}): {err_text}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"কানেকশন টেস্টে ব্যতিক্রম ঘটেছে: {str(e)}"
            }

    def connect_site(self, property_id: str, sa_json_data: Any, sitemap_url: str = "") -> Dict[str, Any]:
        """Saves or updates connected site in SQLite database"""
        prop = property_id.strip()
        prop_type = "Domain" if prop.startswith("sc-domain:") else "URL-prefix"
        
        sa_email = ""
        sa_json_str = ""
        if sa_json_data:
            if isinstance(sa_json_data, dict):
                sa_email = sa_json_data.get("client_email", "")
                sa_json_str = json.dumps(sa_json_data)
            elif isinstance(sa_json_data, str) and sa_json_data.strip():
                try:
                    parsed = json.loads(sa_json_data)
                    sa_email = parsed.get("client_email", "")
                    sa_json_str = sa_json_data.strip()
                except Exception:
                    sa_json_str = sa_json_data.strip()

        conn = get_db()
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("SELECT id FROM sites WHERE property = ?", (prop,))
        row = c.fetchone()
        if row:
            site_id = row['id']
            c.execute("""
                UPDATE sites SET 
                    property_type = ?, sitemap_url = ?, service_account_email = ?,
                    service_account_json = ?, connected_at = ?
                WHERE id = ?
            """, (prop_type, sitemap_url, sa_email, sa_json_str, now, site_id))
        else:
            c.execute("""
                INSERT INTO sites (property, property_type, sitemap_url, service_account_email, service_account_json, connected_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (prop, prop_type, sitemap_url, sa_email, sa_json_str, now))
            site_id = c.lastrowid

        conn.commit()
        conn.close()
        return {"success": True, "site_id": site_id, "property": prop, "service_account_email": sa_email}

    def list_sites(self) -> List[Dict[str, Any]]:
        """Returns all connected sites with aggregated statistics"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM sites ORDER BY id DESC")
        rows = c.fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["has_sa"] = bool(d.get("service_account_json"))
            result.append(d)
        conn.close()
        return result

    # -------------------------------------------------------------------------
    # 2. URL COLLECTION & SITEMAP DISCOVERY
    # -------------------------------------------------------------------------

    def discover_urls_from_sitemap(self, site_id: int, sitemap_url: str = "") -> Dict[str, Any]:
        """Recursively parses XML sitemaps, nested sitemap indexes and robots.txt"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT property, sitemap_url FROM sites WHERE id = ?", (site_id,))
        site = c.fetchone()
        if not site:
            conn.close()
            return {"success": False, "message": "Site not found"}

        prop = site["property"]
        base_url = prop
        if base_url.startswith("sc-domain:"):
            base_url = "https://" + base_url.replace("sc-domain:", "").strip()
        if not base_url.endswith("/"):
            base_url += "/"

        # Determine target sitemap URL
        target_sitemap = sitemap_url.strip() or site["sitemap_url"]
        discovered_sitemaps = []
        if target_sitemap:
            discovered_sitemaps.append(target_sitemap)
        else:
            # 1. Try robots.txt
            robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
            try:
                req = urllib.request.Request(robots_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    robots_text = resp.read().decode('utf-8', errors='ignore')
                    for line in robots_text.splitlines():
                        if line.lower().startswith("sitemap:"):
                            parts = line.split(":", 1)
                            if len(parts) > 1 and parts[1].strip():
                                discovered_sitemaps.append(parts[1].strip())
            except Exception:
                pass

            if not discovered_sitemaps:
                discovered_sitemaps.append(urllib.parse.urljoin(base_url, "/sitemap.xml"))
                discovered_sitemaps.append(urllib.parse.urljoin(base_url, "/sitemap_index.xml"))

        # Recursive parser
        visited_sitemaps = set()
        collected_urls = set()

        def parse_single_sitemap(url: str, depth: int = 0):
            if depth > 4 or url in visited_sitemaps:
                return
            visited_sitemaps.add(url)
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    raw_data = resp.read()
                    if url.endswith(".gz") or raw_data[:2] == b'\x1f\x8b':
                        raw_data = gzip.decompress(raw_data)
                    xml_content = raw_data.decode('utf-8', errors='ignore')

                    import xml.etree.ElementTree as ET
                    # Strip namespace for clean tag parsing
                    xml_content = re.sub(r'\sxmlns="[^"]+"', '', xml_content, count=1)
                    root = ET.fromstring(xml_content)

                    # Sub-sitemaps in index
                    for sm in root.findall(".//sitemap"):
                        loc = sm.find("loc")
                        if loc is not None and loc.text:
                            parse_single_sitemap(loc.text.strip(), depth + 1)

                    # Direct URLs
                    for u in root.findall(".//url"):
                        loc = u.find("loc")
                        if loc is not None and loc.text:
                            clean_u = loc.text.strip()
                            if clean_u:
                                collected_urls.add(clean_u)
            except Exception:
                pass

        for sm_url in discovered_sitemaps:
            parse_single_sitemap(sm_url)

        # Insert new URLs into SQLite
        new_count = 0
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for u in collected_urls:
            # Normalize trailing slash
            norm_u = u.strip()
            c.execute("SELECT id FROM urls WHERE url = ?", (norm_u,))
            if not c.fetchone():
                c.execute("""
                    INSERT INTO urls (site_id, url, source, first_seen, verdict, coverage_state)
                    VALUES (?, ?, 'sitemap', ?, 'UNCHECKED', 'Not Inspected')
                """, (site_id, norm_u, now))
                new_count += 1

        self.recalculate_site_stats(site_id, conn)
        conn.close()

        return {
            "success": True,
            "sitemaps_inspected": list(visited_sitemaps),
            "total_urls_found": len(collected_urls),
            "new_urls_added": new_count
        }

    def add_manual_urls(self, site_id: int, url_list: List[str], source: str = "manual") -> Dict[str, Any]:
        """Adds custom list of URLs or parsed CSV rows"""
        conn = get_db()
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        added = 0
        for u in url_list:
            clean_u = u.strip()
            if not clean_u or not clean_u.startswith("http"):
                continue
            c.execute("SELECT id FROM urls WHERE url = ?", (clean_u,))
            if not c.fetchone():
                c.execute("""
                    INSERT INTO urls (site_id, url, source, first_seen, verdict, coverage_state)
                    VALUES (?, ?, ?, ?, 'UNCHECKED', 'Not Inspected')
                """, (site_id, clean_u, source, now))
                added += 1

        self.recalculate_site_stats(site_id, conn)
        conn.close()
        return {"success": True, "added": added}

    # -------------------------------------------------------------------------
    # 3. QUOTA & RATE LIMITING (Section 6)
    # -------------------------------------------------------------------------

    def check_and_increment_quota(self, prop: str) -> Tuple[bool, int]:
        """Tracks 2,000 requests/day per property quota"""
        today = date.today().isoformat()
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT calls_count, date FROM quotas WHERE property = ?", (prop,))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO quotas (property, date, calls_count, last_reset) VALUES (?, ?, 1, ?)", (prop, today, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return True, 1

        count = row["calls_count"]
        last_date = row["date"]
        if last_date != today:
            count = 1
            c.execute("UPDATE quotas SET date = ?, calls_count = 1, last_reset = ? WHERE property = ?", (today, datetime.now().isoformat(), prop))
        else:
            if count >= 2000:
                conn.close()
                return False, count
            count += 1
            c.execute("UPDATE quotas SET calls_count = ? WHERE property = ?", (count, prop))

        conn.commit()
        conn.close()
        return True, count

    # -------------------------------------------------------------------------
    # 4. OFFICIAL GSC URL INSPECTION API (Section 2 & 5)
    # -------------------------------------------------------------------------

    def inspect_url_official_api(self, site_id: int, url_id: int) -> Dict[str, Any]:
        """Calls official Search Console URL Inspection API for single URL"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM sites WHERE id = ?", (site_id,))
        site = c.fetchone()
        c.execute("SELECT * FROM urls WHERE id = ?", (url_id,))
        url_row = c.fetchone()

        if not site or not url_row:
            conn.close()
            return {"success": False, "message": "Site or URL not found in database."}

        target_url = url_row["url"]
        property_id = site["property"]
        sa_json_str = site["service_account_json"]

        if not sa_json_str:
            conn.close()
            # Perform Live Diagnosis Only when GSC not configured (Section 3 rule)
            live_res = self.run_live_diagnosis(url_id, target_url)
            return {
                "success": False,
                "is_gsc_connected": False,
                "message": "Search Console কানেক্ট করা নেই, শুধু লাইভ চেক সম্পন্ন হয়েছে। ভুয়া স্ট্যাটাস বানানো হয় না।",
                "live_diagnosis": live_res
            }

        # Check Daily Quota (2,000 URLs / day)
        can_proceed, current_calls = self.check_and_increment_quota(property_id)
        if not can_proceed:
            conn.close()
            return {
                "success": False,
                "quota_exhausted": True,
                "message": "আজকের কোটা শেষ (২,০০০ URL সীমা)। বাকি URL আগামীকাল চেক হবে।"
            }

        try:
            sa_info = json.loads(sa_json_str)
            token, token_err = self.get_service_account_token(sa_info)
            if not token:
                conn.close()
                return {"success": False, "message": f"Service Account Token Error: {token_err}"}

            api_endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "inspectionUrl": target_url,
                "siteUrl": property_id
            }

            resp = requests.post(api_endpoint, headers=headers, json=payload, timeout=25)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if resp.status_code == 200:
                raw_data = resp.json()
                insp_result = raw_data.get("inspectionResult", {})
                idx_result = insp_result.get("indexStatusResult", {})

                # Exact Google fields
                verdict = idx_result.get("verdict", "NEUTRAL")  # PASS / NEUTRAL / FAIL
                coverage_state = idx_result.get("coverageState", "Unknown")
                robots_txt_state = idx_result.get("robotsTxtState", "UNKNOWN")
                indexing_state = idx_result.get("indexingState", "UNKNOWN")
                page_fetch_state = idx_result.get("pageFetchState", "UNKNOWN")
                google_canonical = idx_result.get("googleCanonical", "")
                user_canonical = idx_result.get("userCanonical", "")
                last_crawl_time = idx_result.get("lastCrawlTime", "")
                crawled_as = idx_result.get("crawledAs", "MOBILE")

                # Verdict rule from Section 2: "Indexed" label ONLY when verdict == PASS
                display_status = "PASS" if verdict == "PASS" else "FAIL"

                # Save inspection
                c.execute("""
                    INSERT INTO inspections (
                        url_id, verdict, coverage_state, robots_txt_state, indexing_state,
                        page_fetch_state, google_canonical, user_canonical, last_crawl_time,
                        crawled_as, raw_json, checked_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    url_id, display_status, coverage_state, robots_txt_state, indexing_state,
                    page_fetch_state, google_canonical, user_canonical, last_crawl_time,
                    crawled_as, json.dumps(raw_data), now
                ))

                c.execute("""
                    UPDATE urls SET 
                        verdict = ?, coverage_state = ?, last_inspected_at = ?
                    WHERE id = ?
                """, (display_status, coverage_state, now, url_id))

                conn.commit()

                # Step 4: Run Live Diagnosis only for Non-Indexed URLs (Section 5, Step 4)
                live_findings = []
                if display_status != "PASS":
                    live_findings = self.run_live_diagnosis(url_id, target_url)

                self.recalculate_site_stats(site_id, conn)
                conn.close()

                return {
                    "success": True,
                    "target_url": target_url,
                    "verdict": display_status,
                    "coverage_state": coverage_state,
                    "google_canonical": google_canonical,
                    "user_canonical": user_canonical,
                    "last_crawl_time": last_crawl_time,
                    "crawled_as": crawled_as,
                    "robots_txt_state": robots_txt_state,
                    "page_fetch_state": page_fetch_state,
                    "checked_at": now,
                    "live_diagnosis": live_findings,
                    "raw_json": raw_data
                }
            elif resp.status_code == 403:
                conn.close()
                return {
                    "success": False,
                    "status_code": 403,
                    "message": f"Search Console-এ এই ইমেইলকে ইউজার হিসেবে যোগ করুন: {sa_info.get('client_email')}"
                }
            elif resp.status_code == 429:
                conn.close()
                return {
                    "success": False,
                    "status_code": 429,
                    "message": "Google Search Console API Rate Limit (429) পৌঁছে গেছে। অনুগ্রহ করে কিছুক্ষণ অপেক্ষা করুন।"
                }
            else:
                conn.close()
                return {
                    "success": False,
                    "status_code": resp.status_code,
                    "message": f"API Error ({resp.status_code}): {resp.text}"
                }
        except Exception as e:
            conn.close()
            return {"success": False, "message": f"Inspection exception: {str(e)}"}

    # -------------------------------------------------------------------------
    # 5. LIVE DIAGNOSIS (Section 9)
    # -------------------------------------------------------------------------

    def run_live_diagnosis(self, url_id: int, url: str) -> List[Dict[str, Any]]:
        """Live fetch checks: HTTP status, robots, headers, canonical, thin content"""
        findings = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            )

            status_code = 200
            final_url = url
            headers = {}
            html_content = ""

            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    status_code = resp.getcode()
                    final_url = resp.geturl()
                    headers = dict(resp.info())
                    raw_body = resp.read()
                    html_content = raw_body.decode('utf-8', errors='ignore')
            except urllib.error.HTTPError as he:
                status_code = he.code
                final_url = he.geturl()
                headers = dict(he.info())
                try:
                    html_content = he.read().decode('utf-8', errors='ignore')
                except Exception:
                    pass
            except Exception as e:
                findings.append({
                    "check_name": "HTTP Fetch",
                    "result": "FAIL",
                    "message": f"লাইভ ফেচ ব্যর্থ হয়েছে: {str(e)}"
                })
                self._save_findings(url_id, findings, now)
                return findings

            # 1. HTTP Status Code
            if status_code == 200:
                findings.append({"check_name": "HTTP Status", "result": "PASS", "message": "200 OK (Server is responsive)"})
            elif 300 <= status_code < 400:
                findings.append({"check_name": "HTTP Status", "result": "WARN", "message": f"Redirect {status_code} -> {final_url}"})
            elif 400 <= status_code < 500:
                findings.append({"check_name": "HTTP Status", "result": "FAIL", "message": f"Client Error {status_code} (Broken/Dead URL)"})
            else:
                findings.append({"check_name": "HTTP Status", "result": "FAIL", "message": f"Server Error {status_code}"})

            # 2. X-Robots-Tag
            x_robots = headers.get('x-robots-tag', '').lower()
            if 'noindex' in x_robots:
                findings.append({"check_name": "X-Robots-Tag", "result": "FAIL", "message": "X-Robots-Tag হেডারে 'noindex' পাওয়া গেছে!"})
            else:
                findings.append({"check_name": "X-Robots-Tag", "result": "PASS", "message": "X-Robots-Tag এ কোনো noindex নেই"})

            # 3. HTML Parsing (Meta Robots, Canonical, Title, Word Count)
            if html_content:
                # Meta robots
                meta_robots = re.findall(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
                if not meta_robots:
                    meta_robots = re.findall(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']robots["\']', html_content, re.IGNORECASE)

                if meta_robots and 'noindex' in meta_robots[0].lower():
                    findings.append({"check_name": "Meta Robots", "result": "FAIL", "message": f"<meta name='robots'> ট্যাগ পেজ ব্লক করছে: '{meta_robots[0]}'"})
                else:
                    findings.append({"check_name": "Meta Robots", "result": "PASS", "message": "Meta robots ট্যাগ ইনডেক্সিং অ্যালাউ করছে"})

                # Canonical tag
                canon_match = re.findall(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
                if canon_match:
                    declared_canon = canon_match[0].strip()
                    if declared_canon.rstrip('/') == url.rstrip('/'):
                        findings.append({"check_name": "Canonical Tag", "result": "PASS", "message": f"Self-referencing Canonical উপস্থিত ({declared_canon})"})
                    else:
                        findings.append({"check_name": "Canonical Tag", "result": "WARN", "message": f"Canonical অন্য URL-এ পয়েন্ট করছে: {declared_canon}"})
                else:
                    findings.append({"check_name": "Canonical Tag", "result": "WARN", "message": "Canonical ট্যাগ অনুপস্থিত"})

                # Title tag
                title_match = re.findall(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
                if title_match and title_match[0].strip():
                    findings.append({"check_name": "Title Tag", "result": "PASS", "message": f"Title Tag উপস্থিত: '{title_match[0].strip()[:60]}...'"})
                else:
                    findings.append({"check_name": "Title Tag", "result": "FAIL", "message": "Title Tag অনুপস্থিত বা ফাঁকা"})

                # Word Count & Thin Content Check (<150 words warning)
                # Strip scripts and tags
                clean_text = re.sub(r'<script.*?</script>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r'<style.*?</style>', ' ', clean_text, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
                words = [w for w in clean_text.split() if len(w) > 1]
                word_count = len(words)

                if word_count < 150:
                    findings.append({"check_name": "Content Depth", "result": "FAIL", "message": f"Thin Content সতর্কতা: পেজে মাত্র {word_count} শব্দ আছে (<১৫০ শব্দ)"})
                else:
                    findings.append({"check_name": "Content Depth", "result": "PASS", "message": f"কনটেন্ট শব্দসংখ্যা স্বাভাবিক ({word_count} শব্দ)"})

                # Heavy JS rendering check (low text to code ratio with heavy script tags)
                script_count = len(re.findall(r'<script', html_content, re.IGNORECASE))
                if word_count < 100 and script_count > 10:
                    findings.append({"check_name": "JS Rendering", "result": "WARN", "message": "Client-Side Rendering সন্দেহ: বেশি স্ক্রিপ্ট কিন্তু কম টেক্সট। Googlebot রেন্ডার না করলে ফাঁকা দেখাবে।"})
                else:
                    findings.append({"check_name": "JS Rendering", "result": "PASS", "message": "HTML সার্ভার-রেন্ডার্ড টেক্সট শনাক্ত হয়েছে"})

        except Exception as e:
            findings.append({"check_name": "Live Diagnosis", "result": "FAIL", "message": f"ডায়াগনসিস এরর: {str(e)}"})

        self._save_findings(url_id, findings, now)
        return findings

    def _save_findings(self, url_id: int, findings: List[Dict[str, Any]], checked_at: str):
        conn = get_db()
        c = conn.cursor()
        c.execute("DELETE FROM findings WHERE url_id = ?", (url_id,))
        for f in findings:
            c.execute("""
                INSERT INTO findings (url_id, check_name, result, message, checked_at)
                VALUES (?, ?, ?, ?, ?)
            """, (url_id, f["check_name"], f["result"], f["message"], checked_at))
        conn.commit()
        conn.close()

    # -------------------------------------------------------------------------
    # 6. STATS & RECALCULATION
    # -------------------------------------------------------------------------

    def recalculate_site_stats(self, site_id: int, conn=None):
        """Updates total, indexed, non_indexed, unchecked counts and history"""
        should_close = False
        if conn is None:
            conn = get_db()
            should_close = True

        c = conn.cursor()
        c.execute("SELECT COUNT(*) as total FROM urls WHERE site_id = ?", (site_id,))
        total = c.fetchone()["total"]

        c.execute("SELECT COUNT(*) as cnt FROM urls WHERE site_id = ? AND verdict = 'PASS'", (site_id,))
        indexed = c.fetchone()["cnt"]

        c.execute("SELECT COUNT(*) as cnt FROM urls WHERE site_id = ? AND verdict = 'FAIL'", (site_id,))
        non_indexed = c.fetchone()["cnt"]

        c.execute("SELECT COUNT(*) as cnt FROM urls WHERE site_id = ? AND verdict = 'UNCHECKED'", (site_id,))
        unchecked = c.fetchone()["cnt"]

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
            UPDATE sites SET 
                total_urls = ?, indexed_count = ?, non_indexed_count = ?,
                unchecked_count = ?, last_check_at = ?
            WHERE id = ?
        """, (total, indexed, non_indexed, unchecked, now, site_id))

        # Save History snapshot for timeline tracking (Section 4)
        today = date.today().isoformat()
        c.execute("SELECT id FROM history WHERE site_id = ? AND date = ?", (site_id, today))
        h_row = c.fetchone()
        if h_row:
            c.execute("""
                UPDATE history SET 
                    total_urls = ?, indexed_count = ?, non_indexed_count = ?,
                    unchecked_count = ?, created_at = ?
                WHERE id = ?
            """, (total, indexed, non_indexed, unchecked, now, h_row["id"]))
        else:
            c.execute("""
                INSERT INTO history (site_id, date, total_urls, indexed_count, non_indexed_count, unchecked_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (site_id, today, total, indexed, non_indexed, unchecked, now))

        conn.commit()
        if should_close:
            conn.close()

    # -------------------------------------------------------------------------
    # 7. DASHBOARD DATA RETRIEVAL (Section 7)
    # -------------------------------------------------------------------------

    def get_site_dashboard(self, site_id: int, page: int = 1, limit: int = 50, verdict_filter: str = "ALL", coverage_filter: str = "ALL", search: str = "") -> Dict[str, Any]:
        """Provides paginated, lightning-fast data for Index Tab: summary cards, reasons group, table"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM sites WHERE id = ?", (site_id,))
        site = c.fetchone()
        if not site:
            conn.close()
            return {"success": False, "message": "Site not found"}

        site_data = dict(site)
        site_data["has_sa"] = bool(site_data.get("service_account_json"))

        # Fast Summary Stats (Aggregated directly in SQLite)
        c.execute("""
            SELECT 
                COUNT(*) as total_count,
                SUM(CASE WHEN verdict = 'PASS' THEN 1 ELSE 0 END) as indexed_cnt,
                SUM(CASE WHEN verdict = 'FAIL' THEN 1 ELSE 0 END) as non_indexed_cnt,
                SUM(CASE WHEN verdict IS NULL OR verdict = 'UNCHECKED' THEN 1 ELSE 0 END) as unchecked_cnt
            FROM urls WHERE site_id = ?
        """, (site_id,))
        sum_row = c.fetchone()
        total_urls = sum_row[0] if sum_row else 0
        indexed_cnt = sum_row[1] or 0 if sum_row else 0
        non_indexed_cnt = sum_row[2] or 0 if sum_row else 0
        unchecked_cnt = sum_row[3] or 0 if sum_row else 0

        # Fast Reason Groups (Aggregated in SQLite)
        c.execute("""
            SELECT coverage_state, COUNT(*) as cnt
            FROM urls
            WHERE site_id = ? AND verdict = 'FAIL' AND coverage_state IS NOT NULL
            GROUP BY coverage_state
            ORDER BY cnt DESC
        """, (site_id,))
        reason_groups = {row[0]: row[1] for row in c.fetchall()}

        # Filtered URL query with pagination
        where_clauses = ["u.site_id = ?"]
        params = [site_id]

        search = (search or "").strip()
        if search:
            where_clauses.append("u.url LIKE ?")
            params.append(f"%{search}%")

        if verdict_filter and verdict_filter != "ALL":
            where_clauses.append("u.verdict = ?")
            params.append(verdict_filter)

        if coverage_filter and coverage_filter != "ALL":
            where_clauses.append("u.coverage_state = ?")
            params.append(coverage_filter)

        where_sql = " AND ".join(where_clauses)

        # Count total filtered items
        c.execute(f"SELECT COUNT(*) FROM urls u WHERE {where_sql}", params)
        filtered_total = c.fetchone()[0]

        # Fetch page rows with limit and offset
        page = max(1, page)
        limit = min(200, max(10, limit))
        offset = (page - 1) * limit
        paged_params = list(params) + [limit, offset]

        c.execute(f"""
            SELECT u.*, 
                   i.robots_txt_state, i.indexing_state, i.page_fetch_state,
                   i.google_canonical, i.user_canonical, i.last_crawl_time,
                   i.crawled_as, i.checked_at as last_inspection_date
            FROM urls u
            LEFT JOIN inspections i ON i.id = (
                SELECT id FROM inspections WHERE url_id = u.id ORDER BY id DESC LIMIT 1
            )
            WHERE {where_sql}
            ORDER BY u.id ASC
            LIMIT ? OFFSET ?
        """, paged_params)
        url_rows = c.fetchall()

        urls_list = []
        for r in url_rows:
            d = dict(r)
            cov = d.get("coverage_state") or "Not Inspected"
            info = COVERAGE_STATE_MAP.get(cov, {
                "reason_bn": cov,
                "solution_bn": "Google Search Console URL Inspection টুলে পেজটি রিকোয়েস্ট করুন এবং লাইভ টেস্ট চালান।"
            })
            d["reason_bn"] = info["reason_bn"]
            d["solution_bn"] = info["solution_bn"]
            d["gsc_direct_url"] = f"https://search.google.com/search-console/inspect?resource_id={urllib.parse.quote(site['property'], safe='')}&id={urllib.parse.quote(d['url'], safe='')}"
            urls_list.append(d)

        # Distinct coverage options for dropdown
        c.execute("SELECT DISTINCT coverage_state FROM urls WHERE site_id = ? AND coverage_state IS NOT NULL", (site_id,))
        cov_options = [row[0] for row in c.fetchall() if row[0]]

        # Quota usage
        c.execute("SELECT calls_count FROM quotas WHERE property = ?", (site["property"],))
        q_row = c.fetchone()
        quota_used = q_row["calls_count"] if q_row else 0

        # History list
        c.execute("SELECT * FROM history WHERE site_id = ? ORDER BY date ASC LIMIT 14", (site_id,))
        history_rows = [dict(h) for h in c.fetchall()]

        conn.close()

        total_pages = max(1, math.ceil(filtered_total / limit)) if filtered_total > 0 else 1

        return {
            "success": True,
            "site": site_data,
            "summary": {
                "total_urls": total_urls,
                "indexed": indexed_cnt,
                "non_indexed": non_indexed_cnt,
                "unchecked": unchecked_cnt,
                "last_check_at": site_data.get("last_check_at") or "Never",
                "quota_used": quota_used,
                "quota_max": 2000
            },
            "pagination": {
                "page": page,
                "limit": limit,
                "total_filtered": filtered_total,
                "total_pages": total_pages
            },
            "reason_groups": reason_groups,
            "coverage_options": cov_options,
            "urls": urls_list,
            "history": history_rows
        }

    def get_url_details(self, url_id: int) -> Dict[str, Any]:
        """Fetches detailed Google Inspection result and live diagnosis findings"""
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT u.*, s.property FROM urls u JOIN sites s ON u.site_id = s.id WHERE u.id = ?", (url_id,))
        url_row = c.fetchone()
        if not url_row:
            conn.close()
            return {"success": False, "message": "URL not found"}

        url_data = dict(url_row)
        c.execute("SELECT * FROM inspections WHERE url_id = ? ORDER BY id DESC LIMIT 1", (url_id,))
        insp_row = c.fetchone()
        insp_data = dict(insp_row) if insp_row else None

        c.execute("SELECT * FROM findings WHERE url_id = ? ORDER BY id ASC", (url_id,))
        findings = [dict(f) for f in c.fetchall()]

        cov = (insp_data.get("coverage_state") if insp_data else None) or url_data.get("coverage_state") or "Not Inspected"
        info = COVERAGE_STATE_MAP.get(cov, {
            "reason_bn": cov,
            "solution_bn": "Google Search Console URL Inspection টুলে পেজটি রিকোয়েস্ট করুন এবং লাইভ টেস্ট চালান।"
        })

        gsc_direct = f"https://search.google.com/search-console/inspect?resource_id={urllib.parse.quote(url_data['property'], safe='')}&id={urllib.parse.quote(url_data['url'], safe='')}"

        conn.close()

        return {
            "success": True,
            "url": url_data,
            "google_says": insp_data,
            "live_checks": findings,
            "reason_bn": info["reason_bn"],
            "solution_bn": info["solution_bn"],
            "gsc_direct_url": gsc_direct
        }


gsc_engine = GSCIndexEngine()
