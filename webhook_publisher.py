import requests
import json
import logging

logger = logging.getLogger("WebhookPublisher")

class CustomWebhookPublisher:
    """
    Publisher for Custom Coded Websites (Next.js, Node.js, PHP/Laravel, Python, etc.)
    via standard JSON Webhook / REST API.
    """

    def __init__(self, webhook_url: str, api_token: str):
        self.webhook_url = (webhook_url or "").strip()
        self.api_token = (api_token or "").strip()

    def test_connection(self) -> dict:
        """
        Sends a test ping payload to the user's custom webhook endpoint.
        """
        if not self.webhook_url:
            return {"status": "error", "message": "Custom Webhook URL is required."}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
            "X-BeyondSEO-Token": self.api_token,
            "User-Agent": "BeyondSEO-Webhook-Publisher/1.0"
        }

        payload = {
            "event": "ping",
            "action": "test_connection",
            "message": "BeyondSEO Webhook Connection Test",
            "token": self.api_token,
            "timestamp": "now"
        }

        try:
            resp = requests.post(self.webhook_url, headers=headers, json=payload, timeout=12)
            if resp.status_code in [200, 201, 204]:
                return {
                    "status": "success",
                    "message": f"Webhook connection verified successfully (HTTP {resp.status_code})!",
                    "server_response": resp.text[:200]
                }
            elif resp.status_code in [401, 403]:
                return {
                    "status": "error",
                    "message": f"Authentication rejected by your custom server (HTTP {resp.status_code}). Verify that your server matches the token."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Your custom server returned HTTP {resp.status_code}: {resp.text[:200]}"
                }
        except requests.exceptions.SSLError:
            try:
                resp = requests.post(self.webhook_url, headers=headers, json=payload, timeout=12, verify=False)
                if resp.status_code in [200, 201, 204]:
                    return {
                        "status": "success",
                        "message": f"Webhook verified successfully (SSL bypass, HTTP {resp.status_code})!"
                    }
                return {"status": "error", "message": f"Server returned HTTP {resp.status_code}"}
            except Exception as e:
                return {"status": "error", "message": f"SSL connection error: {str(e)}"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": f"Could not reach '{self.webhook_url}'. Check your domain or port."}
        except requests.exceptions.Timeout:
            return {"status": "error", "message": f"Connection timed out while calling '{self.webhook_url}'."}
        except Exception as e:
            return {"status": "error", "message": f"Webhook test failed: {str(e)}"}

    def publish_article(
        self,
        title: str,
        content_html: str,
        content_markdown: str = "",
        slug: str = "",
        meta_title: str = "",
        meta_description: str = "",
        focus_keyword: str = "",
        faq_schema: dict = None,
        status: str = "draft"
    ) -> dict:
        """
        Publishes the full structured article to the user's custom webhook endpoint.
        """
        if not self.webhook_url:
            return {"status": "error", "message": "Custom Webhook URL is required."}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
            "X-BeyondSEO-Token": self.api_token,
            "User-Agent": "BeyondSEO-Webhook-Publisher/1.0"
        }

        payload = {
            "event": "article_publish",
            "token": self.api_token,
            "title": title,
            "slug": slug,
            "meta_title": meta_title or title,
            "meta_description": meta_description,
            "focus_keyword": focus_keyword,
            "content_html": content_html,
            "content_markdown": content_markdown,
            "faq_schema": faq_schema or {},
            "status": status,
            "source": "BeyondSEO-AI-Studio"
        }

        try:
            resp = requests.post(self.webhook_url, headers=headers, json=payload, timeout=25)
            if resp.status_code in [200, 201, 202]:
                resp_data = {}
                try:
                    resp_data = resp.json()
                except Exception:
                    pass
                post_url = resp_data.get("url") or resp_data.get("post_url") or ""
                post_id = resp_data.get("id") or resp_data.get("post_id") or "custom"

                return {
                    "status": "success",
                    "message": "Article successfully published to your custom website!",
                    "post_id": post_id,
                    "post_url": post_url,
                    "server_response": resp.text[:200]
                }
            elif resp.status_code in [401, 403]:
                return {
                    "status": "error",
                    "message": f"Unauthorized (HTTP {resp.status_code}). Please make sure the token on your custom site matches."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Custom server responded with HTTP {resp.status_code}: {resp.text[:200]}"
                }
        except requests.exceptions.SSLError:
            try:
                resp = requests.post(self.webhook_url, headers=headers, json=payload, timeout=25, verify=False)
                if resp.status_code in [200, 201]:
                    return {
                        "status": "success",
                        "message": "Article published to custom website (SSL bypass)!",
                        "server_response": resp.text[:200]
                    }
                return {"status": "error", "message": f"Server returned HTTP {resp.status_code}"}
            except Exception as e:
                return {"status": "error", "message": f"SSL error: {str(e)}"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "message": f"Cannot reach '{self.webhook_url}'. Check if your server is running."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to post to custom webhook: {str(e)}"}
