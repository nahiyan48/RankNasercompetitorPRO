# -*- coding: utf-8 -*-
"""
=============================================================================
RankNaserPro Enterprise Full-Site Crawler & Semrush/Ahrefs-Grade Audit Engine
(সম্পূর্ণ সাইট ক্রলার ও ইন্টারন্যাশনাল মানের সাইট অডিট ইঞ্জিন)
=============================================================================
Features:
- Multi-page BFS site crawler (seed URL -> internal links discovery)
- Robots.txt and sitemap.xml parser (detects sitemaps, blocked rules, orphan pages)
- Inlinks & Outlinks Graph calculation (calculates internal link equity)
- Click Depth calculation (Depth 1, 2, 3, 4+)
- Broken Internal Links Detection (Source Page -> Target 404 -> Anchor Text)
- Cross-Page Duplicate Detection (Duplicate Titles, Duplicate Meta Descriptions, Duplicate H1s)
- Comprehensive Site Health Score (0-100, Semrush/Ahrefs formula)
- Site-Wide Categorized Issues with Bengali Why/Fix & Affected URLs
- Crawled Pages Explorer Table (Status, Depth, Title, H1, Words, Inlinks, Outlinks)
=============================================================================
"""

import os
import re
import time
import json
from urllib.parse import urlparse, urljoin, urldefrag
from collections import defaultdict, deque
import concurrent.futures
import requests
from bs4 import BeautifulSoup

from site_audit_engine import SiteAuditEngine

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 RankNaserSiteAudit/2.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
}

