import requests
import json
import logging
import re
from urllib.parse import urlparse

logger = logging.getLogger("WordPressPublisher")

class WordPressPublisher:
    """
    Automated Publisher for WordPress via the official native WordPress REST API.
    Uses Application Passwords (built into WordPress core, no plugin needed).
    """

    def __init__(self, site_url: str, username: str, app_password: str):
        self.site_url = self._normalize_site_url(site_url)
        self.username = (username or "").strip()
        self.app_password = (app_password or "").strip()
        self.auth = (self.username, self.app_password) if self.username and self.app_password else None

    def _normalize_site_url(self, url: str) -> str:
        if not url:
            return ""
        url = url.strip().rstrip('/')
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
        return url

    def test_connection(self) -> dict:
        """
        Tests credentials by calling /wp-json/wp/v2/users/me.
        """
        if not self.site_url:
            return {"status": "error", "message": "WordPress site URL is required."}
        if not self.username or not self.app_password:
            return {"status": "error", "message": "Username and Application Password are required."}

        endpoint = f"{self.site_url}/wp-json/wp/v2/users/me"
        try:
            headers = {"User-Agent": "BeyondSEO-AutoPublisher/1.0"}
            resp = requests.get(endpoint, auth=self.auth, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "status": "success",
                    "message": f"Connected successfully as '{data.get('name', self.username)}'!",
                    "user_id": data.get("id"),
                    "name": data.get("name", self.username),
                    "roles": data.get("roles", [])
                }
            elif resp.status_code in [401, 403]:
                return {
                    "status": "error",
                    "message": "Authentication failed (401/403). Please verify your WordPress username and Application Password."
                }
            elif resp.status_code == 404:
                return {
                    "status": "error",
                    "message": f"WordPress REST API not found (404) at {endpoint}. Ensure permalinks are enabled (not Plain) and REST API is accessible."
                }
            else:
                return {
                    "status": "error",
                    "message": f"WordPress server returned status {resp.status_code}: {resp.text[:200]}"
                }
        except requests.exceptions.SSLError:
            # Retry with verify=False if self-signed SSL certificate
            try:
                resp = requests.get(endpoint, auth=self.auth, timeout=15, verify=False)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "status": "success",
                        "message": f"Connected successfully as '{data.get('name', self.username)}' (SSL bypass)!",
                        "user_id": data.get("id"),
                        "name": data.get("name", self.username)
                    }
                else:
                    return {"status": "error", "message": f"SSL Connection error: Status {resp.status_code}"}
            except Exception as e:
                return {"status": "error", "message": f"SSL connection error: {str(e)}"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": f"Cannot reach '{self.site_url}'. Check your domain and internet connection."}
        except requests.exceptions.Timeout:
            return {"status": "error", "message": f"Connection timed out while reaching '{self.site_url}'."}
        except Exception as e:
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

    def publish_post(
        self,
        title: str,
        content_html: str,
        slug: str = "",
        excerpt: str = "",
        status: str = "draft",
        focus_keyword: str = "",
        faq_schema: dict = None
    ) -> dict:
        """
        Publishes or saves an article as a Draft in WordPress via REST API.
        """
        if not self.site_url or not self.auth:
            return {"status": "error", "message": "WordPress site URL, username, and password are required."}

        title = (title or "").strip()
        if not title:
            return {"status": "error", "message": "Post title is required."}

        # If schema is provided, append JSON-LD script at bottom of content
        full_html = content_html or ""
        if faq_schema and isinstance(faq_schema, dict):
            schema_json = json.dumps(faq_schema, ensure_ascii=False)
            full_html += f'\n\n<script type="application/ld+json">\n{schema_json}\n</script>'

        endpoint = f"{self.site_url}/wp-json/wp/v2/posts"
        
        # Build payload
        payload = {
            "title": title,
            "content": full_html,
            "status": status if status in ["draft", "publish", "pending"] else "draft",
        }
        if slug:
            payload["slug"] = slug.strip()
        if excerpt:
            payload["excerpt"] = excerpt.strip()

        # Inject popular SEO plugin fields (Yoast SEO, Rank Math) if available in WP
        meta_fields = {}
        if focus_keyword:
            meta_fields["_yoast_wpseo_focuskw"] = focus_keyword
            meta_fields["rank_math_focus_keyword"] = focus_keyword
        if title:
            meta_fields["_yoast_wpseo_title"] = title
            meta_fields["rank_math_title"] = title
        if excerpt:
            meta_fields["_yoast_wpseo_metadesc"] = excerpt
            meta_fields["rank_math_description"] = excerpt

        if meta_fields:
            payload["meta"] = meta_fields

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BeyondSEO-AutoPublisher/1.0"
        }

        try:
            resp = requests.post(
                endpoint,
                auth=self.auth,
                headers=headers,
                data=json.dumps(payload),
                timeout=25
            )

            # If meta fields fail due to REST API schema restrictions, retry without meta
            if resp.status_code == 400 and "meta" in payload:
                logger.info("Retrying post creation without custom meta fields...")
                payload.pop("meta", None)
                resp = requests.post(
                    endpoint,
                    auth=self.auth,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=25
                )

            if resp.status_code in [200, 201]:
                data = resp.json()
                post_id = data.get("id")
                post_link = data.get("link", "")
                edit_link = f"{self.site_url}/wp-admin/post.php?post={post_id}&action=edit"
                
                return {
                    "status": "success",
                    "message": f"Post successfully created as {status.upper()}!",
                    "post_id": post_id,
                    "post_url": post_link,
                    "edit_url": edit_link,
                    "post_status": data.get("status", status),
                    "title": data.get("title", {}).get("rendered", title)
                }
            elif resp.status_code in [401, 403]:
                return {
                    "status": "error",
                    "message": f"Permission denied ({resp.status_code}). User does not have rights to publish posts."
                }
            else:
                err_detail = ""
                try:
                    err_json = resp.json()
                    err_detail = err_json.get("message", resp.text[:200])
                except Exception:
                    err_detail = resp.text[:200]
                return {
                    "status": "error",
                    "message": f"WordPress API error ({resp.status_code}): {err_detail}"
                }
        except requests.exceptions.SSLError:
            try:
                resp = requests.post(
                    endpoint,
                    auth=self.auth,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=25,
                    verify=False
                )
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    post_id = data.get("id")
                    return {
                        "status": "success",
                        "message": f"Post successfully created as {status.upper()} (SSL bypass)!",
                        "post_id": post_id,
                        "post_url": data.get("link", ""),
                        "edit_url": f"{self.site_url}/wp-admin/post.php?post={post_id}&action=edit",
                        "post_status": data.get("status", status)
                    }
                else:
                    return {"status": "error", "message": f"Server error: {resp.status_code}"}
            except Exception as e:
                return {"status": "error", "message": f"SSL Error: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to publish to WordPress: {str(e)}"}
