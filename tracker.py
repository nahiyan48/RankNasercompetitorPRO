#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Competitor Keyword & Article Tracker (আজকের আর্টিকেল ও কিওয়ার্ড মনিটর)
=============================================================================
Author: BeyondSEO Automation
Description:
    Track competitor websites to find newly published articles for today.
    Extracts:
    1. Published Articles (Today's Date)
    2. Targeted Product / Core Topic
    3. Main Focus Keyword
    4. LSI & Secondary Keywords
    5. Search Intent & Headings (H1, H2, H3)
    6. Export to CSV, JSON, and Markdown Report
=============================================================================
"""

import os
import sys
import io

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import re
import csv
import json
import logging
from datetime import datetime, date, timezone
from urllib.parse import urljoin, urlparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET

# Attempt third-party imports with clear guidance if missing
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("\n[!] Necessary libraries are missing. Please install them first:")
    print("    pip install requests beautifulsoup4 python-dateutil\n")
    sys.exit(1)

try:
    from dateutil import parser as date_parser
except ImportError:
    date_parser = None

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Optional AI enhancement
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CompetitorTracker")

# Common English & Web Stopwords to filter out noise
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could',
    'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each', 'few', 'for',
    'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll',
    'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i', 'i\'d',
    'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me',
    'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s',
    'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them',
    'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this',
    'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll',
    'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which',
    'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d',
    'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves', 'read', 'share', 'author', 'posted',
    'comment', 'comments', 'click', 'view', 'updated', 'published', 'table', 'contents', 'conclusion', 'faq', 'faqs'
}

SKIP_PATH_TERMS = {
    'tag', 'tags', 'category', 'categories', 'author', 'authors', 
    'page', 'feed', 'rss', 'wp-json', 'xmlrpc', 'cart', 'checkout',
    'account', 'login', 'signup', 'register', 'terms', 'privacy',
    'privacy-policy', 'terms-conditions', 'contact', 'about-us'
}

BLOG_CATEGORY_SLUGS = {
    'best-products', 'comparisons', 'buying-guides', 'tech-trends', 
    'all', 'news', 'topics', 'archive', 'archives'
}

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
}


class CompetitorTracker:
    def __init__(self, target_url: str, target_date: date = None, gemini_api_key: str = None):
        """
        Initialize competitor tracker.
        :param target_url: Competitor's base website URL (e.g. https://competitor.com)
        :param target_date: Target publication date (default: today's date)
        :param gemini_api_key: Optional Gemini API key for deep AI-powered SEO analysis
        """
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "https://" + target_url
        
        parsed = urlparse(target_url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.target_url = target_url
        clean_path = parsed.path.strip('/')
        self.is_single_page = bool(clean_path and clean_path not in ['blog', 'articles', 'news', 'insights'])
        self.target_date = target_date or datetime.now().date()
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        if self.gemini_api_key and HAS_GEMINI:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            logger.info("Gemini AI integration activated for high-precision keyword analysis.")
        else:
            self.model = None

        self.recent_fallback_urls = []

    def fetch_url(self, url: str, timeout: int = 5) -> str:
        """Fetch content of a URL safely."""
        try:
            resp = self.session.get(url, timeout=timeout)
            if resp.status_code == 200:
                return resp.text
            else:
                logger.debug(f"Failed to fetch {url} (Status: {resp.status_code})")
        except Exception as e:
            logger.debug(f"Error fetching {url}: {e}")
        return ""

    def parse_url_date(self, url: str) -> date:
        """Extract date specifically from URL path structures like /2026/10/04/ or /2026-10-04-"""
        if not url:
            return None
        m = re.search(r"/(20[12]\d)[/-](0?[1-9]|1[0-2])[/-](0?[1-9]|[12]\d|3[01])(?:/|-|_|$)", url)
        if m:
            try:
                return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                pass
        return None

    def is_valid_article_url(self, url: str) -> bool:
        """Validate whether a candidate URL is a genuine article, not a category/tag/utility page."""
        parsed = urlparse(url)
        base_domain = urlparse(self.base_url).netloc.lower()
        if parsed.netloc and parsed.netloc.lower() != base_domain:
            return False
        path = parsed.path.rstrip('/').lower()
        parts = [p for p in path.split('/') if p]
        if not parts:
            return False
        if any(p in SKIP_PATH_TERMS for p in parts):
            return False
        if parts[-1] in BLOG_CATEGORY_SLUGS:
            return False
        return True

    def parse_date_string(self, date_str: str) -> date:
        """Parse various date formats into date object with strict year sanity checks."""
        if not date_str:
            return None
        date_str = str(date_str).strip()
        # Clean weird dots or separators like "10 Sep, 2025 . 1:38 PM"
        clean_str = re.sub(r'[\.\•]', ' ', date_str)
        # Remove prefixes like "event", "Updated : ", "Published : "
        clean_str = re.sub(r'^(event|[a-zA-Z\s]*:)\s*', '', clean_str).strip()
        
        parsed_dt = None
        # Try dateutil parser if available
        if date_parser:
            try:
                dt = date_parser.parse(clean_str, fuzzy=True)
                parsed_dt = dt.date()
            except Exception:
                pass
        
        if not parsed_dt:
            # Fallback regex patterns: YYYY-MM-DD
            m = re.search(r"\b(20[12]\d)[-/.](\d{1,2})[-/.](\d{1,2})\b", date_str)
            if m:
                try:
                    parsed_dt = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                except ValueError:
                    pass

        # Strict year sanity check: must be a realistic recent publication date (2015 to current_year + 1)
        curr_year = datetime.now().year
        if parsed_dt and (2015 <= parsed_dt.year <= curr_year + 1):
            return parsed_dt
                
        return None

    def discover_sitemaps_from_robots(self) -> list:
        """Dynamically discover all sitemaps declared in competitor's robots.txt."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        text = self.fetch_url(robots_url, timeout=6)
        if not text:
            return []
            
        sitemaps = []
        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("sitemap:"):
                sm_url = line.split(":", 1)[1].strip()
                if sm_url and sm_url.startswith("http") and sm_url not in sitemaps:
                    sitemaps.append(sm_url)
        return sitemaps

    def discover_articles_from_sitemaps(self) -> list:
        """Check standard sitemaps and robots.txt for articles published/modified on target_date."""
        sitemap_paths = [
            "/news-sitemap.xml",
            "/sitemaps/google_news",
            "/sitemap-news.xml",
            "/sitemap.xml",
            "/wp-sitemap.xml",
            "/sitemap_index.xml",
            "/post-sitemap.xml"
        ]
        
        discovered_today = []
        dated_candidates = []
        checked_sitemaps = set()
        
        # 1. Combine robots.txt sitemaps + standard sitemaps
        all_sitemaps = self.discover_sitemaps_from_robots()
        for path in sitemap_paths:
            s_url = urljoin(self.base_url, path)
            if s_url not in all_sitemaps:
                all_sitemaps.append(s_url)

        # Prioritize news and recent sitemaps first!
        def _sm_priority(url):
            u = url.lower()
            if "news" in u: return 0
            if "post" in u or "article" in u: return 1
            if "blog" in u: return 2
            return 3
        all_sitemaps.sort(key=_sm_priority)
        
        def process_sitemap(sitemap_url: str, depth: int = 0):
            if depth > 2 or sitemap_url in checked_sitemaps:
                return
            checked_sitemaps.add(sitemap_url)
            
            xml_text = self.fetch_url(sitemap_url, timeout=4)
            if not xml_text or ("<urlset" not in xml_text and "<sitemapindex" not in xml_text and "<rss" not in xml_text):
                return
            
            try:
                soup = BeautifulSoup(xml_text, "xml")
                
                # Check if it's a Sitemap Index
                sub_sitemaps = soup.find_all("sitemap")
                if sub_sitemaps:
                    all_subs = []
                    for sitemap_node in sub_sitemaps:
                        loc_node = sitemap_node.find("loc")
                        if loc_node and loc_node.text:
                            all_subs.append(loc_node.text.strip())
                            
                    # Prioritize news sub-sitemaps or content sub-sitemaps (excluding tags/categories/authors)
                    news_subs = [s for s in all_subs if "news" in s.lower()]
                    content_subs = [s for s in all_subs if any(k in s.lower() for k in ["post", "blog", "article", "entry"]) and not any(skip in s.lower() for skip in ["tag", "category", "author", "user"])]
                    
                    if news_subs:
                        targets = news_subs[:2]
                    elif content_subs:
                        targets = content_subs[-2:]
                    else:
                        non_tax = [s for s in all_subs if not any(skip in s.lower() for skip in ["tag", "tax", "category", "author"])]
                        targets = (non_tax or all_subs)[-2:]

                    for sm in targets:
                        process_sitemap(sm, depth + 1)
                
                # Check urlset
                urls = soup.find_all("url")
                for url_node in urls:
                    loc_node = url_node.find("loc")
                    lastmod_node = (
                        url_node.find("lastmod") or 
                        url_node.find("publication_date") or 
                        url_node.find("pubDate")
                    )
                    
                    if loc_node and loc_node.text:
                        article_url = loc_node.text.strip()
                        if not self.is_valid_article_url(article_url):
                            continue
                            
                        article_date = None
                        if lastmod_node and lastmod_node.text:
                            article_date = self.parse_date_string(lastmod_node.text)
                            
                        if not article_date:
                            article_date = self.parse_url_date(article_url)
                            
                        # Only accept URLs that have a verified date or are explicit article paths
                        is_article_path = any(seg in article_url.lower() for seg in ['/blog/', '/news/', '/article/', '/post/'])
                        if article_date or is_article_path:
                            dated_candidates.append((article_date, article_url))
                            if article_date == self.target_date:
                                discovered_today.append(article_url)
                            
            except Exception as e:
                logger.debug(f"Error parsing sitemap {sitemap_url}: {e}")

        for s_url in all_sitemaps[:5]:
            process_sitemap(s_url)
            if discovered_today or len(dated_candidates) >= 25:
                break
                
        # Sort dated candidates by date DESCENDING (freshest and most recent first!)
        dated_candidates.sort(key=lambda x: x[0] or date(1970, 1, 1), reverse=True)
        for d, u in dated_candidates:
            if u not in self.recent_fallback_urls:
                self.recent_fallback_urls.append(u)
            
        return list(dict.fromkeys(discovered_today))

    def discover_articles_from_rss(self) -> list:
        """Check RSS / Atom feeds for today's articles and recent articles."""
        feed_paths = [
            "/feed",
            "/rss.xml",
            "/feed.xml",
            "/rss",
            "/index.xml"
        ]
        
        discovered_today = []
        dated_candidates = []
        
        for path in feed_paths:
            feed_url = urljoin(self.base_url, path)
            xml_text = self.fetch_url(feed_url, timeout=3.5)
            if not xml_text or ("<rss" not in xml_text and "<feed" not in xml_text and "<channel" not in xml_text):
                continue
                
            try:
                soup = BeautifulSoup(xml_text, "xml")
                items = soup.find_all("item") or soup.find_all("entry")
                    
                for item in items:
                    link_tag = item.find("link")
                    url = ""
                    if link_tag:
                        url = link_tag.get("href") or link_tag.text.strip()
                        
                    pub_date_tag = (
                        item.find("pubDate") or 
                        item.find("published") or 
                        item.find("updated") or 
                        item.find("dc:date")
                    )
                    
                    if url and self.is_valid_article_url(url):
                        p_date = None
                        if pub_date_tag and pub_date_tag.text:
                            p_date = self.parse_date_string(pub_date_tag.text)
                        if not p_date:
                            p_date = self.parse_url_date(url)
                            
                        dated_candidates.append((p_date, url))
                        
                        if p_date == self.target_date:
                            discovered_today.append(url)
                            
            except Exception as e:
                logger.debug(f"Feed parse error on {feed_url}: {e}")
                
            if discovered_today or dated_candidates:
                break
                
        # Sort dated candidates by date DESCENDING (freshest first)
        dated_candidates.sort(key=lambda x: x[0] or date(1970, 1, 1), reverse=True)
        for d, u in dated_candidates:
            if u not in self.recent_fallback_urls:
                self.recent_fallback_urls.append(u)
            
        return list(dict.fromkeys(discovered_today))

    def discover_articles_from_blog_page(self) -> list:
        """Scan competitor's blog or news listing page for today's articles and recent articles."""
        blog_paths = ["/blog", "/blog/", "/articles", "/news", "/insights", ""]
        discovered_today = []
        dated_candidates = []
        
        for path in blog_paths:
            page_url = urljoin(self.base_url, path)
            html = self.fetch_url(page_url, timeout=7)
            if not html:
                continue
                
            soup = BeautifulSoup(html, "html.parser")
            seen_urls = set()
            
            for a in soup.find_all("a", href=True):
                full_link = urljoin(self.base_url, a['href'])
                if full_link in seen_urls or not self.is_valid_article_url(full_link):
                    continue
                    
                path_clean = urlparse(full_link).path.rstrip('/')
                parts = [p for p in path_clean.split('/') if p]
                if not parts:
                    continue
                    
                is_article = False
                if len(parts) >= 2 and parts[0].lower() in ['blog', 'news', 'article', 'articles', 'insights', 'post', 'posts']:
                    is_article = True
                elif len(parts) >= 3 and any(p.isdigit() for p in parts):
                    is_article = True
                elif any(seg in full_link.lower() for seg in ['/blog/', '/news/', '/article/', '/post/']):
                    is_article = True
                    
                if not is_article:
                    continue
                    
                seen_urls.add(full_link)
                
                # Walk up DOM tree up to 4 levels to find card container and date
                date_val = None
                curr = a
                for _ in range(4):
                    if curr and curr.parent:
                        curr = curr.parent
                        time_tag = curr.find("time")
                        if time_tag:
                            dt_str = time_tag.get("datetime") or time_tag.text
                            date_val = self.parse_date_string(dt_str)
                            if date_val:
                                break
                                
                        m = re.search(r'\b(?:event\s*)?(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\b', curr.text)
                        if m:
                            date_val = self.parse_date_string(m.group(1))
                            if date_val:
                                break
                    else:
                        break
                        
                if not date_val:
                    date_val = self.parse_url_date(full_link)
                    
                dated_candidates.append((date_val, full_link))
                if date_val == self.target_date and full_link not in discovered_today:
                    discovered_today.append(full_link)
                    
            if discovered_today or dated_candidates:
                break
                
        # Sort dated candidates by date DESCENDING (freshest and most recent first!)
        dated_candidates.sort(key=lambda x: x[0] or date(1970, 1, 1), reverse=True)
        for d, u in dated_candidates:
            if u not in self.recent_fallback_urls:
                self.recent_fallback_urls.append(u)
            
        return list(dict.fromkeys(discovered_today))

    def discover_top_pages_from_site(self) -> list:
        """
        Universal fallback: Discover top brand, category, service, and landing pages
        from the competitor's website when no blog/sitemap articles exist.
        """
        html = self.fetch_url(self.base_url, timeout=10)
        if not html:
            return []
            
        soup = BeautifulSoup(html, "html.parser")
        base_domain = urlparse(self.base_url).netloc.lower()
        skip_terms = {
            'login', 'register', 'signin', 'signup', 'account', 'cart', 'checkout',
            'wishlist', 'privacy', 'policy', 'terms', 'conditions', 'cookie', 'cookies',
            'contact', 'contact-us', 'about-us', 'search', 'faq', 'help', 'returns',
            'shipping', 'track', 'career', 'careers', 'jobs', 'wp-admin', 'cdn-cgi',
            'customer', 'password', 'feed', 'rss'
        }
        
        discovered_pages = []
        for a in soup.find_all("a", href=True):
            href = a['href'].strip()
            if not href or href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
                
            full_url = urljoin(self.base_url, href).split('#')[0].split('?')[0].rstrip('/')
            parsed = urlparse(full_url)
            if parsed.netloc.lower() != base_domain:
                continue
                
            path = parsed.path.strip('/')
            if not path:
                continue
                
            parts = [p.lower() for p in path.split('/') if p]
            if any(term in p for term in skip_terms for p in parts):
                continue
                
            if len(path) > 3 and full_url not in discovered_pages:
                discovered_pages.append(full_url)
                if len(discovered_pages) >= 8:
                    break
                    
        return discovered_pages

    def extract_article_date(self, soup: BeautifulSoup, html: str, url: str) -> date:
        """Find the publication date from article HTML."""
        # 1. Check JSON-LD
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "{}")
                if isinstance(data, list):
                    items = data
                elif "@graph" in data:
                    items = data["@graph"]
                else:
                    items = [data]
                    
                for it in items:
                    p_date_str = it.get("datePublished") or it.get("dateModified")
                    if p_date_str:
                        p_date = self.parse_date_string(p_date_str)
                        if p_date:
                            return p_date
            except Exception:
                pass
                
        # 2. Check Meta tags (including modified / updated dates)
        meta_keys = [
            {"property": "article:modified_time"},
            {"name": "article:modified_time"},
            {"property": "og:updated_time"},
            {"property": "article:published_time"},
            {"name": "article:published_time"},
            {"property": "og:article:published_time"},
            {"name": "publish-date"},
            {"name": "pubdate"},
            {"itemprop": "datePublished"},
            {"itemprop": "dateModified"}
        ]
        for key in meta_keys:
            tag = soup.find("meta", key)
            if tag and tag.get("content"):
                d = self.parse_date_string(tag.get("content"))
                if d:
                    return d
                    
        # 3. Check <time> tag
        for time_tag in soup.find_all("time"):
            dt_str = time_tag.get("datetime") or time_tag.text
            d = self.parse_date_string(dt_str)
            if d:
                return d
                
        # 4. Check text regex for patterns like "22 Jul 2026" or "October 4, 2026"
        m = re.search(r'\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b', html, re.I)
        if m:
            d = self.parse_date_string(m.group(1))
            if d:
                return d

        # 5. Check URL path
        return self.parse_url_date(url)

    def clean_product_name(self, title: str, h1: str) -> str:
        """Accurately extract target product/service name from title or h1."""
        candidate = h1 or title
        # Remove site branding
        t = re.sub(r'\|\s*.*$', '', candidate).strip()
        t = re.split(r'[:–—]', t)[0].strip()
        
        # Check vs comparison: 'AirPods 5 vs AirPods 4' -> 'AirPods'
        vs_m = re.search(r'([A-Za-z0-9\s]+?)(?:\s+\d+)?\s+vs\s+', t, re.I)
        if vs_m:
            cand = vs_m.group(1).strip()
            cand = re.sub(r'^(the|best|new)\s+', '', cand, flags=re.I).strip()
            return cand.title()
            
        # Strip common guide/ranking prefixes
        t = re.sub(r'^(top\s+\d+|best\s+\d+|best|latest|upcoming|complete|ultimate|the|list\s+of|which|how\s+to\s+choose\s+the|how\s+to\s+choose)\s+', '', t, flags=re.I)
        # Strip suffixes
        t = re.sub(r'\s+(buying\s+guide|guide|detailed\s+review|review|reviews|features|models|list|tips|troubleshooting|setup).*$', '', t, flags=re.I)
        # Strip location & year
        t = re.sub(r'\s+in\s+bangladesh.*$', '', t, flags=re.I)
        t = re.sub(r'\s+(in\s+\d{4}|\d{4}|for\s+summer.*)$', '', t, flags=re.I)
        # Strip common trailing noise
        t = re.sub(r'\s+in\s+fan', '', t, flags=re.I)
        t = re.sub(r'\s+(in|for|of|at|on|with|to|and|by)$', '', t, flags=re.I).strip()
        
        if t.lower().endswith('fans'):
            t = t[:-1]
            
        if t.lower() == 'ac':
            return 'Air Conditioner (AC)'
            
        return t.title() if len(t) >= 2 else "General Product"

    def extract_main_keyword(self, title: str, h1: str, slug: str) -> str:
        """Extract the exact focus keyword targeting Google search."""
        candidate = h1 or title
        # Strip site brand suffix
        t = re.sub(r'\|\s*.*$', '', candidate).strip()
        t = re.split(r'[:–—]', t)[0].strip()
        t = re.sub(r'\s+(detailed\s+review|features\s+&\s+buying\s+guide).*$', '', t, flags=re.I)
        t_clean = re.sub(r'[^\w\s]', '', t).strip()
        
        words = [w for w in t_clean.split() if w.lower() not in ['star', 'tech', 'blog']]
        if 2 <= len(words) <= 6:
            return " ".join(words).title()
            
        # Fallback to slug title
        slug_clean = re.sub(r'[-_/]', ' ', slug).strip()
        slug_words = [w for w in slug_clean.split() if w.lower() not in STOPWORDS and w.lower() not in ['blog', 'news', 'article', 'articles', 'post', 'posts']]
        if slug_words:
            return " ".join(slug_words[:5]).title()
            
        return t.title()

    def extract_keywords_nlp(self, title: str, h1: str, h2s: list, h3s: list, body_text: str, slug: str) -> dict:
        """
        Pure Python High-Precision NLP Engine:
        1. Target Product
        2. Main Focus Keyword
        3. Clean LSI Keywords (No timer, event, or web UI noise)
        """
        # 1. Product Name Detection
        product_name = self.clean_product_name(title, h1)
        
        # 2. Main Focus Keyword
        main_keyword = self.extract_main_keyword(title, h1, slug)
        
        # 3. High-Quality LSI & Secondary Keywords Detection
        lsi_candidates = []
        seen = {main_keyword.lower(), product_name.lower()}
        
        FORBIDDEN = {
            'why', 'would', 'you', 'are', 'can', 'how', 'what', 'where', 'when', 'who', 'which',
            'tip', 'tips', 'pro', 'step', 'steps', 'year', 'in', 'of', 'for', 'at', 'by', 'with',
            'to', 'and', 'or', 'the', 'a', 'an', 'your', 'our', 'my', 'this', 'that', 'these',
            'those', 'feels', 'different', 'needs', 'need', 'understand', 'consider', 'avoid',
            'common', 'mistakes', 'make', 'things', 'right', 'better', 'know', 'important', 'overview',
            'final', 'words', 'thoughts', 'guide', 'buying', 'bought', 'features', 'purchase', 'table',
            'contents', 'comment', 'comments', 'article', 'read', 'more', 'click', 'check', 'arrow',
            'timer', 'min', 'event', 'sep', 'may', 'star', 'tech', 'startech', 'blog', 'post', 'top',
            'best', 'latest', 'list', 'review', 'reviews', 'help', 'helpful', 'from', 'buy', 'get',
            'choosing', 'navigating', 'market', 'price', 'pricing', 'online', 'bangladesh', 'bd',
            'subheading', 'headings', 'heading', 'faqs', 'faq', 'frequently', 'asked', 'questions'
        }
        
        # Method A: High-Entropy Bigrams and Trigrams from body text
        words = re.findall(r'\b[a-zA-Z0-9\-\.]{3,}\b', body_text)
        clean_phrases = []
        for i in range(len(words) - 1):
            w1, w2 = words[i].lower(), words[i+1].lower()
            if w1 not in FORBIDDEN and w2 not in FORBIDDEN and not w1.isdigit() and not w2.isdigit() and w1 != w2:
                # Proper format: title case
                phrase_cand = f"{words[i]} {words[i+1]}".strip().title()
                clean_phrases.append(phrase_cand)
                
            if i < len(words) - 2:
                w3 = words[i+2].lower()
                if (w1 not in FORBIDDEN and w2 not in FORBIDDEN and w3 not in FORBIDDEN and
                    not w1.isdigit() and not w2.isdigit() and not w3.isdigit() and w1 != w2 and w2 != w3):
                    phrase_cand3 = f"{words[i]} {words[i+1]} {words[i+2]}".strip().title()
                    clean_phrases.append(phrase_cand3)
                    
        phrase_counts = Counter(clean_phrases)
        for p, count in phrase_counts.most_common(40):
            p_lower = p.lower()
            if count >= 2 and p_lower not in seen and len(p.split()) in [2, 3]:
                # Don't add if it's a substring of main keyword or product
                if p_lower not in main_keyword.lower() and p_lower not in product_name.lower():
                    lsi_candidates.append(p)
                    seen.add(p_lower)
                    if len(lsi_candidates) >= 7:
                        break
                        
        # Fallback to H2/H3 subheadings if body gave few results
        if len(lsi_candidates) < 5:
            for heading in (h2s + h3s):
                h_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', heading).strip()
                h_words = [w for w in h_clean.split() if w.lower() not in FORBIDDEN and len(w) > 2]
                if 2 <= len(h_words) <= 3:
                    p = " ".join(h_words).title()
                    if p.lower() not in seen:
                        lsi_candidates.append(p)
                        seen.add(p.lower())
                        
        return {
            "product_name": product_name,
            "main_keyword": main_keyword,
            "lsi_keywords": lsi_candidates[:7]
        }

    def analyze_with_gemini(self, title: str, h1: str, headings: list, sample_text: str) -> dict:
        """Use Gemini AI for professional human-grade SEO extraction."""
        if not self.model:
            return None
            
        prompt = f"""
        You are a Senior SEO Strategist and Competitor Intelligence Specialist.
        Analyze this newly published competitor article:
        
        Title: {title}
        H1: {h1}
        Subheadings (H2/H3): {', '.join(headings[:10])}
        Content Excerpt: {sample_text[:2000]}
        
        Extract and return ONLY a valid JSON object in this exact schema:
        {{
            "product_name": "Specific product or service being reviewed, promoted, or discussed (or 'N/A' if general informational)",
            "main_keyword": "The primary focus keyword this article is targeting to rank on Google",
            "search_intent": "Informational | Commercial | Transactional | Navigational",
            "lsi_keywords": ["LSI keyword 1", "LSI keyword 2", "LSI keyword 3", "LSI keyword 4", "LSI keyword 5"],
            "summary": "1 sentence summarizing what the article covers"
        }}
        Do NOT output markdown backticks or extra text, just raw JSON.
        """
        try:
            response = self.model.generate_content(prompt)
            clean_text = response.text.strip()
            # Clean possible markdown json wrapper
            clean_text = re.sub(r'^```json\s*', '', clean_text, flags=re.MULTILINE)
            clean_text = re.sub(r'```$', '', clean_text, flags=re.MULTILINE).strip()
            return json.loads(clean_text)
        except Exception as e:
            logger.debug(f"Gemini API call error: {e}")
            return None

    def analyze_article(self, article_url: str, enforce_date: bool = True) -> dict:
        """Scrape and analyze single article content."""
        html = self.fetch_url(article_url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, "html.parser")
        
        # Check publication date
        pub_date = self.extract_article_date(soup, html, article_url)
        
        # Filter: Only enforce date when strictly checking today's articles
        if enforce_date and pub_date and pub_date != self.target_date:
            return None
            
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").text.strip()
            
        h1_tag = soup.find("h1")
        h1 = h1_tag.text.strip() if h1_tag else title
        
        h2s = [h.text.strip() for h in soup.find_all("h2") if h.text.strip()]
        h3s = [h.text.strip() for h in soup.find_all("h3") if h.text.strip()]
        
        # Meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag.get("content").strip()
            
        # Clean text
        for s in soup(["script", "style", "nav", "footer", "header", "aside"]):
            s.decompose()
        for c in soup.find_all(class_=re.compile(r'(sidebar|comment|share|widget|meta|breadcrumb|author|related|timer|newsletter)', re.I)):
            c.decompose()
        body_text = soup.get_text(separator=" ", strip=True)
        
        parsed_url = urlparse(article_url)
        slug = parsed_url.path
        
        # Default NLP extraction
        nlp_result = self.extract_keywords_nlp(title, h1, h2s, h3s, body_text, slug)
        
        # Optional AI enhancement
        ai_result = None
        if self.model:
            ai_result = self.analyze_with_gemini(title, h1, h2s + h3s, body_text)
            
        if ai_result:
            product_name = ai_result.get("product_name") or nlp_result["product_name"]
            main_keyword = ai_result.get("main_keyword") or nlp_result["main_keyword"]
            lsi_keywords = ai_result.get("lsi_keywords") or nlp_result["lsi_keywords"]
            search_intent = ai_result.get("search_intent", "Informational")
            summary = ai_result.get("summary", meta_desc[:120])
        else:
            product_name = nlp_result["product_name"]
            main_keyword = nlp_result["main_keyword"]
            lsi_keywords = nlp_result["lsi_keywords"]
            search_intent = "N/A"
            summary = meta_desc[:120] if meta_desc else title
            
        return {
            "url": article_url,
            "title": title,
            "published_date": str(pub_date or self.target_date),
            "product_name": product_name,
            "main_keyword": main_keyword,
            "lsi_keywords": lsi_keywords,
            "search_intent": search_intent,
            "summary": summary,
            "h2_headings": h2s[:8]
        }

    def run(self) -> list:
        """Run full competitor scan for today's articles, top ranking pages, or single target page."""
        print("\n" + "="*70)
        print(f"[*] COMPETITOR TRACKER STARTING")
        print(f"[*] Target Site : {self.base_url}")
        print(f"[*] Target Date : {self.target_date}")
        print(f"[*] AI Mode     : {'Active (Gemini 1.5)' if self.model else 'Local Heuristic NLP (Free)'}")
        print("="*70 + "\n")
        
        # 1. Handle Single Page Input Directly
        if getattr(self, 'is_single_page', False):
            print(f"[*] Direct Page URL detected: {self.target_url}")
            print("[*] Analyzing target page directly...")
            data = self.analyze_article(self.target_url, enforce_date=False)
            if data:
                self.save_reports([data])
                return [data]
            else:
                return []

        # 2. Check Blog listing page FIRST (blazing fast, takes ~1s)
        print("[1/3] Checking Blog listing page...")
        candidate_urls = self.discover_articles_from_blog_page()
        print(f"      -> Found {len(candidate_urls)} URLs from blog listing matching today.")

        if not candidate_urls and len(self.recent_fallback_urls) < 4:
            print("[2/3] Scanning XML Sitemaps for new URLs...")
            candidate_urls = self.discover_articles_from_sitemaps()
            print(f"      -> Found {len(candidate_urls)} URLs from sitemap matching today.")
            
        if not candidate_urls and len(self.recent_fallback_urls) < 4:
            print("[3/3] Checking RSS / Atom feeds...")
            candidate_urls = self.discover_articles_from_rss()
            print(f"      -> Found {len(candidate_urls)} URLs from RSS feeds matching today.")
            
        is_recent_fallback = False
        if not candidate_urls:
            if self.recent_fallback_urls:
                unique_recents = list(dict.fromkeys(self.recent_fallback_urls))[:6]
                print(f"\n[-] No new articles detected with today's date ({self.target_date}).")
                print(f"[+] SMART FALLBACK: Analyzing the competitor's {len(unique_recents)} most recent articles instead...\n")
                candidate_urls = unique_recents
                is_recent_fallback = True
            else:
                # 4. Universal Fallback: Discover top pages from website
                print("[4/4] Discovering core landing, category, and product pages from website...")
                site_pages = self.discover_top_pages_from_site()
                if site_pages:
                    print(f"[+] Found {len(site_pages)} top competitor pages to analyze.")
                    candidate_urls = site_pages[:6]
                    is_recent_fallback = True
                else:
                    print(f"\n[-] No pages detected for {self.base_url}.")
                    return []
            
        results = []
        label = "recent / top" if is_recent_fallback else "today's"
        print(f"\n[*] Analyzing {len(candidate_urls)} {label} page(s) in parallel...\n")
        
        def _safe_analyze(url, enforce_d):
            try:
                return self.analyze_article(url, enforce_date=enforce_d)
            except Exception as e:
                logger.debug(f"Error analyzing {url}: {e}")
                return None

        with ThreadPoolExecutor(max_workers=min(len(candidate_urls) or 1, 5)) as executor:
            analyzed = list(executor.map(lambda u: _safe_analyze(u, not is_recent_fallback), candidate_urls))
            
        results = [a for a in analyzed if a]
                
        # If target date check yielded 0 valid articles, immediately fall back to the freshest recent articles!
        if not results and self.recent_fallback_urls:
            unique_recents = list(dict.fromkeys(self.recent_fallback_urls))[:6]
            print(f"\n[-] No articles confirmed for target date ({self.target_date}).")
            print(f"[+] SMART FALLBACK: Analyzing competitor's {len(unique_recents)} most recent active articles in parallel...\n")
            with ThreadPoolExecutor(max_workers=min(len(unique_recents) or 1, 5)) as executor:
                analyzed_fb = list(executor.map(lambda u: _safe_analyze(u, False), unique_recents))
            results = [a for a in analyzed_fb if a]

        # If still no results, fall back to core site pages
        if not results:
            site_pages = self.discover_top_pages_from_site()
            if site_pages:
                print(f"\n[+] Analyzing {len(site_pages[:6])} core pages from website...\n")
                with ThreadPoolExecutor(max_workers=min(len(site_pages[:6]) or 1, 5)) as executor:
                    analyzed_sp = list(executor.map(lambda u: _safe_analyze(u, False), site_pages[:6]))
                results = [a for a in analyzed_sp if a]

        # Sort ALL final results strictly by published_date DESCENDING (newest first!)
        def _get_sort_date(item):
            d_str = item.get("published_date")
            parsed_d = self.parse_date_string(d_str)
            return parsed_d or date(1970, 1, 1)

        results.sort(key=_get_sort_date, reverse=True)
        self.save_reports(results)
        return results

    def save_reports(self, results: list):
        """Save results to CSV, JSON, and Markdown formats."""
        if not results:
            return
            
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        date_str = str(self.target_date)
        domain = urlparse(self.base_url).netloc.replace(".", "_")
        
        # 1. Save CSV
        csv_file = os.path.join(reports_dir, f"competitor_{domain}_{date_str}.csv")
        with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Date", "Competitor URL", "Article Title", "Target Product",
                "Main Keyword", "LSI Keywords", "Search Intent", "Summary"
            ])
            for r in results:
                writer.writerow([
                    r["published_date"],
                    r["url"],
                    r["title"],
                    r["product_name"],
                    r["main_keyword"],
                    " | ".join(r["lsi_keywords"]),
                    r["search_intent"],
                    r["summary"]
                ])
                
        # 2. Save JSON
        json_file = os.path.join(reports_dir, f"competitor_{domain}_{date_str}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        # 3. Save Markdown Summary
        md_file = os.path.join(reports_dir, f"competitor_{domain}_{date_str}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"# Competitor Daily Article & Keyword Report\n\n")
            f.write(f"- **Website:** {self.base_url}\n")
            f.write(f"- **Date:** {self.target_date}\n")
            f.write(f"- **Total Articles Analyzed:** {len(results)}\n\n")
            f.write("---\n\n")
            for idx, r in enumerate(results, 1):
                f.write(f"### {idx}. {r['title']}\n")
                f.write(f"- **URL:** [{r['url']}]({r['url']})\n")
                f.write(f"- **Target Product / Topic:** `{r['product_name']}`\n")
                f.write(f"- **Main Focus Keyword:** `{r['main_keyword']}`\n")
                f.write(f"- **LSI / Secondary Keywords:**\n")
                for lsi in r["lsi_keywords"]:
                    f.write(f"  - {lsi}\n")
                if r.get("search_intent") != "N/A":
                    f.write(f"- **Search Intent:** {r['search_intent']}\n")
                f.write(f"- **Summary:** {r['summary']}\n\n")
                if r.get("h2_headings"):
                    f.write(f"- **Key Subheadings (H2):**\n")
                    for h2 in r["h2_headings"]:
                        f.write(f"  - {h2}\n")
                f.write("\n---\n\n")
                
        print("\n" + "="*70)
        print("[+] REPORTS SAVED SUCCESSFULLY!")
        print(f"    - CSV Report : {csv_file}")
        print(f"    - JSON Report: {json_file}")
        print(f"    - MD Report  : {md_file}")
        print("="*70 + "\n")


def interactive_cli():
    import time
    
    while True:
        print("\n" + "=" * 66)
        print("      COMPETITOR KEYWORD & ARTICLE TRACKER (PRO v1.0)             ")
        print("      Daily Article, Targeted Product & Keyword Intelligence Engine")
        print("=" * 66 + "\n")
        
        try:
            # 1. URL input
            url_input = input("Enter Competitor Website URL (or 'q' to exit): ").strip()
            if not url_input or url_input.lower() in ['q', 'exit', 'quit']:
                print("Exiting tracker. Goodbye!")
                break
                
            # 2. Date input
            today_str = str(date.today())
            date_input = input(f"Enter Target Date (Press Enter for Today [{today_str}]): ").strip()
            if date_input:
                try:
                    target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                except ValueError:
                    print("[!] Invalid date format. Using today's date instead.")
                    target_date = date.today()
            else:
                target_date = date.today()
                
            # 3. Optional Gemini API Key
            gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
            if not gemini_key:
                opt_key = input("Enter Google Gemini API Key (Optional - Press Enter for free offline mode): ").strip()
                if opt_key:
                    gemini_key = opt_key
                    
            tracker = CompetitorTracker(
                target_url=url_input,
                target_date=target_date,
                gemini_api_key=gemini_key if gemini_key else None
            )
            tracker.run()
            
        except Exception as e:
            print(f"\n[ERROR] An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()
            
        print("\n" + "=" * 60)
        print("  [1] Scan another competitor website")
        print("  [2] Exit (Close window)")
        print("=" * 60)
        choice = input("Enter choice (1/2): ").strip()
        if choice in ['2', 'q', 'exit', 'quit']:
            print("\nExiting. Thank you!")
            time.sleep(1)
            break


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_url = sys.argv[1]
            input_date = None
            if len(sys.argv) > 2:
                try:
                    input_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
                except Exception:
                    pass
            tracker = CompetitorTracker(target_url=input_url, target_date=input_date)
            tracker.run()
            input("\nExecution completed. Press Enter to exit...")
        else:
            interactive_cli()
    except Exception as e:
        print(f"\n[ERROR] Execution failed: {e}")
        input("\nPress Enter to exit...")