class FullSiteAuditCrawler:
    def __init__(self, seed_url: str, max_pages: int = 25, max_workers: int = 5):
        if not seed_url.startswith("http://") and not seed_url.startswith("https://"):
            seed_url = "https://" + seed_url
            
        # Clean fragment from seed URL
        seed_url, _ = urldefrag(seed_url)
        self.seed_url = seed_url
        parsed = urlparse(seed_url)
        self.base_domain = parsed.netloc.lower()
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.max_pages = max_pages
        self.max_workers = max_workers
        
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        
        # State
        self.crawled_pages = {} # url -> page_data dict
        self.inlinks_map = defaultdict(set) # target_url -> set(source_urls)
        self.outlinks_map = defaultdict(list) # source_url -> list of (target_url, anchor, is_internal)
        self.broken_links = [] # list of {source, target, status, anchor}
        self.sitemap_urls = set()
        self.disallowed_paths = []
        self.robots_exists = False
        self.sitemap_exists = False

    def normalize_url(self, url: str) -> str:
        """Strip fragments, query tracking params, and normalize casing."""
        try:
            url, _ = urldefrag(url)
            parsed = urlparse(url)
            # ignore non-http schemes (mailto, tel, javascript)
            if parsed.scheme not in ('http', 'https'):
                return ""
            # Strip common tracking parameters (utm_*, gclid, fbclid)
            path = parsed.path or "/"
            query_parts = []
            if parsed.query:
                for q in parsed.query.split("&"):
                    k = q.split("=")[0].lower()
                    if not (k.startswith("utm_") or k in ("fbclid", "gclid", "ref", "source")):
                        query_parts.append(q)
            clean_query = "&".join(query_parts)
            norm = f"{parsed.scheme}://{parsed.netloc.lower()}{path}"
            if clean_query:
                norm += f"?{clean_query}"
            return norm.rstrip('/') if path != '/' else norm
        except Exception:
            return ""

    def is_internal(self, url: str) -> bool:
        """Check if URL belongs to the same base domain."""
        try:
            domain = urlparse(url).netloc.lower()
            return domain == self.base_domain or domain.endswith("." + self.base_domain)
        except Exception:
            return False

    def fetch_robots_and_sitemap(self):
        """Fetch and parse robots.txt and sitemap.xml to find sitemap URLs & crawl rules."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        try:
            resp = self.session.get(robots_url, timeout=6)
            if resp.status_code == 200 and resp.text:
                self.robots_exists = True
                for line in resp.text.splitlines():
                    line = line.strip()
                    if line.lower().startswith("disallow:"):
                        p = line.split(":", 1)[1].strip()
                        if p and p != "/":
                            self.disallowed_paths.append(p)
                    elif line.lower().startswith("sitemap:"):
                        sm = line.split(":", 1)[1].strip()
                        if sm:
                            self._extract_sitemap_urls(sm)
        except Exception:
            pass

        # Try standard sitemap.xml if no sitemap was declared in robots.txt
        if not self.sitemap_urls:
            self._extract_sitemap_urls(urljoin(self.base_url, "/sitemap.xml"))
            self._extract_sitemap_urls(urljoin(self.base_url, "/sitemap_index.xml"))

    def _extract_sitemap_urls(self, sitemap_url: str):
        """Extract up to 50 URLs from an XML sitemap."""
        try:
            resp = self.session.get(sitemap_url, timeout=6)
            if resp.status_code == 200 and resp.text:
                self.sitemap_exists = True
                # Regex match <loc>...</loc>
                locs = re.findall(r'<loc>(https?://[^<]+)</loc>', resp.text, re.I)
                for loc in locs[:60]:
                    norm = self.normalize_url(loc)
                    if norm and self.is_internal(norm):
                        self.sitemap_urls.add(norm)
        except Exception:
            pass

    def _crawl_single_page(self, url: str, depth: int) -> dict:
        """Fetch and parse an individual HTML page."""
        t0 = time.perf_counter()
        try:
            resp = self.session.get(url, timeout=10, allow_redirects=True)
            ttfb_ms = round((time.perf_counter() - t0) * 1000, 1)
            status_code = resp.status_code
            content_type = resp.headers.get("content-type", "").lower()
            
            # If not HTML, record basic info
            if "text/html" not in content_type:
                return {
                    "url": url,
                    "status_code": status_code,
                    "depth": depth,
                    "ttfb_ms": ttfb_ms,
                    "is_html": False,
                    "content_type": content_type,
                    "title": "",
                    "meta_desc": "",
                    "h1": "",
                    "h1_count": 0,
                    "word_count": 0,
                    "canonical": "",
                    "meta_robots": "",
                    "images_count": 0,
                    "missing_alt_count": 0,
                    "discovered_links": [],
                    "raw_html": "",
                    "soup": None,
                    "headers": dict(resp.headers)
                }

            raw_html = resp.text
            soup = BeautifulSoup(raw_html, "html.parser")
            
            # Extract basic on-page elements
            title = soup.title.string.strip() if (soup.title and soup.title.string) else ""
            meta_desc_el = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
            meta_desc = meta_desc_el.get("content", "").strip() if meta_desc_el else ""
            
            h1_tags = [h.get_text(separator=' ', strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)]
            h1 = h1_tags[0] if h1_tags else ""
            
            # Word count
            clean_soup = BeautifulSoup(raw_html, "html.parser")
            for s in clean_soup(["script", "style", "nav", "footer", "header", "aside"]):
                s.decompose()
            body_text = clean_soup.get_text(separator=" ", strip=True)
            word_count = len(body_text.split())
            
            # Canonical & Meta robots
            canonical_el = soup.find("link", rel=lambda v: v and "canonical" in v.lower())
            canonical = canonical_el.get("href", "").strip() if canonical_el else ""
            
            meta_robots_el = soup.find("meta", attrs={"name": re.compile(r"^robots$", re.I)})
            meta_robots = meta_robots_el.get("content", "").lower() if meta_robots_el else ""
            
            # Images
            imgs = soup.find_all("img")
            missing_alt = [img.get("src", "") for img in imgs if not img.get("alt") or not img.get("alt").strip()]
            
            # Links
            discovered_links = []
            for a in soup.find_all("a", href=True):
                raw_href = a.get("href", "").strip()
                if not raw_href or raw_href.startswith("#") or raw_href.startswith("javascript:"):
                    continue
                full_href = urljoin(url, raw_href)
                norm_href = self.normalize_url(full_href)
                if norm_href:
                    anchor = a.get_text(strip=True) or (a.find("img") and a.find("img").get("alt", "")) or "Link"
                    discovered_links.append((norm_href, anchor, self.is_internal(norm_href)))

            return {
                "url": url,
                "status_code": status_code,
                "depth": depth,
                "ttfb_ms": ttfb_ms,
                "is_html": True,
                "content_type": content_type,
                "title": title,
                "meta_desc": meta_desc,
                "h1": h1,
                "h1_count": len(h1_tags),
                "word_count": word_count,
                "canonical": canonical,
                "meta_robots": meta_robots,
                "images_count": len(imgs),
                "missing_alt_count": len(missing_alt),
                "discovered_links": discovered_links,
                "raw_html": raw_html,
                "soup": soup,
                "headers": dict(resp.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "status_code": 0,
                "depth": depth,
                "ttfb_ms": 0,
                "is_html": False,
                "error": str(e),
                "title": "",
                "meta_desc": "",
                "h1": "",
                "h1_count": 0,
                "word_count": 0,
                "canonical": "",
                "meta_robots": "",
                "images_count": 0,
                "missing_alt_count": 0,
                "discovered_links": [],
                "raw_html": "",
                "soup": None,
                "headers": {}
            }

    def run_crawl(self) -> dict:
        """Execute multi-page site crawl starting from seed URL."""
        self.fetch_robots_and_sitemap()
        
        queue = deque([(self.seed_url, 1)])
        visited = {self.seed_url}
        
        # Add sitemap URLs to initial discovery pool if available
        for sm_url in list(self.sitemap_urls)[:10]:
            if sm_url not in visited:
                queue.append((sm_url, 2))
                visited.add(sm_url)

        # BFS crawl up to max_pages
        while queue and len(self.crawled_pages) < self.max_pages:
            batch = []
            while queue and len(batch) < self.max_workers and (len(self.crawled_pages) + len(batch)) < self.max_pages:
                curr_url, curr_depth = queue.popleft()
                batch.append((curr_url, curr_depth))
                
            if not batch:
                break
                
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_url = {executor.submit(self._crawl_single_page, u, d): (u, d) for (u, d) in batch}
                for future in concurrent.futures.as_completed(future_to_url):
                    u, d = future_to_url[future]
                    try:
                        page_data = future.result()
                    except Exception as exc:
                        page_data = {"url": u, "status_code": 0, "depth": d, "error": str(exc), "is_html": False, "discovered_links": []}
                        
                    self.crawled_pages[u] = page_data
                    
                    # Process discovered links
                    for (target_norm, anchor, is_internal) in page_data.get("discovered_links", []):
                        if is_internal:
                            self.inlinks_map[target_norm].add(u)
                            self.outlinks_map[u].append({"target": target_norm, "anchor": anchor, "is_internal": True})
                            
                            # Add to crawl queue if not visited
                            if target_norm not in visited and len(visited) < (self.max_pages * 2):
                                visited.add(target_norm)
                                queue.append((target_norm, d + 1))
                        else:
                            self.outlinks_map[u].append({"target": target_norm, "anchor": anchor, "is_internal": False})

        # Post-Crawl: Probe for broken links among all discovered internal targets
        self._check_broken_internal_links()
        
        # Build master site audit summary
        return self._compile_full_site_report()

    def _check_broken_internal_links(self):
        """Verify internal links that were not crawled to see if any are broken (404)."""
        uncrawled_internal = set()
        for source, links in self.outlinks_map.items():
            for link_info in links:
                if link_info.get("is_internal") and link_info["target"] not in self.crawled_pages:
                    uncrawled_internal.add((source, link_info["target"], link_info.get("anchor", "Link")))
                    
        # Check first 20 internal links with fast HEAD request
        samples_to_check = list(uncrawled_internal)[:20]
        for source_url, target_url, anchor in samples_to_check:
            try:
                head_resp = self.session.head(target_url, timeout=4, allow_redirects=True)
                if head_resp.status_code in (404, 410, 500, 502, 503):
                    self.broken_links.append({
                        "source": source_url,
                        "target": target_url,
                        "status": head_resp.status_code,
                        "anchor": anchor
                    })
            except Exception:
                pass

    def _compile_full_site_report(self) -> dict:
        """Compile complete Semrush/Ahrefs-style multi-page site audit report."""
        pages = list(self.crawled_pages.values())
        total_pages = len(pages)
        
        status_200 = sum(1 for p in pages if p.get("status_code") == 200)
        status_3xx = sum(1 for p in pages if 300 <= p.get("status_code", 0) < 400)
        status_4xx = sum(1 for p in pages if 400 <= p.get("status_code", 0) < 500) + len(self.broken_links)
        status_5xx = sum(1 for p in pages if p.get("status_code", 0) >= 500)
        
        # Depth distribution
        depth_dist = {"1": 0, "2": 0, "3": 0, "4+": 0}
        for p in pages:
            d = p.get("depth", 1)
            if d == 1: depth_dist["1"] += 1
            elif d == 2: depth_dist["2"] += 1
            elif d == 3: depth_dist["3"] += 1
            else: depth_dist["4+"] += 1

        # Duplicate detection across all crawled pages
        title_occurrences = defaultdict(list)
        desc_occurrences = defaultdict(list)
        h1_occurrences = defaultdict(list)
        
        missing_titles = []
        missing_descriptions = []
        missing_h1s = []
        thin_content_pages = []
        slow_pages = []
        images_missing_alt_pages = []
        
        for p in pages:
            u = p["url"]
            t = p.get("title", "")
            d = p.get("meta_desc", "")
            h = p.get("h1", "")
            wc = p.get("word_count", 0)
            ttfb = p.get("ttfb_ms", 0)
            
            if not t:
                missing_titles.append(u)
            else:
                title_occurrences[t].append(u)
                
            if not d:
                missing_descriptions.append(u)
            else:
                desc_occurrences[d].append(u)
                
            if not h:
                missing_h1s.append(u)
            else:
                h1_occurrences[h].append(u)
                
            if 0 < wc < 300:
                thin_content_pages.append(u)
                
            if ttfb > 1200:
                slow_pages.append(u)
                
            if p.get("missing_alt_count", 0) > 0:
                images_missing_alt_pages.append(u)

        duplicate_titles = {t: urls for t, urls in title_occurrences.items() if len(urls) > 1}
        duplicate_descriptions = {d: urls for d, urls in desc_occurrences.items() if len(urls) > 1}
        duplicate_h1s = {h: urls for h, urls in h1_occurrences.items() if len(urls) > 1}

        # Orphan Pages: Pages listed in sitemap that have 0 internal links from crawled pages
        orphan_pages = []
        crawled_urls = set(self.crawled_pages.keys())
        for sm_url in self.sitemap_urls:
            if sm_url in crawled_urls and len(self.inlinks_map.get(sm_url, [])) == 0 and sm_url != self.seed_url:
                orphan_pages.append(sm_url)

        # Categorized Issues Compiler (Semrush-style)
        critical_issues = []
        warnings = []
        notices = []

        # 1. Broken Links (4xx)
        if self.broken_links or status_4xx > 0:
            affected = [b["target"] for b in self.broken_links]
            for p in pages:
                if 400 <= p.get("status_code", 0) < 500:
                    affected.append(p["url"])
            critical_issues.append({
                "id": "IDX-001",
                "title": f"4xx Client Errors & Broken Links ({len(affected)} pages/links affected)",
                "category": "Indexability & Crawlability",
                "severity": "C",
                "affected": list(set(affected)),
                "why": "৪xx (404/410) ব্রোকেন পেজ ও লিংক ইউজারের অভিজ্ঞতা নষ্ট করে এবং গুগলের ক্রল বাজেট অপচয় করে র‍্যাঙ্কিং কমিয়ে দেয়।",
                "fix": "ব্রোকেন ইন্টারনাল লিংকগুলো ঠিক করুন অথবা প্রাসঙ্গিক নতুন পেজে ৩০১ রিডাইরেক্ট সেট করুন।"
            })

        # 2. Server Errors (5xx)
        if status_5xx > 0:
            affected = [p["url"] for p in pages if p.get("status_code", 0) >= 500]
            critical_issues.append({
                "id": "IDX-002",
                "title": f"5xx Server Errors Detected ({len(affected)} pages affected)",
                "category": "Indexability & Crawlability",
                "severity": "C",
                "affected": affected,
                "why": "সার্ভার এরর থাকার কারণে গুগলবট সাইট ক্রল করতে পারে না এবং পেজগুলোকে সার্চ ইনডেক্স থেকে সরিয়ে দেয়।",
                "fix": "ওয়েব সার্ভার ও অ্যাপ্লিকেশনের এরর লগ চেক করুন, ডাটাবেস টাইমআউট এবং পিএইচপি/নোড মেমোরি লিমিট বৃদ্ধি করুন।"
            })

        # 3. Missing Titles
        if missing_titles:
            critical_issues.append({
                "id": "OP-001",
                "title": f"Missing Title Tags ({len(missing_titles)} pages affected)",
                "category": "On-Page SEO",
                "severity": "C",
                "affected": missing_titles,
                "why": "টাইটেল ট্যাগ না থাকলে গুগল সার্চ রেজাল্টে কোনো অর্থবোধক হেডলাইন তৈরি করতে পারে না, ফলে অর্গানিক ট্রাফিক ধ্বংস হয়।",
                "fix": "প্রতিটি পেজের <head>-এ ফোকাস কিওয়ার্ড সম্বলিত ৫০-৬০ ক্যারেক্টারের ইউনিক <title> ট্যাগ যুক্ত করুন।"
            })

        # 4. Duplicate Titles
        if duplicate_titles:
            affected = []
            for t, u_list in duplicate_titles.items():
                affected.extend(u_list)
            warnings.append({
                "id": "OP-002",
                "title": f"Duplicate Title Tags Across Multiple Pages ({len(set(affected))} pages affected)",
                "category": "On-Page SEO",
                "severity": "W",
                "affected": list(set(affected)),
                "why": "একাধিক পেজে একই টাইটেল থাকলে কিওয়ার্ড ক্যানিবালাইজেশন (Keyword Cannibalization) ঘটে এবং গুগল বুঝতে পারে না কোন পেজকে র‍্যাঙ্ক করাবে।",
                "fix": "প্রতিটি পেজের উদ্দেশ্যের সাথে মিল রেখে সম্পূর্ণ আলাদা ও ইউনিক টাইটেল লিখুন।"
            })

        # 5. Missing Meta Descriptions
        if missing_descriptions:
            warnings.append({
                "id": "OP-010",
                "title": f"Missing Meta Descriptions ({len(missing_descriptions)} pages affected)",
                "category": "On-Page SEO",
                "severity": "W",
                "affected": missing_descriptions,
                "why": "মেটা ডেসক্রিপশন না থাকলে গুগল র্যান্ডম টেক্সট স্নsnippet হিসেবে দেখায়, যা সার্চ রেজাল্টে ক্লিক থ্রু রেট (CTR) অনেক কমিয়ে দেয়।",
                "fix": "প্রতিটি পেজে ১১০-১৫৫ ক্যারেক্টারের আকর্ষক মেটা ডেসক্রিপশন ও অ্যাকশন-ড্রিভেন কল-টু-অ্যাকশন (CTA) যোগ করুন।"
            })

        # 6. Duplicate Meta Descriptions
        if duplicate_descriptions:
            affected = []
            for d, u_list in duplicate_descriptions.items():
                affected.extend(u_list)
            warnings.append({
                "id": "OP-010-DUP",
                "title": f"Duplicate Meta Descriptions Across Pages ({len(set(affected))} pages affected)",
                "category": "On-Page SEO",
                "severity": "W",
                "affected": list(set(affected)),
                "why": "একই মেটা ডেসক্রিপশন বারবার ব্যবহার করলে গুগল পেজের স্বাতন্ত্র্য শনাক্ত করতে ব্যর্থ হয়।",
                "fix": "প্রতিটি পেজের স্বতন্ত্র কনটেন্ট সারসংক্ষেপ তৈরি করে আলাদা মেটা ডেসক্রিপশন সেট করুন।"
            })

        # 7. Missing H1 Tags
        if missing_h1s:
            warnings.append({
                "id": "OP-020",
                "title": f"Missing H1 Headings ({len(missing_h1s)} pages affected)",
                "category": "On-Page SEO",
                "severity": "W",
                "affected": missing_h1s,
                "why": "এইচ১ ট্যাগ কনটেন্টের মূল টপিক নির্দেশ করে; এটি না থাকলে গুগলের পেজ ইনটেন্ট বুঝতে সমস্যা হয়।",
                "fix": "প্রতিটি পেজের কনটেন্টের শীর্ষে একটি স্পষ্ট এবং প্রধান কিওয়ার্ডযুক্ত <h1> ট্যাগ যোগ করুন।"
            })

        # 8. Missing Image Alt Attributes
        if images_missing_alt_pages:
            warnings.append({
                "id": "OP-050",
                "title": f"Images Missing Alt Text ({len(images_missing_alt_pages)} pages affected)",
                "category": "On-Page SEO & Accessibility",
                "severity": "W",
                "affected": images_missing_alt_pages,
                "why": "অল্ট টেক্সট ছাড়া গুগল ইমেজ সার্চে ছবি ইন্ডেক্স করতে পারে না এবং দৃষ্টিপ্রতিবন্ধী ইউজারদের স্ক্রিন রিডার ব্যর্থ হয় (WCAG Violation)।",
                "fix": "সাইটের সকল গুরুত্বপূর্ণ ছবিতে অর্থবহ ও প্রাসঙ্গিক alt='...' ডেসক্রিপশন যুক্ত করুন।"
            })

        # 9. Thin Content Pages
        if thin_content_pages:
            warnings.append({
                "id": "OP-040",
                "title": f"Thin Content / Low Word Count Pages ({len(thin_content_pages)} pages affected)",
                "category": "Content Quality & Helpful Content",
                "severity": "W",
                "affected": thin_content_pages,
                "why": "৩০০ শব্দের কম টেক্সট থাকলে গুগল হেল্পফুল কনটেন্ট আপডেটে সাইটের অথরিটি পেনাল্টি হতে পারে।",
                "fix": "পেজে বিস্তারিত গাইড, স্পেসিফিকেশন, সাধারণ প্রশ্ন ও তথ্যবহুল উপশিরোনাম যোগ করে কনটেন্ট সমৃদ্ধ করুন।"
            })

        # 10. High Click Depth (4+)
        deep_pages = [p["url"] for p in pages if p.get("depth", 1) >= 4]
        if deep_pages:
            notices.append({
                "id": "CRAWL-013",
                "title": f"Deep Click Depth (4+ clicks from homepage) ({len(deep_pages)} pages affected)",
                "category": "Site Architecture",
                "severity": "N",
                "affected": deep_pages,
                "why": "হোমপেজ থেকে ৩ ক্লিকে পেজে পৌঁছানো না গেলে ক্রলার ও ইউজারদের কাছে পেজটি লুক্কায়িত মনে হয় এবং লিংক ইকুইটি পায় না।",
                "fix": "প্রধান মেনু, ফুটার বা ক্যাটাগরি পেজ থেকে সরাসরি ইন্টারনাল লিংক দিয়ে ক্লিক ডেপথ ৩-এর মধ্যে নামিয়ে আনুন।"
            })

        # 11. Orphan Pages
        if orphan_pages:
            warnings.append({
                "id": "CRAWL-012",
                "title": f"Orphan Pages Detected in Sitemap ({len(orphan_pages)} pages affected)",
                "category": "Site Architecture",
                "severity": "W",
                "affected": orphan_pages,
                "why": "সাইটম্যাপে লিংক রয়েছে কিন্তু সাইটের অন্য কোনো পেজ থেকে কোনো ইন্টারনাল লিংক নেই—ফলে লিংক জুস শূন্য থাকে।",
                "fix": "প্রাসঙ্গিক অন্য ব্লগ বা সার্ভিস পেজ থেকে এই অর্ফান পেজগুলোর প্রতি ইনবাউন্ড ইন্টারনাল লিংক যুক্ত করুন।"
            })

        # 12. Slow Latency TTFB Pages
        if slow_pages:
            warnings.append({
                "id": "PERF-001",
                "title": f"High Server TTFB Latency (>1.2s) ({len(slow_pages)} pages affected)",
                "category": "Performance & Core Web Vitals",
                "severity": "W",
                "affected": slow_pages,
                "why": "সার্ভার রেসপন্স টাইম (TTFB) ১.২ সেকেন্ডের বেশি হলে Core Web Vitals (LCP/INP) ফেইল করে।",
                "fix": "সার্ভার ক্যাশিং (Redis/FastCGI), CDN (Cloudflare) এবং ডাটাবেস কোয়েরি অপ্টিমাইজ করুন।"
            })

        # Calculate Semrush-Grade Health Score (0-100)
        # 100 - (criticals * 15) - (warnings * 4) - (notices * 1)
        score_penalty = (len(critical_issues) * 15) + (len(warnings) * 4) + (len(notices) * 1)
        health_score = max(20, min(98, 100 - score_penalty))
        
        if health_score >= 85:
            health_grade = "Good (Enterprise Standard)"
        elif health_score >= 70:
            health_grade = "Fair (Moderate Vulnerabilities)"
        elif health_score >= 50:
            health_grade = "Needs Work (High Vulnerabilities)"
        else:
            health_grade = "Critical Issues Detected"

        # Prepare Clean Crawled Pages Table Format
        table_pages = []
        for p in pages:
            u = p["url"]
            table_pages.append({
                "url": u,
                "status_code": p.get("status_code", 200),
                "depth": p.get("depth", 1),
                "title": p.get("title", ""),
                "h1": p.get("h1", ""),
                "word_count": p.get("word_count", 0),
                "ttfb_ms": p.get("ttfb_ms", 0),
                "inlinks_count": len(self.inlinks_map.get(u, [])),
                "outlinks_count": len([l for l in self.outlinks_map.get(u, []) if l.get("is_internal")]),
                "external_links_count": len([l for l in self.outlinks_map.get(u, []) if not l.get("is_internal")]),
                "images_count": p.get("images_count", 0),
                "missing_alt_count": p.get("missing_alt_count", 0),
                "canonical": p.get("canonical", ""),
                "meta_robots": p.get("meta_robots", "")
            })

        # Top Linked Pages & Under-linked Pages
        sorted_by_inlinks = sorted(table_pages, key=lambda x: x["inlinks_count"], reverse=True)
        top_linked_pages = sorted_by_inlinks[:5]
        under_linked_pages = [p for p in sorted_by_inlinks if p["inlinks_count"] <= 1][:5]

        # Evaluate the 151-rule Developer Checklist on the Seed Page DOM
        seed_page = self.crawled_pages.get(self.seed_url, pages[0] if pages else {})
        developer_checklist = {}
        try:
            site_audit_engine = SiteAuditEngine(
                target_url=self.seed_url,
                raw_html=seed_page.get("raw_html", ""),
                status_code=seed_page.get("status_code", 200),
                headers=seed_page.get("headers", {}),
                resp_meta={"ttfb_ms": seed_page.get("ttfb_ms", 0), "status_code": seed_page.get("status_code", 200)},
                soup=seed_page.get("soup"),
                robots_data={"exists": self.robots_exists, "disallow_count": len(self.disallowed_paths)},
                sitemap_data={"exists": self.sitemap_exists, "url_count": len(self.sitemap_urls)},
                main_keyword=""
            )
            developer_checklist = site_audit_engine.evaluate()
        except Exception:
            developer_checklist = {}

        all_site_issues = critical_issues + warnings + notices

        avg_ttfb = round(sum(p.get("ttfb_ms", 0) for p in pages) / total_pages) if total_pages else 0
        total_site_words = sum(p.get("word_count", 0) for p in pages)

        crawl_summary = {
            "total_crawled": total_pages,
            "status_200": status_200,
            "status_3xx": status_3xx,
            "status_4xx": status_4xx,
            "status_5xx": status_5xx,
            "indexable_count": status_200,
            "redirect_count": status_3xx,
            "broken_count": len(self.broken_links) + status_4xx,
            "healthy_pct": round((status_200 / total_pages * 100) if total_pages else 100, 1),
            "broken_links_count": len(self.broken_links),
            "orphan_pages_count": len(orphan_pages),
            "depth_distribution": depth_dist,
            "avg_ttfb_ms": avg_ttfb,
            "total_words": total_site_words,
            "robots_exists": self.robots_exists,
            "sitemap_exists": self.sitemap_exists,
            "sitemap_url_count": len(self.sitemap_urls)
        }

        return {
            "target_url": self.seed_url,
            "domain": self.base_domain,
            "base_domain": self.base_domain,
            "total_crawled": total_pages,
            "health_score": health_score,
            "health_grade": health_grade,
            "crawl_stats": crawl_summary,
            "crawl_summary": crawl_summary,
            "issues_summary": {
                "total_issues": len(critical_issues) + len(warnings) + len(notices),
                "critical_count": len(critical_issues),
                "warnings_count": len(warnings),
                "notices_count": len(notices)
            },
            "site_issues": all_site_issues,
            "critical_errors": critical_issues,
            "warnings": warnings,
            "notices": notices,
            "broken_links": self.broken_links,
            "broken_internal_links": self.broken_links,
            "orphan_pages": orphan_pages,
            "sitemap_status": {
                "found": self.sitemap_exists,
                "total_sitemap_urls": len(self.sitemap_urls),
                "orphan_urls_detected": orphan_pages
            },
            "robots_txt": {
                "found": self.robots_exists,
                "rules_count": len(self.disallowed_paths)
            },
            "top_linked_pages": top_linked_pages,
            "under_linked_pages": under_linked_pages,
            "crawled_pages": table_pages,
            "developer_checklist": developer_checklist
        }
