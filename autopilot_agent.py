import logging
from datetime import datetime, date
from typing import List, Dict, Any, Optional

from tracker import CompetitorTracker
from competitor_spy import CompetitorSpyEngine
from content_writer import ContentWritingAgent
from wordpress_publisher import WordPressPublisher
from webhook_publisher import CustomWebhookPublisher

logger = logging.getLogger("AutopilotAgent")

class AutopilotAgent:
    """
    Autonomous SEO & Content Agent that works fully on the user's behalf.
    Pipeline:
    1. Autonomous Reconnaissance: Scans competitor domain(s) for latest/top pages.
    2. Topic & Opportunity Selection: Autonomously picks the highest-value keyword opportunity.
    3. Competitor Intelligence: Reverse-engineers headings, LSI entities, and content gaps.
    4. Outranking Synthesis: Writes a comprehensive outranking article branded for the user.
    5. Autonomous Publishing: Direct 1-click dispatch to WordPress or Custom Website Webhook.
    """

    def __init__(self, gemini_api_key: Optional[str] = None):
        self.gemini_api_key = gemini_api_key

    def run_autopilot_mission(
        self,
        competitor_domains: List[str],
        brand_name: str = "MyBrand",
        target_country: str = "Bangladesh",
        content_type: str = "long_form_seo",
        tone: str = "Authoritative & Expert",
        target_words: int = 2500,
        wp_config: Optional[Dict[str, str]] = None,
        custom_webhook_config: Optional[Dict[str, str]] = None,
        specific_topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the entire autopilot workflow from discovery to publication.
        """
        logs = []
        def log(icon: str, msg: str):
            timestamp = datetime.now().strftime("%H:%M:%S")
            entry = f"[{timestamp}] {icon} {msg}"
            logs.append(entry)
            logger.info(entry)

        log("🤖", f"Autonomous Agent initialized on behalf of '{brand_name}' (Target Market: {target_country}).")

        # ----------------------------------------------------
        # Phase 1: Competitor Reconnaissance
        # ----------------------------------------------------
        cleaned_domains = [d.strip() for d in competitor_domains if d.strip()]
        if not cleaned_domains and not specific_topic:
            raise ValueError("Please provide at least 1 competitor domain or an overarching target topic.")

        discovered_articles = []
        target_article = None

        if specific_topic:
            log("🎯", f"Direct Autonomous Mission assigned: '{specific_topic}'")
            target_article = {
                "title": specific_topic,
                "url": cleaned_domains[0] if cleaned_domains else "https://competitor.com",
                "main_keyword": specific_topic,
                "product_name": brand_name,
                "lsi_keywords": [f"{specific_topic} price in {target_country}", f"best {specific_topic}", f"{specific_topic} review", "buying guide"]
            }
        else:
            primary_comp = cleaned_domains[0]
            log("🔍", f"Scanning competitor ecosystem: '{primary_comp}'...")
            try:
                tracker = CompetitorTracker(target_url=primary_comp, target_date=date.today(), gemini_api_key=self.gemini_api_key)
                discovered = tracker.run()
                if discovered:
                    discovered_articles = discovered
                    # Pick the freshest or most keyword-dense article
                    target_article = discovered[0]
                    log("💡", f"Autonomous Discovery: Found {len(discovered)} competitor pages. Selected top opportunity: '{target_article.get('title')}'")
                else:
                    log("⚠️", f"No recent sitemap articles found on {primary_comp}. Creating intelligence audit directly from domain.")
                    target_article = {
                        "title": f"Top Industry Guide for {primary_comp}",
                        "url": primary_comp,
                        "main_keyword": f"{brand_name} Solutions",
                        "product_name": brand_name,
                        "lsi_keywords": ["features", "benefits", "price", "comparison"]
                    }
            except Exception as e:
                log("⚠️", f"Recon scan warning: {str(e)}. Proceeding with heuristic fallback.")
                target_article = {
                    "title": f"Complete Market Guide ({target_country})",
                    "url": primary_comp,
                    "main_keyword": brand_name,
                    "product_name": brand_name,
                    "lsi_keywords": ["best choice", "market price", "guide", "review"]
                }

        # ----------------------------------------------------
        # Phase 2: Competitor Deep Dissection & Gap Analysis
        # ----------------------------------------------------
        comp_url = target_article.get("url", "")
        log("🕵️‍♂️", f"Reverse-engineering competitor page: {comp_url}")
        
        audit_data = {}
        try:
            spy_engine = CompetitorSpyEngine(comp_url)
            spy_res = spy_engine.run_full_spy()
            audit_data = spy_res.get("audit", {})
            gaps = audit_data.get("content_gaps", [])
            log("📊", f"Competitor Audit Completed: {audit_data.get('word_count', 0)} words, {len(audit_data.get('all_headings', []))} headings.")
            if gaps:
                log("⚠️", f"Extracted {len(gaps)} collective content gaps & vulnerabilities to exploit.")
        except Exception as e:
            log("⚠️", f"Could not scrape deep DOM from {comp_url}: {str(e)}. Generating competitive blueprint from semantic patterns.")

        # ----------------------------------------------------
        # Phase 3: Autonomous Content Writing & Outranking
        # ----------------------------------------------------
        main_kw = target_article.get("main_keyword") or target_article.get("title", "")
        lsi_list = target_article.get("lsi_keywords", [])
        lsi_str = ", ".join(lsi_list) if isinstance(lsi_list, list) else str(lsi_list)

        log("✍️", f"Autonomous Agent writing Google-outranking master article for keyword: '{main_kw}'...")
        writer = ContentWritingAgent(gemini_api_key=self.gemini_api_key)
        
        article_result = writer.generate_content(
            topic=target_article.get("title", main_kw),
            main_keyword=main_kw,
            lsi_keywords=lsi_str,
            product_name=target_article.get("product_name", brand_name),
            brand_name=brand_name,
            competitor_url=comp_url,
            content_type=content_type,
            tone=tone,
            target_words=target_words,
            target_country=target_country
        )

        log("🏆", f"Master article generated! Word count: {article_result.get('actual_word_count', 0)} words (Estimated read: {article_result.get('estimated_reading_time')}).")
        log("🏷️", f"Embedded Featured Snippet Comparison Table + JSON-LD FAQPage Schema.")

        # ----------------------------------------------------
        # Phase 4: Autonomous Dispatch & Publishing
        # ----------------------------------------------------
        publish_results = []
        
        # 1. WordPress Publishing if configured
        if wp_config and wp_config.get("site_url") and wp_config.get("username") and wp_config.get("app_password"):
            log("🚀", f"Autonomously dispatching article to WordPress site: {wp_config.get('site_url')}...")
            wp_pub = WordPressPublisher(
                site_url=wp_config.get("site_url"),
                username=wp_config.get("username"),
                app_password=wp_config.get("app_password")
            )
            # Use marked visual HTML or convert basic markdown
            wp_res = wp_pub.publish_post(
                title=article_result.get("meta_title") or article_result.get("title"),
                content_html=article_result.get("article_markdown"), # fallback, markdown will be rendered
                slug=article_result.get("slug", ""),
                excerpt=article_result.get("meta_description", ""),
                status=wp_config.get("status", "draft"),
                focus_keyword=main_kw,
                faq_schema=article_result.get("faq_schema")
            )
            publish_results.append({"destination": "wordpress", "result": wp_res})
            if wp_res.get("status") == "success":
                log("✅", f"WordPress Post created successfully (Post ID: #{wp_res.get('post_id')}, Status: {wp_res.get('post_status', 'draft').upper()})!")
                if wp_res.get("post_url"):
                    log("🔗", f"Post URL: {wp_res.get('post_url')}")
            else:
                log("❌", f"WordPress publishing issue: {wp_res.get('message')}")

        # 2. Custom Webhook Publishing if configured
        if custom_webhook_config and custom_webhook_config.get("webhook_url"):
            wh_url = custom_webhook_config.get("webhook_url")
            wh_token = custom_webhook_config.get("api_token", "")
            wh_status = custom_webhook_config.get("status", "draft")
            log("🌐", f"Autonomously streaming payload to Custom Website Webhook: {wh_url}...")
            
            wh_pub = CustomWebhookPublisher(webhook_url=wh_url, api_token=wh_token)
            wh_res = wh_pub.publish_article(
                title=article_result.get("meta_title") or article_result.get("title"),
                content_html=article_result.get("article_markdown"),
                content_markdown=article_result.get("article_markdown", ""),
                slug=article_result.get("slug", ""),
                meta_title=article_result.get("meta_title", ""),
                meta_description=article_result.get("meta_description", ""),
                focus_keyword=main_kw,
                faq_schema=article_result.get("faq_schema"),
                status=wh_status
            )
            publish_results.append({"destination": "custom_webhook", "result": wh_res})
            if wh_res.get("status") == "success":
                log("✅", f"Delivered to Custom Website Webhook successfully! ({wh_res.get('message')})")
            else:
                log("❌", f"Custom Webhook delivery issue: {wh_res.get('message')}")

        log("🎉", "Autonomous Agent Mission successfully completed! All tasks performed on your behalf.")

        return {
            "status": "success",
            "agent_logs": logs,
            "target_article": target_article,
            "audit_data": audit_data,
            "article": article_result,
            "publish_results": publish_results,
            "timestamp": datetime.now().isoformat()
        }
