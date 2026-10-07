#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
Multi-Competitor Reverse Engineering & Master Outranker (5 vs 1 Battle Royale)
=============================================================================
Author: BeyondSEO Automation
Description:
    Analyzes up to 5 competitor URLs simultaneously in parallel,
    benchmarks against the user's target URL, extracts collective intelligence
    (word counts, headings, LSI clusters, content gaps),
    and generates an ultimate outranking master article branded for the user.
=============================================================================
"""

import os
import sys
import re
import json
import logging
from urllib.parse import urlparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from competitor_spy import CompetitorSpyEngine
from content_writer import ContentWritingAgent

logger = logging.getLogger("MultiCompetitorEngine")


def sanitize_product_entity(name: str) -> str:
    """
    Strips search intent noise from a product name so it becomes a clean noun/entity.
    E.g. 'Air Fryer Price in BD' -> 'Air Fryer'
         'Best iPhone 15 Pro Max Price' -> 'iPhone 15 Pro Max'
    """
    if not name:
        return "Product"
    t = name.strip()
    t = re.sub(r'\|\s*.*$', '', t).strip()
    t = re.split(r'[:–—]', t)[0].strip()
    t = re.sub(r'^(?:top\s+\d+|best\s+\d+|best|latest|new|upcoming|complete|ultimate|the|list\s+of|buy|cheap|affordable)\s+', '', t, flags=re.I)
    t = re.sub(r'\b(?:price|prices|pricing|dam|rate|cost|costs|specs|specification|specifications|review|reviews|buying\s+guide|guide|deals?)\b', '', t, flags=re.I)
    t = re.sub(r'\b(?:in\s+bangladesh|in\s+bd|in\s+india|in\s+usa|in\s+uk|in\s+uae|in\s+canada|in\s+australia|bd|bangladesh|india|usa|uk|uae)\b', '', t, flags=re.I)
    t = re.sub(r'\b(?:202[4-9]|203[0-9])\b', '', t, flags=re.I)
    t = re.sub(r'\s+(?:in|for|of|at|on|with|to|and|by)$', '', t, flags=re.I).strip(' -.,:')
    t = re.sub(r'\s+', ' ', t).strip()
    return t.title() if len(t) >= 2 else name.title()


class MultiCompetitorEngine:
    def __init__(
        self,
        competitor_urls: list,
        user_url: str = "",
        brand_name: str = "",
        focus_keyword: str = "",
        gemini_api_key: str = None,
        target_country: str = "Bangladesh"
    ):
        """
        Initialize the 5-Competitor Punch Engine.
        """
        # Clean competitor URLs (filter empty, keep up to 5)
        clean_urls = []
        for u in competitor_urls:
            if not u:
                continue
            u = u.strip()
            if not u.startswith("http://") and not u.startswith("https://"):
                u = "https://" + u
            if u not in clean_urls:
                clean_urls.append(u)
        self.competitor_urls = clean_urls[:5]

        # Clean user URL
        self.user_url = user_url.strip() if user_url else ""
        if self.user_url and not self.user_url.startswith("http://") and not self.user_url.startswith("https://"):
            self.user_url = "https://" + self.user_url

        self.brand_name = brand_name.strip() if brand_name else "Our Editorial Team"
        self.focus_keyword = focus_keyword.strip() if focus_keyword else ""
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.target_country = target_country.strip() if target_country else "Bangladesh"

    def run_multi_audit(self) -> dict:
        """
        Concurrently crawl and audit all competitor URLs and the user's URL.
        """
        if not self.competitor_urls:
            return {"error": "At least 1 competitor URL is required."}

        competitor_results = []
        user_result = None

        all_urls_to_audit = [(u, False) for u in self.competitor_urls]
        if self.user_url:
            all_urls_to_audit.append((self.user_url, True))

        # Run concurrent audits
        with ThreadPoolExecutor(max_workers=min(len(all_urls_to_audit), 6)) as executor:
            future_to_url = {
                executor.submit(self._audit_single_url, url_info[0]): url_info
                for url_info in all_urls_to_audit
            }
            for future in as_completed(future_to_url):
                url, is_user = future_to_url[future]
                try:
                    res = future.result()
                    if is_user:
                        user_result = res
                    else:
                        competitor_results.append(res)
                except Exception as e:
                    logger.error(f"Error auditing {url}: {e}")
                    if is_user:
                        user_result = {"url": url, "error": str(e), "is_user": True}
                    else:
                        competitor_results.append({"url": url, "error": str(e), "is_user": False})

        # Sort competitor results in same order as input
        ordered_competitors = []
        for u in self.competitor_urls:
            for c in competitor_results:
                if c.get("url") == u:
                    ordered_competitors.append(c)
                    break

        return self.synthesize_analysis(ordered_competitors, user_result)

    def _audit_single_url(self, url: str) -> dict:
        """Audit a single URL using CompetitorSpyEngine."""
        spy = CompetitorSpyEngine(url)
        data = spy.run_full_spy()
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")

        if "error" in data or not data.get("audit"):
            return {
                "url": url,
                "domain": domain,
                "status": "failed",
                "error": data.get("error", "Unable to fetch page content")
            }

        audit = data["audit"]
        return {
            "url": url,
            "domain": domain,
            "status": "success",
            "title": audit.get("title", ""),
            "meta_description": audit.get("meta_description", ""),
            "slug": audit.get("slug", ""),
            "main_keyword": audit.get("main_keyword", ""),
            "product_name": audit.get("product_name", ""),
            "word_count": audit.get("word_count", 0),
            "reading_time": audit.get("reading_time", "1 min"),
            "seo_score": audit.get("seo_score", 50),
            "headings_count": len(audit.get("headings", [])),
            "headings": audit.get("headings", []),
            "all_headings": audit.get("all_headings", []),
            "lsi_keywords": audit.get("lsi_keywords", []),
            "ranking_reasons": audit.get("ranking_reasons", []),
            "content_gaps": audit.get("content_gaps", []),
            "schema_types": [s.get("type") for s in audit.get("schemas", []) if s.get("type")]
        }

    def synthesize_analysis(self, competitors: list, user_audit: dict = None) -> dict:
        """
        Synthesize cross-competitor intelligence and create outranking formula.
        """
        valid_comps = [c for c in competitors if c.get("status") == "success"]
        if not valid_comps:
            return {
                "status": "error",
                "message": "All competitor URLs failed to load. Please check the URLs.",
                "competitors": competitors
            }

        # 1. Word Count Statistics
        word_counts = [c.get("word_count", 0) for c in valid_comps]
        max_words = max(word_counts) if word_counts else 1000
        avg_words = round(sum(word_counts) / len(word_counts)) if word_counts else 1000
        min_words = min(word_counts) if word_counts else 500

        # Outrank target: 20-30% above the longest competitor
        target_outrank_words = max(int(max_words * 1.25), 2000)

        # 2. Main Focus Keyword & Product Synthesis
        if not self.focus_keyword:
            kw_candidates = [c.get("main_keyword", "") for c in valid_comps if c.get("main_keyword")]
            if kw_candidates:
                # Most common keyword
                self.focus_keyword = Counter(kw_candidates).most_common(1)[0][0]
            else:
                self.focus_keyword = valid_comps[0].get("title", "Best Solutions")[:40]

        product_candidates = [c.get("product_name", "") for c in valid_comps if c.get("product_name")]
        raw_product = Counter(product_candidates).most_common(1)[0][0] if product_candidates else self.focus_keyword
        product_name = sanitize_product_entity(raw_product)

        # 3. Collective LSI & Entity Cluster
        all_lsis = []
        for c in valid_comps:
            all_lsis.extend([k.lower() for k in c.get("lsi_keywords", []) if len(k) > 2])

        lsi_counter = Counter(all_lsis)
        # Core keywords: present in multiple competitors
        core_keywords = [kw.title() for kw, count in lsi_counter.items() if count >= 2]
        # High value depth keywords: top remaining
        depth_keywords = [kw.title() for kw, count in lsi_counter.most_common(25) if kw.title() not in core_keywords]

        # 4. Master Heading Structure (Aggregated from all 5)
        raw_headings = []
        for c in valid_comps:
            for h in c.get("all_headings", []):
                txt = h.get("text", "").strip()
                if len(txt) > 5 and not re.search(r'^(table of contents|comments|share|subscribe|leave a reply|related articles|cart|checkout|login|register|recent posts|categories|tags)', txt, re.I):
                    # Clean out leading numbering like "1.", "01.", "1 -", "A.", "I."
                    clean_txt = re.sub(r'^(?:(?:\d+|[A-Za-z])[\.\-\:\)]\s*|(?:Step|Part|Tip|Phase|Chapter|No\.?)\s*\d+[\.\-\:\s]*)\s*', '', txt, flags=re.IGNORECASE).strip()
                    if len(clean_txt) > 5:
                        raw_headings.append(clean_txt)

        # Deduplicate while preserving order & diversity
        seen_headings = set()
        master_outline = []
        for h in raw_headings:
            h_norm = re.sub(r'[^a-z0-9]', '', h.lower())
            if h_norm not in seen_headings and len(h_norm) > 6:
                seen_headings.add(h_norm)
                master_outline.append(h)
            if len(master_outline) >= 14:
                break

        # 5. Collective Content Gaps (Opportunities to Win #1)
        collective_gaps = []
        for c in valid_comps:
            for g in c.get("content_gaps", []):
                if g not in collective_gaps:
                    collective_gaps.append(g)

        # Standard high-intent gaps often missed by competitors
        unaddressed_angles = [
            f"Direct Head-to-Head Comparison Matrix with price-to-performance grading",
            f"Real-world Long-Term Durability & Maintenance Costs (tested by {self.brand_name})",
            f"Common Buyer Pitfalls & Counterfeit / Warranty Red Flags to Avoid in 2026",
            f"Structured FAQ addressing pricing, servicing, and official warranty support"
        ]
        for ang in unaddressed_angles:
            if ang not in collective_gaps:
                collective_gaps.append(ang)

        # 6. User URL Benchmark (if user_url was provided)
        user_benchmark = None
        if user_audit and user_audit.get("status") == "success":
            u_words = user_audit.get("word_count", 0)
            u_score = user_audit.get("seo_score", 0)
            u_headings = user_audit.get("headings_count", 0)
            word_gap = max_words - u_words
            missing_keywords = [kw for kw in core_keywords[:8] if kw.lower() not in user_audit.get("meta_description", "").lower() and kw.lower() not in " ".join([h.get('text','') for h in user_audit.get('all_headings',[])]).lower()]

            user_benchmark = {
                "url": user_audit.get("url"),
                "domain": user_audit.get("domain"),
                "word_count": u_words,
                "seo_score": u_score,
                "headings_count": u_headings,
                "word_deficit_vs_top": max(word_gap, 0),
                "is_outranked": u_words < max_words or u_score < 75,
                "missing_core_keywords": missing_keywords[:6],
                "action_items": [
                    f"Expand content by at least +{max(word_gap + 400, 800)} words to surpass Competitor #1.",
                    f"Add missing semantic entities: {', '.join(missing_keywords[:4]) if missing_keywords else 'Add more technical spec breakdowns'}.",
                    f"Introduce interactive comparison tables and FAQPage schema markup.",
                    f"Brand your testing authority using {self.brand_name}'s official editorial guidelines."
                ]
            }

        # 7. Generate Winning Meta Title & Description Options (Geo-targeted)
        meta_pack = self._generate_meta_pack(self.focus_keyword, product_name, self.brand_name, self.target_country)

        return {
            "status": "success",
            "focus_keyword": self.focus_keyword,
            "product_name": product_name,
            "brand_name": self.brand_name,
            "target_country": self.target_country,
            "stats": {
                "competitors_analyzed": len(valid_comps),
                "max_word_count": max_words,
                "avg_word_count": avg_words,
                "min_word_count": min_words,
                "target_outrank_words": target_outrank_words
            },
            "meta_pack": meta_pack,
            "core_keywords": core_keywords[:10],
            "depth_keywords": depth_keywords[:15],
            "master_outline": master_outline[:10],
            "content_gaps": collective_gaps[:8],
            "competitors": competitors,
            "user_benchmark": user_benchmark
        }

    def _generate_meta_pack(self, keyword: str, product: str, brand: str, country: str = "Bangladesh") -> dict:
        """Generate high-CTR Meta Title, Meta Description, and Slug tailored to country search intent."""
        brand_clean = brand or "Expert Lab"
        c = (country or self.target_country or "Bangladesh").lower()
        
        if "bangladesh" in c or c == "bd":
            t1 = f"{product} Price in Bangladesh (2026 Guide) | {brand_clean}"
            if len(t1) > 60:
                t1 = f"{product} Price in BD (2026 Review) | {brand_clean}"
            t2 = f"Best {product} in Bangladesh: Top Models Ranked | {brand_clean}"
            t3 = f"{product} Price in BD & Buying Guide (2026) - {brand_clean}"
            d1 = f"Check latest {product.lower()} price in Bangladesh for 2026. In-depth reviews, top brands compared, electricity bill impact, and official BD warranty from {brand_clean}."
            if len(d1) > 160:
                d1 = d1[:157] + "..."
            d2 = f"Find the best {product.lower()} in BD. Compare prices, specs, pros & cons, and authorized seller warranty from {brand_clean}. Shop smart today!"
            clean_slug = re.sub(r'[^a-z0-9]+', '-', f"{product.lower()}-price-in-bangladesh-2026").strip('-')
        elif "india" in c:
            t1 = f"{product} Price in India (2026 Guide) | {brand_clean}"
            t2 = f"Best {product} in India: Top Picks Ranked | {brand_clean}"
            t3 = f"{product} Review & Price in India (2026) - {brand_clean}"
            d1 = f"Looking for the best {product.lower()} price in India? In-depth reviews, specs comparison, and buyer advice from {brand_clean}. Find your pick!"
            d2 = f"Compare top-rated {product.lower()} models in India for 2026 with unbiased tests and verified warranty from {brand_clean}."
            clean_slug = re.sub(r'[^a-z0-9]+', '-', f"{product.lower()}-price-in-india-2026").strip('-')
        elif "global" in c or "worldwide" in c:
            t1 = f"Best {product} (2026 Guide & Review) | {brand_clean}"
            t2 = f"{product} Buying Guide: Top Picks Tested | {brand_clean}"
            t3 = f"Top {product} Compared: Which Should You Buy? - {brand_clean}"
            d1 = f"Looking for the best {product.lower()} in 2026? In-depth reviews, specs comparison, pros & cons, and honest testing results from {brand_clean}. Read now!"
            d2 = f"Compare top-rated {product.lower()} options with unbiased benchmark results, price breakdown, and buyer advice from {brand_clean}."
            clean_slug = re.sub(r'[^a-z0-9]+', '-', f"best-{product.lower()}-guide-2026").strip('-')
        else:
            t1 = f"Best {product} in {country} (2026 Guide) | {brand_clean}"
            t2 = f"{product} Buying Guide ({country}): Top Picks | {brand_clean}"
            t3 = f"{product} Review & Specs ({country}) - {brand_clean}"
            d1 = f"Looking for the best {product.lower()} in {country}? Compare top models, specs, and expert testing verdicts from {brand_clean}. Read now!"
            d2 = f"Compare top-rated {product.lower()} models in {country} with price breakdowns and buyer advice from {brand_clean}."
            clean_slug = re.sub(r'[^a-z0-9]+', '-', f"best-{product.lower()}-in-{country.lower().replace(' ', '-')}-2026").strip('-')

        return {
            "primary_title": t1,
            "title_options": [t1, t2, t3],
            "primary_description": d1,
            "description_options": [d1, d2],
            "slug": clean_slug
        }

    def generate_master_outrank_article(
        self,
        analysis_data: dict,
        content_type: str = "long_form_seo",
        tone: str = "Authoritative & Expert",
        custom_words: int = 0,
        target_country: str = ""
    ) -> dict:
        """
        Generate the final master outranking article based on the synthesized 5-competitor audit.
        """
        stats = analysis_data.get("stats", {})
        target_words = custom_words or stats.get("target_outrank_words", 2500)
        focus_kw = analysis_data.get("focus_keyword", "")
        product = analysis_data.get("product_name", focus_kw)
        brand = analysis_data.get("brand_name", self.brand_name)
        meta_pack = analysis_data.get("meta_pack", {})
        country = target_country or analysis_data.get("target_country") or self.target_country or "Bangladesh"

        # Combine keywords
        all_lsis = analysis_data.get("core_keywords", []) + analysis_data.get("depth_keywords", [])

        # Competitor summaries
        comp_summaries = []
        comp_domains = []
        for c in analysis_data.get("competitors", []):
            if c.get("status") == "success":
                d = c.get("domain", "")
                if d and d not in comp_domains:
                    comp_domains.append(d)
                comp_summaries.append({
                    "domain": d,
                    "title": c.get("title", ""),
                    "word_count": c.get("word_count", 0),
                    "headings": [h.get("text", "") for h in c.get("all_headings", []) if len(h.get("text", "").strip()) > 5][:8]
                })

        # Call ContentWritingAgent with target_country
        agent = ContentWritingAgent(gemini_api_key=self.gemini_api_key)
        
        article_result = agent.generate_content(
            topic=meta_pack.get("primary_title", f"Ultimate Guide to {product}"),
            main_keyword=focus_kw,
            lsi_keywords=all_lsis[:15],
            product_name=product,
            brand_name=brand,
            content_type=content_type,
            tone=tone,
            target_words=target_words,
            target_country=country,
            competitor_audit={
                "word_count": stats.get("max_word_count", 1500),
                "headings": analysis_data.get("master_outline", []),
                "content_gaps": analysis_data.get("content_gaps", []),
                "competitor_domains": comp_domains,
                "competitors_summary": comp_summaries,
                "core_keywords": analysis_data.get("core_keywords", []),
                "depth_keywords": analysis_data.get("depth_keywords", []),
                "target_country": country
            }
        )

        # Ensure recommended meta from meta_pack if Gemini doesn't override
        if not article_result.get("meta_title"):
            article_result["meta_title"] = meta_pack.get("primary_title")
        if not article_result.get("meta_description"):
            article_result["meta_description"] = meta_pack.get("primary_description")
        if not article_result.get("slug"):
            article_result["slug"] = meta_pack.get("slug")

        return article_result
