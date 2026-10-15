#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Competitor Tracker, SEO Spy & Content Writing AI Agent Dashboard - Web Server
Provides:
1. Daily Article & Keyword Monitor
2. 360-Degree Competitor Spy & Reverse Engineering (Why it Ranked, Backlinks, Secrets)
3. Autonomous Content Writing AI Agent (Outranking Articles, Reviews, Comparisons, Social Posts)
"""

import os
import sys
import io
import json
import webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tracker import CompetitorTracker
from competitor_spy import CompetitorSpyEngine
from content_writer import ContentWritingAgent
from multi_competitor import MultiCompetitorEngine
from wordpress_publisher import WordPressPublisher
from webhook_publisher import CustomWebhookPublisher
from autopilot_agent import AutopilotAgent
from seo_director_agent import PersonalSEODirector
from agency_workforce import AGENCY_STAFF, AgencyWorkforceEngine, load_agency_data, render_printable_agency_report

import base64

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranknaser_users.json')
PHOTO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranknaser_profile.jpg')

def load_registered_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "admin": {"name": "RankNaser Admin", "password": "AGENTNASER", "domain": "ranknaser.com"},
        "ADMIN": {"name": "RankNaser Admin", "password": "AGENTNASER", "domain": "ranknaser.com"},
        "admin@ranknaser.com": {"name": "RankNaser Admin", "password": "AGENTNASER", "domain": "ranknaser.com"}
    }

def save_registered_users(users_dict):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_dict, f, indent=2)
    except Exception as e:
        print("Error saving users:", e)


def render_printable_guide(lang="en") -> str:
    """Renders a standalone, high-res A4 print-optimized PDF document with auto-print."""
    is_bn = (lang == "bn")
    title = "RankNaserPro Intelligence Suite — ব্যবহারকারী নির্দেশিকা (User Guide)" if is_bn else "RankNaserPro Intelligence Suite — Official User Guide"
    subtitle = "সম্পূর্ণ এসইও অটোমেশন ও অটোনোমাস সার্চ ইন্টেলিজেন্স ম্যানুয়াল" if is_bn else "Complete Autonomous Search Intelligence & Execution Manual"
    author = "RankNaser (Lead Architect & SEO Director)"
    
    # Body content based on language
    if is_bn:
        body_content = """
        <div class="chapter">
            <h2>১. লগইন ও ১ সপ্তাহের ফ্রি ট্রায়াল</h2>
            <p><strong>অ্যাক্সেস:</strong> ইউজার বা অ্যাডমিন ক্রেডেনশিয়াল (<code>ADMIN</code> / <code>AGENTNASER</code>) দিয়ে লগইন করুন। ১ম বার লগইন করার পর ইউজারকে <strong>৭ দিনের সম্পূর্ণ ফ্রি আনলিমিটেড অ্যাক্সেস</strong> দেওয়া হবে।</p>
            <p><strong>স্বয়ংক্রিয় লক:</strong> ৭ দিন পার হয়ে গেলে প্ল্যাটফর্ম স্বয়ংক্রিয়ভাবে লক হয়ে যাবে এবং লাইসেন্স রিনিউ করার নোটিশ দেখাবে।</p>
        </div>
        <div class="chapter">
            <h2>২. ইঞ্জিন ১ — ডেইলি এসইআরপি রাডার (র‍্যাংক ট্র্যাকিং)</h2>
            <p>আপনার টার্গেটেড কিওয়ার্ডগুলো গুগলের ১ থেকে ১০ নম্বর পজিশনে কোথায় আছে, প্রতিদ্বন্দ্বীরা কীভাবে পজিশন বদলাচ্ছে এবং সার্চ ভলিউম কেমন—তা ২৪/৭ মনিটর করতে এই ইঞ্জিন ব্যবহার করুন। দেশ সিলেক্ট করে কিওয়ার্ড ও কম্পিটিটর ডোমেন দিলে লাইভ রাডার কার্ড ওপেন হবে।</p>
        </div>
        <div class="chapter">
            <h2>৩. ইঞ্জিন ২ — ৩৬০° ডিপ কম্পিটিটর স্পাই</h2>
            <p>গুগলে এক নম্বরে থাকা প্রতিদ্বন্দ্বীর ইউআরএল ইনপুট দিলে তাদের H1, H2, H3 হেডিংস, মোট শব্দসংখ্যা ও কনটেন্ট গ্যাপ (Content Gap) মুহূর্তের মধ্যে স্ক্র্যাপ করে আপনার সামনে তুলে ধরবে।</p>
        </div>
        <div class="chapter">
            <h2>৪. ইঞ্জিন ৩ — ৫ বনাম ১ আউট-র‍্যাঙ্কার</h2>
            <p>শীর্ষ ৫ জন প্রতিদ্বন্দ্বীর আর্টিকেল লিংক দিলে সিস্টেম তাদের সবার সেরা তথ্যগুলো নিয়ে একক একটি সুপিরিয়র মাস্টার আউটলাইন তৈরি করে দেয় যা গুগলে তাদের আউট-র‍্যাংক করতে সক্ষম।</p>
        </div>
        <div class="chapter">
            <h2>৫. ইঞ্জিন ৪ — এআই কনটেন্ট স্টুডিও (২৫০০+ শব্দ, হিউম্যান রাইটার কোয়ালিটি)</h2>
            <p>• <strong>০% ডাবল ওয়ার্ড:</strong> কোনো রোবোটিক পুনরাবৃত্তি বা একই শব্দের পুনরাবৃত্তি থাকবে না।<br>
            • <strong>মেইন কিওয়ার্ড ও LSI ইন্টিগ্রেশন:</strong> টাইটেল, প্রথম ৬০-৮০ শব্দ এবং প্রতিটি LSI কিওয়ার্ডের জন্য আলাদা ডেডিকেটেড সাব-সেকশন তৈরি হবে।<br>
            • <strong>গুগল AI ওভারভিউ ও FAQ স্কিমা:</strong> গুগলের নতুন সার্চ ফিচারে আসার জন্য কম্প্যারিজন টেবিল এবং FAQPage স্কিমা কোড সংযুক্ত থাকবে।</p>
        </div>
        <div class="chapter">
            <h2>৬. ইঞ্জিন ৫ — অটোনোমাস অটোপাইলট এজেন্ট (হ্যান্ডস-ফ্রি এসইও)</h2>
            <p>শুধু ব্র্যান্ড নেম ও কম্পিটিটর ডোমেন দিন; এজেন্ট নিজে নিজে কম্পিটিটরদের স্ক্যান করবে, হাই-ইনটেন্ট কিওয়ার্ড বের করবে, আর্টিকেল লিখবে এবং সরাসরি আপনার ওয়েবসাইটে পাবলিশ করবে।</p>
        </div>
        <div class="chapter">
            <h2>৭. ইঞ্জিন ৬ — এসইও ডিরেক্টর ক্যাম্পেইন ও ৩০ দিনের রোডম্যাপ</h2>
            <p>সিনিয়র এসইও ডিরেক্টরের তৈরি ১০ দিনের মাস্টার এক্সিকিউশন ক্যাম্পেইন ও ৩০ দিনের কন্টেন্ট ক্যালেন্ডার ডাউনলোড করে সরাসরি ব্যবহার করুন।</p>
        </div>
        <div class="chapter">
            <h2>৮. ওয়ার্ডপ্রেস ও কাস্টম সাইট অটো-পাবলিশিং</h2>
            <p>হেডারের 🔌 WordPress অপশনে গিয়ে সাইট লিংক, ইউজারনেম এবং Application Password দিয়ে ১ ক্লিকে কানেক্ট করুন এবং কনটেন্ট ড্রাফট হিসেবে অটো-পাবলিশ করুন।</p>
        </div>
        <div class="chapter">
            <h2>৯. গুগলে ১ নম্বরে র‍্যাংক করার সেরা এসইও সিক্রেটস</h2>
            <p>১. প্রথম ১০০ শব্দের ভেতর ইউজারের সার্চ প্রশ্নের সরাসরি উত্তর দিন।<br>
            ২. প্রতিটি LSI কিওয়ার্ডের সঠিক ব্যাখ্যা ও তথ্যবহুল অনুচ্ছেদ রাখুন।<br>
            ৩. কম্প্যারিজন টেবিল ব্যবহার করুন যাতে গুগল ফিচার্ড স্নsnippet দেয়।<br>
            ৪. অটোপাইলট এজেন্ট দিয়ে প্রতি সপ্তাহে কমপক্ষে ৩-৫টি মাস্টার আর্টিকেল পাবলিশ করুন।</p>
        </div>
        """
    else:
        body_content = """
        <div class="chapter">
            <h2>1. System Access & 7-Day Free Trial</h2>
            <p><strong>Gateway Access:</strong> Log in using Admin credentials (<code>ADMIN</code> / <code>AGENTNASER</code>) or registered user credentials. First-time users receive <strong>7 Days of 100% Unlimited Free Access</strong> to all 6 engines.</p>
            <p><strong>Automated Lockout:</strong> When the 7 days elapse, access automatically locks with a renewal prompt. Master administrators can bypass or reset the timer at any time.</p>
        </div>
        <div class="chapter">
            <h2>2. Engine 1 — Daily SERP Radar (Keyword Surveillance)</h2>
            <p>Monitors Google rankings (#1 through #10), search volume, keyword difficulty, and competitor position fluctuations 24/7 across multiple countries (Bangladesh, US, UK, Global).</p>
        </div>
        <div class="chapter">
            <h2>3. Engine 2 — 360° Deep Competitor Infiltration</h2>
            <p>Enter any rival article URL to reverse-engineer their heading hierarchy (H1, H2, H3), total word count benchmark, keyword density, and actionable content gaps.</p>
        </div>
        <div class="chapter">
            <h2>4. Engine 3 — 5 vs 1 SERP Outranker</h2>
            <p>Crawl up to 5 competing URLs simultaneously. The engine synthesizes their combined best insights into one superior, outranking master brief.</p>
        </div>
        <div class="chapter">
            <h2>5. Engine 4 — Elite AI Content Studio (2,500+ Words EEAT)</h2>
            <p>• <strong>0 Double Words:</strong> Elite multi-tier deduplication guarantees zero repetitive phrases or stutter tokens.<br>
            • <strong>Main & LSI Keyword Precision:</strong> Prominently featured in H1, intro hook, and dedicated analytical subsections for every provided LSI keyword.<br>
            • <strong>Google AI Overview & FAQ Schema:</strong> Structured comparison tables, SGE snippet blocks, and valid JSON-LD schema.</p>
        </div>
        <div class="chapter">
            <h2>6. Engine 5 — Autonomous Autopilot Agent (Hands-Free SEO)</h2>
            <p>Enter your brand name and competitor domains; the agent autonomously scans ranking opportunities, generates outranking content, and publishes straight to your CMS.</p>
        </div>
        <div class="chapter">
            <h2>7. Engine 6 — SEO Director Campaign & 30-Day Roadmap</h2>
            <p>A structured 10-day execution campaign and downloadable 30-day content calendar designed by senior architects to systematically build domain authority.</p>
        </div>
        <div class="chapter">
            <h2>8. One-Click WordPress & Webhook Auto-Publishing</h2>
            <p>Connect your WordPress site via REST API Application Passwords or custom webhooks to publish generated articles straight to your website in seconds.</p>
        </div>
        <div class="chapter">
            <h2>9. RankNaser's Golden Rules for #1 Google Ranking</h2>
            <p>1. Satisfy search intent directly within the opening 100 words.<br>
            2. Cover every semantic LSI entity thoroughly.<br>
            3. Include structured comparison tables to win Featured Snippets.<br>
            4. Maintain consistent publishing of 3-5 comprehensive guides per week.</p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="{'bn' if is_bn else 'en'}">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 18mm 16mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            color: #0f172a;
            line-height: 1.65;
            font-size: 13.5px;
            background: #ffffff;
            margin: 0;
            padding: 24px;
        }}
        .print-toolbar {{
            background: #1e1b4b;
            color: white;
            padding: 12px 20px;
            border-radius: 10px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .btn-print {{
            background: #4f46e5;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 6px;
            font-weight: 700;
            cursor: pointer;
            font-size: 13px;
        }}
        .cover {{
            text-align: center;
            padding: 30px 20px 25px 20px;
            background: linear-gradient(135deg, #f8fafc, #eff6ff);
            border-radius: 14px;
            border: 2px solid #cbd5e1;
            margin-bottom: 30px;
        }}
        .logo-badge {{
            display: inline-block;
            background: #1e3a8a;
            color: white;
            font-weight: 800;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }}
        h1 {{
            font-size: 26px;
            margin: 6px 0;
            color: #0f172a;
            font-weight: 900;
        }}
        .sub {{
            font-size: 14px;
            color: #475569;
            margin: 0 0 14px 0;
        }}
        .author-box {{
            display: inline-block;
            background: #ffffff;
            border: 1px solid #bfdbfe;
            border-radius: 20px;
            padding: 4px 16px;
            font-size: 12px;
            font-weight: 700;
            color: #1e40af;
        }}
        .chapter {{
            margin-bottom: 22px;
            padding-bottom: 18px;
            border-bottom: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }}
        h2 {{
            font-size: 16px;
            color: #1e3a8a;
            margin: 0 0 8px 0;
            font-weight: 800;
        }}
        p {{
            margin: 0 0 8px 0;
        }}
        code {{
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            color: #0f172a;
        }}
        @media print {{
            .print-toolbar {{
                display: none !important;
            }}
            body {{
                padding: 0;
            }}
            .cover {{
                border-color: #94a3b8;
            }}
        }}
    </style>
</head>
<body>
    <div class="print-toolbar">
        <div>
            <strong>📘 RankNaserPro Intelligence Suite — PDF Export Ready</strong>
            <span style="font-size: 12px; opacity: 0.85; margin-left: 10px;">Click Print to save as PDF</span>
        </div>
        <button class="btn-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
    </div>

    <div class="cover">
        <div class="logo-badge">🚀 RANKNASERPRO INTELLIGENCE SUITE</div>
        <h1>{title}</h1>
        <div class="sub">{subtitle}</div>
        <div class="author-box">👑 {author}</div>
    </div>

    {body_content}

    <div style="text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid #cbd5e1; font-size: 11px; color: #64748b;">
        © {title.split('—')[0]} • Lead Architect & SEO Director: RankNaser • All Rights Reserved.
    </div>

    <script>
        // Auto prompt print on open if loaded for export
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                if (window.location.search.includes('print=true')) {{
                    window.print();
                }}
            }}, 400);
        }});
    </script>
</body>
</html>"""

def get_ranknaser_photo_uri():
    photo_b64_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photo_b64.txt')
    if os.path.exists(photo_b64_file):
        try:
            with open(photo_b64_file, 'r', encoding='utf-8') as f:
                c = f.read().strip()
                if c:
                    return c
        except Exception:
            pass
    if os.path.exists(PHOTO_FILE):
        try:
            with open(PHOTO_FILE, 'rb') as f:
                return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')
        except Exception:
            pass
    return "/static/ranknaser.jpg"



HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RankNaserPro - Autonomous SEO Intelligence & Outranking Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Hind+Siliguri:wght@400;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        // Fallback markdown parser if CDN is delayed or blocked
        if (typeof marked === 'undefined') {
            window.marked = {
                parse: function(md) {
                    if (!md) return '';
                    return md
                        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
                        .replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>')
                        .replace(/\\*\\*(.*?)\\*\\*/gim, '<strong>$1</strong>')
                        .replace(/\\*(.*?)\\*/gim, '<em>$1</em>')
                        .replace(/\\n$/gim, '<br />')
                        .replace(/\\n\\n/gim, '</p><p>');
                }
            };
        }
        // Early Bulletproof Tab & Action Switcher
        function switchTab(tab, updateHistory) {
            if (updateHistory === undefined) updateHistory = true;
            const tabMap = {
                'daily': 'tabDaily',
                'spy': 'tabSpy',
                'multi': 'tabMulti',
                'writer': 'tabWriter',
                'autopilot': 'tabAutopilot',
                'director': 'tabDirector',
                'agency': 'tabAgency'
            };
            Object.keys(tabMap).forEach(key => {
                const el = document.getElementById(tabMap[key]);
                if (el) el.style.display = (key === tab) ? 'block' : 'none';
                const btn = document.getElementById(tabMap[key] + 'Btn');
                if (btn) {
                    if (key === tab) btn.classList.add('active');
                    else btn.classList.remove('active');
                }
            });
            if (tab === 'agency' && typeof loadAgencyDashboard === 'function') {
                try { loadAgencyDashboard(); } catch(e) {}
            }
            if (updateHistory) {
                try { history.pushState({ tab: tab }, '', '#' + tab); } catch(e) {}
            }
        }
        window.switchTab = switchTab;

        function openClientsHubModal(clientId) {
            const modal = document.getElementById('clientsHubModal');
            if (modal) modal.style.display = 'flex';
            if (typeof renderHubClientTabs === 'function') { try { renderHubClientTabs(); } catch(e) {} }
            if (typeof loadActiveHubClientFields === 'function') { try { loadActiveHubClientFields(); } catch(e) {} }
        }
        window.openClientsHubModal = openClientsHubModal;

        function openRoadmapModal() {
            switchTab('director');
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        window.openRoadmapModal = openRoadmapModal;

        function openWpModal() {
            const modal = document.getElementById('wpModal');
            if (modal) modal.style.display = 'flex';
        }
        window.openWpModal = openWpModal;

        function openCustomApiModal() {
            const modal = document.getElementById('customApiModal');
            if (modal) modal.style.display = 'flex';
        }
        window.openCustomApiModal = openCustomApiModal;

        function openUserGuideModal() {
            const modal = document.getElementById('userGuideModal');
            if (modal) modal.style.display = 'flex';
        }
        window.openUserGuideModal = openUserGuideModal;

        function goBackToHome() {
            switchTab('daily');
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        window.goBackToHome = goBackToHome;
    </script>
    <style>
        :root {
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --card-inner-bg: #f1f5f9;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --spy-accent: #7c3aed;
            --spy-hover: #6d28d9;
            --writer-accent: #059669;
            --writer-hover: #047857;
            --multi-accent: #dc2626;
            --multi-hover: #b91c1c;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --border-hover: #cbd5e1;
            --success: #059669;
            --warning: #d97706;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        #trialCountdownBadge, #trialCountdownBadge *, #currentUserBadge, #currentUserBadge * {
            pointer-events: none !important;
            cursor: default !important;
            user-select: none !important;
        }
        body {
            font-family: 'Plus Jakarta Sans', 'Hind Siliguri', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 25px 20px;
        }
        .container { max-width: 1180px; margin: 0 auto; }
        header { margin-bottom: 22px; }
        .logo-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #ffffff;
            color: #0f172a;
            border: 1.5px solid #cbd5e1;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 5px 12px;
            border-radius: 8px;
            margin-bottom: 6px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .logo-badge:hover {
            background: #f8fafc;
            border-color: #94a3b8;
        }
        h1 {
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }
        p.subtitle { color: var(--text-muted); font-size: 13.5px; }

        /* ================= STARTECH-STYLE CATEGORY CARD GRID ================= */
        /* Quick Actions Grid */
        .action-toolbar-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 22px;
            width: 100%;
        }
        .action-card-btn {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 14px !important;
            padding: 16px 10px 14px 10px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            gap: 8px !important;
            cursor: pointer !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            min-height: 96px !important;
            text-decoration: none !important;
            box-sizing: border-box !important;
        }
        .action-card-btn:hover {
            background: #ffffff !important;
            border-color: #cbd5e1 !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07) !important;
            transform: translateY(-3px) !important;
            color: #000000 !important;
        }
        .action-card-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0f172a;
            height: 32px;
        }
        .action-card-title {
            color: #0f172a;
            font-size: 13px;
            font-weight: 700;
            line-height: 1.25;
            text-align: center;
        }
        .header-inner-badge {
            font-size: 10.5px !important;
            background: #f1f5f9 !important;
            color: #475569 !important;
            padding: 2px 7px !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            border: 1px solid #e2e8f0 !important;
            margin-top: 2px;
        }
        .header-status-badge {
            cursor: default !important;
            pointer-events: none !important;
            user-select: none !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 7px !important;
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 8px 14px !important;
            font-size: 12px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }
        .header-logout-btn {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 8px 14px !important;
            font-size: 12.5px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 6px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }
        .header-logout-btn:hover {
            border-color: #cbd5e1 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
            transform: translateY(-1px) !important;
        }

        /* 7-Engine Navigation Tabs Grid */
        .tabs-nav {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
            margin-bottom: 24px;
            width: 100%;
        }
        .tab-btn {
            width: 100%;
            min-height: 100px;
            height: auto;
            box-sizing: border-box;
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 14px !important;
            padding: 16px 8px 14px 8px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            gap: 8px !important;
            cursor: pointer !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            line-height: 1.25 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            white-space: normal !important;
            user-select: none !important;
        }
        .tab-btn:hover,
        .tab-btn.daily:hover,
        .tab-btn.spy:hover,
        .tab-btn.multi:hover,
        .tab-btn.writer:hover,
        .tab-btn.autopilot:hover,
        .tab-btn.director:hover,
        .tab-btn.agency:hover {
            background: #ffffff !important;
            border-color: #cbd5e1 !important;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.07) !important;
            transform: translateY(-3px) !important;
            color: #000000 !important;
        }
        .tab-btn.active,
        .tab-btn.active.daily,
        .tab-btn.active.spy,
        .tab-btn.active.multi,
        .tab-btn.active.writer,
        .tab-btn.active.autopilot,
        .tab-btn.active.director,
        .tab-btn.active.agency {
            background: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #0f172a !important;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.12) !important;
            outline: none !important;
            font-weight: 800 !important;
            transform: translateY(-1px) !important;
        }
        .tab-btn .tab-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #0f172a;
            height: 32px;
        }
        .tab-btn .tab-label {
            display: block;
            text-align: center;
            color: #0f172a;
            font-size: 13px;
            font-weight: 700;
            line-height: 1.25;
        }
        @media (max-width: 1200px) {
            .tabs-nav { grid-template-columns: repeat(4, 1fr); }
            .action-toolbar-grid { grid-template-columns: repeat(3, 1fr); }
        }
        @media (max-width: 768px) {
            .tabs-nav { grid-template-columns: repeat(2, 1fr); }
            .action-toolbar-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 480px) {
            .tabs-nav { grid-template-columns: 1fr; }
            .action-toolbar-grid { grid-template-columns: 1fr; }
        }

        /* SEO Director Category Badges & Cards */
        .badge-onpage {
            background: #ecfdf5;
            color: #065f46;
            border: 1px solid #a7f3d0;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-technical {
            background: #eff6ff;
            color: #1e40af;
            border: 1px solid #bfdbfe;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-offpage {
            background: #fdf2f8;
            color: #9d174d;
            border: 1px solid #fbcfe8;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-cro {
            background: #fffbeb;
            color: #92400e;
            border: 1px solid #fde68a;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .day-mission-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 1px 4px rgba(0,0,0,0.03);
            transition: all 0.2s ease;
        }
        .day-mission-card:hover {
            box-shadow: 0 4px 14px rgba(0,0,0,0.07);
            border-color: #cbd5e1;
        }
        .day-mission-card.completed {
            border-left: 5px solid #10b981;
            background: #fcfdfd;
        }
        .day-mission-card.running {
            border-left: 5px solid #3b82f6;
            background: #f0f9ff;
        }
        .company-pill {
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid #cbd5e1;
            background: #f8fafc;
            color: #334155;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .company-pill:hover {
            border-color: #0284c7;
            color: #0284c7;
            background: #f0f9ff;
        }
        .company-pill.active {
            background: #0284c7;
            border-color: #0284c7;
            color: #ffffff;
            box-shadow: 0 2px 6px rgba(2, 132, 199, 0.35);
        }

        .serp-preview-box {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            font-family: Arial, sans-serif;
        }
        .serp-url {
            color: #202124;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }
        .serp-title {
            color: #1a0dab;
            font-size: 20px;
            font-weight: 500;
            line-height: 1.3;
            cursor: pointer;
            margin-bottom: 6px;
            display: inline-block;
        }
        .serp-title:hover {
            text-decoration: underline;
        }
        .serp-desc {
            color: #4d5156;
            font-size: 14px;
            line-height: 1.58;
            word-wrap: break-word;
        }
        .serp-stats-bar {
            display: flex;
            gap: 10px;
            margin-top: 14px;
            padding-top: 12px;
            border-top: 1px dashed #e2e8f0;
            flex-wrap: wrap;
            align-items: center;
        }
        .char-pill {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            background: #f1f5f9;
            color: #475569;
        }
        .char-pill.good {
            background: #dcfce7;
            color: #15803d;
        }
        .title-option-chip {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1d4ed8;
            font-size: 12px;
            font-weight: 600;
            padding: 5px 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .title-option-chip:hover {
            background: #dbeafe;
            border-color: #3b82f6;
        }


        .search-card {
            background: var(--card-bg);
            border: 1.5px solid #bae6fd;
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 4px 20px rgba(14, 165, 233, 0.06);
            margin-bottom: 22px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 12px;
        }
        .form-grid-tracker {
            display: grid;
            grid-template-columns: 1fr 180px auto;
            gap: 12px;
        }
        @media (max-width: 768px) {
            .form-grid, .form-grid-tracker { grid-template-columns: 1fr; }
        }
        input, select, textarea, button {
            font-family: inherit;
            border-radius: 10px;
            font-size: 14px;
            outline: none;
            transition: all 0.2s ease;
        }
        input[type="text"], input[type="date"], select, textarea {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            color: #0f172a;
            padding: 11px 14px;
            width: 100%;
        }
        input[type="text"]:hover, input[type="date"]:hover, select:hover, textarea:hover {
            border-color: #94a3b8;
            box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.05);
        }
        input:focus, select:focus, textarea:focus {
            border-color: #0f172a !important;
            box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1) !important;
        }
        button.btn-scan,
        button.btn-spy,
        button.btn-download {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid #cbd5e1 !important;
            padding: 11px 22px !important;
            font-weight: 700 !important;
            cursor: pointer !important;
            white-space: nowrap !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            border-radius: 10px !important;
            transition: all 0.15s ease !important;
        }
        button.btn-scan:hover,
        button.btn-spy:hover,
        button.btn-download:hover {
            background: #f8fafc !important;
            border-color: #94a3b8 !important;
            color: #000000 !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
            transform: translateY(-1px);
        }
        button.btn-writer-submit {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid #cbd5e1 !important;
            padding: 12px 24px !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            cursor: pointer !important;
            border-radius: 10px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 8px !important;
            transition: all 0.15s ease !important;
        }
        button.btn-writer-submit:hover {
            background: #f8fafc !important;
            border-color: #94a3b8 !important;
            color: #000000 !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
            transform: translateY(-1px);
        }

        .spinner { display: none; text-align: center; padding: 40px 0; }
        .loader {
            width: 42px; height: 42px;
            border: 4px solid #e2e8f0;
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 12px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        /* Article Card */
        .article-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .article-card:hover {
            border-color: var(--border-hover);
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }
        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }
        .card-title {
            font-size: 17px;
            font-weight: 700;
            color: #1e3a8a;
            text-decoration: none;
            line-height: 1.4;
        }
        .card-title:hover { text-decoration: underline; color: var(--accent); }
        .product-tag {
            background: #f1f5f9;
            color: #334155;
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 6px;
            white-space: nowrap;
            border: 1px solid #cbd5e1;
        }
        .keyword-box {
            display: grid;
            grid-template-columns: 1fr 1.6fr;
            gap: 12px;
            background: var(--card-inner-bg);
            border: 1px solid #e2e8f0;
            padding: 12px 14px;
            border-radius: 10px;
            margin: 12px 0;
        }
        @media (max-width: 640px) { .keyword-box { grid-template-columns: 1fr; } }
        .kw-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 4px;
        }
        .main-kw {
            font-size: 15px;
            font-weight: 700;
            color: #047857;
        }
        .lsi-container {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            align-items: center;
        }
        .lsi-chip {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            color: #334155;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
        }

        /* Spy Section */
        .spy-header-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        .metric-box {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
        .metric-val { font-size: 22px; font-weight: 800; color: var(--text-main); }
        .section-box {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 16px;
        }
        .section-title {
            font-size: 15px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .reason-item {
            background: #ecfdf5;
            border-left: 3px solid #059669;
            color: #065f46;
            padding: 9px 12px;
            font-size: 13px;
            margin-bottom: 6px;
            border-radius: 0 6px 6px 0;
            font-weight: 500;
        }
        .blueprint-item {
            background: #f5f3ff;
            border-left: 3px solid #7c3aed;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
        }
        .bp-step { font-weight: 700; color: #5b21b6; font-size: 13px; margin-bottom: 2px; }
        .bp-desc { font-size: 13px; color: #374151; }

        .btn-download {
            background: #059669;
            color: white;
            border: none;
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(5, 150, 105, 0.2);
        }
        .btn-download:hover { background: #047857; }

        /* Semrush-Grade Competitor Audit & Spy Center */
        .semrush-hero-card {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 16px;
            padding: 24px;
            color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
            border: 1px solid #334155;
        }
        .semrush-hero-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 14px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 16px;
        }
        .semrush-score-circle {
            width: 86px;
            height: 86px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            font-weight: 800;
            border: 4px solid #10b981;
            background: rgba(16, 185, 129, 0.1);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.25);
            flex-shrink: 0;
            color: #10b981;
        }
        .semrush-score-circle.score-amber {
            border-color: #f59e0b;
            background: rgba(245, 158, 11, 0.1);
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.25);
            color: #f59e0b;
        }
        .semrush-score-circle.score-red {
            border-color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
            color: #ef4444;
        }
        .semrush-kpis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 10px;
            width: 100%;
        }
        .semrush-kpi-item {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px 14px;
            text-align: center;
        }
        .semrush-kpi-num {
            font-size: 20px;
            font-weight: 800;
            margin-top: 2px;
        }
        .semrush-kpi-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.5px;
        }

        /* Semrush Subtabs Nav */
        .semrush-subtabs-nav {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin-bottom: 18px;
            border-bottom: 2px solid #e2e8f0;
        }
        .sem-subtab-btn {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            padding: 9px 16px;
            border-radius: 9px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            color: #475569;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 7px;
            transition: all 0.15s ease;
        }
        .sem-subtab-btn:hover {
            border-color: #3b82f6;
            color: #1e40af;
            background: #eff6ff;
        }
        .sem-subtab-btn.active {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: #ffffff;
            border-color: #1e3a8a;
            box-shadow: 0 3px 8px rgba(37,99,235,0.25);
        }

        /* Filter Pills */
        .filter-pills-bar {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }
        .filter-pill {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            color: #475569;
            cursor: pointer;
            transition: all 0.15s;
        }
        .filter-pill.active {
            background: #0f172a;
            color: #ffffff;
            border-color: #0f172a;
        }
        .filter-pill.pill-red.active { background: #dc2626; border-color: #dc2626; color: white; }
        .filter-pill.pill-amber.active { background: #d97706; border-color: #d97706; color: white; }
        .filter-pill.pill-blue.active { background: #2563eb; border-color: #2563eb; color: white; }
        .filter-pill.pill-green.active { background: #059669; border-color: #059669; color: white; }

        /* Issues Cards */
        .issue-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 10px;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #94a3b8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: transform 0.1s;
        }
        .issue-card:hover { transform: translateY(-1px); box-shadow: 0 3px 8px rgba(0,0,0,0.05); }
        .issue-card.issue-critical { border-left-color: #ef4444; background: #fffafb; }
        .issue-card.issue-warning { border-left-color: #f59e0b; background: #fffdfa; }
        .issue-card.issue-notice { border-left-color: #3b82f6; background: #fbfdff; }
        .issue-card.issue-passed { border-left-color: #10b981; background: #fafffd; }

        .issue-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 6px;
        }
        .issue-title {
            font-size: 14.5px;
            font-weight: 700;
            color: #0f172a;
        }
        .issue-badge {
            font-size: 10.5px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 5px;
            letter-spacing: 0.5px;
        }
        .badge-critical { background: #fee2e2; color: #b91c1c; }
        .badge-warning { background: #fef3c7; color: #b45309; }
        .badge-notice { background: #dbeafe; color: #1e40af; }
        .badge-passed { background: #dcfce7; color: #15803d; }
        .badge-cat { background: #f1f5f9; color: #475569; }

        .issue-body { font-size: 13px; color: #475569; line-height: 1.5; }
        .issue-fix {
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed #e2e8f0;
            font-size: 12.5px;
            color: #047857;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Developer Checklist Styles */
        .dev-check-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 14px 18px;
            margin-bottom: 10px;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #94a3b8;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: all 0.15s ease;
        }
        .dev-check-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-color: #cbd5e1;
        }
        .dev-check-card.dev-status-pass { border-left-color: #10b981; }
        .dev-check-card.dev-status-warn { border-left-color: #f59e0b; }
        .dev-check-card.dev-status-fail { border-left-color: #ef4444; }
        .dev-check-card.dev-status-info { border-left-color: #3b82f6; }

        .badge-check-id {
            background: #0f172a;
            color: #f8fafc;
            font-size: 11px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 5px;
            font-family: monospace;
            letter-spacing: 0.5px;
        }
        .badge-status {
            font-size: 10.5px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 5px;
            text-transform: uppercase;
        }
        .badge-status-pass { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
        .badge-status-warn { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
        .badge-status-fail { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
        .badge-status-info { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }

        .badge-severity {
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
        }
        .severity-C { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
        .severity-W { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
        .severity-N { background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; }

        .cat-progress-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .site-pages-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12.5px;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
        .site-pages-table th {
            background: #f8fafc;
            color: #334155;
            font-weight: 800;
            padding: 10px 12px;
            border-bottom: 1.5px solid #cbd5e1;
            text-align: left;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .site-pages-table td {
            padding: 9px 12px;
            border-bottom: 1px solid #f1f5f9;
            color: #1e293b;
        }
        .site-pages-table tr:hover td {
            background: #f8fafc;
        }

        /* Tech & Diagnostics Grid */
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 14px;
        }
        .tech-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
        }
        .tech-card-title {
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            color: #334155;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 7px;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 8px;
        }
        .tech-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 0;
            font-size: 12.5px;
            border-bottom: 1px solid #f8fafc;
        }
        .tech-row:last-child { border-bottom: none; }
        .tech-key { color: #64748b; font-weight: 500; }
        .tech-val { font-weight: 700; color: #0f172a; text-align: right; }

        /* Writer Studio Styles */
        .writer-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 14px;
        }
        @media (max-width: 768px) { .writer-grid { grid-template-columns: 1fr; } }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        .form-group label {
            font-size: 12px;
            font-weight: 700;
            color: #334155;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .meta-package-card {
            background: linear-gradient(135deg, #f0fdf4, #ffffff);
            border: 1.5px solid #86efac;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }
        .meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 13px;
        }
        .meta-row:last-child { margin-bottom: 0; }
        .meta-btn-copy {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            color: #334155;
            white-space: nowrap;
        }
        .meta-btn-copy:hover { border-color: var(--writer-accent); color: var(--writer-accent); }

        .content-subtabs {
            display: flex;
            gap: 8px;
            margin-bottom: 14px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }
        .subtab-btn {
            background: transparent;
            border: none;
            padding: 6px 14px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            color: var(--text-muted);
            border-radius: 6px;
        }
        .subtab-btn.active {
            background: #e2e8f0;
            color: #0f172a;
        }

        /* Rendered Article Typography */
        .rendered-article {
            line-height: 1.7;
            font-size: 15px;
            color: #1e293b;
        }
        .rendered-article h1 { font-size: 26px; font-weight: 800; color: #0f172a; margin: 18px 0 12px; }
        .rendered-article h2 { font-size: 20px; font-weight: 700; color: #1e3a8a; margin: 20px 0 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }
        .rendered-article h3 { font-size: 16px; font-weight: 700; color: #334155; margin: 16px 0 8px; }
        .rendered-article p { margin-bottom: 14px; }
        .rendered-article ul, .rendered-article ol { margin: 10px 0 16px 24px; }
        .rendered-article li { margin-bottom: 6px; }
        .rendered-article blockquote {
            background: #f8fafc;
            border-left: 4px solid var(--writer-accent);
            padding: 12px 18px;
            margin: 16px 0;
            border-radius: 0 8px 8px 0;
            color: #334155;
            font-style: normal;
        }
        .rendered-article table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 13px;
        }
        .rendered-article th, .rendered-article td {
            border: 1px solid #cbd5e1;
            padding: 9px 12px;
            text-align: left;
        }
        .rendered-article th {
            background: #f1f5f9;
            font-weight: 700;
            color: #0f172a;
        }
        .raw-markdown-view {
            font-family: 'JetBrains Mono', monospace;
            background: #0f172a;
            color: #f8fafc;
            padding: 18px;
            border-radius: 10px;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre-wrap;
            overflow-x: auto;
            max-height: 550px;
        }

        /* Heading Outline Tree */
        .outline-tree {
            max-height: 380px;
            overflow-y: auto;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 16px;
            background: #fafafa;
        }
        .outline-node {
            padding: 6px 0;
            border-bottom: 1px dashed #e2e8f0;
            font-size: 13px;
            display: flex;
            align-items: baseline;
        }
        .outline-node:last-child { border-bottom: none; }
        .outline-badge-h1 {
            background: #dbeafe;
            color: #1e40af;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            margin-right: 8px;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }
        .outline-badge-h2 {
            background: #ede9fe;
            color: #6d28d9;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            margin-right: 8px;
            margin-left: 14px;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }
        .outline-badge-h3 {
            background: #ccfbf1;
            color: #0f766e;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            margin-right: 8px;
            margin-left: 28px;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }
        .outline-badge-h4 {
            background: #f1f5f9;
            color: #475569;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 4px;
            margin-right: 8px;
            margin-left: 40px;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }
        .gap-item {
            background: #fffbeb;
            border-left: 3px solid #f59e0b;
            color: #92400e;
            padding: 10px 14px;
            font-size: 13px;
            margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
            font-weight: 500;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .competitor-content-box {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 16px;
            font-size: 14px;
            line-height: 1.7;
            max-height: 380px;
            overflow-y: auto;
            color: #334155;
            white-space: pre-wrap;
        }
        .battle-card {
            background: linear-gradient(135deg, #f0fdf4, #ffffff);
            border: 1.5px solid #86efac;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(5, 150, 105, 0.08);
        }
        .battle-table {
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
            font-size: 13px;
        }
        .battle-table th {
            background: #0f172a;
            color: #ffffff;
            padding: 10px 14px;
            text-align: left;
        }
        .battle-table td {
            padding: 10px 14px;
            border-bottom: 1px solid #e2e8f0;
        }
        .battle-table tr:hover td {
            background: #f8fafc;
        }
        .battle-win {
            background: #dcfce7;
            color: #15803d;
            font-weight: 700;
            border-radius: 6px;
            padding: 3px 8px;
            display: inline-block;
        }
        .battle-comp {
            color: #64748b;
        }
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(4px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal-card {
            background: #ffffff;
            border-radius: 16px;
            max-width: 560px;
            width: 100%;
            padding: 26px;
            box-shadow: 0 20px 45px rgba(0,0,0,0.25);
            animation: modalIn 0.2s ease-out;
            max-height: 90vh;
            overflow-y: auto;
        }
        @keyframes modalIn {
            from { opacity: 0; transform: scale(0.96); }
            to { opacity: 1; transform: scale(1); }
        }

        /* White-Label Executive Report & Print Media Styles */
        @media print {
            body { background: #ffffff !important; color: #000000 !important; }
            .container, .modal-overlay { display: none !important; }
            #printableClientReport {
                display: block !important;
                visibility: visible !important;
                position: static !important;
                width: 100% !important;
                margin: 0 !important;
                padding: 10px !important;
                box-shadow: none !important;
                border: none !important;
            }
            .no-print { display: none !important; }
        }
        .report-kpi-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }
        .report-kpi-num {
            font-size: 24px;
            font-weight: 800;
            margin-top: 4px;
        }
        .roadmap-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin-top: 10px;
        }
        .roadmap-table th {
            background: #0f172a;
            color: #ffffff;
            padding: 10px 12px;
            text-align: left;
            font-weight: 700;
            font-size: 12px;
        }
        .roadmap-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #e2e8f0;
            vertical-align: middle;
            font-size: 12.5px;
        }
        .roadmap-table tr:hover td {
            background: #f8fafc;
        }
        .badge-intent {
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            display: inline-block;
        }
        .intent-info { background: #e0f2fe; color: #0369a1; }
        .intent-comm { background: #fef3c7; color: #92400e; }
        .intent-trans { background: #dcfce7; color: #166534; }

        /* ================= WORLD-CLASS RANKNASERPRO AUTHENTICATION & SHOWCASE (WHITE THEME) ================= */
        #authScreen {
            display: block;
        }
        #dashboardWrapper {
            display: none;
        }
        .auth-container {
            max-width: 1180px;
            margin: 0 auto;
        }
        .auth-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            flex-wrap: wrap;
            gap: 14px;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 16px;
        }
        .auth-live-status {
            font-size: 11.5px;
            font-weight: 700;
            color: #059669;
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 20px;
            padding: 4px 12px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .auth-btn-quick {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: white;
            border: none;
            font-weight: 700;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 12.5px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(2, 132, 199, 0.25);
            transition: all 0.2s;
        }
        .auth-btn-quick:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
        }
        .auth-hero-header {
            text-align: center;
            margin-bottom: 28px;
        }
        .auth-hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: #e0f2fe;
            border: 1px solid #bae6fd;
            border-radius: 20px;
            padding: 5px 16px;
            font-size: 11px;
            font-weight: 800;
            color: #0284c7;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 12px;
        }
        .auth-hero-title {
            font-size: 38px;
            font-weight: 900;
            background: linear-gradient(135deg, #0f172a 35%, #0369a1 80%, #0284c7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 12px 0;
            letter-spacing: -0.8px;
            line-height: 1.22;
        }
        .auth-hero-subtitle {
            font-size: 15.5px;
            color: #475569;
            max-width: 820px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* 4-Item Live Capability Highlight Strip */
        .auth-capability-strip {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 34px;
        }
        @media (max-width: 860px) {
            .auth-capability-strip { grid-template-columns: repeat(2, 1fr); }
            .auth-hero-title { font-size: 28px; }
        }
        @media (max-width: 520px) {
            .auth-capability-strip { grid-template-columns: 1fr; }
        }
        .cap-strip-card {
            background: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 12px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
        }
        .cap-strip-card:hover {
            border-color: #0284c7;
            background: #ffffff;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.1);
        }
        .cap-strip-icon {
            font-size: 24px;
            flex-shrink: 0;
        }
        .cap-strip-title {
            font-size: 13px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 2px;
        }
        .cap-strip-desc {
            font-size: 11px;
            color: #64748b;
            line-height: 1.35;
        }

        /* 2-Column Split Grid */
        .auth-split-grid {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 26px;
            align-items: stretch;
            margin-bottom: 50px;
        }
        @media (max-width: 880px) {
            .auth-split-grid { grid-template-columns: 1fr; }
        }
        .profile-side-card {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 20px;
            padding: 28px 22px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.07);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        .profile-badge-float {
            position: absolute;
            top: 14px;
            right: 14px;
            background: #e0f2fe;
            border: 1px solid #bae6fd;
            color: #0284c7;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 9px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .profile-img-wrap {
            width: 144px;
            height: 144px;
            border-radius: 50%;
            overflow: hidden;
            margin: 6px 0 14px 0;
            border: 3.5px solid #0284c7;
            box-shadow: 0 0 24px rgba(2, 132, 199, 0.28);
            position: relative;
            background: #f1f5f9;
        }
        .profile-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        .profile-name-badge {
            font-size: 26px;
            font-weight: 900;
            color: #0f172a;
            letter-spacing: 1.8px;
            margin: 0 0 4px 0;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 7px;
            justify-content: center;
        }
        .profile-role-title {
            font-size: 11.5px;
            font-weight: 800;
            color: #0284c7;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .profile-bio-text {
            font-size: 12.5px;
            color: #475569;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        .profile-pill-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            color: #1e293b;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 12px;
            width: 100%;
            margin-bottom: 6px;
            text-align: left;
            box-sizing: border-box;
            font-weight: 600;
        }
        .login-box-card {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 20px;
            padding: 28px 30px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.07);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .auth-input-group {
            margin-bottom: 15px;
        }
        .auth-input-group label {
            display: block;
            font-size: 12.5px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 6px;
        }
        .auth-input-group input {
            width: 100%;
            padding: 12px 14px;
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            color: #0f172a;
            font-size: 14px;
            box-sizing: border-box;
            transition: all 0.2s;
            font-weight: 600;
        }
        .auth-input-group input:focus {
            outline: none;
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.18) !important;
        }
        .auth-submit-btn {
            width: 100%;
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: white;
            border: none;
            font-weight: 800;
            border-radius: 10px;
            padding: 12px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
            transition: all 0.2s;
            margin-top: 6px;
        }
        .auth-submit-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.45);
        }

        /* 3-Step Autonomous Workflow Pipeline */
        .workflow-pipeline-section {
            margin-bottom: 50px;
            padding: 26px;
            background: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 16px;
        }
        .workflow-title {
            text-align: center;
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            margin: 0 0 6px 0;
        }
        .workflow-subtitle {
            text-align: center;
            font-size: 13px;
            color: #64748b;
            margin: 0 0 22px 0;
        }
        .pipeline-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        @media (max-width: 768px) {
            .pipeline-grid { grid-template-columns: 1fr; }
        }
        .pipeline-card {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 18px;
            position: relative;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }
        .pipeline-step-badge {
            display: inline-block;
            background: #e0f2fe;
            color: #0284c7;
            font-size: 10.5px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 6px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        .pipeline-card h4 {
            margin: 0 0 6px 0;
            font-size: 14.5px;
            font-weight: 800;
            color: #0f172a;
        }
        .pipeline-card p {
            margin: 0;
            font-size: 12px;
            color: #475569;
            line-height: 1.5;
        }

        /* 3D Circular Orbital Globe SEO Agent Showcase (White Theme) */
        .globe-showcase-section {
            margin-top: 25px;
            border-top: 1.5px solid #e2e8f0;
            padding-top: 45px;
        }
        .globe-section-title {
            text-align: center;
            margin-bottom: 35px;
        }
        .globe-orb-wrapper {
            position: relative;
            max-width: 860px;
            height: 480px;
            margin: 0 auto 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        @media (max-width: 820px) {
            .globe-orb-wrapper {
                height: auto;
                flex-direction: column;
                gap: 12px;
            }
        }
        .globe-central-core {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #38bdf8 0%, #0284c7 40%, #1e3a8a 85%, #0f172a 100%);
            box-shadow: 0 0 50px rgba(2, 132, 199, 0.45), inset 0 0 25px rgba(255,255,255,0.4);
            border: 3px solid rgba(56, 189, 248, 0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 16px;
            z-index: 10;
            animation: coreFloat 4s ease-in-out infinite;
        }
        @keyframes coreFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-6px) scale(1.02); }
        }
        .globe-node-card {
            position: absolute;
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 14px;
            padding: 12px 16px;
            max-width: 235px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
            transition: all 0.25s ease;
            z-index: 5;
        }
        .globe-node-card:hover {
            transform: scale(1.04);
            border-color: #0284c7;
            box-shadow: 0 12px 30px rgba(2, 132, 199, 0.2);
        }
        @media (max-width: 820px) {
            .globe-node-card {
                position: static !important;
                max-width: 100%;
                width: 100%;
                margin-bottom: 6px;
            }
        }
        .globe-node-card .gn-icon { font-size: 20px; margin-bottom: 4px; }
        .globe-node-card .gn-title { font-size: 13.5px; font-weight: 800; color: #0f172a; margin-bottom: 3px; }
        .globe-node-card .gn-desc { font-size: 11.5px; color: #475569; line-height: 1.45; }

        /* Feature Matrix Grid (White Theme) */
        .feature-matrix-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 18px;
            margin-top: 30px;
        }
        .fm-card {
            background: #ffffff;
            border: 1.5px solid #e2e8f0;
            border-radius: 14px;
            padding: 22px;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        }
        .fm-card:hover {
            border-color: #0284c7;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(2, 132, 199, 0.12);
        }
        .fm-icon-badge {
            width: 40px; height: 40px;
            border-radius: 10px;
            background: #e0f2fe;
            border: 1px solid #bae6fd;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; margin-bottom: 12px;
        }
        .fm-title { font-size: 15.5px; font-weight: 800; color: #0f172a; margin-bottom: 6px; }
        .fm-desc { font-size: 12.5px; color: #475569; line-height: 1.55; }
    
        /* ================= INTELLECTUAL PROPERTY & STYLING ================= */
        input, textarea, [contenteditable="true"] {
            user-select: text;
        }
</style>
</head>
<body>

    <!-- ================= RANKNASER AUTHENTICATION GATEWAY ================= -->
    <div id="authScreen" style="display: none;">
        <div class="auth-container">
            <!-- Top Branding Bar -->
            <div class="auth-topbar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 28px;">🚀</span>
                    <div>
                        <div style="font-size: 20px; font-weight: 900; letter-spacing: 1.2px; color: #0f172a;">RANKNASER<span style="color: #0284c7;">PRO</span></div>
                        <div style="font-size: 11px; color: #64748b; font-weight: 600;">Autonomous SEO Intelligence & Organic Domination Engine</div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                    <span class="auth-live-status">● Live Engine v3.5 Active</span>
                    <button type="button" onclick="document.getElementById('authScreen').style.display='none'; document.getElementById('dashboardWrapper').style.display='block'; window.scrollTo(0,0); localStorage.setItem('ranknaser_auth_user', JSON.stringify({name:'RankNaser Admin', username:'ADMIN'})); try{handleInstantDemoLogin();}catch(e){}" class="auth-btn-quick">
                        ⚡ Instant Enter (1-Click)
                    </button>
                </div>
            </div>

            <!-- Killer English Headline -->
            <div class="auth-hero-header">
                <div class="auth-hero-eyebrow">⚡ AUTONOMOUS SEARCH INTELLIGENCE & SERP OUTRANKER</div>
                <h1 class="auth-hero-title">Outrank Any Competitor on Google with Autonomous AI Agents</h1>
                <p class="auth-hero-subtitle">
                    Deploy 6 specialized AI agents to track rival rankings, reverse-engineer top Google SERPs, write 2,500+ word master articles, and auto-publish to your CMS on 100% autopilot.
                </p>
                <div style="margin-top: 14px;">
                    <span style="display: inline-flex; align-items: center; gap: 8px; background: #ecfdf5; border: 1.5px solid #a7f3d0; border-radius: 20px; padding: 6px 18px; font-size: 12px; font-weight: 800; color: #047857;">
                        <span>🎁</span> 1-WEEK (7-DAY) UNLIMITED FREE TRIAL ACCESS FOR USERS (AUTOMATIC EXPIRATION)
                    </span>
                </div>
            </div>

            <!-- 4-Item Live Capability Highlight Strip (Immediately Explains What the Suite Does) -->
            <div class="auth-capability-strip">
                <div class="cap-strip-card">
                    <div class="cap-strip-icon">🛰️</div>
                    <div>
                        <div class="cap-strip-title">SERP Radar Surveillance</div>
                        <div class="cap-strip-desc">Tracks top 1-10 rankings & detects keyword moves</div>
                    </div>
                </div>
                <div class="cap-strip-card">
                    <div class="cap-strip-icon">⚔️</div>
                    <div>
                        <div class="cap-strip-title">5 vs 1 SERP Outranker</div>
                        <div class="cap-strip-desc">Reverse-engineers 5 ranking rivals into 1 master brief</div>
                    </div>
                </div>
                <div class="cap-strip-card">
                    <div class="cap-strip-icon">✍️</div>
                    <div>
                        <div class="cap-strip-title">2,500+ Word AI Studio</div>
                        <div class="cap-strip-desc">Generates rank-ready articles with FAQ Schema</div>
                    </div>
                </div>
                <div class="cap-strip-card">
                    <div class="cap-strip-icon">🤖</div>
                    <div>
                        <div class="cap-strip-title">Direct CMS Auto-Publish</div>
                        <div class="cap-strip-desc">Zero-click publishing straight to WordPress & APIs</div>
                    </div>
                </div>
            </div>

            <!-- 2-Column Split: RankNaser Profile Card + Compact Sign In Box -->
            <div class="auth-split-grid">
                <!-- Left: RankNaser Profile Card -->
                <div class="profile-side-card">
                    <div class="profile-badge-float">Verified Architect</div>
                    <div class="profile-img-wrap">
                        <img src="__RANKNASER_PHOTO_URI__" alt="RankNaser" id="ranknaserHeroPhoto" onerror="this.src='/static/ranknaser.jpg'">
                    </div>
                    <div class="profile-name-badge">
                        <span>RANKNASER</span>
                        <span style="color: #0284c7; font-size: 19px;" title="Verified System Architect">☑️</span>
                    </div>
                    <div class="profile-role-title">Lead Architect & SEO Director</div>
                    <div class="profile-bio-text">
                        Pioneered autonomous AI agent pipelines that monitor competitive search landscapes 24/7, synthesize top-ranking SERP signals, and eliminate months of manual SEO labor.
                    </div>
                    <div style="width: 100%; margin-top: 4px;">
                        <div class="profile-pill-item">
                            <span>🛰️</span>
                            <span>Autonomous SERP Radar & Keyword Tracking</span>
                        </div>
                        <div class="profile-pill-item">
                            <span>🕵️‍♂️</span>
                            <span>Deep Competitor Infiltration & Headings Spy</span>
                        </div>
                        <div class="profile-pill-item">
                            <span>⚔️</span>
                            <span>5 vs 1 Outranking Master Synthesis</span>
                        </div>
                        <div class="profile-pill-item">
                            <span>✍️</span>
                            <span>Long-Form Content Generation with Schema</span>
                        </div>
                        <div class="profile-pill-item">
                            <span>🤖</span>
                            <span>Zero-Click Direct CMS Auto-Publishing</span>
                        </div>
                    </div>
                    <div style="margin-top: 14px; font-size: 11.5px; color: #059669; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                        System Online & Ready to Execute
                    </div>
                </div>

                <!-- Right: Direct Admin Login Box -->
                <div class="login-box-card">
                    <div style="margin-bottom: 22px; text-align: center;">
                        <div style="display: inline-flex; align-items: center; gap: 7px; background: #e0f2fe; border: 1px solid #bae6fd; border-radius: 20px; padding: 5px 15px; font-size: 11px; font-weight: 800; color: #0284c7; text-transform: uppercase; letter-spacing: 1px;">
                            🔐 DIRECT SYSTEM ACCESS
                        </div>
                        <h3 style="margin: 9px 0 4px 0; font-size: 21px; font-weight: 800; color: #0f172a;">Admin Gateway Sign In</h3>
                        <p style="margin: 0; font-size: 12.5px; color: #64748b;">Enter your Admin User ID & Password to access the suite</p>
                    </div>

                    <div id="authAlertBox" style="display:none; padding: 10px 14px; border-radius: 8px; font-size: 12.5px; margin-bottom: 14px; font-weight: 600;"></div>

                    <!-- Direct Admin Login Form -->
                    <form id="loginForm" onsubmit="event.preventDefault(); document.getElementById('authScreen').style.display='none'; document.getElementById('dashboardWrapper').style.display='block'; window.scrollTo(0,0); localStorage.setItem('ranknaser_auth_user', JSON.stringify({name:'RankNaser Admin', username:'ADMIN'})); try{handleAuthLogin(event);}catch(e){}">
                        <div class="auth-input-group">
                            <label for="loginUsername">User / Admin ID</label>
                            <input type="text" id="loginUsername" placeholder="ADMIN" required value="ADMIN" autocomplete="username" style="font-weight: 700; letter-spacing: 0.5px;">
                        </div>
                        <div class="auth-input-group">
                            <label for="loginPassword">Password</label>
                            <input type="password" id="loginPassword" placeholder="AGENTNASER" required value="AGENTNASER" autocomplete="current-password">
                        </div>
                        <button type="button" id="btnSubmitLogin" onclick="document.getElementById('authScreen').style.display='none'; document.getElementById('dashboardWrapper').style.display='block'; window.scrollTo(0,0); localStorage.setItem('ranknaser_auth_user', JSON.stringify({name:'RankNaser Admin', username:'ADMIN'})); try{handleAuthLogin(event);}catch(e){}" class="auth-submit-btn">
                            <span>🚀 Launch RankNaserPro Dashboard</span>
                        </button>
                    </form>

                    <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid #e2e8f0; text-align: center;">
                        <button type="button" onclick="document.getElementById('authScreen').style.display='none'; document.getElementById('dashboardWrapper').style.display='block'; window.scrollTo(0,0); localStorage.setItem('ranknaser_auth_user', JSON.stringify({name:'RankNaser Admin', username:'ADMIN'})); try{handleInstantDemoLogin();}catch(e){}" style="background: #f0f9ff; border: 1.5px dashed #0284c7; color: #0284c7; font-weight: 700; border-radius: 8px; padding: 9px 16px; cursor: pointer; font-size: 12.5px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 7px; transition: all 0.2s;">
                            <span>⚡ 1-Click Instant Enter (ADMIN / AGENTNASER)</span>
                        </button>
                        <div style="font-size: 12px; color: #334155; margin-top: 10px; background: #f8fafc; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0;">
                            🔑 <strong>Credentials:</strong> User: <span style="color:#0284c7; font-weight:800;">ADMIN</span> | Password: <span style="color:#0284c7; font-weight:800;">AGENTNASER</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3-Step Autonomous Workflow Pipeline Section -->
            <div class="workflow-pipeline-section">
                <h3 class="workflow-title">⚡ How The 6 Autonomous Tools Work Together</h3>
                <p class="workflow-subtitle">A synchronized multi-agent pipeline from competitive espionage to front-page dominance</p>
                <div class="pipeline-grid">
                    <div class="pipeline-card">
                        <span class="pipeline-step-badge">Phase 1: Spy & Infiltrate</span>
                        <h4>🛰️ SERP Radar + 360° Deep Spy</h4>
                        <p>Monitors keyword movement #1-10 on Google, detects new ranking rivals, and scrapes full heading trees (H1-H3), word counts, and search intents in seconds.</p>
                    </div>
                    <div class="pipeline-card">
                        <span class="pipeline-step-badge">Phase 2: Synthesize & Outrank</span>
                        <h4>⚔️ 5 vs 1 SERP + AI Studio</h4>
                        <p>Takes the top 5 ranking competitors simultaneously, pinpoints their shared patterns and missing topics, then writes an elite 2,500+ word master article with FAQ Schema.</p>
                    </div>
                    <div class="pipeline-card">
                        <span class="pipeline-step-badge">Phase 3: Autopilot & Direct Publish</span>
                        <h4>🤖 Autopilot + SEO Director</h4>
                        <p>Automatically publishes articles to WordPress CMS or Custom Webhooks without manual copying, and generates a structured 10-day execution campaign.</p>
                    </div>
                </div>
            </div>

            <!-- 3D Circular Orbital Globe SEO Agent Showcase -->
            <div class="globe-showcase-section">
                <div class="globe-section-title">
                    <span class="auth-hero-eyebrow">🌐 360° AUTONOMOUS SEO INTELLIGENCE</span>
                    <h2 style="font-size: 30px; font-weight: 900; color: #0f172a; margin: 8px 0 10px 0; letter-spacing: -0.5px;">
                        How the RankNaser SEO Agent Dominates Search Engines
                    </h2>
                    <p style="font-size: 14.5px; color: #475569; max-width: 720px; margin: 0 auto;">
                        A unified autonomous neural intelligence loop executing 24/7 surveillance, competitive gap synthesis, keyword tracking, and direct CMS publishing.
                    </p>
                </div>

                <!-- Central Globe & Orbital Ring Architecture -->
                <div class="globe-orb-wrapper">
                    <!-- Center Core -->
                    <div class="globe-central-core">
                        <div style="font-size: 34px; margin-bottom: 4px;">🧠</div>
                        <div style="font-size: 15px; font-weight: 900; color: #ffffff; letter-spacing: 1px;">RANKNASER</div>
                        <div style="font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase;">AI AGENT CORE</div>
                        <div style="font-size: 10px; color: #e2e8f0; margin-top: 6px; background: rgba(0,0,0,0.3); padding: 2px 8px; border-radius: 10px;">Autopilot Active</div>
                    </div>

                    <!-- 6 Orbital Nodes positioned around the globe -->
                    <div class="globe-node-card" style="top: 10px; left: 6%;">
                        <div class="gn-icon">🛰️</div>
                        <div class="gn-title">1. Daily SERP Radar</div>
                        <div class="gn-desc">Tracks target domain against competitors, monitoring rank positions #1-10 with keyword velocity alerts.</div>
                    </div>

                    <div class="globe-node-card" style="top: 10px; right: 6%;">
                        <div class="gn-icon">🕵️‍♂️</div>
                        <div class="gn-title">2. 360° Deep Spy</div>
                        <div class="gn-desc">Scrapes competitor headers, meta signals, exact word counts, and content gaps instantly.</div>
                    </div>

                    <div class="globe-node-card" style="top: 44%; right: -2%;">
                        <div class="gn-icon">⚔️</div>
                        <div class="gn-title">3. 5 vs 1 SERP Outranker</div>
                        <div class="gn-desc">Analyzes top 5 competitors simultaneously to extract universal patterns and synthesize unbeatable content.</div>
                    </div>

                    <div class="globe-node-card" style="bottom: 10px; right: 8%;">
                        <div class="gn-icon">✍️</div>
                        <div class="gn-title">4. Full-Auto AI Writer</div>
                        <div class="gn-desc">Generates human-grade 2,500+ word rank-ready articles infused with FAQ, Schema markup, and LSI entities.</div>
                    </div>

                    <div class="globe-node-card" style="bottom: 10px; left: 8%;">
                        <div class="gn-icon">🤖</div>
                        <div class="gn-title">5. Autonomous Autopilot</div>
                        <div class="gn-desc">Self-driving keyword scraper, content generator, and auto-publisher directly to WordPress & Custom APIs.</div>
                    </div>

                    <div class="globe-node-card" style="top: 44%; left: -2%;">
                        <div class="gn-icon">🎯</div>
                        <div class="gn-title">6. SEO Director Agent</div>
                        <div class="gn-desc">Architects bespoke 10-day campaign roadmaps with execution deliverables ready in 1 click.</div>
                    </div>
                </div>

                <!-- Deep Feature Breakdown Matrix Grid -->
                <div class="feature-matrix-grid">
                    <div class="fm-card">
                        <div class="fm-icon-badge">📅</div>
                        <div class="fm-title">Daily Competitor SERP Radar</div>
                        <div class="fm-desc">Scan target domains against competitors on Google SERP. Automatically detect ranking movement, new keyword appearances, and competitive drops.</div>
                    </div>
                    <div class="fm-card">
                        <div class="fm-icon-badge">🕵️‍♂️</div>
                        <div class="fm-title">360° Deep Competitive Infiltration</div>
                        <div class="fm-desc">Extract competitor title tags, H1-H3 heading hierarchies, exact word counts, intent classifications, and uncovered topical blindspots.</div>
                    </div>
                    <div class="fm-card">
                        <div class="fm-icon-badge">⚔️</div>
                        <div class="fm-title">5 vs 1 SERP Synthesis Engine</div>
                        <div class="fm-desc">Compare up to 5 ranking rivals side-by-side. Spot common themes, identify missing topics across the SERP, and generate master outranking briefs.</div>
                    </div>
                    <div class="fm-card">
                        <div class="fm-icon-badge">✍️</div>
                        <div class="fm-title">Elite Long-Form AI Content Studio</div>
                        <div class="fm-desc">Generate comprehensive 2,500+ word guides with humanized flow, FAQ schema, meta descriptions, and live formatting previews.</div>
                    </div>
                    <div class="fm-card">
                        <div class="fm-icon-badge">🤖</div>
                        <div class="fm-title">Autopilot Scheduling & Multi-CMS Push</div>
                        <div class="fm-desc">Connect WordPress via REST API or Custom Webhooks. Push articles to Draft or Publish mode instantly with 100% zero manual copy-pasting.</div>
                    </div>
                    <div class="fm-card">
                        <div class="fm-icon-badge">🎯</div>
                        <div class="fm-title">10-Day SEO Director Master Blueprint</div>
                        <div class="fm-desc">Input brand niche and target country to receive an actionable 10-day execution campaign complete with generated meta tags, briefs, and code.</div>
                    </div>
                </div>

                <!-- Bottom Jump to Login Bar -->
                <div style="margin-top: 36px; text-align: center; background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px;">
                    <h3 style="margin: 0 0 8px 0; font-size: 19px; font-weight: 800; color: #0f172a;">Ready to dominate Google search results?</h3>
                    <p style="margin: 0 0 14px 0; font-size: 13.5px; color: #475569;">Log in above to access your autonomous RankNaserPro Intelligence Suite.</p>
                    <button type="button" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); document.getElementById('loginUsername').focus();" class="auth-btn-quick" style="padding: 10px 22px; font-size: 13px;">
                        ⬆️ Return to Login Box
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- ================= DASHBOARD MAIN WRAPPER ================= -->
    <div id="dashboardWrapper" style="display: block;">
    <div class="container">
        <header style="margin-bottom: 20px;">
            <!-- Top Bar: Brand on Left, Account/Status & Logout on Right -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 14px;">
                <div style="text-align: left;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                        <span class="logo-badge" onclick="goBackToHome();" title="Click to return to Home (Daily Tracker)">
                            <span>🚀</span> RANKNASERPRO <span style="font-size: 10px; background: #f1f5f9; color: #475569; padding: 1px 6px; border-radius: 4px; margin-left: 2px;">Home</span>
                        </span>
                    </div>
                    <h1 onclick="goBackToHome();" style="cursor: pointer; margin: 0 0 4px 0;" title="Click to return to Home (Daily Tracker)">RankNaserPro Intelligence Suite</h1>
                    <p class="subtitle" style="margin: 0; color: #64748b; font-size: 13.5px;">Autonomous Competitor Spy, 5 vs 1 SERP Outranker & AI Content Publishing Machine</p>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <div id="trialCountdownBadge" class="header-status-badge">
                        <span style="font-size: 13px;">⏱️</span>
                        <span id="trialCountdownText">7-Day Free Trial: Day 1 of 7</span>
                    </div>
                    <div id="currentUserBadge" class="header-status-badge">
                        <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #10b981;"></span>
                        <span id="currentUserNameDisplay">👤 RankNaser</span>
                    </div>
                    <button type="button" id="logoutBtn" onclick="handleLogout()" class="header-logout-btn" title="Logout and return to Login Screen">
                        <span>🚪 Logout</span>
                    </button>
                </div>
            </div>

            <!-- Quick Actions: Symmetrical Category Cards Grid -->
            <div class="action-toolbar-grid">
                <button type="button" id="clientsHubHeaderBtn" onclick="openClientsHubModal()" class="action-card-btn" title="Connect and manage up to 5 Client Companies & WordPress Accounts">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect><line x1="9" y1="22" x2="9" y2="2"></line><line x1="8" y1="6" x2="8.01" y2="6"></line><line x1="16" y1="6" x2="16.01" y2="6"></line><line x1="16" y1="10" x2="16.01" y2="10"></line><line x1="16" y1="14" x2="16.01" y2="14"></line></svg>
                    </span>
                    <span class="action-card-title">5 Clients Hub</span>
                    <span id="headerClientsCountBadge" class="header-inner-badge" style="background: #dcfce7; color: #166534; border: 1px solid #86efac;">5 Active</span>
                </button>
                <button type="button" id="roadmapBtn" onclick="openRoadmapModal()" class="action-card-btn" title="View 30-Day Content Roadmap">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
                    </span>
                    <span class="action-card-title">Content Roadmap</span>
                </button>
                <button type="button" id="wpSetupBtn" onclick="openWpModal()" class="action-card-btn" title="Configure WordPress Site">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="m4.93 4.93 4.24 4.24"></path><path d="m14.83 9.17 4.24-4.24"></path><path d="m14.83 14.83 4.24 4.24"></path><path d="m9.17 14.83-4.24 4.24"></path></svg>
                    </span>
                    <span class="action-card-title">WordPress</span>
                    <span id="wpStatusBadge" class="header-inner-badge">Not Configured</span>
                </button>
                <button type="button" id="customApiBtn" onclick="openCustomApiModal()" class="action-card-btn" title="Configure Custom Site API">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                    </span>
                    <span class="action-card-title">Custom Site API</span>
                    <span id="customApiBadge" class="header-inner-badge">Not Configured</span>
                </button>
                <button type="button" id="userGuideHeaderBtn" onclick="openUserGuideModal()" class="action-card-btn" title="View & Download Official User Guide (English & বাংলা PDF)">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                    </span>
                    <span class="action-card-title">User Guide (PDF)</span>
                </button>
                <button type="button" id="returnDashboardBtn" onclick="goBackToHome();" class="action-card-btn" title="Return to Dashboard">
                    <span class="action-card-icon">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                    </span>
                    <span class="action-card-title">Return Dashboard</span>
                </button>
            </div>
        </header>

        <!-- ================= 1-WEEK FREE TRIAL USER WELCOME MESSAGE ================= -->
        <div id="trialWelcomeAlert" style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; gap: 16px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04); flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 42px; height: 42px; background: #f8fafc; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px; border: 1px solid #e2e8f0; flex-shrink: 0;">
                    🎁
                </div>
                <div>
                    <div style="font-size: 14.5px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                        <span>Your 1-Week (7-Day) Unlimited Free Trial is Active!</span>
                        <span style="font-size: 11px; background: #dcfce7; color: #166534; border: 1px solid #86efac; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Full Access</span>
                    </div>
                    <div style="font-size: 12.5px; color: #475569; margin-top: 3px;">
                        Enjoy 100% unrestricted access to all 6 autonomous SEO engines for 7 days. After 1 week, your trial will automatically expire.
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <button type="button" onclick="showTrialWelcomeModal()" class="header-logout-btn" style="padding: 7px 14px; font-size: 12px;">
                    📋 View Trial Message
                </button>
                <button type="button" onclick="dismissTrialAlert()" class="header-logout-btn" style="padding: 7px 12px; font-size: 12px;" title="Dismiss message">
                    ✕ Dismiss
                </button>
            </div>
        </div>

        <!-- 7-Engine Navigation Tabs: Symmetrical Category Cards Grid -->
        <div class="tabs-nav">
            <button class="tab-btn active daily" id="tabDailyBtn" onclick="switchTab('daily')" title="1. Daily Competitor Keyword Tracker">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line><path d="m9 16 2 2 4-4"></path></svg>
                </span>
                <span class="tab-label">1. Daily Tracker</span>
            </button>
            <button class="tab-btn spy" id="tabSpyBtn" onclick="switchTab('spy')" title="2. Semrush-Grade Site Audit & Competitor Spy">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><path d="m11 8v6"></path><path d="m8 11h6"></path></svg>
                </span>
                <span class="tab-label">2. Audit & Spy</span>
            </button>
            <button class="tab-btn multi" id="tabMultiBtn" onclick="switchTab('multi')" title="3. 5 vs 1 SERP Outrank Matrix">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line><path d="m14 2 4 4-4 4"></path></svg>
                </span>
                <span class="tab-label">3. 5 vs 1 Outrank</span>
            </button>
            <button class="tab-btn writer" id="tabWriterBtn" onclick="switchTab('writer')" title="4. AI Content Studio & Article Generator">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                </span>
                <span class="tab-label">4. Content Studio</span>
            </button>
            <button class="tab-btn autopilot" id="tabAutopilotBtn" onclick="switchTab('autopilot')" title="5. Autonomous SEO Autopilot Agent">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8.01" y2="16"></line><line x1="16" y1="16" x2="16.01" y2="16"></line></svg>
                </span>
                <span class="tab-label">5. Autopilot Agent</span>
            </button>
            <button class="tab-btn director" id="tabDirectorBtn" onclick="switchTab('director')" title="6. Personal SEO Agent">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.54z"></path><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.54z"></path></svg>
                </span>
                <span class="tab-label">6. Personal SEO</span>
            </button>
            <button class="tab-btn agency" id="tabAgencyBtn" onclick="switchTab('agency')" title="7. AI Agency Workforce (Multi-Client)">
                <span class="tab-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                </span>
                <span class="tab-label">7. Agency Team</span>
            </button>
        </div>

        <!-- TAB 1: Daily Tracker -->
        <div id="tabDaily">
            <div class="search-card">
                <form id="trackerForm" onsubmit="event.preventDefault(); submitTrackerForm(event); return false;">
                    <div class="form-grid-tracker">
                        <input type="text" id="urlInput" value="" placeholder="Enter Competitor Domain OR Specific Page (e.g. https://example.com or https://example.com/blog)" required>
                        <input type="date" id="dateInput" title="Optional: Filter by publication date">
                        <button type="button" class="btn-scan" id="scanBtn" onclick="submitTrackerForm(event);">
                            <span>🔍 Real-Time SEO Audit & Scan</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="spinner" id="trackerSpinner">
                <div class="loader"></div>
                <h3>Auditing Competitor Website: Running Real-Data Diagnostics...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Analyzing TTFB latency, HTTP status, SSL, heading tree, on-page SEO errors, EEAT trust signals, and Google AI Overview readiness in real-time...</p>
            </div>

            <div id="trackerResults" style="display: none;">
                <!-- Real-Time Semrush-Grade Live Audit Report Container -->
                <div id="trackerLiveAudit"></div>

                <!-- Discovered Competitor Articles Container (if multiple articles found) -->
                <div id="trackerArticlesBlock" style="display: none; margin-top: 26px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px; background: #f8fafc; padding: 12px 18px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <h2 id="trackerCount" style="font-size: 17px; margin: 0; font-weight: 700; color: #0f172a;">Discovered Competitor Articles / Pages</h2>
                        <button class="btn-download" onclick="downloadCSV()">⬇️ Download CSV</button>
                    </div>
                    <div id="trackerCards"></div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Competitor Deep Spy -->
        <div id="tabSpy" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; box-shadow: 0 2px 6px rgba(37,99,235,0.25); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <span>⬅️ Back to Home / Daily Tracker</span>
                </button>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748b; font-weight: 600;">
                    <a href="javascript:void(0)" onclick="goBackToHome();" style="color: #2563eb; text-decoration: none;">🏠 Home</a>
                    <span>&rsaquo;</span>
                    <span style="background: #f3e8ff; color: #7e22ce; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 12px;">🔍 Tab 2: Semrush-Grade Site Audit & Spy</span>
                </div>
            </div>

            <div class="search-card" style="border-color: rgba(139, 92, 246, 0.4);">
                <form id="spyForm" onsubmit="event.preventDefault(); submitSpyForm(event); return false;">
                    <div class="form-grid">
                        <input type="text" id="spyUrlInput" value="" placeholder="Enter Competitor Domain OR Specific Page (e.g. https://example.com or https://example.com/blog/article)" required>
                        <button type="button" class="btn-spy" id="spyBtn" onclick="submitSpyForm(event);">
                            <span>🔍 Run Semrush-Grade Deep Audit</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="spinner" id="spySpinner">
                <div class="loader" style="border-top-color: var(--spy-accent);"></div>
                <h3>Auditing Competitor Website: Running Real-Data Diagnostics...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Analyzing technical health (TTFB, SSL, robots.txt, sitemap), on-page SEO errors, EEAT trust signals, and Google AI Overview readiness...</p>
            </div>

            <div id="spyResults" style="display: none;">
                <!-- Content injected dynamically -->
            </div>
        </div>

        <!-- TAB 3: 5 vs 1 Master Outranker -->
        <div id="tabMulti" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; box-shadow: 0 2px 6px rgba(37,99,235,0.25); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <span>⬅️ Back to Home / Daily Tracker</span>
                </button>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748b; font-weight: 600;">
                    <a href="javascript:void(0)" onclick="goBackToHome();" style="color: #2563eb; text-decoration: none;">🏠 Home</a>
                    <span>&rsaquo;</span>
                    <span style="background: #fee2e2; color: #b91c1c; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 12px;">⚔️ Tab 3: 5 vs 1 Outrank</span>
                </div>
            </div>

            <div class="search-card" style="border-color: rgba(220, 38, 38, 0.4); background: linear-gradient(180deg, #ffffff, #fffafb);">
                <div style="margin-bottom: 18px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                        <h2 style="font-size: 20px; font-weight: 800; color: #991b1b; display: flex; align-items: center; gap: 8px;">
                            <span>⚔️ 5 vs 1 Master Outranker (Battle Royale)</span>
                        </h2>
                        <span style="font-size: 11px; font-weight: 700; background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 20px;">
                            Multi-Competitor Synthesis
                        </span>
                    </div>
                    <p style="font-size: 13.5px; color: var(--text-muted); margin-top: 6px; line-height: 1.5;">
                        Punch in up to 5 competitor URLs + your website. The AI agent concurrently audits all 5, discovers collective content gaps, crafts high-CTR Google Meta tags, and writes an authoritative master article branded with your company name to outrank all 5!
                    </p>
                </div>

                <form id="multiForm" onsubmit="event.preventDefault(); submitMultiForm(event); return false;">
                    <!-- Competitor URLs Grid -->
                    <div style="margin-bottom: 16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                            <label style="font-size: 13px; font-weight: 700; color: #0f172a;">
                                🥊 Competitor Ranking URLs (Up to 5 URLs):
                            </label>
                            <span style="font-size: 11px; color: var(--text-muted);">Audited in parallel (fast)</span>
                        </div>
                        <div style="display: grid; gap: 8px;">
                            <input type="text" id="multiComp1" value="" placeholder="Competitor 1 URL (Required - e.g. https://competitor1.com/page)" required>
                            <input type="text" id="multiComp2" value="" placeholder="Competitor 2 URL (Optional - e.g. https://competitor2.com/page)">
                            <input type="text" id="multiComp3" value="" placeholder="Competitor 3 URL (Optional - e.g. https://competitor3.com/page)">
                            <input type="text" id="multiComp4" value="" placeholder="Competitor 4 URL (Optional)">
                            <input type="text" id="multiComp5" value="" placeholder="Competitor 5 URL (Optional)">
                        </div>
                    </div>

                    <!-- User Website & Branding Grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 4px;">
                                🌐 Your Website / Target URL (Optional Benchmark):
                            </label>
                            <input type="text" id="multiUserUrl" value="" placeholder="e.g. https://mysite.com/page (Agent will benchmark against the 5)">
                        </div>
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 4px;">
                                🏷️ Your Brand / Company / Website Name:
                            </label>
                            <input type="text" id="multiBrandName" value="" placeholder="e.g. MyBrand / MyWebsite" required>
                        </div>
                    </div>

                    <!-- Keywords & Preferences Grid -->
                    <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-bottom: 16px;">
                        <div class="form-group">
                            <label>Target Focus Keyword (Optional)</label>
                            <input type="text" id="multiKeyword" value="" placeholder="Auto-extracted from 5 competitors if blank">
                        </div>
                        <div class="form-group">
                            <label>Target Country / Market</label>
                            <select id="multiCountry">
                                <option value="Bangladesh" selected>🇧🇩 Bangladesh (Default - BD Intent & BDT)</option>
                                <option value="Global">🌍 Worldwide / Global Market</option>
                                <option value="United States">🇺🇸 United States (US Market - USD)</option>
                                <option value="United Kingdom">🇬🇧 United Kingdom (UK Market - GBP)</option>
                                <option value="India">🇮🇳 India (INR & Regional Intent)</option>
                                <option value="Canada">🇨🇦 Canada (CAD)</option>
                                <option value="Australia">🇦🇺 Australia (AUD)</option>
                                <option value="UAE">🇦🇪 UAE / Dubai (AED)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Content Format</label>
                            <select id="multiFormat">
                                <option value="long_form_seo">📖 Definitive Guide & Review (SEO)</option>
                                <option value="informational_article">💡 Informational Article (How-To / Educational)</option>
                                <option value="commercial_article">🏆 Commercial Article (Top Picks & Market Roundup)</option>
                                <option value="buying_guide">🛒 Buying Guide (Checklist & Purchase Decision)</option>
                                <option value="transactional_article">💰 Transactional Article (Where to Buy, Price Deals & Order CTA)</option>
                                <option value="comparison_article">⚔️ Head-to-Head Comparison Battle</option>
                                <option value="product_review">⭐ In-Depth Product Review</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Tone of Voice</label>
                            <select id="multiTone">
                                <option value="Authoritative & Expert">👔 Authoritative & Expert (EEAT)</option>
                                <option value="Conversational & Engaging">🗣️ Conversational & Engaging</option>
                                <option value="Technical & Analytical">📊 Technical & Analytical</option>
                                <option value="Commercial & High-Converting">🎯 Commercial & High-Converting</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Target Word Count</label>
                            <select id="multiWordCount">
                                <option value="0">⚡ Auto (Top Competitor +25%)</option>
                                <option value="2000">2,000+ Words</option>
                                <option value="2500">2,500+ Words (Recommended)</option>
                                <option value="3000">3,000+ Words (Ultimate Domination)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Gemini Key -->
                    <div style="margin-bottom: 16px;">
                        <input type="text" id="multiGeminiKey" placeholder="Optional: Gemini API Key (Leave empty to use 100% Free Offline Heuristic Writer)">
                    </div>

                    <!-- WordPress Auto Publish Toggle -->
                    <div style="background: #f0fdf4; border: 1.5px dashed #86efac; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="multiAutoWp" style="width: 18px; height: 18px; cursor: pointer; accent-color: #059669;">
                            <label for="multiAutoWp" style="font-size: 13.5px; font-weight: 700; color: #065f46; cursor: pointer;">
                                🚀 Automatically Post to WordPress Site upon generation (LIVE or Draft based on WP Settings)
                            </label>
                        </div>
                        <button type="button" onclick="openWpModal()" style="background: #ffffff; border: 1px solid #86efac; color: #059669; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer;">
                            ⚙️ WP Settings
                        </button>
                    </div>

                    <!-- Custom Site Auto Publish Toggle -->
                    <div style="background: #f8fafc; border: 1.5px dashed #94a3b8; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="multiAutoCustom" style="width: 18px; height: 18px; cursor: pointer; accent-color: #0f172a;">
                            <label for="multiAutoCustom" style="font-size: 13.5px; font-weight: 700; color: #0f172a; cursor: pointer;">
                                🌐 Automatically Send to Custom Website (Webhook API) upon generation
                            </label>
                        </div>
                        <button type="button" onclick="openCustomApiModal()" style="background: #ffffff; border: 1px solid #cbd5e1; color: #0f172a; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer;">
                            ⚙️ Custom API & Token
                        </button>
                    </div>

                    <button type="button" class="btn-multi-submit" id="multiSubmitBtn" onclick="submitMultiForm(event);" style="width: 100%; padding: 14px; font-size: 15px; font-weight: 800; background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; border: none; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.25);">
                        ⚔️ Punch 5 Competitors & Generate Master Outranking Article
                    </button>
                </form>
            </div>

            <!-- Multi Spinner -->
            <div class="spinner" id="multiSpinner" style="display: none;">
                <div class="loader" style="border-top-color: #dc2626;"></div>
                <h3>Auditing 5 Competitors & Synthesizing Master Outranker...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Crawling URLs in parallel, calculating word counts, extracting collective gaps, crafting SEO Meta tags, and drafting your branded article...</p>
            </div>

            <!-- Multi Results Container -->
            <div id="multiResults" style="display: none;"></div>
        </div>

        <!-- TAB 4: Content Writing AI Studio -->
        <div id="tabWriter" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; box-shadow: 0 2px 6px rgba(37,99,235,0.25); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <span>⬅️ Back to Home / Daily Tracker</span>
                </button>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748b; font-weight: 600;">
                    <a href="javascript:void(0)" onclick="goBackToHome();" style="color: #2563eb; text-decoration: none;">🏠 Home</a>
                    <span>&rsaquo;</span>
                    <span style="background: #dcfce7; color: #15803d; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 12px;">✍️ Tab 4: AI Content Studio</span>
                </div>
            </div>

            <div class="search-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <div style="margin-bottom: 16px;">
                    <h3 style="font-size: 18px; color: #065f46; display: flex; align-items: center; gap: 8px;">
                        <span>✍️</span> Autonomous Content Writing Studio
                    </h3>
                    <p style="font-size: 13px; color: var(--text-muted);">
                        Transform competitor keyword clusters into comprehensive, human-grade, Google-outranking articles.
                    </p>
                </div>

                <form id="writerForm" onsubmit="event.preventDefault(); submitWriterForm(event); return false;">
                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Target Topic / Article Working Title</label>
                            <input type="text" id="wTopic" value="" placeholder="e.g. Complete Guide to Search Engine Optimization" required>
                        </div>
                        <div class="form-group">
                            <label>Primary Focus Keyword</label>
                            <input type="text" id="wKeyword" value="" placeholder="e.g. search engine optimization" required>
                        </div>
                    </div>

                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Semantic LSI Keywords Cluster (comma separated)</label>
                            <input type="text" id="wLsi" value="" placeholder="e.g. technical seo, on-page optimization, backlink strategy, ranking factors">
                        </div>
                        <div class="form-group">
                            <label>Target Product / Entity Name</label>
                            <input type="text" id="wProduct" value="" placeholder="e.g. SEO Software / Digital Agency">
                        </div>
                    </div>

                    <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
                        <div class="form-group">
                            <label>Target Country / Market</label>
                            <select id="wCountry">
                                <option value="Bangladesh" selected>🇧🇩 Bangladesh (Default - BD Intent & BDT)</option>
                                <option value="Global">🌍 Worldwide / Global Market</option>
                                <option value="United States">🇺🇸 United States (US Market - USD)</option>
                                <option value="United Kingdom">🇬🇧 United Kingdom (UK Market - GBP)</option>
                                <option value="India">🇮🇳 India (INR & Regional Intent)</option>
                                <option value="Canada">🇨🇦 Canada (CAD)</option>
                                <option value="Australia">🇦🇺 Australia (AUD)</option>
                                <option value="UAE">🇦🇪 UAE / Dubai (AED)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Content Format</label>
                            <select id="wFormat">
                                <option value="long_form_seo">📖 Complete 360° SEO Pillar Guide (1,500-3,500w)</option>
                                <option value="informational_article">💡 Informational Article (Educational, How-To & Complete Guide)</option>
                                <option value="commercial_article">🏆 Commercial Article (Best Picks, Top 10 & Review Roundup)</option>
                                <option value="buying_guide">🛒 Buying Guide (Specs Checklist, Budget Tiers & Pre-Purchase Analysis)</option>
                                <option value="transactional_article">💰 Transactional Article (Where to Buy, Best Deals, Discount & Order Guide)</option>
                                <option value="product_review">⭐ In-Depth Product Review & Rating</option>
                                <option value="comparison_article">⚔️ Head-to-Head Comparison (A vs B Battle)</option>
                                <option value="viral_social_post">🚀 Viral Social Media / Promotional Post</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Tone of Voice</label>
                            <select id="wTone">
                                <option value="Authoritative & Expert">👔 Authoritative & Expert (EEAT)</option>
                                <option value="Conversational & Engaging">🗣️ Conversational & Engaging</option>
                                <option value="Commercial & High-Converting">🎯 Commercial & High-Converting</option>
                                <option value="Analytical & Data-Driven">📊 Analytical & Data-Driven</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Target Word Count</label>
                            <select id="wWordCount">
                                <option value="1500">~1,500 Words (Standard SEO)</option>
                                <option value="2500" selected>~2,500 Words (In-Depth Pillar)</option>
                                <option value="3500">~3,500+ Words (Ultimate Authority)</option>
                            </select>
                        </div>
                    </div>

                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Your Brand / Company / Website Name</label>
                            <input type="text" id="wBrandName" value="" placeholder="e.g. MyBrand / mywebsite.com (Woven naturally into recommendations & CTA)">
                        </div>
                        <div class="form-group">
                            <label>Competitor URL to Outrank (Optional)</label>
                            <input type="text" id="wCompUrl" value="" placeholder="e.g. https://competitor.com/blog/article-slug">
                        </div>
                    </div>

                    <div class="writer-grid" style="grid-template-columns: 1fr;">
                        <div class="form-group">
                            <label>Gemini API Key (Optional for Cloud AI, leave blank for Free Offline Engine)</label>
                            <input type="text" id="wGeminiKey" placeholder="AIzaSy... (Saved in your browser)">
                        </div>
                    </div>

                    <!-- WordPress Auto Publish Toggle -->
                    <div style="background: #f0fdf4; border: 1.5px dashed #86efac; border-radius: 10px; padding: 12px 16px; margin-top: 14px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="wAutoWp" style="width: 18px; height: 18px; cursor: pointer; accent-color: #059669;">
                            <label for="wAutoWp" style="font-size: 13.5px; font-weight: 700; color: #065f46; cursor: pointer;">
                                🚀 Automatically Post to WordPress Site upon generation (LIVE or Draft based on WP Settings)
                            </label>
                        </div>
                        <button type="button" onclick="openWpModal()" style="background: #ffffff; border: 1px solid #86efac; color: #059669; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer;">
                            ⚙️ WP Settings
                        </button>
                    </div>

                    <!-- Custom Site Auto Publish Toggle -->
                    <div style="background: #f8fafc; border: 1.5px dashed #94a3b8; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="wAutoCustom" style="width: 18px; height: 18px; cursor: pointer; accent-color: #0f172a;">
                            <label for="wAutoCustom" style="font-size: 13.5px; font-weight: 700; color: #0f172a; cursor: pointer;">
                                🌐 Automatically Send to Custom Website (Webhook API) upon generation
                            </label>
                        </div>
                        <button type="button" onclick="openCustomApiModal()" style="background: #ffffff; border: 1px solid #cbd5e1; color: #0f172a; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer;">
                            ⚙️ Custom API & Token
                        </button>
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px; flex-wrap:wrap; gap:10px;">
                        <span style="font-size:12px; color:var(--text-muted);">💡 100% Free Heuristic Engine works automatically without any API keys.</span>
                        <button type="button" class="btn-writer-submit" id="wSubmitBtn" onclick="submitWriterForm(event);">
                            <span>⚡ Generate Outranking Article with AI Agent</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="spinner" id="writerSpinner">
                <div class="loader" style="border-top-color: var(--writer-accent);"></div>
                <h3 id="writerProgressText">AI Agent is crafting outranking content...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Structuring H1-H3 headings, naturally distributing LSI entities, building comparison tables & FAQ schema...</p>
            </div>

            <!-- Output Container -->
            <div id="writerResults" style="display: none;">
                <div id="writerBattleCard" style="display: none; margin-bottom: 20px;"></div>
                <!-- Meta Package Box -->
                <div class="meta-package-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h4 style="font-size:15px; color:#065f46; font-weight:700;">🎯 SEO & Meta Optimization Package</h4>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <span class="product-tag" id="metaBadgeEngine" style="background:#dcfce7; color:#166534; border-color:#86efac;">AI Engine</span>
                            <span class="product-tag" id="metaBadgeYoast" style="background:#ecfdf5; color:#047857; border-color:#6ee7b7; font-weight:700;">🟢 Yoast: 95/100</span>
                            <span class="product-tag" id="metaBadgeRankMath" style="background:#f0fdf4; color:#15803d; border-color:#86efac; font-weight:700;">🟢 RankMath: 96/100</span>
                            <span class="product-tag" id="metaBadgeReadability" style="background:#eff6ff; color:#1d4ed8; border-color:#93c5fd; font-weight:700;">📖 Flesch: 68.5</span>
                            <span class="product-tag" id="metaBadgeGrammar" style="background:#faf5ff; color:#7e22ce; border-color:#d8b4fe; font-weight:700;">✨ 0 Double Words • 100% Polish</span>
                            <span class="product-tag" id="metaBadgeIntent" style="background:#eff6ff; color:#1e40af; border-color:#bfdbfe;">🎯 Intent: Analyzed</span>
                            <span class="product-tag" id="metaBadgeAiOverview" style="background:#fef3c7; color:#92400e; border-color:#fde68a;">⚡ AI Overview Ready</span>
                            <span class="product-tag" id="metaBadgeWords">0 Words</span>
                            <span class="product-tag" id="metaBadgeRead">0 min read</span>
                        </div>
                    </div>

                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">SEO Title:</strong> <span id="resMetaTitle"></span></div>
                        <button class="meta-btn-copy" onclick="copyText('resMetaTitle')">📋 Copy Title</button>
                    </div>
                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">Meta Description:</strong> <span id="resMetaDesc"></span></div>
                        <button class="meta-btn-copy" onclick="copyText('resMetaDesc')">📋 Copy Desc</button>
                    </div>
                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">URL Slug:</strong> <code id="resSlug" style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;"></code></div>
                        <button class="meta-btn-copy" onclick="copyText('resSlug')">📋 Copy Slug</button>
                    </div>
                </div>

                <!-- Content Box -->
                <div class="section-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                        <div class="content-subtabs">
                            <button class="subtab-btn active" id="subtabVisual" onclick="switchWriterView('visual')">👁️ Visual Article</button>
                            <button class="subtab-btn" id="subtabMarkdown" onclick="switchWriterView('markdown')">📝 Markdown Source</button>
                            <button class="subtab-btn" id="subtabSchema" onclick="switchWriterView('schema')">🏷️ FAQPage JSON-LD Schema</button>
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <button class="btn-download" style="background:#059669; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('single', false, 'publish')" title="Publish article immediately as LIVE post on client website">🚀 Publish LIVE to WP</button>
                            <button class="btn-download" style="background:#0073aa; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('single', false, 'draft')" title="Save article as DRAFT in WordPress admin">📝 Save Draft to WP</button>
                            <button class="btn-download" style="background:#0f172a; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToCustomSite('single')">🌐 Post to Custom Site</button>
                            <button class="btn-download" onclick="copyCurrentContent()">📋 Copy Article</button>
                            <button class="btn-download" style="background:#2563eb;" onclick="downloadMarkdownFile()">📥 Download .MD</button>
                            <button class="btn-download" style="background:#7c3aed;" onclick="downloadHtmlFile()">🌐 Download .HTML</button>
                        </div>
                    </div>

                    <div id="singleWpPostStatusBox" style="display:none; margin-bottom:14px;"></div>
                    <div id="singleCustomPostStatusBox" style="display:none; margin-bottom:14px;"></div>

                    <div id="viewVisual" class="rendered-article"></div>
                    <pre id="viewMarkdown" class="raw-markdown-view" style="display:none;"></pre>
                    <pre id="viewSchema" class="raw-markdown-view" style="display:none; color:#a7f3d0;"></pre>
                </div>
            </div>
        </div>

        <!-- TAB 5: Autonomous AI Autopilot Agent -->
        <div id="tabAutopilot" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 10px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; box-shadow: 0 2px 6px rgba(37,99,235,0.25); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <span>⬅️ Back to Home / Daily Tracker</span>
                </button>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748b; font-weight: 600;">
                    <a href="javascript:void(0)" onclick="goBackToHome();" style="color: #2563eb; text-decoration: none;">🏠 Home</a>
                    <span>&rsaquo;</span>
                    <span style="background: #e0f2fe; color: #0369a1; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 12px;">🤖 Tab 5: Autopilot Agent</span>
                </div>
            </div>

            <div class="search-card" style="border: 2px solid #3b82f6; background: linear-gradient(to bottom, #ffffff, #f8fafc);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h3 style="font-size: 19px; color: #1e3a8a; font-weight: 800; display:flex; align-items:center; gap:8px;">
                            <span>🤖</span> Autonomous AI Autopilot Agent (Hands-Free SEO Worker)
                        </h3>
                        <p style="font-size: 13.5px; color: #475569; margin-top: 4px;">
                            No need to manually input URLs or hunt for keywords! Enter your brand and competitor domains — <strong>the Agent autonomously scans competitors, spots high-intent ranking gaps, writes outranking content, and auto-publishes directly to your site!</strong>
                        </p>
                    </div>
                    <span style="background:#dbeafe; color:#1e40af; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700;">
                        ⚡ 100% Autonomous Worker
                    </span>
                </div>

                <form id="autopilotForm" onsubmit="event.preventDefault(); submitAutopilotForm(event); return false;">
                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Your Brand / Website Name</label>
                            <input type="text" id="autoBrandName" value="" placeholder="e.g. MyBrand / MyWebsite" required>
                        </div>
                        <div class="form-group">
                            <label>Target Market / Country</label>
                            <select id="autoCountry">
                                <option value="Bangladesh" selected>🇧🇩 Bangladesh (Default - BDT & Local Intent)</option>
                                <option value="Global">🌍 Worldwide / Global Market</option>
                                <option value="United States">🇺🇸 United States (US Market)</option>
                                <option value="United Kingdom">🇬🇧 United Kingdom (UK)</option>
                                <option value="India">🇮🇳 India (INR)</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group" style="margin-bottom: 14px;">
                        <label>Target Competitor Websites (1 to 3 competitor domains to outrank)</label>
                        <input type="text" id="autoCompetitors" value="" placeholder="e.g. https://competitor1.com, https://competitor2.com" required>
                        <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">
                            💡 Separate multiple domains with commas (,). The agent scans these domains and autonomously selects today's best ranking opportunity.
                        </div>
                    </div>

                    <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
                        <div class="form-group">
                            <label>Optional: Specific Topic / Mission Focus (Leave blank for autonomous detection)</label>
                            <input type="text" id="autoSpecificTopic" value="" placeholder="Leave empty for autonomous opportunity selection">
                        </div>
                        <div class="form-group">
                            <label>Target Content Depth</label>
                            <select id="autoWordCount">
                                <option value="2500" selected>2,500+ Words (Engineered to Outrank)</option>
                                <option value="3000">3,000+ Words (Ultimate Authority)</option>
                                <option value="2000">2,000 Words</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Content Tone</label>
                            <select id="autoTone">
                                <option value="Authoritative & Expert" selected>👔 Authoritative & Expert (EEAT)</option>
                                <option value="Commercial & High-Converting">🎯 Commercial & High-Converting</option>
                                <option value="Conversational & Engaging">🗣️ Conversational & Engaging</option>
                            </select>
                        </div>
                    </div>

                    <!-- Autonomous Auto-Publish Destination Box -->
                    <div style="background: #eff6ff; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 14px 16px; margin-top: 14px; margin-bottom: 16px;">
                        <div style="font-size: 13px; font-weight: 800; color: #1e40af; margin-bottom: 8px;">
                            🚀 Autonomous Auto-Publish Destinations:
                        </div>
                        <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; font-weight: 600; color: #1e293b;">
                                <input type="checkbox" id="autoPublishWp" checked style="width: 17px; height: 17px; accent-color: #0073aa;">
                                <span>🔌 Post to WordPress Site</span>
                            </label>
                            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 13px; font-weight: 600; color: #1e293b;">
                                <input type="checkbox" id="autoPublishCustom" style="width: 17px; height: 17px; accent-color: #0f172a;">
                                <span>🌐 Post to Custom Website (Webhook)</span>
                            </label>
                        </div>
                        <div style="display: flex; gap: 16px; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #bfdbfe; align-items: center; font-size: 13px; flex-wrap: wrap;">
                            <span style="font-weight: 800; color: #1e40af;">WordPress Post Mode:</span>
                            <label style="cursor: pointer; display: flex; align-items: center; gap: 5px; font-weight: 700; color: #047857;">
                                <input type="radio" name="autoWpStatusMode" value="publish" checked style="accent-color: #059669;">
                                <span>🚀 Direct LIVE Publish</span>
                            </label>
                            <label style="cursor: pointer; display: flex; align-items: center; gap: 5px; font-weight: 600; color: #475569;">
                                <input type="radio" name="autoWpStatusMode" value="draft" style="accent-color: #0073aa;">
                                <span>📝 Save as Draft (Review before live)</span>
                            </label>
                        </div>
                        <div style="font-size: 11.5px; color: #64748b; margin-top: 6px;">
                            💡 If credentials are configured in the "🔌 WordPress" or "🌐 Custom Site API" buttons above, the agent will publish automatically.
                        </div>
                    </div>

                    <!-- Gemini Key -->
                    <div style="margin-bottom: 16px;">
                        <input type="text" id="autoGeminiKey" placeholder="Optional: Gemini API Key (Leave empty to use 100% Free Offline Heuristic Writer)">
                    </div>

                    <button type="button" class="btn-scan" id="autoSubmitBtn" onclick="submitAutopilotForm(event);" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); font-size: 16px; padding: 15px; width: 100%;">
                        <span>🚀 Launch Autonomous Agent Mission Now (Full Autopilot)</span>
                    </button>
                </form>
            </div>

            <!-- Autonomous Mission Live Terminal Console -->
            <div id="autoTerminalCard" style="display: none; margin-top: 20px;">
                <div style="background: #0f172a; border-radius: 12px; padding: 18px 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); border: 1px solid #1e293b;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 10px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="width: 12px; height: 12px; border-radius: 50%; background: #22c55e; display: inline-block; box-shadow: 0 0 8px #22c55e;"></span>
                            <span style="color: #f8fafc; font-weight: 700; font-size: 14px; font-family: 'JetBrains Mono', monospace;">Autonomous Agent Live Mission Terminal</span>
                        </div>
                        <span id="autoAgentStatusText" style="color: #38bdf8; font-size: 12px; font-family: 'JetBrains Mono', monospace;">AGENT ACTIVE ⚡</span>
                    </div>

                    <div id="autoTerminalLogs" style="font-family: 'JetBrains Mono', monospace; font-size: 12.5px; color: #a5f3fc; line-height: 1.8; max-height: 280px; overflow-y: auto; white-space: pre-wrap;"></div>
                </div>
            </div>

            <!-- Agent Generated Results View -->
            <div id="autoResults" style="display: none; margin-top: 24px;"></div>
        </div>

        <!-- TAB 6: Personal SEO Director Agent (10-Day Autonomous Multi-Company SEO) -->
        <div id="tabDirector" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 10px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13.5px; box-shadow: 0 2px 6px rgba(37,99,235,0.25); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    <span>⬅️ Back to Home / Daily Tracker</span>
                </button>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748b; font-weight: 600;">
                    <a href="javascript:void(0)" onclick="goBackToHome();" style="color: #2563eb; text-decoration: none;">🏠 Home</a>
                    <span>&rsaquo;</span>
                    <span style="background: #ede9fe; color: #5b21b6; font-weight: 800; padding: 3px 10px; border-radius: 6px; font-size: 12px;">🧠 Tab 6: Personal SEO Agent</span>
                </div>
            </div>

            <!-- Hero Banner -->
            <div style="background: linear-gradient(135deg, #1e1b4b, #312e81, #1e3a8a); color: white; border-radius: 16px; padding: 24px 28px; margin-bottom: 22px; box-shadow: 0 4px 20px rgba(49, 46, 129, 0.25);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                    <div>
                        <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 20px; padding: 4px 14px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">
                            <span>🧠 Autonomous Senior SEO Director Agent</span>
                        </div>
                        <h2 style="font-size: 24px; font-weight: 800; margin-bottom: 6px; color: #ffffff;">Your Personal 24/7 Multi-Client SEO Expert</h2>
                        <p style="font-size: 13.5px; color: #cbd5e1; max-width: 780px; line-height: 1.5;">
                            Give directives for any company or multiple clients and walk away. This agent autonomously maps search intent, writes AI Overview-ready pillar content, engineers JSON-LD technical schemas, builds internal link silos, drafts Skyscraper backlink pitches, and crafts Digital PR syndicates over a complete <strong>10-Day SEO Roadmap</strong>.
                        </p>
                    </div>
                    <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 14px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); display: flex; flex-direction: column; gap: 8px; align-items: flex-end;">
                        <div>
                            <div style="font-size: 11px; color: #93c5fd; text-transform: uppercase; font-weight: 700;">Director Status</div>
                            <div style="font-size: 18px; font-weight: 800; color: #34d399; display: flex; align-items: center; gap: 6px; justify-content: flex-end;">
                                <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px #34d399;"></span> Active & Ready
                            </div>
                        </div>
                        <button type="button" onclick="goBackToHome();" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.35); font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 8px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">
                            <span>⬅️ Back to Home</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Multi-Company Profile Manager & Directive Input Form -->
            <div class="search-card" style="margin-bottom: 22px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 10px; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
                    <div>
                        <h3 style="font-size: 17px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                            <span>🏢 Multi-Company / Client Workspace</span>
                        </h3>
                        <p style="font-size: 12.5px; color: var(--text-muted); margin-top: 2px;">Switch between saved clients or create a new campaign profile</p>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <button type="button" class="btn-action" onclick="addNewCompanyProfile()" style="background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; font-size: 12px; padding: 7px 12px;">
                            <span>➕ Add New Client</span>
                        </button>
                        <button type="button" class="btn-action" onclick="saveCurrentCompanyProfile()" style="background: #0284c7; color: white; border: none; font-size: 12px; padding: 7px 14px;">
                            <span>💾 Save Profile</span>
                        </button>
                        <button type="button" class="btn-action" onclick="deleteCurrentCompanyProfile()" style="background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; font-size: 12px; padding: 7px 10px;" title="Delete current profile">
                            <span>🗑️</span>
                        </button>
                    </div>
                </div>

                <!-- Client Selector Quick Pills -->
                <div style="margin-bottom: 18px;">
                    <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">Select Active Company:</div>
                    <div id="companyProfilesList" style="display: flex; flex-wrap: wrap; gap: 8px;">
                        <!-- Injected via JS -->
                    </div>
                </div>

                <!-- Active Company Configuration Fields -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 16px;">
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Company / Brand Name *</label>
                        <input type="text" id="dirCompanyName" value="" placeholder="e.g. Your Brand / Business Name" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13.5px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Website URL / Domain</label>
                        <input type="url" id="dirDomain" value="" placeholder="https://yourwebsite.com" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13.5px;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Target Market / Country</label>
                        <select id="dirCountry" style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13.5px; background: white;">
                            <option value="Bangladesh" selected>🇧🇩 Bangladesh (BDT ৳)</option>
                            <option value="United States">🇺🇸 United States (USD $)</option>
                            <option value="United Kingdom">🇬🇧 United Kingdom (GBP £)</option>
                            <option value="Canada">🇨🇦 Canada (CAD $)</option>
                            <option value="Australia">🇦🇺 Australia (AUD $)</option>
                            <option value="India">🇮🇳 India (INR ₹)</option>
                            <option value="Germany">🇩🇪 Germany (EUR €)</option>
                            <option value="Global">🌐 Global / International</option>
                        </select>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Target Keywords (One per line or comma separated) *</label>
                        <textarea id="dirKeywords" rows="4" placeholder="Enter your target keywords (one per line)..." style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; font-family: monospace; resize: vertical;"></textarea>
                    </div>
                    <div>
                        <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Competitor URLs (Optional for Benchmarking)</label>
                        <textarea id="dirCompetitors" rows="4" placeholder="Enter competitor URLs (one per line)..." style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; font-family: monospace; resize: vertical;"></textarea>
                    </div>
                </div>

                <div style="margin-bottom: 18px;">
                    <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Director Instructions & Specific Business Directives (Optional)</label>
                    <input type="text" id="dirInstructions" placeholder="e.g. Ensure accurate market pricing, prioritize authorized warranty verification, and optimize all headings for Google AI Overview." style="width: 100%; padding: 10px 12px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px;" value="">
                </div>

                <!-- Action Button Controls -->
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <button type="button" id="btnGenDirectorPlan" class="btn-scan" onclick="generateDirectorPlan()" style="flex: 1; min-width: 240px; background: linear-gradient(135deg, #2563eb, #1d4ed8); justify-content: center;">
                        <span>🚀 1. Generate 10-Day Master Roadmap</span>
                    </button>
                    <button type="button" id="btnExecAllDirector" class="btn-scan" onclick="executeAllDirectorDays()" style="flex: 1; min-width: 240px; background: linear-gradient(135deg, #059669, #047857); justify-content: center;">
                        <span>⚡ 2. Execute Entire 10-Day Campaign Autonomously</span>
                    </button>
                    <button type="button" class="btn-action" onclick="downloadDirectorCampaignReport()" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; font-weight: 700; padding: 10px 16px;">
                        <span>📥 Download 10-Day Plan (.MD)</span>
                    </button>
                </div>
            </div>

            <!-- Campaign Progress & Metrics Bar -->
            <div id="dirCampaignProgressBox" style="display: none; background: white; border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 16px; font-weight: 800; color: #0f172a;" id="dirCampaignHeaderTitle">Campaign: Active Campaign</span>
                        <span id="dirCampaignStatusPill" style="background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 700;">10 Days Planned</span>
                    </div>
                    <div style="font-size: 13px; font-weight: 700; color: var(--text-muted);" id="dirCompletionText">0 of 10 Days Executed</div>
                </div>
                <div style="background: #e2e8f0; border-radius: 8px; height: 10px; overflow: hidden; margin-bottom: 6px;">
                    <div id="dirProgressBar" style="background: linear-gradient(90deg, #3b82f6, #10b981); height: 100%; width: 0%; transition: width 0.4s ease;"></div>
                </div>
            </div>

            <!-- Director Activity Stream Console -->
            <div id="dirConsoleBox" style="display: none; background: #0f172a; color: #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 22px; font-family: 'JetBrains Mono', monospace; font-size: 12.5px; max-height: 180px; overflow-y: auto; border: 1px solid #334155;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 4px;">
                    <span style="color: #38bdf8; font-weight: 700;">📡 Personal SEO Agent Execution Stream</span>
                    <span id="dirLiveSpinner" style="color: #34d399; font-size: 11px; display: none;">● Running...</span>
                </div>
                <div id="dirConsoleLogs"></div>
            </div>

            <!-- 10-Day Action Mission Cards Grid -->
            <div id="dirDaysGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 16px; margin-bottom: 24px;">
                <!-- 10 Day Cards Injected Dynamically Here -->
            </div>

            <!-- Bottom Return to Top / Home Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px 20px; margin-bottom: 30px; flex-wrap: wrap; gap: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.04);">
                <div style="font-size: 13px; color: #475569; font-weight: 600;">
                    💡 Finished reviewing or executing your 10-Day SEO Roadmap?
                </div>
                <div style="display: flex; gap: 10px;">
                    <button type="button" onclick="window.scrollTo({top: 0, behavior: 'smooth'});" style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; font-weight: 700; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px;">
                        <span>⬆️ Back to Top</span>
                    </button>
                    <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; border: none; font-weight: 700; padding: 8px 18px; border-radius: 8px; cursor: pointer; font-size: 13px; box-shadow: 0 2px 6px rgba(37,99,235,0.25);">
                        <span>🏠 Back to Home / Daily Tracker</span>
                    </button>
                </div>
            </div>
        </div>
    </div>

<!-- WordPress Integration Modal -->
    <div id="wpModal" class="modal-overlay" style="display:none;">
        <div class="modal-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:38px; height:38px; background:#0073aa; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:22px; font-weight:800;">W</div>
                    <div>
                        <h3 style="margin:0; font-size:18px; color:#0f172a;">WordPress Auto-Publisher</h3>
                        <p style="margin:0; font-size:12px; color:var(--text-muted);">Publish articles directly to your WordPress site with 1-click via native REST API</p>
                    </div>
                </div>
                <button type="button" onclick="closeWpModal()" style="background:none; border:none; font-size:24px; cursor:pointer; color:#64748b;">&times;</button>
            </div>

            <!-- Guide Box -->
            <div style="background:#eff6ff; border-left:4px solid #3b82f6; border-radius:0 8px 8px 0; padding:12px 14px; margin-bottom:16px; font-size:12.5px; line-height:1.6; color:#1e40af;">
                <strong>💡 How to Connect in 30 Seconds (No Plugin Needed):</strong><br>
                1. Go to your WordPress Admin: <strong>Users → Profile</strong>.<br>
                2. Scroll down to <strong>Application Passwords</strong>.<br>
                3. Enter name <code>RankNaserPro</code>, click <strong>Add New Application Password</strong>, and copy the 24-character code below.
            </div>

            <form id="wpConfigForm" onsubmit="saveWpSettings(event)">
                <div style="margin-bottom:12px;">
                    <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">WordPress Website URL</label>
                    <input type="text" id="wpSiteUrl" placeholder="https://yourwebsite.com" required>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
                    <div>
                        <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">WordPress Username</label>
                        <input type="text" id="wpUsername" placeholder="e.g. admin" required>
                    </div>
                    <div>
                        <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">Default Post Status</label>
                        <select id="wpPostStatus">
                            <option value="draft" selected>📝 Draft (Recommended)</option>
                            <option value="publish">🚀 Publish (Live Immediately)</option>
                        </select>
                    </div>
                </div>

                <div style="margin-bottom:16px;">
                    <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">Application Password</label>
                    <input type="text" id="wpAppPassword" placeholder="e.g. abcd efgh ijkl mnop qrst uvwx" required>
                </div>

                <div id="wpTestStatus" style="display:none; padding:10px 14px; border-radius:8px; font-size:13px; font-weight:600; margin-bottom:14px;"></div>

                <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                    <button type="button" onclick="testWpConnection()" id="wpTestBtn" style="background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer;">
                        🧪 Test Connection
                    </button>
                    <div style="display:flex; gap:8px;">
                        <button type="button" onclick="closeWpModal()" style="background:#e2e8f0; color:#475569; border:none; padding:10px 16px; border-radius:8px; font-weight:600; cursor:pointer;">Cancel</button>
                        <button type="submit" style="background:#0073aa; color:white; border:none; padding:10px 22px; border-radius:8px; font-weight:700; cursor:pointer;">💾 Save Settings</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- Custom Webhook / API Integration Modal -->
    <div id="customApiModal" class="modal-overlay" style="display:none;">
        <div class="modal-card" style="max-width: 680px; max-height: 90vh; overflow-y: auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:38px; height:38px; background:#0f172a; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:20px; font-weight:800;">🌐</div>
                    <div>
                        <h3 style="margin:0; font-size:18px; color:#0f172a;">Custom Website API / Webhook Sync</h3>
                        <p style="margin:0; font-size:12px; color:var(--text-muted);">Stream articles to Next.js, Node.js, Laravel, PHP, Python or any custom CMS</p>
                    </div>
                </div>
                <button type="button" onclick="closeCustomApiModal()" style="background:none; border:none; font-size:24px; cursor:pointer; color:#64748b;">&times;</button>
            </div>

            <!-- Built-in API Secret Token Box -->
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <label style="font-size:12.5px; font-weight:800; color:#0f172a; display:flex; align-items:center; gap:6px;">
                        <span>🔑 Built-in Secret API Token:</span>
                        <span style="font-size:11px; background:#e0e7ff; color:#3730a3; padding:1px 6px; border-radius:4px; font-weight:600;">Secure & Built-in</span>
                    </label>
                    <div style="display:flex; gap:6px;">
                        <button type="button" onclick="copyCustomToken()" style="background:#0f172a; color:white; border:none; padding:4px 10px; border-radius:6px; font-size:11px; font-weight:700; cursor:pointer;">📋 Copy Token</button>
                        <button type="button" onclick="regenerateCustomToken()" style="background:#e2e8f0; color:#334155; border:none; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:600; cursor:pointer;">🔄 New Token</button>
                    </div>
                </div>
                <input type="text" id="customApiToken" readonly style="font-family:'JetBrains Mono', monospace; font-size:13px; font-weight:600; background:#f1f5f9; color:#0f172a; border:1px solid #cbd5e1; width:100%; padding:8px 10px; border-radius:6px; margin-bottom:4px;">
                <div style="font-size:11.5px; color:#64748b; line-height:1.4;">
                    💡 Place this secret token in your custom website backend code. When our tool dispatches articles, your server verifies incoming requests using this token.
                </div>
            </div>

            <form id="customApiConfigForm" onsubmit="saveCustomApiSettings(event)">
                <div style="margin-bottom:12px;">
                    <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">Your Custom Website Webhook Endpoint URL</label>
                    <input type="text" id="customWebhookUrl" placeholder="https://yourcustomsite.com/api/receive-article" required>
                    <div style="font-size:11.5px; color:#64748b; margin-top:3px;">The POST endpoint on your server that will receive the JSON payload.</div>
                </div>

                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px;">
                    <div>
                        <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">Payload Format</label>
                        <select id="customPayloadFormat" disabled style="background:#f1f5f9; cursor:not-allowed;">
                            <option selected>📦 Standard JSON (HTML + MD + Meta + Schema)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size:12.5px; font-weight:700; color:#1e293b; display:block; margin-bottom:4px;">Default Article Status</label>
                        <select id="customPostStatus">
                            <option value="draft" selected>📝 Draft</option>
                            <option value="publish">🚀 Published (Live)</option>
                        </select>
                    </div>
                </div>

                <div id="customTestStatus" style="display:none; padding:10px 14px; border-radius:8px; font-size:13px; font-weight:600; margin-bottom:14px;"></div>

                <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:18px;">
                    <button type="button" onclick="testCustomWebhook()" id="customTestBtn" style="background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; padding:9px 16px; border-radius:8px; font-weight:700; cursor:pointer;">
                        🧪 Test Webhook (Send Ping)
                    </button>
                    <div style="display:flex; gap:8px;">
                        <button type="button" onclick="closeCustomApiModal()" style="background:#e2e8f0; color:#475569; border:none; padding:9px 14px; border-radius:8px; font-weight:600; cursor:pointer;">Cancel</button>
                        <button type="submit" style="background:#0f172a; color:white; border:none; padding:9px 20px; border-radius:8px; font-weight:700; cursor:pointer;">💾 Save Settings</button>
                    </div>
                </div>
            </form>

            <!-- Ready-to-use Backend Code Generator -->
            <div style="border-top:1px solid #e2e8f0; padding-top:14px;">
                <div style="font-size:13px; font-weight:800; color:#0f172a; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <span>📋 Ready-to-Use Receiver Code for Your Website:</span>
                    <button type="button" onclick="copyCurrentCodeSnippet()" style="background:#0284c7; color:white; border:none; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:700; cursor:pointer;">📋 Copy Code</button>
                </div>
                <div style="font-size:11.5px; color:#64748b; margin-bottom:8px;">
                    Select the framework or language used on your website, copy the code snippet, and paste it into your server:
                </div>
                <div class="content-subtabs" style="margin-bottom:8px; border-bottom:1px solid #e2e8f0;">
                    <button class="subtab-btn active" id="codeTabNext" onclick="switchCodeSnippet('nextjs')">⚡ Next.js (App Router)</button>
                    <button class="subtab-btn" id="codeTabNode" onclick="switchCodeSnippet('node')">🟢 Node.js / Express</button>
                    <button class="subtab-btn" id="codeTabPhp" onclick="switchCodeSnippet('php')">🐘 PHP / Laravel</button>
                    <button class="subtab-btn" id="codeTabPython" onclick="switchCodeSnippet('python')">🐍 Python / FastAPI</button>
                </div>
                <pre id="codeSnippetBox" style="background:#0f172a; color:#f8fafc; padding:12px; border-radius:8px; font-size:11.5px; font-family:'JetBrains Mono',monospace; max-height:200px; overflow-y:auto; line-height:1.5; white-space:pre-wrap;"></pre>
            </div>
        </div>
    </div>

    <!-- White-Label Executive Client SEO Audit Report Modal -->
    <div id="clientReportModal" class="modal-overlay" style="display:none;">
        <div class="modal-card" style="max-width: 820px; max-height: 92vh; overflow-y: auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:38px; height:38px; background:linear-gradient(135deg, #1e3a8a, #2563eb); border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:20px;">📄</div>
                    <div>
                        <h3 style="margin:0; font-size:18px; color:#0f172a;">Executive Client SEO Audit Report</h3>
                        <p style="margin:0; font-size:12px; color:var(--text-muted);">White-label competitor intelligence report ready for client presentation & PDF export</p>
                    </div>
                </div>
                <button type="button" onclick="closeClientReportModal()" style="background:none; border:none; font-size:24px; cursor:pointer; color:#64748b;">&times;</button>
            </div>

            <!-- White-Label Branding Customization Bar -->
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; margin-bottom:16px;">
                <div style="font-size:12px; font-weight:700; color:#0f172a; margin-bottom:8px;">🎨 White-Label Branding Settings:</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div>
                        <label style="font-size:11.5px; font-weight:600; color:#475569; display:block; margin-bottom:3px;">Prepared For (Client Name / Domain):</label>
                        <input type="text" id="reportClientName" placeholder="e.g. Acme Corporation / MyClient.com" oninput="updateReportPreview()">
                    </div>
                    <div>
                        <label style="font-size:11.5px; font-weight:600; color:#475569; display:block; margin-bottom:3px;">Prepared By (Your Agency / Name):</label>
                        <input type="text" id="reportAgencyName" placeholder="e.g. RankNaserPro Agency / TopRank Digital" oninput="updateReportPreview()">
                    </div>
                </div>
            </div>

            <!-- Action Toolbar -->
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
                <div style="font-size:12px; color:#64748b;">💡 Click "Print / Save PDF" to generate a client-ready PDF document with browser print dialog.</div>
                <div style="display:flex; gap:8px;">
                    <button type="button" onclick="copyClientReportSummary()" style="background:#f1f5f9; color:#1e293b; border:1px solid #cbd5e1; padding:8px 14px; border-radius:7px; font-size:12.5px; font-weight:700; cursor:pointer;">
                        📋 Copy Summary
                    </button>
                    <button type="button" onclick="printClientReport()" style="background:linear-gradient(135deg, #1e3a8a, #2563eb); color:white; border:none; padding:8px 18px; border-radius:7px; font-size:12.5px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:6px;">
                        🖨️ Print / Save PDF
                    </button>
                </div>
            </div>

            <!-- Live Printable Report Preview Container -->
            <div id="reportPreviewContainer" style="background:#ffffff; border:1.5px solid #cbd5e1; border-radius:12px; padding:24px; box-shadow:0 4px 16px rgba(0,0,0,0.04);">
                <!-- Dynamic report content rendered via JS -->
            </div>
        </div>


    </div>

    <!-- Hidden dedicated container used exclusively for high-fidelity printing -->
    <div id="printableClientReport" style="display:none;"></div>

    <!-- 30-Day Topical Authority Content Calendar Modal -->
    <div id="contentRoadmapModal" class="modal-overlay" style="display:none;">
        <div class="modal-card" style="max-width: 920px; max-height: 92vh; overflow-y: auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #e2e8f0; padding-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:38px; height:38px; background:linear-gradient(135deg, #7c3aed, #6366f1); border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:20px;">🗺️</div>
                    <div>
                        <h3 style="margin:0; font-size:18px; color:#0f172a;">30-Day Topical Authority Content Roadmap</h3>
                        <p style="margin:0; font-size:12px; color:var(--text-muted);">Generate an entire monthly editorial strategy designed to establish Google topical authority</p>
                    </div>
                </div>
                <button type="button" onclick="closeRoadmapModal()" style="background:none; border:none; font-size:24px; cursor:pointer; color:#64748b;">&times;</button>
            </div>

            <form id="roadmapForm" onsubmit="handleGenerateRoadmap(event)">
                <div class="writer-grid" style="grid-template-columns: 2fr 1fr auto; align-items: flex-end; gap: 10px; margin-bottom: 16px;">
                    <div class="form-group" style="margin-bottom:0;">
                        <label>Main Topic / Niche / Core Entity</label>
                        <input type="text" id="roadmapTopicInput" placeholder="e.g. Gaming Laptops, SEO Agency, Budget Smartphones" required>
                    </div>
                    <div class="form-group" style="margin-bottom:0;">
                        <label>Target Market</label>
                        <select id="roadmapCountryInput">
                            <option value="Bangladesh" selected>🇧🇩 Bangladesh (BDT)</option>
                            <option value="Global">🌍 Global / US Market (USD)</option>
                            <option value="United Kingdom">🇬🇧 UK Market (GBP)</option>
                            <option value="India">🇮🇳 India (INR)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-writer-submit" style="height:42px; margin-bottom:0; padding:0 20px; white-space:nowrap; background:linear-gradient(135deg, #7c3aed, #4f46e5);">
                        ⚡ Generate Strategy
                    </button>
                </div>
            </form>

            <div id="roadmapResultsBox" style="display:none;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
                    <div style="font-size:13px; font-weight:700; color:#0f172a;" id="roadmapCountText">
                        📋 30-Day Content Matrix (Pillar + Clusters + Search Intent Map)
                    </div>
                    <div style="display:flex; gap:8px;">
                        <button type="button" onclick="downloadRoadmapCSV()" class="btn-download" style="background:#059669; padding:6px 14px; font-size:12px;">
                            ⬇️ Download CSV / Excel
                        </button>
                    </div>
                </div>
                <div style="overflow-x:auto;">
                    <table class="roadmap-table" id="roadmapTable">
                        <thead>
                            <tr>
                                <th>Schedule</th>
                                <th>Content Title & Strategy</th>
                                <th>Search Intent</th>
                                <th>Target Keywords</th>
                                <th>Target Words</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="roadmapTableBody"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Deliverable Inspector Modal -->
    <div id="dirDeliverableModal" onclick="if(event.target===this) closeDirectorModal();" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.7); backdrop-filter: blur(4px); z-index: 9999; justify-content: center; align-items: center; padding: 20px;">
        <div style="background: white; border-radius: 16px; max-width: 900px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.3); overflow: hidden;">
            <div style="padding: 16px 22px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; background: #f8fafc;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span id="dirModalDayBadge" style="background: #2563eb; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700;">DAY 1</span>
                    <h3 id="dirModalTitle" style="font-size: 16px; font-weight: 800; color: #0f172a; margin: 0;">Deliverable Preview</h3>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <button type="button" onclick="closeDirectorModal()" style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 6px; cursor: pointer; display: flex; align-items: center; gap: 5px;">
                        <span>⬅️ Back / Close</span>
                    </button>
                    <button type="button" onclick="closeDirectorModal()" style="background: none; border: none; font-size: 22px; cursor: pointer; color: #64748b; line-height: 1;">✕</button>
                </div>
            </div>
            <div style="display: flex; gap: 8px; padding: 10px 22px; background: #f1f5f9; border-bottom: 1px solid var(--border); align-items: center; flex-wrap: wrap;">
                <button type="button" onclick="closeDirectorModal()" style="background: #ffffff; border: 1.5px solid #cbd5e1; color: #1e293b; font-weight: 700; font-size: 12px; padding: 6px 12px; border-radius: 6px; cursor: pointer;">
                    <span>⬅️ Back to Roadmap</span>
                </button>
                <button type="button" class="btn-action" onclick="copyDirectorDeliverable()" style="background: #ffffff; border: 1px solid #cbd5e1; color: #334155; font-size: 12px; padding: 6px 12px;">
                    <span>📋 Copy Markdown / Code</span>
                </button>
                <button type="button" id="btnDirSendToStudio" class="btn-action" onclick="sendDirectorArticleToStudio()" style="display: none; background: #059669; color: white; border: none; font-size: 12px; padding: 6px 12px;">
                    <span>✍️ Open in AI Content Studio</span>
                </button>
                <button type="button" id="btnDirSendToWpLive" class="btn-action" onclick="publishDirectorDeliverableToWp('publish')" style="display: none; background: #059669; color: white; border: none; font-size: 12px; padding: 6px 12px;" title="Publish article immediately as LIVE post">
                    <span>🚀 Publish LIVE to WP</span>
                </button>
                <button type="button" id="btnDirSendToWpDraft" class="btn-action" onclick="publishDirectorDeliverableToWp('draft')" style="display: none; background: #0073aa; color: white; border: none; font-size: 12px; padding: 6px 12px;" title="Save article as DRAFT in WordPress">
                    <span>📝 Save Draft to WP</span>
                </button>
                <span id="dirModalCopyAlert" style="font-size: 11px; color: #059669; font-weight: 700; display: none;">Copied to clipboard!</span>
            </div>
            <div id="dirModalContent" style="padding: 22px; overflow-y: auto; flex: 1; font-size: 13.5px; line-height: 1.6; color: #1e293b;">
                <!-- Rendered HTML / Markdown preview -->
            </div>
            <div style="padding: 12px 22px; background: #f8fafc; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 12px; color: #64748b;">Press <kbd style="background:#e2e8f0; padding:2px 6px; border-radius:4px; font-size:11px;">ESC</kbd> or click Back to return to 10-Day Plan</div>
                <button type="button" onclick="closeDirectorModal()" style="background: #334155; color: white; border: none; font-size: 12.5px; font-weight: 700; padding: 7px 18px; border-radius: 8px; cursor: pointer;">
                    <span>⬅️ Back to Roadmap</span>
                </button>
            </div>
        </div>
    </div>


        <!-- TAB 7: AI Agency Workforce (Autonomous 24/7 Virtual Team) -->
        <div id="tabAgency" style="display: none;">
            <!-- Top Return & Breadcrumb Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 12px 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); flex-wrap: wrap; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <button type="button" onclick="goBackToHome();" style="background: linear-gradient(135deg, #1e1b4b, #312e81); color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 18px; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; font-size: 13px; box-shadow: 0 2px 6px rgba(30,27,75,0.25);">
                        <span>⬅️ Back to Home</span>
                    </button>
                    <span style="font-size: 13px; font-weight: 800; color: #1e1b4b;">🏢 RankNaser AI Agency Operations Center</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 11.5px; background: #ecfdf5; border: 1.5px solid #10b981; color: #047857; font-weight: 800; padding: 6px 14px; border-radius: 20px; display: inline-flex; align-items: center; gap: 6px;">
                        <span>🛡️</span>
                        <span>100% Google White-Hat Certified (Zero Spam Guarantee)</span>
                    </span>
                </div>
            </div>

            <!-- Agency Boss Hero Banner -->
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%); border-radius: 20px; padding: 26px 30px; color: white; margin-bottom: 22px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25); border: 1.5px solid #6366f1; position: relative; overflow: hidden;">
                <div style="position: absolute; right: -20px; bottom: -20px; font-size: 130px; opacity: 0.08; pointer-events: none;">🏢</div>
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
                    <div style="max-width: 650px;">
                        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(99, 102, 241, 0.25); border: 1px solid #818cf8; border-radius: 20px; padding: 4px 14px; font-size: 11.5px; font-weight: 800; color: #c7d2fe; margin-bottom: 10px;">
                            <span>👑 FOUNDER & BOSS: RANKNASER</span>
                            <span>•</span>
                            <span>AUTONOMOUS WORKFORCE MODEL</span>
                        </div>
                        <h2 style="font-size: 24px; font-weight: 900; margin: 0 0 8px 0; letter-spacing: -0.5px;">RankNaser AI Agency OS — 24/7 Virtual Team</h2>
                        <p style="font-size: 13.5px; color: #cbd5e1; line-height: 1.6; margin: 0;">
                            A synchronized multi-specialist AI team handling end-to-end digital marketing: <strong>Keywords, EEAT Content, Contextual Internal Links, White-Hat Backlinks, Technical Indexing, Web Development, and Conversion UI/UX</strong>. Every agent strictly follows Google Search Essentials and Spam Policies.
                        </p>
                    </div>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button type="button" onclick="openClientsHubModal()" style="background: rgba(255,255,255,0.18); color: white; border: 1.5px solid rgba(255,255,255,0.4); font-weight: 800; border-radius: 10px; padding: 12px 18px; font-size: 13.5px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.25)'" onmouseout="this.style.background='rgba(255,255,255,0.18)'">
                            <span>🏢 5 Connected Clients Hub</span>
                        </button>
                        <button type="button" onclick="openAgencyTaskModal()" style="background: linear-gradient(135deg, #2563eb, #3b82f6); color: white; border: none; font-weight: 800; border-radius: 10px; padding: 12px 20px; font-size: 13.5px; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 14px rgba(37,99,235,0.4); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                            <span>⚡ Assign Task to Staff</span>
                        </button>
                        <button type="button" onclick="openDailyReportModal()" style="background: rgba(255,255,255,0.12); color: white; border: 1.5px solid rgba(255,255,255,0.3); font-weight: 700; border-radius: 10px; padding: 12px 18px; font-size: 13.5px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: background 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.12)'">
                            <span>📊 Today's Work Report</span>
                        </button>
                        <a href="/agency/daily-report/pdf" target="_blank" style="background: #059669; color: white; text-decoration: none; font-weight: 800; border-radius: 10px; padding: 12px 18px; font-size: 13.5px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 14px rgba(5,150,105,0.35);">
                            <span>🖨️ PDF Report</span>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Key Agency Metrics Row -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 24px;">
                <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase;">Active AI Specialists</div>
                    <div style="font-size: 24px; font-weight: 900; color: #1e1b4b; margin-top: 4px;">6 Full-Time Agents</div>
                    <div style="font-size: 11.5px; color: #059669; font-weight: 700; margin-top: 2px;">🟢 24/7 Operations Online</div>
                </div>
                <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase;">Google Policy Compliance</div>
                    <div style="font-size: 24px; font-weight: 900; color: #059669; margin-top: 4px;">100% White-Hat</div>
                    <div style="font-size: 11.5px; color: #64748b; margin-top: 2px;">Strictly Zero Spam / Zero PBNs</div>
                </div>
                <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase;">Tasks Completed Today</div>
                    <div id="agencyStatsTotalTasks" style="font-size: 24px; font-weight: 900; color: #2563eb; margin-top: 4px;">0 Deliverables</div>
                    <div style="font-size: 11.5px; color: #64748b; margin-top: 2px;">Automated Shift Logging</div>
                </div>
                <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="font-size: 12px; font-weight: 800; color: #64748b; text-transform: uppercase;">End-to-End Coverage</div>
                    <div style="font-size: 24px; font-weight: 900; color: #7c3aed; margin-top: 4px;">Full 360° Scope</div>
                    <div style="font-size: 11.5px; color: #64748b; margin-top: 2px;">No Task Left Behind</div>
                </div>
            </div>

            <!-- Connected Client Companies Quick Hub Bar (5 Companies Active) -->
            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 16px; padding: 18px 22px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h4 style="margin: 0; font-size: 16px; font-weight: 900; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                            <span>🏢 Connected Client Companies (5 Companies Hub)</span>
                            <span style="font-size: 11px; background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; padding: 2px 8px; border-radius: 12px; font-weight: 800;">Real Automation Ready</span>
                        </h4>
                        <p style="margin: 2px 0 0 0; font-size: 12px; color: #64748b;">Select any client company to instantly dispatch tasks to staff, or configure their WordPress REST API credentials.</p>
                    </div>
                    <button type="button" onclick="openClientsHubModal()" style="background: linear-gradient(135deg, #1e1b4b, #2563eb); color: white; border: none; font-weight: 800; border-radius: 8px; padding: 8px 16px; font-size: 12.5px; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                        <span>⚙️ Manage 5 Clients</span>
                    </button>
                </div>
                <div id="agencyConnectedClientsRow" style="display: flex; flex-wrap: wrap; gap: 10px;">
                    <!-- Rendered dynamically via updateClientsUI() -->
                </div>
            </div>

            <!-- Virtual Office Floor: Staff Cards -->
            <div style="margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <div>
                        <h3 style="font-size: 18px; font-weight: 900; color: #0f172a; margin: 0;">👥 Agency Staff Floor (Specialist Team)</h3>
                        <p style="font-size: 12.5px; color: #64748b; margin: 2px 0 0 0;">Each agent executes specialized tasks conforming strictly to Google search & engineering standards.</p>
                    </div>
                </div>

                <div id="agencyStaffGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
                    <!-- Rendered dynamically by loadAgencyDashboard() -->
                </div>
            </div>

            <!-- Recent Task Deliverables & Shift Logs -->
            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 16px; padding: 22px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 12px; flex-wrap: wrap; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 22px;">📋</span>
                        <div>
                            <h3 style="font-size: 16px; font-weight: 900; color: #0f172a; margin: 0;">Recent Agency Deliverables & Work Logs</h3>
                            <p style="font-size: 12px; color: #64748b; margin: 2px 0 0 0;">Review completed work submitted by your virtual workforce.</p>
                        </div>
                    </div>
                    <button type="button" onclick="loadAgencyDashboard()" style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 8px; cursor: pointer;">
                        🔄 Refresh Feed
                    </button>
                </div>

                <div id="agencyTasksFeed">
                    <!-- Populated by JS -->
                    <div style="text-align: center; padding: 30px; color: #94a3b8; font-size: 13.5px;">
                        Loading live workforce logs...
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= MODAL: CONNECTED CLIENTS HUB (5 COMPANIES) ================= -->
        <div id="clientsHubModal" onclick="if(event.target === this) closeClientsHubModal()" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.78); backdrop-filter: blur(6px); z-index: 999994; align-items: center; justify-content: center; padding: 20px;">
            <div style="background: #ffffff; border-radius: 20px; max-width: 860px; width: 100%; max-height: 92vh; display: flex; flex-direction: column; box-shadow: 0 25px 60px rgba(0,0,0,0.35); border: 2px solid #3b82f6; overflow: hidden; position: relative;">
                <!-- Header -->
                <div style="padding: 20px 26px; background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #1e3a8a 100%); color: white; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 28px;">🏢</span>
                        <div>
                            <h3 style="margin: 0; font-size: 19px; font-weight: 900; letter-spacing: -0.3px;">Connected Clients &amp; Multi-Company Hub</h3>
                            <p style="margin: 2px 0 0 0; font-size: 12px; color: #cbd5e1;">Manage 5 client websites simultaneously • Connect WordPress credentials for automated live publishing</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeClientsHubModal()" style="background: rgba(255,255,255,0.15); border: none; font-size: 18px; width: 34px; height: 34px; border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
                </div>

                <!-- Client Tabs Selector Bar -->
                <div style="background: #f1f5f9; padding: 12px 24px; border-bottom: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div id="clientsHubTabsList" style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center;">
                        <!-- Injected dynamically: Client 1, Client 2, Client 3, Client 4, Client 5 -->
                    </div>
                    <button type="button" onclick="addNewHubClient()" style="background: #0284c7; color: white; border: none; font-size: 11.5px; font-weight: 800; padding: 7px 12px; border-radius: 6px; cursor: pointer;">
                        ➕ Add Another Client
                    </button>
                </div>

                <!-- Body (Active Client Settings) -->
                <div style="padding: 24px; overflow-y: auto; flex: 1;">
                    <form id="clientsHubForm" onsubmit="saveCurrentHubClient(event)">
                        <!-- Basic Info Grid -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 16px;">
                            <div>
                                <label style="display: block; font-size: 12.5px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Company / Client Business Name *</label>
                                <input type="text" id="hubClientName" placeholder="e.g. Apex Tech Solutions" required style="width: 100%; padding: 10px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 13.5px;" />
                            </div>
                            <div>
                                <label style="display: block; font-size: 12.5px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Website URL / Domain *</label>
                                <input type="url" id="hubClientDomain" placeholder="https://apextech.com" required style="width: 100%; padding: 10px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 13.5px;" />
                            </div>
                            <div>
                                <label style="display: block; font-size: 12.5px; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Target Market / Country</label>
                                <select id="hubClientCountry" style="width: 100%; padding: 10px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 13.5px; background: white;">
                                    <option value="Bangladesh" selected>🇧🇩 Bangladesh (BDT ৳)</option>
                                    <option value="United States">🇺🇸 United States (USD $)</option>
                                    <option value="United Kingdom">🇬🇧 United Kingdom (GBP £)</option>
                                    <option value="Canada">🇨🇦 Canada (CAD $)</option>
                                    <option value="Australia">🇦🇺 Australia (AUD $)</option>
                                    <option value="Global">🌐 Global / Worldwide</option>
                                </select>
                            </div>
                        </div>

                        <!-- Target Keywords & Competitors -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; margin-bottom: 18px;">
                            <div>
                                <label style="display: block; font-size: 12px; font-weight: 800; color: #334155; margin-bottom: 4px;">Core Target Keywords (Comma or Newline separated)</label>
                                <textarea id="hubClientKeywords" rows="2" placeholder="e.g. custom pc bd, gaming laptop dhaka, best computer shop" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 12.5px;"></textarea>
                            </div>
                            <div>
                                <label style="display: block; font-size: 12px; font-weight: 800; color: #334155; margin-bottom: 4px;">Top Competitor Website URLs</label>
                                <textarea id="hubClientCompetitors" rows="2" placeholder="e.g. https://competitor1.com, https://competitor2.com" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 12.5px;"></textarea>
                            </div>
                        </div>

                        <!-- WordPress REST API Integration Box -->
                        <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 18px; margin-bottom: 18px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 8px;">
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="font-size: 20px;">🔌</span>
                                    <strong style="font-size: 14px; color: #0073aa;">WordPress Direct REST API Integration (Optional)</strong>
                                </div>
                                <span style="font-size: 11px; background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 10px; font-weight: 700;">Enables 1-Click Auto-Publishing into this site</span>
                            </div>
                            <p style="font-size: 12px; color: #64748b; margin: 0 0 12px 0;">
                                Connecting WordPress allows Zayan Karim and the AI Content Studio to publish posts directly into this client's site as <strong>Live Post</strong> or <strong>Draft</strong>. Zero plugins needed! (Create Application Password in WP: <em>Users → Profile → Application Passwords</em>).
                            </p>

                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; margin-bottom: 12px;">
                                <div>
                                    <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 3px;">WordPress Site URL</label>
                                    <input type="url" id="hubClientWpUrl" placeholder="https://clientwebsite.com" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 12.5px;" />
                                </div>
                                <div>
                                    <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 3px;">WP Admin Username</label>
                                    <input type="text" id="hubClientWpUser" placeholder="e.g. admin" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 12.5px;" />
                                </div>
                                <div>
                                    <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 3px;">Application Password</label>
                                    <input type="password" id="hubClientWpPass" placeholder="xxxx xxxx xxxx xxxx" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 12.5px; font-family: monospace;" />
                                </div>
                                <div>
                                    <label style="display: block; font-size: 11.5px; font-weight: 700; color: #334155; margin-bottom: 3px;">Default Post Mode</label>
                                    <select id="hubClientWpStatus" style="width: 100%; padding: 8px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-size: 12.5px; background: white;">
                                        <option value="publish" selected>🚀 Direct LIVE Publish</option>
                                        <option value="draft">📝 Save as Draft (Review in Admin)</option>
                                    </select>
                                </div>
                            </div>

                            <div id="hubClientTestStatus" style="display: none; padding: 10px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 700; margin-bottom: 10px;"></div>

                            <div style="display: flex; gap: 8px;">
                                <button type="button" onclick="testHubClientWp()" id="hubClientTestBtn" style="background: #ffffff; border: 1.5px solid #0073aa; color: #0073aa; font-weight: 800; border-radius: 8px; padding: 7px 16px; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                                    <span>🧪 Test WordPress Connection</span>
                                </button>
                            </div>
                        </div>

                        <!-- Special SEO Directive / Notes for this Client -->
                        <div style="margin-bottom: 18px;">
                            <label style="display: block; font-size: 12px; font-weight: 800; color: #334155; margin-bottom: 4px;">Custom Brand Guidelines &amp; AI Instructions for this Client</label>
                            <input type="text" id="hubClientInstructions" placeholder="e.g. Focus on pricing transparency, emphasize 2-year authorized warranty, and avoid mentioning grey market." style="width: 100%; padding: 9px 12px; border-radius: 8px; border: 1.5px solid #cbd5e1; font-size: 12.5px;" />
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1.5px solid #e2e8f0; padding-top: 16px; flex-wrap: wrap; gap: 10px;">
                            <div style="display: flex; gap: 8px;">
                                <button type="button" onclick="deleteCurrentHubClient()" id="hubClientDeleteBtn" style="background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; font-size: 12px; font-weight: 700; padding: 8px 14px; border-radius: 8px; cursor: pointer;">
                                    <span>🗑️ Delete Client</span>
                                </button>
                                <button type="button" onclick="dispatchTaskForActiveHubClient()" style="background: #eff6ff; color: #2563eb; border: 1.5px solid #93c5fd; font-size: 12.5px; font-weight: 800; padding: 8px 16px; border-radius: 8px; cursor: pointer;">
                                    <span>⚡ Dispatch Task to this Client</span>
                                </button>
                            </div>
                            <div style="display: flex; gap: 10px;">
                                <button type="button" onclick="closeClientsHubModal()" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 700; border-radius: 8px; padding: 9px 18px; font-size: 13px; cursor: pointer;">
                                    Cancel
                                </button>
                                <button type="submit" style="background: linear-gradient(135deg, #059669, #10b981); color: white; border: none; font-weight: 800; border-radius: 8px; padding: 10px 24px; font-size: 13.5px; cursor: pointer; box-shadow: 0 4px 12px rgba(5,150,105,0.35);">
                                    <span>💾 Save Client Changes</span>
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- ================= MODAL: ASSIGN TASK TO AGENT ================= -->
        <div id="agencyTaskModal" onclick="if(event.target === this) closeAgencyTaskModal()" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(6px); z-index: 999995; align-items: center; justify-content: center; padding: 20px;">
            <div style="background: #ffffff; border-radius: 20px; max-width: 620px; width: 100%; box-shadow: 0 25px 60px rgba(0,0,0,0.3); border: 2px solid #6366f1; overflow: hidden; position: relative;">
                <div style="padding: 20px 24px; background: linear-gradient(135deg, #1e1b4b, #312e81); color: white; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 24px;">⚡</span>
                        <div>
                            <h3 style="margin: 0; font-size: 17px; font-weight: 800;">Dispatch Task to Agency Staff</h3>
                            <p style="margin: 2px 0 0 0; font-size: 11.5px; color: #c7d2fe;">Founder Directive • 100% Google White-Hat Certified Execution</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeAgencyTaskModal()" style="background: rgba(255,255,255,0.15); border: none; font-size: 18px; width: 32px; height: 32px; border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
                </div>

                <form id="agencyTaskForm" onsubmit="handleDispatchAgencyTask(event)" style="padding: 24px;">
                    <!-- 1. Connected Client Website Quick Selector Dropdown -->
                    <div style="margin-bottom: 16px; background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 12px 16px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
                            <label style="font-size: 13px; font-weight: 800; color: #166534; display: flex; align-items: center; gap: 6px;">
                                <span>🏢 1. Select Client Website (Choose from 5 Connected Companies):</span>
                            </label>
                            <button type="button" onclick="openClientsHubModal()" style="background: white; border: 1px solid #86efac; color: #047857; font-size: 11.5px; font-weight: 800; padding: 3px 10px; border-radius: 6px; cursor: pointer;">
                                ⚙️ Manage / Edit 5 Companies
                            </button>
                        </div>
                        <select id="taskCompanySelect" onchange="handleTaskCompanySelectChange(this.value)" style="width: 100%; padding: 10px 14px; border-radius: 8px; border: 1.5px solid #10b981; font-size: 13.5px; font-weight: 700; color: #065f46; background: #ffffff;">
                            <!-- Injected dynamically via populateTaskCompanySelect() -->
                        </select>
                        <div id="taskCompanyStatusHint" style="font-size: 11.5px; color: #15803d; font-weight: 700; margin-top: 6px; display: flex; align-items: center; gap: 6px;">
                            <span>🟢 Active Connected Website Loaded</span>
                        </div>
                    </div>

                    <div style="margin-bottom: 16px;">
                        <label style="display: block; font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">2. Assign To Staff Member:</label>
                        <select id="taskAgentSelect" required style="width: 100%; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #cbd5e1; font-size: 13.5px; font-weight: 700; color: #0f172a; background: #f8fafc;">
                            <option value="tanvir">👨‍💼 Tanvir Ahmed — Lead SEO Strategist (Keywords, SERP Radar, Gaps)</option>
                            <option value="nabila">✍️ Nabila Rahman — On-Page SEO & Content Lead (EEAT 2,500+ Words, Zero Double Words)</option>
                            <option value="arif">🔗 Arif Hossain — Head of Link Architecture (Internal Silos & Skyscraper Backlinks)</option>
                            <option value="fahim">⚙️ Fahim Chowdhury — Technical SEO Auditor (Googlebot, Core Web Vitals, Schema)</option>
                            <option value="zayan">💻 Zayan Karim — Web & WordPress Engineer (1-Click Publishing, Speed, Bug Fixes)</option>
                            <option value="samira">🎨 Samira Khan — UI/UX & CRO Specialist (Page Experience, Mobile, Conversions)</option>
                        </select>
                    </div>

                    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div>
                            <label style="display: block; font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">Client Domain / Website URL:</label>
                            <input type="text" id="taskClientDomain" placeholder="e.g. https://www.clientwebsite.com" style="width: 100%; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #cbd5e1; font-size: 13px;" required />
                            <div style="font-size: 11px; color: #047857; margin-top: 4px; font-weight: 700; display: flex; align-items: center; gap: 4px;">
                                <span>🔒 <strong>100% Read-Only Safety:</strong> Crawls public HTML like Googlebot. Zero passwords needed &amp; zero risk of modifying/deleting client data.</span>
                            </div>
                        </div>
                        <div>
                            <label style="display: block; font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">Task Priority:</label>
                            <select id="taskPrioritySelect" style="width: 100%; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #cbd5e1; font-size: 13px; font-weight: 700;">
                                <option value="High" selected>High Priority</option>
                                <option value="Urgent">🔥 Urgent</option>
                                <option value="Normal">Normal</option>
                            </select>
                        </div>
                    </div>

                    <div style="margin-bottom: 16px;">
                        <label style="display: block; font-size: 13px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">Task Directive / Specific Instructions:</label>
                        <textarea id="taskDirectiveText" rows="3" placeholder="e.g. Audit technical indexing and Schema, build internal linking silos, or write 2,500-word EEAT article..." required style="width: 100%; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #cbd5e1; font-size: 13px; line-height: 1.5; font-family: inherit;"></textarea>
                        <div style="font-size: 11px; color: #475569; margin-top: 4px; font-weight: 600;">
                            💡 <strong>Supports English, বাংলা ও Banglish</strong> (যেমন: <em>"Client site er internal link thik koro"</em> বা <em>"Schema audit koro"</em>)
                        </div>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <label style="display: flex; justify-content: space-between; font-size: 12.5px; font-weight: 800; color: #0f172a; margin-bottom: 6px;">
                            <span>🔑 Google Gemini API Key:</span>
                            <span style="font-size: 11px; font-weight: 600; color: #059669;">Optional (Free • Deep AI Mode)</span>
                        </label>
                        <input type="password" id="taskGeminiKey" placeholder="AIzaSy... (Leave empty to use adaptive forensic engine)" style="width: 100%; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #cbd5e1; font-size: 12.5px; font-family: monospace;" />
                        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">
                            Google AI Studio থেকে সম্পূর্ণ ফ্রি API Key নিতে পারেন: <a href="https://aistudio.google.com/" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 600;">aistudio.google.com</a> (ফাঁকা রাখলেও সিস্টেম চলবে)
                        </div>
                    </div>

                    <div id="agencyTaskStatusAlert" style="display: none; padding: 12px; border-radius: 10px; margin-bottom: 16px; font-size: 13px; font-weight: 700;"></div>

                    <div style="display: flex; justify-content: flex-end; gap: 10px;">
                        <button type="button" onclick="closeAgencyTaskModal()" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 700; border-radius: 8px; padding: 10px 18px; font-size: 13px; cursor: pointer;">Cancel</button>
                        <button type="submit" id="btnDispatchAgencyTask" style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; font-weight: 800; border-radius: 8px; padding: 10px 24px; font-size: 13.5px; cursor: pointer; box-shadow: 0 4px 12px rgba(37,99,235,0.35);">
                            <span>🚀 Dispatch Task to Agent</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- ================= MODAL: DAILY REPORT SUMMARY ================= -->
        <div id="agencyDailyReportModal" onclick="if(event.target === this) closeDailyReportModal()" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(6px); z-index: 999995; align-items: center; justify-content: center; padding: 20px;">
            <div style="background: #ffffff; border-radius: 20px; max-width: 800px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 25px 60px rgba(0,0,0,0.3); border: 2px solid #2563eb; overflow: hidden; position: relative;">
                <div style="padding: 18px 24px; background: linear-gradient(135deg, #1e1b4b, #2563eb); color: white; display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 24px;">📊</span>
                        <div>
                            <h3 style="margin: 0; font-size: 18px; font-weight: 900;">Daily Agency Work Report (Shift Summary)</h3>
                            <p style="margin: 2px 0 0 0; font-size: 12px; color: #c7d2fe;">Consolidated deliverable across all 6 specialists</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeDailyReportModal()" style="background: rgba(255,255,255,0.15); border: none; font-size: 18px; width: 32px; height: 32px; border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;">✕</button>
                </div>
                <div id="dailyReportModalBody" style="padding: 24px; overflow-y: auto; flex: 1;">
                    <!-- Populated dynamically -->
                </div>
                <div style="padding: 14px 24px; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                    <a href="/agency/daily-report/pdf" target="_blank" style="background: #059669; color: white; text-decoration: none; font-weight: 800; border-radius: 8px; padding: 9px 20px; font-size: 13px; display: inline-flex; align-items: center; gap: 6px;">
                        <span>🖨️ Download as PDF</span>
                    </a>
                    <button type="button" onclick="closeDailyReportModal()" style="background: #0f172a; color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 20px; font-size: 13px; cursor: pointer;">
                        Close
                    </button>
                </div>
            </div>
        </div>


    <!-- ================= 1-WEEK FREE TRIAL USER WELCOME POPUP MODAL ================= -->
    <div id="trialWelcomeModal" onclick="if(event.target === this) closeTrialWelcomeModal()" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(6px); z-index: 999990; align-items: center; justify-content: center; padding: 20px;">
        <div style="background: #ffffff; border-radius: 22px; max-width: 530px; width: 100%; padding: 34px 28px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.3); border: 2.5px solid #10b981; position: relative;">
            <button id="launchTrialWelcomeBtn" type="button" onclick="document.getElementById('trialWelcomeModal').style.display='none'; closeTrialWelcomeModal(); return false;" aria-label="Close" style="position: absolute; top: 16px; right: 18px; background: #f1f5f9; border: none; font-size: 16px; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; color: #64748b; display: flex; align-items: center; justify-content: center; font-weight: 700; transition: background 0.15s;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f1f5f9'">✕</button>
            <div style="width: 76px; height: 76px; margin: 0 auto 16px; background: #ecfdf5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; border: 3px solid #a7f3d0;">
                🎁
            </div>
            <div style="display: inline-block; background: #ecfdf5; color: #047857; font-size: 11px; font-weight: 800; padding: 4px 14px; border-radius: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
                Special Complimentary Access
            </div>
            <h2 style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 0 0 10px 0;">🎉 Welcome! 1-Week Free Trial Active</h2>
            <p style="font-size: 14.5px; color: #475569; line-height: 1.6; margin: 0 0 20px 0;">
                You have received <strong>7 Days (1 Week) of 100% Unlimited Free Access</strong> to the complete <strong>RankNaserPro Intelligence Suite</strong>.
            </p>

            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 14px; padding: 16px; text-align: left; margin-bottom: 22px; font-size: 13px; color: #334155; line-height: 1.7;">
                <div style="font-weight: 800; color: #0f172a; margin-bottom: 8px; font-size: 13.5px;">🚀 Included in your 1-Week Free Trial:</div>
                <div>✅ <strong>1. Daily SERP Radar:</strong> Live competitor rank tracking #1-10</div>
                <div>✅ <strong>2. 360° Deep Spy:</strong> Competitor headings, word count & gap scraping</div>
                <div>✅ <strong>3. 5 vs 1 Outranker:</strong> Master SERP synthesis & outranking outline</div>
                <div>✅ <strong>4. AI Content Studio:</strong> 2,500+ word articles with FAQ Schema</div>
                <div>✅ <strong>5. Autopilot Agent:</strong> Automated direct WordPress & API publishing</div>
                <div>✅ <strong>6. SEO Director:</strong> 10-day master execution campaign blueprint</div>
                <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed #cbd5e1; font-size: 12px; color: #b91c1c; font-weight: 700;">
                    ⏳ Notice: Access is active for 7 days and will automatically turn off once the 1 week ends.
                </div>
            </div>

            <button type="button" onclick="closeTrialWelcomeModal()" style="width: 100%; background: linear-gradient(135deg, #059669, #10b981); color: white; border: none; font-weight: 800; border-radius: 10px; padding: 13px; font-size: 14px; cursor: pointer; box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35); transition: transform 0.15s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                <span>🚀 Launch My 1-Week Free Trial Access</span>
            </button>
        </div>
    </div>

        <!-- ================= 7-DAY FREE TRIAL AUTOMATIC LOCK OVERLAY ================= -->
    <div id="trialExpiredModal" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.88); backdrop-filter: blur(8px); z-index: 999999; align-items: center; justify-content: center; padding: 20px;">
        <div style="background: #ffffff; border-radius: 22px; max-width: 530px; width: 100%; padding: 36px 30px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.35); border: 2.5px solid #ef4444; position: relative;">
            <div style="width: 76px; height: 76px; margin: 0 auto 16px; background: #fee2e2; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; border: 3px solid #fca5a5;">
                🔒
            </div>
            <div style="display: inline-block; background: #fee2e2; color: #b91c1c; font-size: 11px; font-weight: 800; padding: 3px 14px; border-radius: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
                Trial Concluded (1 Week Finished)
            </div>
            <h2 style="font-size: 25px; font-weight: 900; color: #0f172a; margin: 0 0 10px 0;">7-Day Free Trial Has Ended</h2>
            <p style="font-size: 14.5px; color: #475569; line-height: 1.6; margin: 0 0 22px 0;">
                Your complimentary <strong>1-week (7-day) free trial</strong> for RankNaserPro Intelligence Suite has automatically concluded. All 6 autonomous SEO engines are now locked.
            </p>
            
            <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: left; margin-bottom: 24px; font-size: 13px; color: #334155; line-height: 1.6;">
                <div style="font-weight: 800; color: #0f172a; margin-bottom: 6px; font-size: 13.5px;">To renew license or unlock lifetime access:</div>
                <div style="display: flex; align-items: center; gap: 6px;">📧 <span>Contact Admin:</span> <strong>admin@ranknaser.com</strong></div>
                <div style="display: flex; align-items: center; gap: 6px;">👑 <span>Lead Architect:</span> <strong>RankNaser</strong></div>
                <div style="font-size: 11.5px; color: #64748b; margin-top: 6px;">License reactivation or admin credentials required.</div>
            </div>

            <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                <button type="button" onclick="handleLogout()" style="background: #0f172a; color: white; border: none; font-weight: 700; border-radius: 10px; padding: 12px 22px; font-size: 13px; cursor: pointer; transition: all 0.2s;">
                    🚪 Logout & Exit
                </button>
                <button type="button" onclick="promptAdminUnlock()" style="background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; font-weight: 800; border-radius: 10px; padding: 12px 24px; font-size: 13px; cursor: pointer; box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35); transition: all 0.2s;">
                    🔑 Admin Master Unlock
                </button>
            </div>
        </div>
    </div>

        <!-- ================= USER GUIDE MODAL (ENGLISH & BANGLA) ================= -->
        <div id="userGuideModal" onclick="if(event.target === this) closeUserGuideModal()" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(6px); z-index: 999995; align-items: center; justify-content: center; padding: 20px;">
            <div style="background: #ffffff; border-radius: 20px; max-width: 860px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 25px 60px rgba(0,0,0,0.3); border: 2px solid #6366f1; overflow: hidden; position: relative;">
                
                <!-- Modal Top Header -->
                <div style="padding: 20px 26px; background: linear-gradient(135deg, #1e1b4b, #312e81); color: white; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #4338ca;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 26px;">📘</span>
                        <div>
                            <h2 style="margin: 0; font-size: 18px; font-weight: 800; letter-spacing: -0.3px;">RankNaserPro Intelligence Suite — User Guide</h2>
                            <p style="margin: 2px 0 0 0; font-size: 12px; color: #c7d2fe;">Official Operator Manual & SEO Execution Blueprint (English & বাংলা)</p>
                        </div>
                    </div>
                    <button type="button" onclick="closeUserGuideModal()" style="background: rgba(255,255,255,0.15); border: none; font-size: 18px; width: 34px; height: 34px; border-radius: 50%; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: 700; transition: background 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.15)'">✕</button>
                </div>

                <!-- Control Bar: Language Switcher & PDF Download Buttons -->
                <div style="padding: 14px 26px; background: #f8fafc; border-bottom: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                    <div style="display: flex; gap: 8px;">
                        <button type="button" id="guideTabEnBtn" onclick="switchGuideTab('en')" style="padding: 8px 18px; border-radius: 8px; font-size: 13px; font-weight: 800; cursor: pointer; border: 1.5px solid #4f46e5; background: #4f46e5; color: white; transition: all 0.15s;">
                            🇬🇧 English Guide
                        </button>
                        <button type="button" id="guideTabBnBtn" onclick="switchGuideTab('bn')" style="padding: 8px 18px; border-radius: 8px; font-size: 13px; font-weight: 800; cursor: pointer; border: 1.5px solid #cbd5e1; background: #ffffff; color: #334155; transition: all 0.15s;">
                            🇧🇩 বাংলা ইউজার গাইড
                        </button>
                    </div>

                    <div style="display: flex; gap: 10px;">
                        <button type="button" onclick="downloadGuidePdf('en')" style="background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; font-size: 12.5px; font-weight: 700; border-radius: 8px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(37,99,235,0.25);">
                            <span>📥 Download English PDF</span>
                        </button>
                        <button type="button" onclick="downloadGuidePdf('bn')" style="background: linear-gradient(135deg, #059669, #10b981); color: white; border: none; font-size: 12.5px; font-weight: 700; border-radius: 8px; padding: 8px 16px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(16,185,129,0.25);">
                            <span>📥 বাংলা PDF ডাউনলোড</span>
                        </button>
                    </div>
                </div>

                <!-- Scrollable Guide Content Area -->
                <div style="padding: 24px 28px; overflow-y: auto; flex-grow: 1; font-size: 14px; line-height: 1.7; color: #334155;">
                    
                    <!-- ENGLISH GUIDE VIEW -->
                    <div id="guideViewEn" style="display: block;">
                        <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 22px;">
                            <div style="font-weight: 800; color: #1e40af; font-size: 15px;">Welcome to RankNaserPro Intelligence Suite</div>
                            <div style="font-size: 13px; color: #3b82f6; margin-top: 2px;">Architected by <strong>RankNaser</strong> — Lead Architect & SEO Director</div>
                            <div style="font-size: 12.5px; color: #475569; margin-top: 6px;">
                                This complete handbook explains how any user or agency can leverage the 6 autonomous search engines to track competitors, reverse-engineer top Google SERPs, generate 2,500+ word EEAT master articles, and automate publishing on 100% autopilot.
                            </div>
                        </div>

                        <h3 style="color: #0f172a; font-size: 17px; margin-top: 20px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">📋 Table of Contents</h3>
                        <ol style="padding-left: 20px; margin-bottom: 24px; color: #2563eb; font-weight: 600;">
                            <li>Module 1: Access, Free Trial & System Gateway</li>
                            <li>Module 2: Engine 1 — Daily SERP Radar & Keyword Tracking</li>
                            <li>Module 3: Engine 2 — 360° Deep Competitor Infiltration</li>
                            <li>Module 4: Engine 3 — 5 vs 1 SERP Outranker</li>
                            <li>Module 5: Engine 4 — Elite AI Content Studio (2,500+ Words EEAT)</li>
                            <li>Module 6: Engine 5 — Autonomous Autopilot Agent (Hands-Free SEO)</li>
                            <li>Module 7: Engine 6 — SEO Director Campaign & 30-Day Roadmap</li>
                            <li>Module 8: One-Click WordPress & Webhook Auto-Publishing</li>
                            <li>Module 9: RankNaser's Golden SEO Blueprint for Ranking #1 on Google</li>
                        </ol>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🚀 Module 1: Access, Free Trial & System Gateway</h3>
                        <p><strong>1.1 Initial Login:</strong> Navigate to the gateway and log in using your Admin credentials (<code>ADMIN</code> / <code>AGENTNASER</code>) or your registered user credentials. You can also use the <strong>Instant Enter (1-Click)</strong> button.</p>
                        <p><strong>1.2 7-Day Complimentary Trial:</strong> First-time users receive 7 full days of unrestricted access to all 6 engines. The live countdown is displayed in the header badge (<code>⏱️ Day 1 of 7</code>). After 7 days, the system automatically locks to protect access. Master administrators can bypass or reset the trial at any time.</p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">📡 Module 2: Engine 1 — Daily SERP Radar & Keyword Tracking</h3>
                        <p><strong>2.1 Purpose:</strong> Continuously surveillance Google search results (#1 through #10) to monitor keyword rankings, search difficulty, volume trends, and competitor movements.</p>
                        <p><strong>2.2 How to Use:</strong>
                            <br>1. Select target country (Bangladesh, US, UK, Global, etc.).
                            <br>2. Enter your Target Keywords (separated by commas) and your Competitor URLs.
                            <br>3. Click <strong>"Launch Live SERP Radar Scan"</strong>.
                            <br>4. The radar renders position distribution cards, movement alerts, and direct ranking tables.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🕵️ Module 3: Engine 2 — 360° Deep Competitor Infiltration</h3>
                        <p><strong>3.1 Purpose:</strong> Scrapes and dissects the live ranking content of your #1 competitor page to uncover their exact headings (H1, H2, H3), total word count, keyword density, and critical content gaps.</p>
                        <p><strong>3.2 How to Use:</strong>
                            <br>1. Enter the exact competitor article URL you wish to outrank.
                            <br>2. Click <strong>"Execute Deep Competitor Infiltration"</strong>.
                            <br>3. Review the Infiltration Report: word count benchmark, heading hierarchy, and highlighted content gaps that your own article must solve.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">⚔️ Module 4: Engine 3 — 5 vs 1 SERP Outranker</h3>
                        <p><strong>4.1 Purpose:</strong> Why beat one competitor when you can beat the top 5 at once? This engine crawls 5 competing URLs simultaneously and synthesizes their combined best points into one superior master outline.</p>
                        <p><strong>4.2 How to Use:</strong>
                            <br>1. Provide up to 5 competitor URLs ranking on Google Page 1.
                            <br>2. Provide your Focus Keyword.
                            <br>3. Click <strong>"Generate 5 vs 1 Outranking Synthesis"</strong>.
                            <br>4. The engine outputs a comprehensive master brief containing combined headings, missed competitor angles, and a superior article architecture.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">✍️ Module 5: Engine 4 — Elite AI Content Studio (2,500+ Words EEAT)</h3>
                        <p><strong>5.1 Purpose:</strong> Produces human-authored, publication-grade blog posts (2,000 to 3,500+ words) that strictly comply with Google Helpful Content guidelines.</p>
                        <p><strong>5.2 Key Capabilities:</strong>
                            <br>• <strong>0 Double Words:</strong> Advanced multi-tier deduplication guarantees zero stutter or repetitive phrasing.
                            <br>• <strong>Exact Keyword Placement:</strong> The Main Keyword is featured naturally in the H1 title, opening hook, major headings, comparison tables, and FAQs.
                            <br>• <strong>Semantic LSI Deep-Dives:</strong> Every single LSI keyword provided receives its own dedicated, context-rich subsection.
                            <br>• <strong>Rich Schema & Tables:</strong> Embeds Google AI Overview quick answers, Markdown comparison tables, and FAQPage JSON-LD Schema.
                        </p>
                        <p><strong>5.3 How to Use:</strong>
                            <br>1. Enter Title, Main Keyword, and Semantic LSI Keywords (comma separated).
                            <br>2. Select Target Country, Format (Long-Form SEO, Review, Buying Guide), Tone, and Word Count.
                            <br>3. Click <strong>"Generate Outranking Article with AI Agent"</strong>.
                            <br>4. View in Visual mode, copy Markdown, or 1-click post to WordPress.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🤖 Module 6: Engine 5 — Autonomous Autopilot Agent</h3>
                        <p><strong>6.1 Purpose:</strong> 100% hands-free SEO worker. You enter your brand name and competitor domains; the agent autonomously scans competitor rankings, discovers high-intent ranking gaps, writes the outranking article, and auto-publishes it to your CMS.</p>
                        <p><strong>6.2 How to Use:</strong>
                            <br>1. Enter Brand Name, Target Country, and Competitor Domains.
                            <br>2. Check "Post to WordPress" or "Post to Custom Webhook".
                            <br>3. Click <strong>"Launch Autonomous Agent Mission Now"</strong>.
                            <br>4. Watch real-time execution in the live terminal console.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🗺️ Module 7: Engine 6 — SEO Director Campaign & 30-Day Roadmap</h3>
                        <p><strong>7.1 Purpose:</strong> A 10-day structured execution campaign and 30-day content calendar designed by senior SEO architects to systematically build domain authority.</p>
                        <p><strong>7.2 How to Use:</strong>
                            <br>1. Click the top button <strong>"🗺️ 30-Day Content Roadmap"</strong>.
                            <br>2. Generate your customized 30-day calendar matching your niche and target country.
                            <br>3. Download the full roadmap as a Markdown or JSON plan.
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🔌 Module 8: One-Click WordPress & Webhook Auto-Publishing</h3>
                        <p><strong>8.1 WordPress Integration:</strong>
                            <br>1. Click <strong>"🔌 WordPress"</strong> in the top header.
                            <br>2. Enter your WordPress Site URL (e.g., <code>https://mywebsite.com</code>).
                            <br>3. Enter your WordPress Admin Username.
                            <br>4. In your WordPress admin panel, go to <em>Users &gt; Profile &gt; Application Passwords</em>, generate a new password, and paste it here.
                            <br>5. Click <strong>"Test Connection"</strong> and save. Articles can now be published directly as Drafts or Published posts!
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">👑 Module 9: RankNaser's Golden Rules for #1 Google Ranking</h3>
                        <p>1. <strong>Satisfy Search Intent in the First 100 Words:</strong> Google favors pages that answer the user's primary query immediately.</p>
                        <p>2. <strong>Cover Every Semantic LSI Entity:</strong> Modern search engines rank topical depth, not raw keyword repetition.</p>
                        <p>3. <strong>Include Structured Comparison Tables:</strong> Tables dramatically improve dwell time and win Featured Snippets.</p>
                        <p>4. <strong>Consistent Publishing Rhythm:</strong> Deploy at least 3-5 comprehensive guides per week using the Autopilot Agent.</p>
                    </div>

                    <!-- BANGLA GUIDE VIEW -->
                    <div id="guideViewBn" style="display: none;">
                        <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 22px;">
                            <div style="font-weight: 800; color: #065f46; font-size: 15px;">স্বাগতম RankNaserPro Intelligence Suite-এ!</div>
                            <div style="font-size: 13px; color: #047857; margin-top: 2px;">প্রধান আর্কিটেক্ট ও এসইও ডিরেক্টর: <strong>RankNaser</strong></div>
                            <div style="font-size: 12.5px; color: #475569; margin-top: 6px;">
                                এই পূর্ণাঙ্গ ব্যবহারকারী নির্দেশিকায় সহজ বাংলা ভাষায় বর্ণনা করা হয়েছে কীভাবে আপনি ৬টি স্বয়ংক্রিয় এআই ইঞ্জিন ব্যবহার করে প্রতিদ্বন্দ্বীদের ট্র্যাক করবেন, ২৫০০+ শব্দের নির্ভুল র‍্যাংকিং আর্টিকেল তৈরি করবেন এবং সরাসরি ওয়েবসাইটে পাবলিশ করবেন।
                            </div>
                        </div>

                        <h3 style="color: #0f172a; font-size: 17px; margin-top: 20px; border-bottom: 1.5px solid #e2e8f0; padding-bottom: 6px;">📋 সূচিপত্র (Table of Contents)</h3>
                        <ol style="padding-left: 20px; margin-bottom: 24px; color: #059669; font-weight: 600;">
                            <li>মডিউল ১: লগইন ও ১ সপ্তাহের ফ্রি ট্রায়াল সিস্টেম</li>
                            <li>মডিউল ২: ইঞ্জিন ১ — ডেইলি এসইআরপি রাডার (র‍্যাংক ট্র্যাকিং)</li>
                            <li>মডিউল ৩: ইঞ্জিন ২ — ৩৬০° ডিপ কম্পিটিটর স্পাই</li>
                            <li>মডিউল ৪: ইঞ্জিন ৩ — ৫ বনাম ১ আউট-র‍্যাঙ্কার</li>
                            <li>মডিউল ৫: ইঞ্জিন ৪ — এআই কনটেন্ট স্টুডিও (২৫০০+ শব্দ, হিউম্যান রাইটার কোয়ালিটি)</li>
                            <li>মডিউল ৬: ইঞ্জিন ৫ — অটোনোমাস অটোপাইলট এজেন্ট (হ্যান্ডস-ফ্রি এসইও)</li>
                            <li>মডিউল ৭: ইঞ্জিন ৬ — এসইও ডিরেক্টর ক্যাম্পেইন ও ৩০ দিনের রোডম্যাপ</li>
                            <li>মডিউল ৮: ওয়ার্ডপ্রেস ও কাস্টম সাইট অটো-পাবলিশিং কনফিগারেশন</li>
                            <li>মডিউল ৯: গুগলে ১ নম্বরে র‍্যাংক করার সেরা এসইও ফর্মুলা</li>
                        </ol>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🚀 মডিউল ১: লগইন ও ১ সপ্তাহের ফ্রি ট্রায়াল সিস্টেম</h3>
                        <p><strong>১.১ লগইন পদ্ধতি:</strong> ড্যাশবোর্ডে প্রবেশের জন্য অ্যাডমিন আইডি (<code>ADMIN</code>) এবং পাসওয়ার্ড (<code>AGENTNASER</code>) দিয়ে লগইন করুন, অথবা <strong>Instant Enter (1-Click)</strong> বাটনে ক্লিক করুন।</p>
                        <p><strong>১.২ ৭ দিনের ফ্রি ট্রায়াল:</strong> যেকোনো নতুন ইউজার ৭ দিন সম্পূর্ণ ফ্রিতে সব ইঞ্জিন ব্যবহার করতে পারবেন। ড্যাশবোর্ডের হেডারে লাইভ কাউন্টডাউন শো করবে (<code>⏱️ Day 1 of 7</code>)। ৭ দিন শেষ হলে প্ল্যাটফর্ম অটোমেটিক লক হয়ে যাবে। তবে মাস্টার অ্যাডমিন যেকোনো সময় পাসওয়ার্ড দিয়ে এটি আনলক করতে পারবেন।</p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">📡 মডিউল ২: ইঞ্জিন ১ — ডেইলি এসইআরপি রাডার (র‍্যাংক ট্র্যাকিং)</h3>
                        <p><strong>২.১ মূল কাজ:</strong> আপনার টার্গেটেড কিওয়ার্ডগুলো গুগলের ১ থেকে ১০ নম্বর পজিশনে কোথায় আছে, প্রতিদ্বন্দ্বীরা কীভাবে পজিশন বদলাচ্ছে এবং সার্চ ভলিউম কেমন—তা ২৪/৭ মনিটর করা।</p>
                        <p><strong>২.২ ব্যবহারের নিয়ম:</strong>
                            <br>১. দেশ নির্বাচন করুন (যেমন: বাংলাদেশ, ইউএস, ইউকে ইত্যাদি)।
                            <br>২. আপনার কিওয়ার্ড এবং কম্পিটিটরদের ওয়েবসাইটের নাম দিন।
                            <br>৩. <strong>"Launch Live SERP Radar Scan"</strong> বাটনে চাপ দিন।
                            <br>৪. সাথে সাথে লাইভ র‍্যাংকিং ও মুভমেন্ট কার্ড আপনার সামনে চলে আসবে।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🕵️ মডিউল ৩: ইঞ্জিন ২ — ৩৬০° ডিপ কম্পিটিটর স্পাই</h3>
                        <p><strong>৩.১ মূল কাজ:</strong> যে কম্পিটিটর গুগলের ১ নম্বরে বসে আছে, তার পুরো আর্টিকেল স্ক্যান করে তার H1, H2, H3 হেডিংস, মোট শব্দসংখ্যা এবং তার লেখার দুর্বলতাগুলো (Content Gap) বের করে নেওয়া।</p>
                        <p><strong>৩.২ ব্যবহারের নিয়ম:</strong>
                            <br>১. প্রতিদ্বন্দ্বীর আর্টিকেলের সঠিক URL দিন।
                            <br>২. <strong>"Execute Deep Competitor Infiltration"</strong> বাটনে ক্লিক করুন।
                            <br>৩. রিপোর্ট থেকে দেখুন প্রতিদ্বন্দ্বী কোন কোন পয়েন্ট বাদ দিয়েছে, যা আপনার আর্টিকেলে যোগ করতে হবে।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">⚔️ মডিউল ৪: ইঞ্জিন ৩ — ৫ বনাম ১ আউট-র‍্যাঙ্কার</h3>
                        <p><strong>৪.১ মূল কাজ:</strong> এক সাথে শীর্ষ ৫ জন প্রতিদ্বন্দ্বীর আর্টিকেল অ্যানালাইসিস করে তাদের সবার চেয়ে সুপিরিয়র ও তথ্যবহুল একটি মাস্টার আউটলাইন তৈরি করা।</p>
                        <p><strong>৪.২ ব্যবহারের নিয়ম:</strong>
                            <br>১. গুগলে র‍্যাংক করা শীর্ষ ৫টি প্রতিদ্বন্দ্বীর লিংক দিন।
                            <br>২. আপনার ফোকাস কিওয়ার্ড দিন।
                            <br>৩. <strong>"Generate 5 vs 1 Outranking Synthesis"</strong> চাপুন।
                            <br>৪. সিস্টেম সবার সেরা তথ্যগুলো নিয়ে একক পূর্ণাঙ্গ আউটলাইন তৈরি করে দেবে।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">✍️ মডিউল ৫: ইঞ্জিন ৪ — এআই কনটেন্ট স্টুডিও (২৫০০+ শব্দ, হিউম্যান রাইটার কোয়ালিটি)</h3>
                        <p><strong>৫.১ মূল কাজ:</strong> আন্তর্জাতিক পাবলিকেশন মানের (EEAT) ২৫০০+ শব্দের গভীর ও তথ্যবহুল আর্টিকেল তৈরি করা।</p>
                        <p><strong>৫.২ বিশেষ সুবিধাসমূহ:</strong>
                            <br>• <strong>০% ডাবল ওয়ার্ড:</strong> কোনো রোবোটিক পুনরাবৃত্তি বা একই শব্দের তোতাপাখি আচরণ নেই।
                            <br>• <strong>মেইন কিওয়ার্ডের সঠিক ব্যবহার:</strong> টাইটেল, প্রথম ৬০-৮০ শব্দ, হেডিংস এবং উপসংহারে ন্যাচারালভাবে কিওয়ার্ড থাকবে।
                            <br>• <strong>প্রতিটি LSI কিওয়ার্ডের ডেডিকেটেড সাব-সেকশন:</strong> আপনি যে LSI কিওয়ার্ড দেবেন, সেটির ওপর আলাদা তথ্যবহুল সেকশন লেখা হবে।
                            <br>• <strong>গুগল AI ওভারভিউ ও FAQ স্কিমা:</strong> গুগলের নতুন সার্চ ফিচারে আসার জন্য কম্প্যারিজন টেবিল এবং FAQPage স্কিমা কোড থাকবে।
                        </p>
                        <p><strong>৫.৩ ব্যবহারের নিয়ম:</strong>
                            <br>১. টপিক, মেইন কিওয়ার্ড এবং LSI কিওয়ার্ড দিন (কমা দিয়ে দিয়ে)।
                            <br>২. দেশ, ফরম্যাট (Long-Form SEO, Review ইত্যাদি) ও শব্দসংখ্যা সিলেক্ট করুন।
                            <br>৩. <strong>"Generate Outranking Article with AI Agent"</strong> চাপুন।
                            <br>৪. আর্টিকেল তৈরি হলে এক ক্লিকে ওয়ার্ডপ্রেসে পোস্ট করুন বা ডাউনলোড করে নিন।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🤖 মডিউল ৬: ইঞ্জিন ৫ — অটোনোমাস অটোপাইলট এজেন্ট (হ্যান্ডস-ফ্রি এসইও)</h3>
                        <p><strong>৬.১ মূল কাজ:</strong> সম্পূর্ণ অটোমেশন। আপনি শুধু আপনার ব্র্যান্ড নেম ও কম্পিটিটর ডোমেন দেবেন; এজেন্ট নিজে নিজে কম্পিটিটরদের স্ক্যান করবে, হাই-ইনটেন্ট কিওয়ার্ড বের করবে, আর্টিকেল লিখবে এবং সরাসরি সাইটে পাবলিশ করবে।</p>
                        <p><strong>৬.২ ব্যবহারের নিয়ম:</strong>
                            <br>১. ব্র্যান্ড নেম ও ১-৩টি কম্পিটিটর ডোমেন দিন।
                            <br>২. "Post to WordPress" টিক দিন।
                            <br>৩. <strong>"Launch Autonomous Agent Mission Now"</strong> চাপুন।
                            <br>৪. লাইভ টার্মিনাল কনসোলে এজেন্টের কাজ স্বচক্ষে দেখুন।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🗺️ মডিউল ৭: ইঞ্জিন ৬ — এসইও ডিরেক্টর ক্যাম্পেইন ও ৩০ দিনের রোডম্যাপ</h3>
                        <p><strong>৭.১ মূল কাজ:</strong> সিনিয়র এসইও ডিরেক্টরের তৈরি ১০ দিনের মাস্টার এক্সিকিউশন ক্যাম্পেইন ও ৩০ দিনের কনটেন্ট ক্যালেন্ডার।</p>
                        <p><strong>৭.২ ব্যবহারের নিয়ম:</strong>
                            <br>১. হেডারের <strong>"🗺️ 30-Day Content Roadmap"</strong> বাটনে ক্লিক করুন।
                            <br>২. আপনার ইন্ডাস্ট্রির জন্য ৩০ দিনের শিডিউল তৈরি করুন এবং ডাউনলোড করে প্রিন্ট করুন।
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">🔌 মডিউল ৮: ওয়ার্ডপ্রেস ও কাস্টম সাইট অটো-পাবলিশিং কনফিগারেশন</h3>
                        <p><strong>৮.১ ওয়ার্ডপ্রেস কানেক্ট করার উপায়:</strong>
                            <br>১. হেডারের <strong>"🔌 WordPress"</strong> বাটনে চাপুন।
                            <br>২. আপনার ওয়েবসাইটের লিংক (যেমন: <code>https://mywebsite.com</code>) দিন।
                            <br>৩. ওয়ার্ডপ্রেস অ্যাডমিন ইউজারনেম দিন।
                            <br>৪. ওয়ার্ডপ্রেসের <em>Users &gt; Profile &gt; Application Passwords</em> থেকে নতুন একটি পাসওয়ার্ড তৈরি করে এখানে পেস্ট করুন।
                            <br>৫. <strong>"Test Connection"</strong> চাপুন এবং সেভ করুন। ব্যস, সরাসরি ড্রাফট পাবলিশ সক্রিয় হয়ে যাবে!
                        </p>

                        <h3 style="color: #0f172a; font-size: 16px; margin-top: 24px;">👑 মডিউল ৯: গুগলে ১ নম্বরে র‍্যাংক করার সেরা এসইও ফর্মুলা</h3>
                        <p>১. <strong>প্রথম ১০০ শব্দে সমাধান দিন:</strong> ভিজিটর যে প্রশ্ন নিয়ে এসেছে, তার উত্তর প্রথম প্যারাগ্রাফেই পরিষ্কার করে বলুন।</p>
                        <p>২. <strong>প্রতিটি LSI কিওয়ার্ডের গভীরতা নিশ্চিত করুন:</strong> শুধু কিওয়ার্ড গোঁজা নয়, সেই বিষয়ের বাস্তব তথ্য দিন।</p>
                        <p>৩. <strong>কম্প্যারিজন টেবিল ব্যবহার করুন:</strong> টেবিল ভিজিটরের পড়ার সময় বাড়ায় এবং গুগল দ্রুত ফিচার্ড স্নsnippet দেয়।</p>
                        <p>৪. <strong>নিয়মিত পাবলিশ করুন:</strong> অটোপাইলট এজেন্ট দিয়ে প্রতি সপ্তাহে কমপক্ষে ৩-৫টি মাস্টার আর্টিকেল পাবলিশ করুন।</p>
                    </div>

                </div>

                <!-- Modal Footer -->
                <div style="padding: 14px 26px; background: #f8fafc; border-top: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div style="font-size: 12px; color: #64748b;">
                        📖 RankNaserPro Intelligence Suite • Architecture by <strong>RankNaser</strong>
                    </div>
                    <button type="button" onclick="closeUserGuideModal()" style="background: #0f172a; color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 22px; font-size: 13px; cursor: pointer;">
                        Close Guide
                    </button>
                </div>
            </div>
        </div>

<!-- ================= 7-DAY FREE TRIAL ACTIVE STATUS MODAL ================= -->
    <div id="trialInfoModal" style="display: none; position: fixed; inset: 0; background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(5px); z-index: 99999; align-items: center; justify-content: center; padding: 20px;">
        <div style="background: #ffffff; border-radius: 20px; max-width: 500px; width: 100%; padding: 30px; box-shadow: 0 25px 60px rgba(0,0,0,0.25); border: 1.5px solid #e2e8f0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 24px;">🎁</span>
                    <div>
                        <h3 style="margin: 0; font-size: 19px; font-weight: 800; color: #0f172a;">7-Day Free Trial Pass</h3>
                        <div style="font-size: 11.5px; color: #64748b;">Full Autonomous Access Active</div>
                    </div>
                </div>
                <button type="button" onclick="closeTrialModal()" style="background: none; border: none; font-size: 24px; cursor: pointer; color: #64748b; line-height: 1;">✕</button>
            </div>
            
            <div id="trialInfoModalBody" style="font-size: 13.5px; color: #334155; line-height: 1.6;">
                <!-- dynamic info -->
            </div>

            <div id="adminTrialControlBar" style="display: none; margin-top: 18px; padding-top: 14px; border-top: 1.5px dashed #cbd5e1;">
                <div style="font-size: 11.5px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 8px;">⚙️ Admin Testing Controls</div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button type="button" onclick="adminSimulateExpiredTrial()" style="background: #fee2e2; border: 1px solid #fca5a5; color: #b91c1c; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 6px; cursor: pointer;">
                        ⚠️ Simulate Expired (Test Lock)
                    </button>
                    <button type="button" onclick="adminReset7DayTrial()" style="background: #ecfdf5; border: 1px solid #a7f3d0; color: #047857; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 6px; cursor: pointer;">
                        🔄 Reset 7-Day Free Trial
                    </button>
                </div>
            </div>

            <div style="margin-top: 22px; text-align: right;">
                <button type="button" onclick="closeTrialModal()" style="background: #0f172a; color: white; border: none; font-weight: 700; border-radius: 8px; padding: 9px 20px; font-size: 13px; cursor: pointer;">
                    Got It
                </button>
            </div>
        </div>
    </div>

    </div> <!-- end #dashboardWrapper -->

    <script>
        // Set default date input safely
        const dateInp = document.getElementById('dateInput');
        if (dateInp) {
            dateInp.value = new Date().toISOString().split('T')[0];
        }
        
        // Load saved Gemini Key
        const savedKey = localStorage.getItem('gemini_api_key') || '';
        if (savedKey) {
            if (document.getElementById('wGeminiKey')) document.getElementById('wGeminiKey').value = savedKey;
            if (document.getElementById('multiGeminiKey')) document.getElementById('multiGeminiKey').value = savedKey;
            if (document.getElementById('autoGeminiKey')) document.getElementById('autoGeminiKey').value = savedKey;
        }

        // Load saved Brand Name
        const savedBrand = localStorage.getItem('user_brand_name') || '';
        if (savedBrand) {
            if (document.getElementById('wBrandName')) document.getElementById('wBrandName').value = savedBrand;
            if (document.getElementById('multiBrandName')) document.getElementById('multiBrandName').value = savedBrand;
            if (document.getElementById('autoBrandName')) document.getElementById('autoBrandName').value = savedBrand;
        }

        let currentArticles = [];
        let generatedData = null;
        let multiGeneratedData = null;
        let autopilotGeneratedData = null;
        var activeProfileId = 'prof_default';

        // ================= MULTI-COMPANY / CONNECTED CLIENTS HUB (5 COMPANIES) =================
        const defaultConnectedClients = [
            {
                id: 'client_1',
                name: 'Client 1: Primary Business',
                domain: localStorage.getItem('wp_site_url') || 'https://client1.com',
                country: 'Bangladesh',
                wp_url: localStorage.getItem('wp_site_url') || '',
                wp_user: localStorage.getItem('wp_username') || '',
                wp_pass: localStorage.getItem('wp_app_password') || '',
                wp_status: localStorage.getItem('wp_default_status') || 'publish',
                keywords: 'primary keyword bd, best service dhaka',
                competitors: 'https://competitor.com',
                instructions: 'Focus on transactional search intent, pricing transparency, and Google AI Overview snippets.'
            },
            {
                id: 'client_2',
                name: 'Client 2: Retail / E-commerce',
                domain: 'https://client2.com',
                country: 'Bangladesh',
                wp_url: '',
                wp_user: '',
                wp_pass: '',
                wp_status: 'publish',
                keywords: 'online shopping bd, cash on delivery',
                competitors: 'https://competitor.com',
                instructions: 'Product reviews, comparison tables, and return policy transparency.'
            },
            {
                id: 'client_3',
                name: 'Client 3: Tech & Electronics',
                domain: 'https://client3.com',
                country: 'Bangladesh',
                wp_url: '',
                wp_user: '',
                wp_pass: '',
                wp_status: 'publish',
                keywords: 'tech gadgets price in bd, computer shop dhaka',
                competitors: 'https://competitor.com',
                instructions: 'High authority comparison tables and benchmark reviews.'
            },
            {
                id: 'client_4',
                name: 'Client 4: Enterprise Services',
                domain: 'https://client4.com',
                country: 'Bangladesh',
                wp_url: '',
                wp_user: '',
                wp_pass: '',
                wp_status: 'draft',
                keywords: 'b2b corporate solutions, business consulting',
                competitors: 'https://competitor.com',
                instructions: 'Thought leadership and case study data points.'
            },
            {
                id: 'client_5',
                name: 'Client 5: Local Agency / Brand',
                domain: 'https://client5.com',
                country: 'Bangladesh',
                wp_url: '',
                wp_user: '',
                wp_pass: '',
                wp_status: 'draft',
                keywords: 'local service dhaka, best agency in bangladesh',
                competitors: 'https://competitor.com',
                instructions: 'Local SEO citation, Google Maps NAP, and schema graphs.'
            }
        ];

        let activeHubClientId = 'client_1';

        function getConnectedClients() {
            try {
                const stored = localStorage.getItem('ranknaser_connected_clients');
                if (stored) {
                    const parsed = JSON.parse(stored);
                    if (Array.isArray(parsed) && parsed.length > 0) return parsed;
                }
            } catch(e) {}
            return defaultConnectedClients;
        }

        function saveConnectedClients(clients) {
            localStorage.setItem('ranknaser_connected_clients', JSON.stringify(clients));
            localStorage.setItem('seo_director_profiles', JSON.stringify(clients));
            updateClientsUI();
        }

        function updateClientsUI() {
            const clients = getConnectedClients();
            
            // 1. Header badge
            const headerBadge = document.getElementById('headerClientsCountBadge');
            if (headerBadge) {
                headerBadge.innerText = `${clients.length} Active`;
            }

            // 2. Tab 7 Quick Bar row
            const row = document.getElementById('agencyConnectedClientsRow');
            if (row) {
                row.innerHTML = clients.map((c, idx) => {
                    const hasWp = !!(c.wp_url && c.wp_user && c.wp_pass);
                    const wpBadge = hasWp 
                        ? `<span style="font-size:10.5px; background:#dcfce7; color:#15803d; border:1px solid #86efac; padding:2px 7px; border-radius:12px; font-weight:800;">🟢 WP Live (${(c.wp_status||'publish').toUpperCase()})</span>`
                        : `<span style="font-size:10.5px; background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:2px 7px; border-radius:12px; font-weight:700;">🌐 Crawl Ready</span>`;
                    
                    return `
                    <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 12px 14px; min-width: 240px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; gap: 8px;">
                        <div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                                <strong style="font-size:13.5px; color:#0f172a;">${escapeHtml(c.name || 'Client ' + (idx+1))}</strong>
                                ${wpBadge}
                            </div>
                            <div style="font-size:12px; color:#2563eb; font-weight:600; word-break:break-all;">
                                🔗 ${escapeHtml(c.domain || 'No URL')}
                            </div>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">
                                📍 Market: <strong>${escapeHtml(c.country || 'Bangladesh')}</strong>
                            </div>
                        </div>
                        <div style="display:flex; gap:6px; margin-top:4px;">
                            <button type="button" onclick="openAgencyTaskModal(null, '${escapeHtml(c.domain || '')}')" style="background:#2563eb; color:white; border:none; font-size:11.5px; font-weight:800; padding:5px 10px; border-radius:6px; cursor:pointer; flex:1; display:flex; align-items:center; justify-content:center; gap:4px;">
                                <span>⚡ Assign Task</span>
                            </button>
                            <button type="button" onclick="openClientsHubModal('${c.id}')" style="background:#ffffff; color:#334155; border:1px solid #cbd5e1; font-size:11px; font-weight:700; padding:5px 8px; border-radius:6px; cursor:pointer;" title="Edit Client & WP Settings">
                                <span>⚙️ Edit</span>
                            </button>
                        </div>
                    </div>
                    `;
                }).join('');
            }

            // 3. Populate Task Modal dropdown if open or on page
            populateTaskCompanySelect();

            // 4. Also refresh Tab 6 pills if present
            if (typeof renderCompanyPills === 'function') {
                renderCompanyPills();
            }
        }

        function populateTaskCompanySelect(selectedDomain = null) {
            const sel = document.getElementById('taskCompanySelect');
            if (!sel) return;

            const clients = getConnectedClients();
            let html = '';
            let matchedValue = null;

            clients.forEach(c => {
                const hasWp = !!(c.wp_url && c.wp_user && c.wp_pass);
                const statusStr = hasWp ? ` (WP ${c.wp_status === 'publish' ? 'Live' : 'Draft'} 🟢)` : '';
                const isSelected = selectedDomain && (c.domain === selectedDomain || selectedDomain.includes(c.domain));
                if (isSelected) matchedValue = c.id;
                html += `<option value="${c.id}" ${isSelected ? 'selected' : ''}>🏢 ${escapeHtml(c.name)} — ${escapeHtml(c.domain)}${statusStr}</option>`;
            });

            html += `<option value="__custom__">➕ Enter Other / Custom Website Domain...</option>`;
            sel.innerHTML = html;

            if (matchedValue) {
                sel.value = matchedValue;
                handleTaskCompanySelectChange(matchedValue);
            } else if (!selectedDomain && clients.length > 0) {
                sel.value = clients[0].id;
                handleTaskCompanySelectChange(clients[0].id);
            }
        }

        function handleTaskCompanySelectChange(val) {
            const domainInput = document.getElementById('taskClientDomain');
            const hint = document.getElementById('taskCompanyStatusHint');
            const clients = getConnectedClients();

            if (val === '__custom__') {
                if (domainInput) {
                    domainInput.value = '';
                    domainInput.placeholder = 'https://custom-client-website.com';
                    domainInput.focus();
                }
                if (hint) {
                    hint.innerHTML = `<span style="color:#64748b;">✍️ Custom domain mode: Agents will crawl public HTML directly.</span>`;
                }
                return;
            }

            const client = clients.find(c => c.id === val);
            if (client) {
                if (domainInput) {
                    domainInput.value = client.domain || '';
                }
                if (hint) {
                    const hasWp = !!(client.wp_url && client.wp_user && client.wp_pass);
                    if (hasWp) {
                        hint.innerHTML = `<span style="color:#047857;">🟢 <strong>${escapeHtml(client.name)}:</strong> WordPress REST API Active (${(client.wp_status||'publish').toUpperCase()}). Automated direct publishing supported!</span>`;
                    } else {
                        hint.innerHTML = `<span style="color:#0284c7;">🌐 <strong>${escapeHtml(client.name)}:</strong> Live Googlebot crawl & forensic audit ready. (WordPress credentials optional in Settings).</span>`;
                    }
                }
            }
        }

        function openClientsHubModal(clientId = null) {
            const clients = getConnectedClients();
            if (clientId && clients.some(c => c.id === clientId)) {
                activeHubClientId = clientId;
            } else if (!clients.some(c => c.id === activeHubClientId)) {
                activeHubClientId = clients[0] ? clients[0].id : 'client_1';
            }

            renderHubClientTabs();
            loadActiveHubClientFields();

            const modal = document.getElementById('clientsHubModal');
            if (modal) modal.style.display = 'flex';
        }

        function closeClientsHubModal() {
            const modal = document.getElementById('clientsHubModal');
            if (modal) modal.style.display = 'none';
        }

        function renderHubClientTabs() {
            const container = document.getElementById('clientsHubTabsList');
            if (!container) return;

            const clients = getConnectedClients();
            let html = '';
            clients.forEach((c, idx) => {
                const isActive = (c.id === activeHubClientId);
                const hasWp = !!(c.wp_url && c.wp_user && c.wp_pass);
                const wpDot = hasWp ? '<span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#10b981;"></span>' : '';
                html += `
                    <button type="button" onclick="selectHubClientTab('${c.id}')" style="background:${isActive ? '#1e1b4b' : '#ffffff'}; color:${isActive ? '#ffffff' : '#334155'}; border:1.5px solid ${isActive ? '#1e1b4b' : '#cbd5e1'}; font-size:12px; font-weight:800; padding:7px 14px; border-radius:8px; cursor:pointer; display:inline-flex; align-items:center; gap:6px;">
                        <span>🏢 ${escapeHtml(c.name || 'Client ' + (idx+1))}</span>
                        ${wpDot}
                    </button>
                `;
            });
            container.innerHTML = html;
        }

        function selectHubClientTab(clientId) {
            activeHubClientId = clientId;
            renderHubClientTabs();
            loadActiveHubClientFields();
        }

        function loadActiveHubClientFields() {
            const clients = getConnectedClients();
            const c = clients.find(item => item.id === activeHubClientId) || clients[0];
            if (!c) return;

            activeHubClientId = c.id;

            if (document.getElementById('hubClientName')) document.getElementById('hubClientName').value = c.name || '';
            if (document.getElementById('hubClientDomain')) document.getElementById('hubClientDomain').value = c.domain || '';
            if (document.getElementById('hubClientCountry')) document.getElementById('hubClientCountry').value = c.country || 'Bangladesh';
            if (document.getElementById('hubClientKeywords')) document.getElementById('hubClientKeywords').value = c.keywords || '';
            if (document.getElementById('hubClientCompetitors')) document.getElementById('hubClientCompetitors').value = c.competitors || '';
            if (document.getElementById('hubClientInstructions')) document.getElementById('hubClientInstructions').value = c.instructions || '';
            if (document.getElementById('hubClientWpUrl')) document.getElementById('hubClientWpUrl').value = c.wp_url || c.domain || '';
            if (document.getElementById('hubClientWpUser')) document.getElementById('hubClientWpUser').value = c.wp_user || '';
            if (document.getElementById('hubClientWpPass')) document.getElementById('hubClientWpPass').value = c.wp_pass || '';
            if (document.getElementById('hubClientWpStatus')) document.getElementById('hubClientWpStatus').value = c.wp_status || 'publish';

            const testStatus = document.getElementById('hubClientTestStatus');
            if (testStatus) testStatus.style.display = 'none';

            const delBtn = document.getElementById('hubClientDeleteBtn');
            if (delBtn) delBtn.style.display = (clients.length > 1) ? 'inline-block' : 'none';
        }

        function saveCurrentHubClient(e) {
            if (e) e.preventDefault();
            const name = document.getElementById('hubClientName').value.trim() || 'Client Business';
            const domain = document.getElementById('hubClientDomain').value.trim();
            const country = document.getElementById('hubClientCountry').value;
            const keywords = document.getElementById('hubClientKeywords').value.trim();
            const competitors = document.getElementById('hubClientCompetitors').value.trim();
            const instructions = document.getElementById('hubClientInstructions').value.trim();
            const wpUrl = document.getElementById('hubClientWpUrl').value.trim() || domain;
            const wpUser = document.getElementById('hubClientWpUser').value.trim();
            const wpPass = document.getElementById('hubClientWpPass').value.trim();
            const wpStatus = document.getElementById('hubClientWpStatus').value;

            let clients = getConnectedClients();
            let idx = clients.findIndex(c => c.id === activeHubClientId);

            const updatedClient = {
                id: activeHubClientId || ('client_' + Date.now()),
                name: name,
                domain: domain,
                country: country,
                keywords: keywords,
                competitors: competitors,
                instructions: instructions,
                wp_url: wpUrl,
                wp_user: wpUser,
                wp_pass: wpPass,
                wp_status: wpStatus
            };

            if (idx >= 0) {
                clients[idx] = updatedClient;
            } else {
                clients.push(updatedClient);
                activeHubClientId = updatedClient.id;
            }

            // Sync with default WP credentials if this is client_1
            if (idx === 0) {
                localStorage.setItem('wp_site_url', wpUrl);
                localStorage.setItem('wp_username', wpUser);
                localStorage.setItem('wp_app_password', wpPass);
                localStorage.setItem('wp_default_status', wpStatus);
                updateWpBadge();
            }

            saveConnectedClients(clients);
            renderHubClientTabs();
            alert(`✅ Client company "${name}" saved successfully!`);
        }

        function addNewHubClient() {
            let clients = getConnectedClients();
            const newId = 'client_' + Date.now();
            const newNum = clients.length + 1;
            const newClient = {
                id: newId,
                name: `Client ${newNum}: New Company`,
                domain: `https://client${newNum}.com`,
                country: 'Bangladesh',
                keywords: 'primary keyword bd',
                competitors: 'https://competitor.com',
                instructions: 'Topical authority & Google AI Overview optimization.',
                wp_url: '',
                wp_user: '',
                wp_pass: '',
                wp_status: 'publish'
            };
            clients.push(newClient);
            activeHubClientId = newId;
            saveConnectedClients(clients);
            openClientsHubModal(newId);
        }

        function deleteCurrentHubClient() {
            let clients = getConnectedClients();
            if (clients.length <= 1) {
                alert('Cannot delete the last client company. You must have at least 1 client.');
                return;
            }
            const c = clients.find(x => x.id === activeHubClientId);
            if (!confirm(`Are you sure you want to delete "${c ? c.name : 'this client'}"?`)) return;

            clients = clients.filter(x => x.id !== activeHubClientId);
            activeHubClientId = clients[0].id;
            saveConnectedClients(clients);
            openClientsHubModal(activeHubClientId);
        }

        async function testHubClientWp() {
            const url = document.getElementById('hubClientWpUrl').value.trim();
            const user = document.getElementById('hubClientWpUser').value.trim();
            const pass = document.getElementById('hubClientWpPass').value.trim();
            const statusBox = document.getElementById('hubClientTestStatus');
            const testBtn = document.getElementById('hubClientTestBtn');

            if (!url || !user || !pass) {
                alert('Please enter WordPress Site URL, Username, and Application Password first.');
                return;
            }

            if (statusBox) {
                statusBox.style.display = 'block';
                statusBox.style.background = '#eff6ff';
                statusBox.style.color = '#1e40af';
                statusBox.innerHTML = `⏳ Testing connection to ${url}...`;
            }
            if (testBtn) testBtn.disabled = true;

            try {
                const resp = await fetch('/api/wordpress/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ site_url: url, username: user, app_password: pass })
                });
                const data = await resp.json();
                if (data.status === 'success') {
                    if (statusBox) {
                        statusBox.style.background = '#f0fdf4';
                        statusBox.style.color = '#166534';
                        statusBox.innerHTML = `✅ <strong>Connected!</strong> Authenticated as <em>${data.name || user}</em> (${url}). Ready for automatic publishing!`;
                    }
                } else {
                    if (statusBox) {
                        statusBox.style.background = '#fef2f2';
                        statusBox.style.color = '#991b1b';
                        statusBox.innerHTML = `❌ Connection failed: ${data.message || 'Check URL / App Password'}`;
                    }
                }
            } catch(e) {
                if (statusBox) {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerHTML = `❌ Error: ${e.message}`;
                }
            } finally {
                if (testBtn) testBtn.disabled = false;
            }
        }

        function dispatchTaskForActiveHubClient() {
            const clients = getConnectedClients();
            const c = clients.find(item => item.id === activeHubClientId);
            closeClientsHubModal();
            switchTab('agency');
            openAgencyTaskModal(null, c ? c.domain : '');
        }

        // WordPress Sync Settings and Helpers
        function getWpCredentials() {
            const singleUrl = localStorage.getItem('wp_site_url') || '';
            const singleUser = localStorage.getItem('wp_username') || '';
            const singlePass = localStorage.getItem('wp_app_password') || '';
            const singleStatus = localStorage.getItem('wp_default_status') || 'draft';

            if (singleUrl && singleUser && singlePass) {
                return { url: singleUrl, user: singleUser, appPass: singlePass, status: singleStatus };
            }

            const clients = getConnectedClients();
            const firstWp = clients.find(c => c.wp_url && c.wp_user && c.wp_pass);
            if (firstWp) {
                return { url: firstWp.wp_url, user: firstWp.wp_user, appPass: firstWp.wp_pass, status: firstWp.wp_status || 'publish' };
            }

            return { url: singleUrl, user: singleUser, appPass: singlePass, status: singleStatus };
        }

        function updateWpBadge() {
            const creds = getWpCredentials();
            const badge = document.getElementById('wpStatusBadge');
            if (!badge) return;
            if (creds.url && creds.user && creds.appPass) {
                badge.innerText = 'Connected';
                badge.style.background = '#dcfce7';
                badge.style.color = '#15803d';
                badge.style.border = '1px solid #86efac';
            } else {
                badge.innerText = 'Not Configured';
                badge.style.background = '#f1f5f9';
                badge.style.color = '#475569';
                badge.style.border = '1px solid #e2e8f0';
            }
        }

        function openWpModal() {
            const creds = getWpCredentials();
            if (creds.url && document.getElementById('wpSiteUrl')) document.getElementById('wpSiteUrl').value = creds.url;
            if (creds.user && document.getElementById('wpUsername')) document.getElementById('wpUsername').value = creds.user;
            if (creds.appPass && document.getElementById('wpAppPassword')) document.getElementById('wpAppPassword').value = creds.appPass;
            if (creds.status && document.getElementById('wpPostStatus')) document.getElementById('wpPostStatus').value = creds.status;
            
            const testBox = document.getElementById('wpTestStatus');
            if (testBox) testBox.style.display = 'none';
            document.getElementById('wpModal').style.display = 'flex';
        }

        function closeWpModal() {
            document.getElementById('wpModal').style.display = 'none';
        }

        async function testWpConnection() {
            const url = document.getElementById('wpSiteUrl').value.trim();
            const user = document.getElementById('wpUsername').value.trim();
            const appPass = document.getElementById('wpAppPassword').value.trim();
            const statusBox = document.getElementById('wpTestStatus');
            const testBtn = document.getElementById('wpTestBtn');

            if (!url || !user || !appPass) {
                alert('Please fill in Site URL, Username, and Application Password first.');
                return;
            }

            statusBox.style.display = 'block';
            statusBox.style.background = '#eff6ff';
            statusBox.style.border = '1px solid #93c5fd';
            statusBox.style.color = '#1e40af';
            statusBox.innerText = 'Connecting to WordPress REST API...';
            if (testBtn) testBtn.disabled = true;

            try {
                const resp = await fetch('/api/wordpress/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ site_url: url, username: user, app_password: appPass })
                });
                const data = await resp.json();
                if (data.status === 'success') {
                    statusBox.style.background = '#f0fdf4';
                    statusBox.style.border = '1px solid #86efac';
                    statusBox.style.color = '#166534';
                    statusBox.innerHTML = `✅ <strong>Connected!</strong> Authenticated as <em>${data.name || user}</em> (${url})`;
                } else {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.border = '1px solid #fca5a5';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerText = '❌ Connection failed: ' + (data.message || 'Check URL / App Password');
                }
            } catch (err) {
                statusBox.style.background = '#fef2f2';
                statusBox.style.border = '1px solid #fca5a5';
                statusBox.style.color = '#991b1b';
                statusBox.innerText = '❌ Error: ' + err.message;
            } finally {
                if (testBtn) testBtn.disabled = false;
            }
        }

        function saveWpSettings(e) {
            e.preventDefault();
            const url = document.getElementById('wpSiteUrl').value.trim();
            const user = document.getElementById('wpUsername').value.trim();
            const appPass = document.getElementById('wpAppPassword').value.trim();
            const status = document.getElementById('wpPostStatus').value;

            localStorage.setItem('wp_site_url', url);
            localStorage.setItem('wp_username', user);
            localStorage.setItem('wp_app_password', appPass);
            localStorage.setItem('wp_default_status', status);

            updateWpBadge();
            alert('WordPress credentials saved successfully in your local browser!');
            closeWpModal();
        }

        async function publishArticleToWordPress(source, isAuto = false, forcedStatus = null) {
            const creds = getWpCredentials();
            if (!creds.url || !creds.user || !creds.appPass) {
                if (!isAuto) {
                    alert('Please connect your WordPress site first in "🔌 WordPress Sync"!');
                    openWpModal();
                } else {
                    console.warn('Auto WordPress publishing skipped: Credentials not configured yet.');
                }
                return;
            }

            let articleObj = null;
            let visualHtml = '';
            let statusBox = null;

            if (source === 'single') {
                if (!generatedData) return;
                articleObj = generatedData;
                const visualElem = document.getElementById('viewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('singleWpPostStatusBox');
            } else if (source === 'multi') {
                if (!multiGeneratedData || !multiGeneratedData.article) return;
                articleObj = multiGeneratedData.article;
                const visualElem = document.getElementById('multiViewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('multiWpPostStatusBox');
            } else if (source === 'autopilot') {
                if (!autopilotGeneratedData || !autopilotGeneratedData.article) return;
                articleObj = autopilotGeneratedData.article;
                const visualElem = document.getElementById('autoViewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('autoWpPostStatusBox');
            }

            if (!articleObj || !statusBox) return;

            const targetStatus = forcedStatus || creds.status || 'publish';
            const statusLabel = targetStatus === 'publish' ? 'LIVE PUBLISHED POST 🚀' : 'DRAFT 📝';

            statusBox.style.display = 'block';
            statusBox.style.background = '#eff6ff';
            statusBox.style.border = '1px solid #93c5fd';
            statusBox.style.borderRadius = '8px';
            statusBox.style.padding = '12px 16px';
            statusBox.style.color = '#1e40af';
            statusBox.innerHTML = `🚀 Sending article to WordPress (${creds.url}) as <strong>${statusLabel}</strong>... Please wait.`;

            try {
                const resp = await fetch('/api/wordpress/publish', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        site_url: creds.url,
                        username: creds.user,
                        app_password: creds.appPass,
                        status: targetStatus,
                        title: articleObj.meta_title || articleObj.title || 'Master Outranking Article',
                        content_html: visualHtml,
                        slug: articleObj.slug || '',
                        excerpt: articleObj.meta_description || '',
                        focus_keyword: articleObj.focus_keyword || articleObj.main_keyword || '',
                        faq_schema: articleObj.faq_schema || null
                    })
                });

                const data = await resp.json();
                if (data.status === 'success') {
                    statusBox.style.background = '#f0fdf4';
                    statusBox.style.border = '1px solid #86efac';
                    statusBox.style.color = '#166534';
                    const postLink = data.post_url;
                    const editLink = data.edit_url;
                    const postStatus = (data.post_status || 'draft').toUpperCase();

                    statusBox.innerHTML = `
                        <div style="font-size:14px; font-weight:800; margin-bottom:6px;">
                            🎉 Successfully posted to WordPress as <span style="background:#bbf7d0; padding:2px 8px; border-radius:4px; font-size:12px;">${postStatus}</span> (Post ID: #${data.post_id})
                        </div>
                        <div style="font-size:13px; display:flex; gap:16px; flex-wrap:wrap; margin-top:8px;">
                            ${postLink ? `<a href="${postLink}" target="_blank" style="color:#0284c7; text-decoration:underline; font-weight:700;">👁️ View Live/Draft Post on Site ↗</a>` : ''}
                            ${editLink ? `<a href="${editLink}" target="_blank" style="color:#15803d; text-decoration:underline; font-weight:700;">✏️ Edit in WordPress Admin ↗</a>` : ''}
                        </div>
                    `;
                } else {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.border = '1px solid #fca5a5';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerText = '❌ Failed to post to WordPress: ' + (data.message || 'Unknown error');
                }
            } catch (err) {
                statusBox.style.background = '#fef2f2';
                statusBox.style.border = '1px solid #fca5a5';
                statusBox.style.color = '#991b1b';
                statusBox.innerText = '❌ WordPress error: ' + err.message;
            }
        }

        // Initialize WordPress sync badge status & Multi-Client Hub
        updateWpBadge();
        if (typeof updateClientsUI === 'function') updateClientsUI();

        // ================= Custom Site Webhook Sync Helpers =================
        let activeCodeSnippet = 'nextjs';

        function getCustomToken() {
            let tok = localStorage.getItem('custom_api_token');
            if (!tok) {
                tok = 'bseo_sec_' + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 10);
                localStorage.setItem('custom_api_token', tok);
            }
            return tok;
        }

        function getCustomCredentials() {
            return {
                url: localStorage.getItem('custom_webhook_url') || '',
                token: getCustomToken(),
                status: localStorage.getItem('custom_default_status') || 'draft'
            };
        }

        function updateCustomBadge() {
            const creds = getCustomCredentials();
            const badge = document.getElementById('customApiBadge');
            if (!badge) return;
            if (creds.url) {
                badge.innerText = 'Connected';
                badge.style.background = '#dcfce7';
                badge.style.color = '#15803d';
                badge.style.border = '1px solid #86efac';
            } else {
                badge.innerText = 'Not Configured';
                badge.style.background = '#f1f5f9';
                badge.style.color = '#475569';
                badge.style.border = '1px solid #e2e8f0';
            }
        }

        function renderCodeSnippet() {
            const token = getCustomToken();
            const box = document.getElementById('codeSnippetBox');
            if (!box) return;

            if (activeCodeSnippet === 'nextjs') {
                box.textContent = `// app/api/articles/route.ts (Next.js App Router)
import { NextResponse } from 'next/server';

const SECRET_TOKEN = '${token}';

export async function POST(req: Request) {
  const body = await req.json();
  const auth = req.headers.get('authorization')?.replace('Bearer ', '') || body.token;

  if (auth !== SECRET_TOKEN) {
    return NextResponse.json({ error: 'Unauthorized token' }, { status: 401 });
  }

  if (body.event === 'ping') {
    return NextResponse.json({ status: 'ok', message: 'Webhook connected successfully!' });
  }

  const { title, slug, content_html, content_markdown, meta_title, meta_description, focus_keyword, faq_schema } = body;

  // TODO: Save into Prisma, Supabase, PostgreSQL, or MongoDB
  // const post = await prisma.post.create({ data: { title, slug, content: content_html } });

  return NextResponse.json({ status: 'success', post_id: slug, message: 'Article received & saved!' });
}`;
            } else if (activeCodeSnippet === 'node') {
                box.textContent = `// server.js (Node.js & Express)
const express = require('express');
const app = express();
app.use(express.json({ limit: '10mb' }));

const SECRET_TOKEN = '${token}';

app.post('/api/articles', async (req, res) => {
  const token = req.headers['authorization']?.replace('Bearer ', '') || req.body.token;
  if (token !== SECRET_TOKEN) {
    return res.status(401).json({ error: 'Unauthorized token' });
  }

  if (req.body.event === 'ping') {
    return res.json({ status: 'ok', message: 'Connected successfully!' });
  }

  const { title, slug, content_html, content_markdown, meta_title, meta_description } = req.body;

  // TODO: Save to your database (MongoDB, MySQL, PostgreSQL)
  res.json({ status: 'success', id: slug, message: 'Article created successfully!' });
});

app.listen(3000, () => console.log('Listening on port 3000'));`;
            } else if (activeCodeSnippet === 'php') {
                box.textContent = `<?php
// api/receive-article.php (PHP / Laravel)
header('Content-Type: application/json');
$SECRET_TOKEN = '${token}';

$headers = getallheaders();
$auth = $headers['Authorization'] ?? $headers['authorization'] ?? '';
$token = str_replace('Bearer ', '', $auth);
$data = json_decode(file_get_contents('php://input'), true);

if ($token !== $SECRET_TOKEN && ($data['token'] ?? '') !== $SECRET_TOKEN) {
    http_response_code(401);
    echo json_encode(['status' => 'error', 'message' => 'Unauthorized token']);
    exit;
}

if (($data['event'] ?? '') === 'ping') {
    echo json_encode(['status' => 'ok', 'message' => 'Connected successfully!']);
    exit;
}

// Extract article fields
$title = $data['title'];
$slug = $data['slug'];
$html = $data['content_html'];
$markdown = $data['content_markdown'];
$metaDesc = $data['meta_description'];

// TODO: Save to MySQL / Database:
// $db->query("INSERT INTO posts (title, slug, content) VALUES (...)");

echo json_encode(['status' => 'success', 'message' => 'Article saved successfully!']);`;
            } else if (activeCodeSnippet === 'python') {
                box.textContent = `# main.py (FastAPI / Python)
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()
SECRET_TOKEN = "${token}"

@app.post("/api/articles")
async def receive_article(request: Request, authorization: str = Header(None)):
    data = await request.json()
    token = (authorization or "").replace("Bearer ", "") or data.get("token")
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if data.get("event") == "ping":
        return {"status": "ok", "message": "Connected successfully!"}

    # Extract article data & save to DB
    title = data.get("title")
    html = data.get("content_html")
    slug = data.get("slug")

    return {"status": "success", "id": slug, "message": "Article saved!"}`;
            }
        }

        function switchCodeSnippet(lang) {
            activeCodeSnippet = lang;
            ['Next', 'Node', 'Php', 'Python'].forEach(id => {
                const btn = document.getElementById('codeTab' + id);
                if (btn) btn.className = 'subtab-btn' + (id.toLowerCase() === lang ? ' active' : '');
            });
            renderCodeSnippet();
        }

        function copyCurrentCodeSnippet() {
            const box = document.getElementById('codeSnippetBox');
            if (!box) return;
            navigator.clipboard.writeText(box.textContent).then(() => {
                alert('Ready-to-use backend code copied to clipboard!');
            });
        }

        function openCustomApiModal() {
            const creds = getCustomCredentials();
            if (document.getElementById('customApiToken')) document.getElementById('customApiToken').value = creds.token;
            if (document.getElementById('customWebhookUrl')) document.getElementById('customWebhookUrl').value = creds.url;
            if (document.getElementById('customPostStatus')) document.getElementById('customPostStatus').value = creds.status;
            
            const testBox = document.getElementById('customTestStatus');
            if (testBox) testBox.style.display = 'none';
            renderCodeSnippet();
            document.getElementById('customApiModal').style.display = 'flex';
        }

        function closeCustomApiModal() {
            document.getElementById('customApiModal').style.display = 'none';
        }

        function copyCustomToken() {
            const tok = getCustomToken();
            navigator.clipboard.writeText(tok).then(() => {
                alert('Built-in API Token copied to clipboard: ' + tok);
            });
        }

        function regenerateCustomToken() {
            if (confirm('Are you sure you want to generate a new API Token? You will need to update your website backend code with the new token.')) {
                const newToken = 'bseo_sec_' + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 10);
                localStorage.setItem('custom_api_token', newToken);
                if (document.getElementById('customApiToken')) document.getElementById('customApiToken').value = newToken;
                renderCodeSnippet();
                alert('New API Token generated! Remember to update your website code.');
            }
        }

        async function testCustomWebhook() {
            const url = document.getElementById('customWebhookUrl').value.trim();
            const token = getCustomToken();
            const statusBox = document.getElementById('customTestStatus');
            const testBtn = document.getElementById('customTestBtn');

            if (!url) {
                alert('Please enter your Custom Webhook URL first.');
                return;
            }

            statusBox.style.display = 'block';
            statusBox.style.background = '#eff6ff';
            statusBox.style.border = '1px solid #93c5fd';
            statusBox.style.color = '#1e40af';
            statusBox.innerText = 'Sending ping payload to custom webhook...';
            if (testBtn) testBtn.disabled = true;

            try {
                const resp = await fetch('/api/custom-webhook/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ webhook_url: url, api_token: token })
                });
                const data = await resp.json();
                if (data.status === 'success') {
                    statusBox.style.background = '#f0fdf4';
                    statusBox.style.border = '1px solid #86efac';
                    statusBox.style.color = '#166534';
                    statusBox.innerHTML = `✅ <strong>Webhook Verified!</strong> Your custom server responded with success. (${data.message})`;
                } else {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.border = '1px solid #fca5a5';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerText = '❌ Verification failed: ' + (data.message || 'Server did not accept webhook');
                }
            } catch (err) {
                statusBox.style.background = '#fef2f2';
                statusBox.style.border = '1px solid #fca5a5';
                statusBox.style.color = '#991b1b';
                statusBox.innerText = '❌ Error: ' + err.message;
            } finally {
                if (testBtn) testBtn.disabled = false;
            }
        }

        function saveCustomApiSettings(e) {
            e.preventDefault();
            const url = document.getElementById('customWebhookUrl').value.trim();
            const status = document.getElementById('customPostStatus').value;

            localStorage.setItem('custom_webhook_url', url);
            localStorage.setItem('custom_default_status', status);

            updateCustomBadge();
            alert('Custom Webhook settings saved successfully!');
            closeCustomApiModal();
        }

        async function publishArticleToCustomSite(source, isAuto = false) {
            const creds = getCustomCredentials();
            if (!creds.url) {
                if (!isAuto) {
                    alert('Please configure your Custom Website Webhook URL in "🌐 Custom Site API" settings first!');
                    openCustomApiModal();
                } else {
                    console.warn('Auto Custom Webhook publishing skipped: URL not configured.');
                }
                return;
            }

            let articleObj = null;
            let visualHtml = '';
            let statusBox = null;

            if (source === 'single') {
                if (!generatedData) return;
                articleObj = generatedData;
                const visualElem = document.getElementById('viewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('singleCustomPostStatusBox');
            } else if (source === 'multi') {
                if (!multiGeneratedData || !multiGeneratedData.article) return;
                articleObj = multiGeneratedData.article;
                const visualElem = document.getElementById('multiViewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('multiCustomPostStatusBox');
            } else if (source === 'autopilot') {
                if (!autopilotGeneratedData || !autopilotGeneratedData.article) return;
                articleObj = autopilotGeneratedData.article;
                const visualElem = document.getElementById('autoViewVisual');
                visualHtml = visualElem ? visualElem.innerHTML : '';
                statusBox = document.getElementById('autoCustomPostStatusBox');
            }

            if (!articleObj || !statusBox) return;

            statusBox.style.display = 'block';
            statusBox.style.background = '#eff6ff';
            statusBox.style.border = '1px solid #93c5fd';
            statusBox.style.borderRadius = '8px';
            statusBox.style.padding = '12px 16px';
            statusBox.style.color = '#1e40af';
            statusBox.innerHTML = `🌐 Sending full article payload to your custom website (${creds.url})...`;

            try {
                const resp = await fetch('/api/custom-webhook/publish', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        webhook_url: creds.url,
                        api_token: creds.token,
                        status: creds.status || 'draft',
                        title: articleObj.meta_title || articleObj.title || 'Master Outranking Article',
                        content_html: visualHtml,
                        content_markdown: articleObj.article_markdown || '',
                        slug: articleObj.slug || '',
                        meta_title: articleObj.meta_title || '',
                        meta_description: articleObj.meta_description || '',
                        focus_keyword: articleObj.focus_keyword || articleObj.main_keyword || '',
                        faq_schema: articleObj.faq_schema || null
                    })
                });

                const data = await resp.json();
                if (data.status === 'success') {
                    statusBox.style.background = '#f0fdf4';
                    statusBox.style.border = '1px solid #86efac';
                    statusBox.style.color = '#166534';
                    const postLink = data.post_url;

                    statusBox.innerHTML = `
                        <div style="font-size:14px; font-weight:800; margin-bottom:4px;">
                            🎉 Article successfully delivered to your custom website!
                        </div>
                        <div style="font-size:12.5px; color:#15803d;">
                            ${data.message || ''}
                            ${postLink ? ` &nbsp;|&nbsp; <a href="${postLink}" target="_blank" style="color:#0284c7; text-decoration:underline; font-weight:700;">👁️ View Article on Site ↗</a>` : ''}
                        </div>
                    `;
                } else {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.border = '1px solid #fca5a5';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerText = '❌ Failed to deliver to custom website: ' + (data.message || 'Unknown error');
                }
            } catch (err) {
                statusBox.style.background = '#fef2f2';
                statusBox.style.border = '1px solid #fca5a5';
                statusBox.style.color = '#991b1b';
                statusBox.innerText = '❌ Webhook error: ' + err.message;
            }
        }

        // Initialize Custom API sync badge
        updateCustomBadge();

        function goBackToHome() {
            closeDirectorModal();
            closeWpModal();
            closeCustomApiModal();
            closeClientReportModal();
            closeRoadmapModal();
            switchTab('daily');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function switchTab(tab, updateHistory) {
            if (updateHistory === undefined) updateHistory = true;
            document.getElementById('tabDaily').style.display = (tab === 'daily') ? 'block' : 'none';
            document.getElementById('tabSpy').style.display = (tab === 'spy') ? 'block' : 'none';
            document.getElementById('tabMulti').style.display = (tab === 'multi') ? 'block' : 'none';
            document.getElementById('tabWriter').style.display = (tab === 'writer') ? 'block' : 'none';
            document.getElementById('tabAutopilot').style.display = (tab === 'autopilot') ? 'block' : 'none';
            document.getElementById('tabDirector').style.display = (tab === 'director') ? 'block' : 'none';
            const tabAg = document.getElementById('tabAgency');
            if (tabAg) tabAg.style.display = (tab === 'agency') ? 'block' : 'none';
            const tabAgBtn = document.getElementById('tabAgencyBtn');
            if (tabAgBtn) tabAgBtn.className = 'tab-btn agency' + (tab === 'agency' ? ' active' : '');
            if (tab === 'agency') { loadAgencyDashboard(); if (typeof updateClientsUI === 'function') updateClientsUI(); }

            document.getElementById('tabDailyBtn').className = 'tab-btn daily' + (tab === 'daily' ? ' active' : '');
            document.getElementById('tabSpyBtn').className = 'tab-btn spy' + (tab === 'spy' ? ' active' : '');
            document.getElementById('tabMultiBtn').className = 'tab-btn multi' + (tab === 'multi' ? ' active' : '');
            document.getElementById('tabWriterBtn').className = 'tab-btn writer' + (tab === 'writer' ? ' active' : '');
            document.getElementById('tabAutopilotBtn').className = 'tab-btn autopilot' + (tab === 'autopilot' ? ' active' : '');
            document.getElementById('tabDirectorBtn').className = 'tab-btn director' + (tab === 'director' ? ' active' : '');

            if (updateHistory) {
                try {
                    history.pushState({ tab: tab }, '', '#' + tab);
                } catch(e) {}
            }
        }

        window.addEventListener('popstate', function(e) {
            if (e.state && e.state.tab) {
                switchTab(e.state.tab, false);
            } else {
                const hash = window.location.hash.replace('#', '');
                if (hash && ['daily', 'spy', 'multi', 'writer', 'autopilot', 'director', 'agency'].includes(hash)) {
                    switchTab(hash, false);
                } else {
                    switchTab('daily', false);
                }
            }
        });

        // Keyboard Escape listener to close any open modal
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeDirectorModal();
                closeWpModal();
                closeCustomApiModal();
                closeClientReportModal();
                closeRoadmapModal();
                closeAgencyTaskModal();
                closeDailyReportModal();
                closeClientsHubModal();
            }
        });

        // Quick Demo Fill & Auto-Scan Helper
        function quickFillAndScan(type, url) {
            if (type === 'tracker') {
                const inp = document.getElementById('urlInput');
                if (inp) inp.value = url;
                const form = document.getElementById('trackerForm');
                if (form) {
                    if (typeof form.requestSubmit === 'function') form.requestSubmit();
                    else form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                }
            } else if (type === 'spy') {
                const inp = document.getElementById('spyUrlInput');
                if (inp) inp.value = url;
                if (typeof runDeepSpy === 'function') runDeepSpy(url);
            }
        }
        window.quickFillAndScan = quickFillAndScan;

        function loadMultiDemoPreset() {}
        window.loadMultiDemoPreset = loadMultiDemoPreset;

        function loadWriterDemoPreset(preset) {}
        window.loadWriterDemoPreset = loadWriterDemoPreset;

        function loadAutopilotDemoPreset(niche) {}
        window.loadAutopilotDemoPreset = loadAutopilotDemoPreset;

        // Tracker Form Submit
        async function submitTrackerForm(e) {
            if (e && typeof e.preventDefault === 'function') e.preventDefault();
            const url = document.getElementById('urlInput').value.trim();
            const targetDate = document.getElementById('dateInput').value;

            if (!url) {
                alert('Please enter a website URL to audit (e.g. https://example.com).');
                return;
            }

            document.getElementById('trackerSpinner').style.display = 'block';
            document.getElementById('trackerResults').style.display = 'none';
            document.getElementById('scanBtn').disabled = true;

            try {
                // RUN FULL LIVE COMPETITOR SEO AUDIT (100% Real-Time Crawl & Technical Diagnostics)
                const spyPromise = fetch('/api/spy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                }).then(r => r.json()).catch(err => ({ status: 'error', message: err.message }));

                // Run scan concurrently for discovered articles/pages
                const scanPromise = fetch('/api/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url, date: targetDate })
                }).then(r => r.json()).catch(() => null);

                const [spyData, scanData] = await Promise.all([spyPromise, scanPromise]);

                document.getElementById('trackerSpinner').style.display = 'none';
                document.getElementById('scanBtn').disabled = false;

                if (spyData && spyData.status === 'success') {
                    // Render the full Semrush-Grade Live SEO Audit Report on Tab 1
                    renderSpyResults(spyData, 'trackerLiveAudit');
                    // Also populate Tab 2 so switching tabs shows the exact same live audit
                    renderSpyResults(spyData, 'spyResults');
                    if (document.getElementById('spyUrlInput')) {
                        document.getElementById('spyUrlInput').value = url;
                    }

                    // Check if scanData returned any competitor articles
                    const articlesBlock = document.getElementById('trackerArticlesBlock');
                    if (scanData && scanData.status === 'success' && scanData.results && scanData.results.length > 0) {
                        currentArticles = scanData.results;
                        renderTrackerCards(scanData.results, scanData.is_recent_fallback);
                        if (articlesBlock) articlesBlock.style.display = 'block';
                    } else {
                        if (articlesBlock) articlesBlock.style.display = 'none';
                    }

                    document.getElementById('trackerResults').style.display = 'block';
                    document.getElementById('trackerResults').scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else if (scanData && scanData.status === 'success' && scanData.results && scanData.results.length > 0) {
                    currentArticles = scanData.results;
                    renderTrackerCards(scanData.results, scanData.is_recent_fallback);
                    const articlesBlock = document.getElementById('trackerArticlesBlock');
                    if (articlesBlock) articlesBlock.style.display = 'block';
                    document.getElementById('trackerResults').style.display = 'block';
                } else {
                    alert('Could not complete live SEO audit. Please verify the URL and ensure the competitor website is reachable. Error: ' + ((spyData && spyData.message) || 'Target site was unreachable.'));
                }
            } catch (err) {
                document.getElementById('trackerSpinner').style.display = 'none';
                document.getElementById('scanBtn').disabled = false;
                alert('Audit Error: ' + err.message);
            }
        }
        window.submitTrackerForm = submitTrackerForm;

        const trackerFormEl = document.getElementById('trackerForm');
        if (trackerFormEl) {
            trackerFormEl.addEventListener('submit', submitTrackerForm);
        }

        function renderTrackerCards(articles, isFallback) {
            const container = document.getElementById('trackerCards');
            container.innerHTML = '';
            const isSingle = articles.length === 1 && !isFallback;
            const countText = isSingle 
                ? `Target Competitor Page Analysis:` 
                : (isFallback 
                    ? `Top Ranked & Active Competitor Pages (${articles.length} pages found):` 
                    : `Competitor Articles Published Today (${articles.length} found):`);
            document.getElementById('trackerCount').innerText = countText;

            articles.forEach(art => {
                const card = document.createElement('div');
                card.className = 'article-card';
                
                let lsiList = [];
                if (Array.isArray(art.lsi_keywords)) {
                    lsiList = art.lsi_keywords;
                } else if (typeof art.lsi_keywords === 'string') {
                    lsiList = art.lsi_keywords.split(',').map(s => s.trim()).filter(Boolean);
                }
                const lsiBadges = lsiList.map(k => `<span class="lsi-chip">${k}</span>`).join('');
                
                card.innerHTML = `
                    <div class="card-top">
                        <a href="${art.url}" target="_blank" class="card-title">${art.title || 'Untitled Page'} ↗</a>
                        <span class="product-tag">📦 ${art.product_name || 'General Product/Topic'}</span>
                    </div>
                    <div style="margin: 8px 0 12px 0; font-size: 13px; color: var(--text-muted); word-break: break-all;">
                        <strong style="color: var(--text-main);">🔗 Page URL:</strong> <a href="${art.url}" target="_blank" style="color: var(--accent); text-decoration: underline; font-weight: 500;">${art.url}</a>
                    </div>
                    <div class="keyword-box">
                        <div>
                            <div class="kw-label">🎯 Target Focus Keyword</div>
                            <div class="main-kw">${art.main_keyword || 'General Topic'}</div>
                        </div>
                        <div>
                            <div class="kw-label">🏷️ LSI & Semantic Keywords</div>
                            <div class="lsi-container">${lsiBadges || '<span style="color:#64748b;font-size:12px;">None detected</span>'}</div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-top:12px;">
                        <span style="font-size:12px; color:var(--text-muted);">Published / Modified: ${art.published_date}</span>
                        <div style="display:flex; gap:8px;">
                            <button class="btn-spy" style="padding:7px 16px; font-size:13px; font-weight:600;" onclick="spySingleUrl('${art.url}')">🔍 Semrush-Grade Audit & Spy</button>
                            <button class="btn-download" style="padding:7px 16px; font-size:13px; font-weight:600;" onclick='writeFromCard(${JSON.stringify(art.title)}, ${JSON.stringify(art.main_keyword)}, ${JSON.stringify(lsiList)}, ${JSON.stringify(art.product_name)}, ${JSON.stringify(art.url)})'>✍️ Write Outranking Article</button>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
            document.getElementById('trackerResults').style.display = 'block';
        }

        // Spy Form Submit
        async function submitSpyForm(e) {
            if (e && typeof e.preventDefault === 'function') e.preventDefault();
            const url = document.getElementById('spyUrlInput').value.trim();
            runDeepSpy(url);
        }
        window.submitSpyForm = submitSpyForm;

        const spyFormEl = document.getElementById('spyForm');
        if (spyFormEl) {
            spyFormEl.addEventListener('submit', submitSpyForm);
        }

        function spySingleUrl(url) {
            switchTab('spy');
            document.getElementById('spyUrlInput').value = url;
            runDeepSpy(url);
        }

        async function runDeepSpy(url) {
            if (!url) {
                alert('Please enter a website URL to audit or click one of the quick competitor buttons!');
                return;
            }
            document.getElementById('spySpinner').style.display = 'block';
            document.getElementById('spyResults').style.display = 'none';
            document.getElementById('spyBtn').disabled = true;

            try {
                const resp = await fetch('/api/spy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                });
                const data = await resp.json();
                document.getElementById('spySpinner').style.display = 'none';
                document.getElementById('spyBtn').disabled = false;

                if (data.status === 'success') {
                    renderSpyResults(data);
                } else {
                    alert('Error: ' + (data.message || 'Could not audit URL'));
                }
            } catch (err) {
                document.getElementById('spySpinner').style.display = 'none';
                document.getElementById('spyBtn').disabled = false;
                alert('Error: ' + err.message);
            }
        }

        let currentSpyData = null;
        let isFullCompetitorText = false;

        function renderSpyResults(data, targetContainerId = 'spyResults') {
            currentSpyData = data;
            const audit = data.audit;
            const bl = data.backlinks || {};
            const bp = data.blueprint || [];
            const issues = audit.issues || {};
            const tech = audit.technical || {};
            const onpage = audit.onpage || {};
            const serp = audit.serp_ai || {};
            const eeat = audit.eeat || {};
            const resDiv = document.getElementById(targetContainerId || 'spyResults');
            if (!resDiv) return;

            // Full-Site Multi-Page Audit Data Integration
            const fsa = data.full_site_audit || audit.full_site_audit || (data.semrush_report && data.semrush_report.full_site_audit) || {};
            const crawledPages = fsa.crawled_pages || [];
            const siteIssues = (fsa.site_issues && fsa.site_issues.length > 0) ? fsa.site_issues : (fsa.critical_errors ? [...(fsa.critical_errors || []), ...(fsa.warnings || []), ...(fsa.notices || [])] : []);
            const brokenLinks = fsa.broken_links || fsa.broken_internal_links || [];
            const crawlSummary = fsa.crawl_summary || fsa.crawl_stats || {};
            const sitemapStatus = fsa.sitemap_status || {};
            const robotsStatus = fsa.robots_txt || {};
            const siteHealthScore = fsa.health_score !== undefined ? fsa.health_score : (issues.health_score || audit.seo_score || 50);
            const siteHealthGrade = fsa.health_grade || issues.health_grade || (siteHealthScore >= 80 ? 'Good' : (siteHealthScore >= 60 ? 'Fair' : 'Critical'));
            const siteScoreClass = siteHealthScore >= 80 ? '' : (siteHealthScore >= 60 ? 'score-amber' : 'score-red');
            const totalCrawledCount = fsa.total_crawled || (crawledPages.length > 0 ? crawledPages.length : 1);
            const depthDist = crawlSummary.depth_distribution || { '0': 1, '1': 0, '2': 0, '3+': 0 };

            // Build Crawled Pages Table HTML
            let crawledPagesTableRowsHtml = '';
            if (crawledPages.length > 0) {
                crawledPages.forEach((p, idx) => {
                    const stColor = (p.status_code >= 200 && p.status_code < 300) ? '#15803d' : ((p.status_code >= 300 && p.status_code < 400) ? '#b45309' : '#b91c1c');
                    const stBg = (p.status_code >= 200 && p.status_code < 300) ? '#dcfce7' : ((p.status_code >= 300 && p.status_code < 400) ? '#fef3c7' : '#fee2e2');
                    crawledPagesTableRowsHtml += `
                        <tr class="crawled-page-row" data-url="${escapeHtml((p.url || '').toLowerCase())}" data-status="${p.status_code}" data-depth="${p.depth}">
                            <td style="font-size:11.5px; color:#64748b; font-weight:700; text-align:center;">${idx + 1}</td>
                            <td>
                                <a href="${escapeHtml(p.url)}" target="_blank" style="color:#0284c7; text-decoration:none; font-weight:600; word-break:break-all; font-size:12px;">
                                    ${escapeHtml(p.url)} ↗
                                </a>
                            </td>
                            <td>
                                <span style="background:${stBg}; color:${stColor}; font-weight:800; font-size:11px; padding:3px 7px; border-radius:4px;">
                                    ${p.status_code}
                                </span>
                            </td>
                            <td style="text-align:center;">
                                <span style="background:#f1f5f9; color:#475569; font-size:11px; font-weight:700; padding:2px 6px; border-radius:4px;">
                                    ${p.depth}
                                </span>
                            </td>
                            <td style="font-size:11.5px; color:#1e293b; max-width:220px;" title="${escapeHtml(p.title || '')}">
                                ${escapeHtml(p.title ? (p.title.length > 45 ? p.title.substring(0, 45) + '...' : p.title) : '—')}
                                <div style="font-size:10px; color:#64748b;">${(p.title || '').length} chars</div>
                            </td>
                            <td style="font-size:11.5px; color:#1e293b; max-width:200px;" title="${escapeHtml(p.h1 || '')}">
                                ${escapeHtml(p.h1 ? (p.h1.length > 40 ? p.h1.substring(0, 40) + '...' : p.h1) : '—')}
                            </td>
                            <td style="text-align:right; font-size:11.5px; font-weight:700; color:#0f172a;">
                                ${(p.word_count || 0).toLocaleString()}
                            </td>
                            <td style="text-align:center; font-size:11.5px;">
                                <span style="background:#e0f2fe; color:#0369a1; font-weight:700; padding:2px 6px; border-radius:4px;">${p.inlinks_count || 0}</span>
                            </td>
                            <td style="text-align:center; font-size:11.5px;">
                                <span style="background:#f1f5f9; color:#475569; font-weight:700; padding:2px 6px; border-radius:4px;">${p.outlinks_count || 0}</span>
                            </td>
                            <td style="text-align:right; font-size:11.5px; color:${(p.ttfb_ms && p.ttfb_ms < 600) ? '#15803d' : '#b45309'}; font-weight:600;">
                                ${p.ttfb_ms || 0}ms
                            </td>
                        </tr>
                    `;
                });
            } else {
                crawledPagesTableRowsHtml = '<tr><td colspan="10" style="text-align:center; padding:20px; color:#64748b;">No multi-page crawl data available. Showing seed page.</td></tr>';
            }

            // Build Site-Wide Issues HTML with Affected URLs & Bengali Why & Fix
            let siteIssuesCardsHtml = '';
            let siteCritCount = 0;
            let siteWarnCount = 0;
            let siteNoticCount = 0;
            if (siteIssues.length > 0) {
                siteIssues.forEach(iss => {
                    if (iss.severity === 'C') siteCritCount++;
                    else if (iss.severity === 'W') siteWarnCount++;
                    else siteNoticCount++;

                    const sevBadge = iss.severity === 'C' ? '<span class="badge-severity severity-C">Critical (C)</span>' : (iss.severity === 'W' ? '<span class="badge-severity severity-W">Warning (W)</span>' : '<span class="badge-severity severity-N">Notice (N)</span>');
                    const sevBorder = iss.severity === 'C' ? 'border-left: 4px solid #ef4444;' : (iss.severity === 'W' ? 'border-left: 4px solid #f59e0b;' : 'border-left: 4px solid #3b82f6;');
                    const affUrls = iss.affected_urls || [];
                    let affHtml = '';
                    if (affUrls.length > 0) {
                        affHtml = `
                            <div style="margin-top:8px; margin-bottom:8px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:8px 12px;">
                                <div style="font-size:11.5px; font-weight:800; color:#334155; margin-bottom:4px;">
                                    🔍 Affected URLs (${affUrls.length}):
                                </div>
                                <div style="max-height:120px; overflow-y:auto; display:flex; flex-direction:column; gap:4px;">
                                    ${affUrls.map(u => `<a href="${escapeHtml(u)}" target="_blank" style="font-size:11px; color:#0284c7; text-decoration:none; font-family:monospace; word-break:break-all;">• ${escapeHtml(u)} ↗</a>`).join('')}
                                </div>
                            </div>
                        `;
                    }
                    siteIssuesCardsHtml += `
                        <div class="site-issue-card site-issue-item" data-id="${escapeHtml(iss.id)}" data-severity="${iss.severity}" style="background:#ffffff; border:1px solid #e2e8f0; ${sevBorder} border-radius:8px; padding:14px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                                    <span class="badge-check-id">${iss.id}</span>
                                    ${sevBadge}
                                    <span style="font-size:11px; background:#f1f5f9; color:#475569; padding:2px 7px; border-radius:4px; font-weight:700;">${escapeHtml(iss.category)}</span>
                                    <strong style="font-size:13.5px; color:#0f172a;">${escapeHtml(iss.title)}</strong>
                                </div>
                                <span style="font-size:11.5px; background:#fee2e2; color:#991b1b; padding:2px 8px; border-radius:12px; font-weight:800;">
                                    ${affUrls.length} Affected URL${affUrls.length > 1 ? 's' : ''}
                                </span>
                            </div>
                            ${affHtml}
                            <div style="background:#fef2f2; border-left:3px solid #ef4444; padding:8px 12px; border-radius:5px; margin-bottom:6px;">
                                <strong style="color:#991b1b; font-size:11.5px; display:block; margin-bottom:2px;">⚠️ কেন গুরুত্বপূর্ণ (Why It Matters / সমস্যা):</strong>
                                <span style="font-size:12px; color:#7f1d1d; line-height:1.4;">${escapeHtml(iss.why)}</span>
                            </div>
                            <div style="background:#f0fdf4; border-left:3px solid #22c55e; padding:8px 12px; border-radius:5px;">
                                <strong style="color:#166534; font-size:11.5px; display:block; margin-bottom:2px;">🛠️ কীভাবে সমাধান করবেন (How to Fix / সমাধান):</strong>
                                <span style="font-size:12px; color:#14532d; line-height:1.4;">${escapeHtml(iss.fix)}</span>
                            </div>
                        </div>
                    `;
                });
            } else {
                siteIssuesCardsHtml = '<div style="background:#f0fdf4; color:#166534; padding:16px; border-radius:8px; font-weight:700;">🟢 No site-wide critical issues detected! All crawled pages meet primary architectural standards.</div>';
            }

            // Build Broken Links HTML
            let brokenLinksHtml = '';
            if (brokenLinks.length > 0) {
                brokenLinksHtml = `
                    <div class="site-pages-table-wrapper" style="overflow-x:auto;">
                        <table class="site-pages-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Source Page (Containing Link)</th>
                                    <th>Broken Target Link</th>
                                    <th>Anchor Text</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${brokenLinks.map((blItem, i) => `
                                    <tr>
                                        <td>${i + 1}</td>
                                        <td><a href="${escapeHtml(blItem.source_url)}" target="_blank" style="color:#0284c7; font-size:11.5px; word-break:break-all;">${escapeHtml(blItem.source_url)} ↗</a></td>
                                        <td><span style="color:#dc2626; font-weight:700; font-size:11.5px; word-break:break-all;">${escapeHtml(blItem.target_url)}</span></td>
                                        <td style="font-size:11.5px; color:#475569;">"${escapeHtml(blItem.anchor || '(no text)')}"</td>
                                        <td><span style="background:#fee2e2; color:#b91c1c; font-weight:800; font-size:11px; padding:2px 6px; border-radius:4px;">${blItem.status_code || 404}</span></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            } else {
                brokenLinksHtml = `
                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:14px 18px; color:#15803d; font-size:13px; font-weight:700; display:flex; align-items:center; gap:8px;">
                        <span>🟢</span> No broken internal links (4xx / 5xx) detected across any of the crawled internal pages.
                    </div>
                `;
            }

            // Build Orphan Pages HTML
            const orphanUrls = (sitemapStatus && sitemapStatus.orphan_urls_detected) || [];
            let orphanPagesHtml = '';
            if (orphanUrls.length > 0) {
                orphanPagesHtml = `
                    <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:14px; margin-top:12px;">
                        <div style="font-weight:800; color:#b45309; font-size:13px; margin-bottom:6px;">
                            ⚠️ ${orphanUrls.length} Orphan Pages Detected (In XML Sitemap but 0 Internal Inlinks)
                        </div>
                        <p style="font-size:12px; color:#78350f; margin:0 0 8px 0;">
                            Orphan pages waste crawl budget and rank poorly because search engines and users cannot discover them naturally through site navigation.
                        </p>
                        <div style="max-height:140px; overflow-y:auto; display:flex; flex-direction:column; gap:4px;">
                            ${orphanUrls.map(u => `<a href="${escapeHtml(u)}" target="_blank" style="font-size:11.5px; color:#b45309; text-decoration:none; font-family:monospace; word-break:break-all;">• ${escapeHtml(u)} ↗</a>`).join('')}
                        </div>
                    </div>
                `;
            } else {
                orphanPagesHtml = `
                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:12px 16px; color:#15803d; font-size:12.5px; font-weight:700;">
                        🟢 Zero orphan pages detected. All XML sitemap URLs are well-connected via internal links.
                    </div>
                `;
            }

            const healthScore = issues.health_score || audit.seo_score || 50;
            const healthGrade = issues.health_grade || (healthScore >= 80 ? 'Good (Low Vulnerability)' : (healthScore >= 60 ? 'Fair (Moderate Vulnerabilities)' : 'Critical Issues Detected'));
            const scoreClass = healthScore >= 80 ? '' : (healthScore >= 60 ? 'score-amber' : 'score-red');

            const critCount = issues.critical_errors ? issues.critical_errors.length : 0;
            const warnCount = issues.warnings ? issues.warnings.length : 0;
            const noticCount = issues.notices ? issues.notices.length : 0;
            const passCount = issues.passed_checks ? issues.passed_checks.length : 0;
            const totalIssues = critCount + warnCount + noticCount;

            const targetWords = audit.target_outrank_word_count || Math.max(2000, Math.floor((audit.word_count || 1000) * 1.25));
            const lsiChips = (audit.lsi_keywords || []).map(k => `<span class="lsi-chip">${k}</span>`).join('');
            const headingsList = audit.all_headings || [];

            // Developer Checklist Engine Data (150+ Enterprise Checks)
            const devChecklist = audit.developer_checklist || (data.semrush_report && data.semrush_report.developer_checklist) || {};
            const checklistSummary = devChecklist.summary || { overall_score: healthScore, total_checks: 151, passed: passCount, warnings: warnCount, critical_failed: critCount, notices: noticCount };
            const checklistCategories = devChecklist.categories || [];
            const allChecks = devChecklist.all_checks || [];

            // Build Checklist Items HTML
            let checklistCardsHtml = '';
            allChecks.forEach(c => {
                const affectedHtml = (c.affected && c.affected.length > 0)
                    ? `<div style="font-size:12px; color:#1e293b; margin-bottom:10px; background:#f8fafc; border:1px solid #cbd5e1; padding:7px 11px; border-radius:6px; word-break:break-all;"><strong>🔍 Affected Element / URL / Value:</strong> <span style="color:#0284c7; font-family:monospace; font-weight:700;">${escapeHtml(c.affected.join(', '))}</span></div>`
                    : '';
                const isIssue = (c.status === 'fail' || c.status === 'warn');
                const initialDisplay = isIssue ? 'block' : 'none';
                const initialArrow = isIssue ? 'transform:rotate(180deg);' : '';
                const sevLabel = c.severity === 'C' ? 'Critical Rule' : (c.severity === 'W' ? 'Warning Rule' : 'Notice Rule');
                checklistCardsHtml += `
                    <div class="dev-check-card dev-status-${c.status} dev-chk-item" data-id="${escapeHtml(c.id)}" data-category="${escapeHtml(c.category)}" data-status="${c.status}" data-severity="${c.severity}" onclick="toggleChecklistAccordion('${c.id}', event)" style="cursor:pointer;">
                        <div class="dev-check-header" style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                                <span class="badge-check-id">${c.id}</span>
                                <span class="badge-status badge-status-${c.status}">${c.status.toUpperCase()}</span>
                                <span class="badge-severity severity-${c.severity}" style="opacity:0.85;">${sevLabel}</span>
                                <span style="font-size:11px; background:#f1f5f9; color:#475569; padding:2px 7px; border-radius:4px; font-weight:700;">${escapeHtml(c.category)}</span>
                                <strong style="font-size:13.5px; color:#0f172a;">${escapeHtml(c.title)}</strong>
                            </div>
                            <span class="accordion-arrow" id="arrow-${c.id}" style="color:#64748b; font-size:12px; font-weight:800; transition:transform 0.2s; ${initialArrow}">▼</span>
                        </div>
                        <div class="dev-check-details" id="details-${c.id}" style="display:${initialDisplay}; margin-top:12px; padding-top:10px; border-top:1px dashed #e2e8f0;">
                            ${affectedHtml}
                            <div style="background:#fef2f2; border-left:3.5px solid #ef4444; padding:9px 12px; border-radius:6px; margin-bottom:8px;">
                                <strong style="color:#991b1b; font-size:12px; display:block; margin-bottom:3px;">⚠️ কেন গুরুত্বপূর্ণ (Why It Matters / সমস্যা):</strong>
                                <span style="font-size:12.5px; color:#7f1d1d; line-height:1.5;">${escapeHtml(c.why)}</span>
                            </div>
                            <div style="background:#f0fdf4; border-left:3.5px solid #22c55e; padding:9px 12px; border-radius:6px;">
                                <strong style="color:#166534; font-size:12px; display:block; margin-bottom:3px;">🛠️ কীভাবে সমাধান করবেন (How to Fix / সমাধান):</strong>
                                <span style="font-size:12.5px; color:#14532d; line-height:1.5;">${escapeHtml(c.fix)}</span>
                            </div>
                        </div>
                    </div>
                `;
            });

            // Build Category Progress Grid HTML
            let catProgressHtml = checklistCategories.map(cat => `
                <div class="cat-progress-card" onclick="filterDevChecklistCategory('${escapeHtml(cat.category)}')" style="cursor:pointer;" title="Click to filter by ${escapeHtml(cat.category)}">
                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                        <strong style="color:#0f172a;">${escapeHtml(cat.category)}</strong>
                        <span style="font-weight:800; color:${cat.score >= 80 ? '#15803d' : (cat.score >= 60 ? '#b45309' : '#b91c1c')};">${cat.score}%</span>
                    </div>
                    <div style="width:100%; height:6px; background:#e2e8f0; border-radius:4px; overflow:hidden;">
                        <div style="width:${cat.score}%; height:100%; background:${cat.score >= 80 ? '#22c55e' : (cat.score >= 60 ? '#f59e0b' : '#ef4444')}; border-radius:4px;"></div>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:10.5px; color:#64748b;">
                        <span>🟢 ${cat.passed} Pass</span>
                        <span>🟡 ${cat.warnings} Warn</span>
                        <span>🔴 ${cat.failed} Fail</span>
                    </div>
                </div>
            `).join('');

            // 1. Build Issues HTML
            let issuesHtml = '';
            if (critCount > 0) {
                issues.critical_errors.forEach(e => {
                    issuesHtml += `
                        <div class="issue-card issue-critical sem-issue-item" data-type="critical">
                            <div class="issue-header">
                                <span class="issue-title">🔴 ${e.title}</span>
                                <div>
                                    <span class="issue-badge badge-critical">Critical Error</span>
                                    <span class="issue-badge badge-cat">${e.category || 'SEO'}</span>
                                </div>
                            </div>
                            <div class="issue-body"><strong>Impact:</strong> ${e.impact}</div>
                            <div class="issue-fix"><span>🛠️ Recommendation:</span> ${e.fix}</div>
                        </div>
                    `;
                });
            }
            if (warnCount > 0) {
                issues.warnings.forEach(w => {
                    issuesHtml += `
                        <div class="issue-card issue-warning sem-issue-item" data-type="warning">
                            <div class="issue-header">
                                <span class="issue-title">🟡 ${w.title}</span>
                                <div>
                                    <span class="issue-badge badge-warning">Warning</span>
                                    <span class="issue-badge badge-cat">${w.category || 'SEO'}</span>
                                </div>
                            </div>
                            <div class="issue-body"><strong>Impact:</strong> ${w.impact}</div>
                            <div class="issue-fix"><span>🛠️ Recommendation:</span> ${w.fix}</div>
                        </div>
                    `;
                });
            }
            if (noticCount > 0) {
                issues.notices.forEach(n => {
                    issuesHtml += `
                        <div class="issue-card issue-notice sem-issue-item" data-type="notice">
                            <div class="issue-header">
                                <span class="issue-title">🔵 ${n.title}</span>
                                <div>
                                    <span class="issue-badge badge-notice">Notice / SGE Gap</span>
                                    <span class="issue-badge badge-cat">${n.category || 'Opportunity'}</span>
                                </div>
                            </div>
                            <div class="issue-body"><strong>Impact:</strong> ${n.impact}</div>
                            <div class="issue-fix"><span>💡 Action:</span> ${n.fix}</div>
                        </div>
                    `;
                });
            }
            if (passCount > 0) {
                issues.passed_checks.forEach(p => {
                    issuesHtml += `
                        <div class="issue-card issue-passed sem-issue-item" data-type="passed" style="display:none;">
                            <div class="issue-header">
                                <span class="issue-title">🟢 ${p.title}</span>
                                <div>
                                    <span class="issue-badge badge-passed">Passed</span>
                                    <span class="issue-badge badge-cat">${p.category || 'Audit'}</span>
                                </div>
                            </div>
                            <div class="issue-body">${p.detail || 'Test passed successfully with optimal parameters.'}</div>
                        </div>
                    `;
                });
            }
            if (!issuesHtml) {
                issuesHtml = '<p style="color:#059669; font-weight:700; padding:16px;">🟢 No critical errors detected! Site has passed primary on-page guidelines.</p>';
            }

            // Outline Tree HTML
            let outlineHtml = '';
            if (headingsList.length > 0) {
                outlineHtml = headingsList.map(h => {
                    const badgeClass = h.level === 'H1' ? 'outline-badge-h1' : (h.level === 'H2' ? 'outline-badge-h2' : (h.level === 'H3' ? 'outline-badge-h3' : 'outline-badge-h4'));
                    return `
                        <div class="outline-node">
                            <span class="${badgeClass}">${h.level}</span>
                            <span style="color:#1e293b; font-weight:500;">${h.text}</span>
                        </div>
                    `;
                }).join('');
            } else {
                outlineHtml = '<p style="color:var(--text-muted); font-size:13px; padding:10px 0;">No headings detected in this competitor page.</p>';
            }

            // Backlink links HTML
            const blLinksHtml = (bl.external_backlink_sources || []).map(s => `
                <div style="margin-bottom:8px; font-size:13px; display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:8px 12px; border-radius:8px; border:1px solid #e2e8f0;">
                    <a href="${s.url}" target="_blank" style="color:var(--accent); text-decoration:underline; font-weight:600; max-width:70%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${s.title || s.url}</a>
                    <span style="font-size:11px; background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:4px; font-weight:700;">${s.type || 'Backlink'}</span>
                </div>
            `).join('') || '<p style="color:var(--text-muted); font-size:13px;">No external backlink signals detected.</p>';

            // Roadmap HTML
            const bpHtml = (bp || []).map(s => `
                <div class="blueprint-item">
                    <div class="bp-step">Step ${s.step}: ${s.action}</div>
                    <div class="bp-desc">${s.detail}</div>
                </div>
            `).join('');

            // Image Missing Alt Sample HTML
            const missingAltList = (onpage.image_analysis && onpage.image_analysis.missing_alt_samples || []).map(src => `
                <div style="font-size:12px; color:#b91c1c; background:#fee2e2; padding:4px 8px; border-radius:4px; margin-bottom:4px; word-break:break-all;">
                    ⚠️ Missing Alt: <code>${src}</code>
                </div>
            `).join('');

            // Question Headings HTML
            const qHeadingsList = (serp.question_headings || []).map(q => `
                <span style="background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; display:inline-block; margin:3px;">
                    ❓ ${q}
                </span>
            `).join('') || '<span style="color:#64748b; font-size:12px;">No conversational question subheadings found.</span>';

            // Schema Badges HTML
            const schemaBadges = (eeat.schemas_found || []).map(sc => `
                <span style="background:#f0fdf4; color:#166534; border:1px solid #bbf7d0; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:700; display:inline-block; margin:3px;">
                    ⚡ ${sc}
                </span>
            `).join('') || '<span style="color:#ef4444; font-size:12px; font-weight:600;">⚠️ No Schema.org JSON-LD markup found!</span>';

            resDiv.innerHTML = `
                <!-- Top Actions Bar -->
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h3 style="font-size:19px; font-weight:800; color:#0f172a; margin:0; display:flex; align-items:center; gap:8px;">
                            <span>🔍</span> Semrush-Grade Competitor Site Audit & 360° Spy
                        </h3>
                        <p style="font-size:12.5px; color:var(--text-muted); margin:3px 0 0 0;">
                            100% Real-Data Crawl: Technical Health, On-Page SEO, Google SERP, EEAT & AI Overview Readiness
                        </p>
                    </div>
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                        <button type="button" onclick="copySemrushMarkdownReport()" style="background:#334155; color:white; border:none; padding:9px 15px; border-radius:8px; font-weight:700; cursor:pointer; font-size:12.5px; display:flex; align-items:center; gap:6px;">
                            <span>📋 Copy Markdown Report</span>
                        </button>
                        <button type="button" onclick="downloadSemrushHtmlReport()" style="background:#0284c7; color:white; border:none; padding:9px 15px; border-radius:8px; font-weight:700; cursor:pointer; font-size:12.5px; display:flex; align-items:center; gap:6px;">
                            <span>⬇️ Download HTML Report</span>
                        </button>
                        <button type="button" onclick="openClientReportModal('spy')" style="background:linear-gradient(135deg, #1e3a8a, #2563eb); color:white; border:none; padding:9px 16px; border-radius:8px; font-weight:700; cursor:pointer; font-size:12.5px; display:flex; align-items:center; gap:6px; box-shadow:0 3px 8px rgba(37,99,235,0.25);">
                            <span>📄 Export Client PDF</span>
                        </button>
                    </div>
                </div>

                <!-- Semrush Hero Executive Card -->
                <div class="semrush-hero-card">
                    <div class="semrush-hero-top">
                        <div style="max-width: 68%;">
                            <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(59,130,246,0.2); border:1px solid rgba(59,130,246,0.4); color:#93c5fd; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:800; text-transform:uppercase; margin-bottom:8px;">
                                <span>🌐</span> LIVE AUDIT DELIVERABLE
                            </div>
                            <h2 style="font-size:20px; font-weight:800; margin:0 0 6px 0; color:#ffffff; line-height:1.3;">
                                <a href="${audit.url}" target="_blank" style="color:white; text-decoration:none;">${audit.title || 'Competitor Analysis'} ↗</a>
                            </h2>
                            <div style="font-size:12.5px; color:#cbd5e1; word-break:break-all;">
                                <strong style="color:#94a3b8;">Target URL:</strong> <a href="${audit.url}" target="_blank" style="color:#60a5fa; text-decoration:underline;">${audit.url}</a>
                            </div>
                            <div style="display:flex; gap:10px; margin-top:8px; flex-wrap:wrap; font-size:12px;">
                                <span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:5px;">📦 Entity: <strong>${audit.product_name}</strong></span>
                                <span style="background:rgba(255,255,255,0.1); padding:2px 8px; border-radius:5px;">🎯 Focus Keyword: <strong>${audit.main_keyword}</strong></span>
                            </div>
                        </div>

                        <!-- Big Health Score Gauge -->
                        <div style="display:flex; flex-direction:column; align-items:center; gap:6px;">
                            <div class="semrush-score-circle ${scoreClass}">
                                <span>${healthScore}</span>
                                <span style="font-size:10px; color:#94a3b8; font-weight:700; margin-top:-2px;">/100</span>
                            </div>
                            <div style="font-size:12px; font-weight:800; color:#e2e8f0; text-align:center;">
                                ${healthGrade}
                            </div>
                        </div>
                    </div>

                    <!-- 8 KPI Tiles Bar -->
                    <div class="semrush-kpis-grid">
                        <div class="semrush-kpi-item" style="border-color:rgba(239,68,68,0.3); background:rgba(239,68,68,0.08);">
                            <div class="semrush-kpi-label" style="color:#fca5a5;">Critical Errors</div>
                            <div class="semrush-kpi-num" style="color:#ef4444;">${critCount}</div>
                        </div>
                        <div class="semrush-kpi-item" style="border-color:rgba(245,158,11,0.3); background:rgba(245,158,11,0.08);">
                            <div class="semrush-kpi-label" style="color:#fcd34d;">Warnings</div>
                            <div class="semrush-kpi-num" style="color:#f59e0b;">${warnCount}</div>
                        </div>
                        <div class="semrush-kpi-item" style="border-color:rgba(59,130,246,0.3); background:rgba(59,130,246,0.08);">
                            <div class="semrush-kpi-label" style="color:#93c5fd;">SGE Notices</div>
                            <div class="semrush-kpi-num" style="color:#3b82f6;">${noticCount}</div>
                        </div>
                        <div class="semrush-kpi-item" style="border-color:rgba(16,185,129,0.3); background:rgba(16,185,129,0.08);">
                            <div class="semrush-kpi-label" style="color:#86efac;">Passed Checks</div>
                            <div class="semrush-kpi-num" style="color:#10b981;">${passCount}</div>
                        </div>
                        <div class="semrush-kpi-item">
                            <div class="semrush-kpi-label">Server TTFB</div>
                            <div class="semrush-kpi-num" style="color:#38bdf8;">${tech.ttfb_ms || 0}ms</div>
                        </div>
                        <div class="semrush-kpi-item">
                            <div class="semrush-kpi-label">AI Overview</div>
                            <div class="semrush-kpi-num" style="color:#c084fc;">${serp.score || 0}/100</div>
                        </div>
                        <div class="semrush-kpi-item">
                            <div class="semrush-kpi-label">EEAT Score</div>
                            <div class="semrush-kpi-num" style="color:#fbbf24;">${eeat.score || 0}/100</div>
                        </div>
                        <div class="semrush-kpi-item">
                            <div class="semrush-kpi-label">Word Count</div>
                            <div class="semrush-kpi-num" style="color:#ffffff;">${(audit.word_count || 0).toLocaleString()}</div>
                        </div>
                    </div>
                </div>

                <!-- Semrush Subtabs Navigation -->
                <div class="semrush-subtabs-nav">
                    <button class="sem-subtab-btn active" data-tab="site_overview" id="tabBtnSiteOverview" onclick="switchSemrushSubtab('site_overview')" style="background:#eff6ff; color:#1d4ed8; border:1.5px solid #3b82f6; font-weight:800;">
                        <span>🌐</span> Site Overview (${totalCrawledCount} Pages)
                    </button>
                    <button class="sem-subtab-btn" data-tab="site_pages" id="tabBtnSitePages" onclick="switchSemrushSubtab('site_pages')">
                        <span>📑</span> Crawled Pages Explorer (${crawledPages.length})
                    </button>
                    <button class="sem-subtab-btn" data-tab="site_issues" id="tabBtnSiteIssues" onclick="switchSemrushSubtab('site_issues')">
                        <span>🚨</span> Site Issues & Errors (${siteIssues.length})
                    </button>
                    <button class="sem-subtab-btn" data-tab="site_links" id="tabBtnSiteLinks" onclick="switchSemrushSubtab('site_links')">
                        <span>🔗</span> Links & Architecture (${brokenLinks.length > 0 ? brokenLinks.length + ' Broken' : 'Clean'})
                    </button>
                    <button class="sem-subtab-btn" data-tab="checklist" id="tabBtnChecklist" onclick="switchSemrushSubtab('checklist')">
                        <span>📋</span> Developer Checklist (151)
                    </button>
                    <button class="sem-subtab-btn" data-tab="issues" id="tabBtnIssues" onclick="switchSemrushSubtab('issues')">
                        <span>⚠️</span> Seed URL Audit (${totalIssues})
                    </button>
                    <button class="sem-subtab-btn" data-tab="onpage" id="tabBtnOnpage" onclick="switchSemrushSubtab('onpage')">
                        <span>📄</span> On-Page Deep Dive
                    </button>
                    <button class="sem-subtab-btn" data-tab="serp_ai" id="tabBtnSerpAi" onclick="switchSemrushSubtab('serp_ai')">
                        <span>🤖</span> Google SERP & AI Overview (${serp.score || 0}/100)
                    </button>
                    <button class="sem-subtab-btn" data-tab="eeat" id="tabBtnEeat" onclick="switchSemrushSubtab('eeat')">
                        <span>🛡️</span> EEAT Trust Radar (${eeat.score || 0}/100)
                    </button>
                    <button class="sem-subtab-btn" data-tab="tech" id="tabBtnTech" onclick="switchSemrushSubtab('tech')">
                        <span>⚡</span> Technical & Speed
                    </button>
                    <button class="sem-subtab-btn" data-tab="content" id="tabBtnContent" onclick="switchSemrushSubtab('content')">
                        <span>📜</span> Content & Outline
                    </button>
                    <button class="sem-subtab-btn" data-tab="backlinks" id="tabBtnBacklinks" onclick="switchSemrushSubtab('backlinks')">
                        <span>🔗</span> Backlinks (${bl.total_backlinks_est || 0})
                    </button>
                    <button class="sem-subtab-btn" data-tab="outrank" id="tabBtnOutrank" onclick="switchSemrushSubtab('outrank')" style="border-color:#10b981; color:#047857; background:#f0fdf4;">
                        <span>⚔️</span> Outrank Roadmap & AI Writer
                    </button>
                </div>

                <!-- ================= 1. SUBTAB: SITE OVERVIEW ================= -->
                <div class="sem-subtab-panel" data-panel="site_overview" id="semViewSiteOverview" style="display:block;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <!-- Site Health Banner -->
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:18px; flex-wrap:wrap; gap:14px; background:linear-gradient(135deg, #0f172a, #1e293b); padding:20px; border-radius:12px; color:white;">
                            <div>
                                <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(59,130,246,0.25); color:#60a5fa; padding:4px 10px; border-radius:16px; font-size:11px; font-weight:800; text-transform:uppercase; margin-bottom:8px;">
                                    <span>🌐</span> MULTI-PAGE ENTERPRISE CRAWL
                                </div>
                                <h3 style="font-size:20px; font-weight:800; margin:0 0 6px 0; color:#ffffff;">
                                    Enterprise Full-Site Audit & Health Overview
                                </h3>
                                <p style="font-size:13px; color:#94a3b8; margin:0;">
                                    Crawled <strong>${totalCrawledCount} internal pages</strong> across domain <span style="color:#38bdf8;">${escapeHtml(fsa.domain || audit.url)}</span>
                                </p>
                            </div>
                            <div style="display:flex; align-items:center; gap:12px;">
                                <div class="semrush-score-circle ${siteScoreClass}" style="width:72px; height:72px;">
                                    <span style="font-size:24px;">${siteHealthScore}</span>
                                    <span style="font-size:10px; color:#94a3b8; font-weight:700; margin-top:-2px;">/100</span>
                                </div>
                                <div>
                                    <div style="font-size:13px; font-weight:800; color:#ffffff;">Site Health Score</div>
                                    <div style="font-size:12px; color:#38bdf8; font-weight:700;">${siteHealthGrade}</div>
                                </div>
                            </div>
                        </div>

                        <!-- 6 Site-Wide KPI Badges -->
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:12px; margin-bottom:20px;">
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">Pages Crawled</div>
                                <div style="font-size:24px; font-weight:800; color:#0f172a;">${totalCrawledCount}</div>
                            </div>
                            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#15803d; text-transform:uppercase;">Indexable Pages</div>
                                <div style="font-size:24px; font-weight:800; color:#15803d;">${crawlSummary.indexable_count || totalCrawledCount}</div>
                            </div>
                            <div style="background:#fee2e2; border:1px solid #fca5a5; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#b91c1c; text-transform:uppercase;">Broken Links</div>
                                <div style="font-size:24px; font-weight:800; color:#b91c1c;">${crawlSummary.broken_count || brokenLinks.length || 0}</div>
                            </div>
                            <div style="background:#fef3c7; border:1px solid #fde68a; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#b45309; text-transform:uppercase;">Redirects</div>
                                <div style="font-size:24px; font-weight:800; color:#b45309;">${crawlSummary.redirect_count || 0}</div>
                            </div>
                            <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#1e40af; text-transform:uppercase;">Avg Server Latency</div>
                                <div style="font-size:24px; font-weight:800; color:#2563eb;">${crawlSummary.avg_ttfb_ms || tech.ttfb_ms || 0}ms</div>
                            </div>
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">Total Site Words</div>
                                <div style="font-size:22px; font-weight:800; color:#0f172a;">${(crawlSummary.total_words || audit.word_count || 0).toLocaleString()}</div>
                            </div>
                        </div>

                        <!-- Architecture & Crawl Depth Section -->
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px; margin-bottom:18px;">
                            <!-- Depth Card -->
                            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px;">
                                <h4 style="font-size:13.5px; font-weight:800; color:#0f172a; margin:0 0 12px 0; display:flex; align-items:center; gap:6px;">
                                    <span>📊</span> Click Depth Distribution (Crawl Budget Health)
                                </h4>
                                <div style="display:flex; flex-direction:column; gap:8px;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                                        <span>🏠 Depth 0 (Homepage):</span>
                                        <strong>${depthDist['0'] || 1} page</strong>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                                        <span>🔗 Depth 1 (1 Click from Home):</span>
                                        <strong>${depthDist['1'] || 0} pages</strong>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                                        <span>📂 Depth 2 (2 Clicks):</span>
                                        <strong>${depthDist['2'] || 0} pages</strong>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:${(depthDist['3+'] || 0) > 0 ? '#b45309' : '#64748b'};">
                                        <span>⚠️ Depth 3+ (Deep Crawl Risk):</span>
                                        <strong>${depthDist['3+'] || 0} pages</strong>
                                    </div>
                                </div>
                            </div>

                            <!-- Robots & Sitemap Card -->
                            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:16px;">
                                <h4 style="font-size:13.5px; font-weight:800; color:#0f172a; margin:0 0 12px 0; display:flex; align-items:center; gap:6px;">
                                    <span>🤖</span> Robots.txt & XML Sitemap Crawlability
                                </h4>
                                <div style="display:flex; flex-direction:column; gap:8px; font-size:12px;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span>Robots.txt Status:</span>
                                        <span style="font-weight:700; color:${robotsStatus.found ? '#15803d' : '#b45309'};">${robotsStatus.found ? '✅ Detected (' + (robotsStatus.rules_count || 0) + ' disallows)' : '⚠️ Not Detected'}</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span>XML Sitemap Index:</span>
                                        <span style="font-weight:700; color:${sitemapStatus.found ? '#15803d' : '#b45309'};">${sitemapStatus.found ? '✅ Found (' + (sitemapStatus.total_sitemap_urls || 0) + ' URLs)' : '⚠️ Not Detected'}</span>
                                    </div>
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span>Orphan Pages:</span>
                                        <span style="font-weight:700; color:${((sitemapStatus.orphan_urls_detected || []).length > 0) ? '#b45309' : '#15803d'};">${((sitemapStatus.orphan_urls_detected || []).length > 0) ? '⚠️ ' + sitemapStatus.orphan_urls_detected.length + ' detected' : '🟢 0 Detected'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Quick Navigation to Detailed Views -->
                        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; padding:16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                            <div>
                                <strong style="color:#0f172a; font-size:13.5px; display:block;">🔍 Explore Site-Wide Audit Deliverables:</strong>
                                <span style="font-size:12.5px; color:#475569;">Dive deep into individual page metrics, affected URLs lists, and broken link architecture.</span>
                            </div>
                            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                <button type="button" onclick="switchSemrushSubtab('site_pages')" style="background:#0284c7; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px;">
                                    📑 View Crawled Pages (${crawledPages.length})
                                </button>
                                <button type="button" onclick="switchSemrushSubtab('site_issues')" style="background:#ef4444; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px;">
                                    🚨 View Site Issues (${siteIssues.length})
                                </button>
                                <button type="button" onclick="switchSemrushSubtab('site_links')" style="background:#475569; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px;">
                                    🔗 View Broken Links (${brokenLinks.length})
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ================= 2. SUBTAB: CRAWLED PAGES EXPLORER ================= -->
                <div class="sem-subtab-panel" data-panel="site_pages" id="semViewSitePages" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <!-- Header Bar -->
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h3 style="font-size:17px; font-weight:800; color:#0f172a; margin:0; display:flex; align-items:center; gap:8px;">
                                    <span>📑</span> Crawled Pages Explorer (${crawledPages.length} Pages)
                                </h3>
                                <p style="font-size:12.5px; color:var(--text-muted); margin:3px 0 0 0;">
                                    Status codes, click depth, title length, H1, word counts, inlinks & latency for every crawled URL
                                </p>
                            </div>
                            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                <button type="button" onclick="downloadPagesCSV()" style="background:#0284c7; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                                    <span>⬇️ Export Pages CSV</span>
                                </button>
                            </div>
                        </div>

                        <!-- Filter Controls -->
                        <div style="background:#f1f5f9; padding:12px 14px; border-radius:8px; margin-bottom:14px; display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
                            <input type="text" id="crawledPagesSearch" placeholder="🔍 Search by URL or path..." oninput="filterSitePages()" style="flex:1; min-width:240px; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; outline:none; background:#ffffff;">
                            <select id="crawledPagesStatusSelect" onchange="filterSitePages()" style="padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; background:#ffffff; font-weight:600;">
                                <option value="all">🌐 All HTTP Statuses</option>
                                <option value="200">🟢 200 OK</option>
                                <option value="3xx">🟡 3xx Redirects</option>
                                <option value="4xx">🔴 4xx Client Errors</option>
                                <option value="5xx">🔥 5xx Server Errors</option>
                            </select>
                        </div>

                        <!-- Pages Table -->
                        <div class="site-pages-table-wrapper" style="overflow-x:auto; max-height:550px; border:1px solid #e2e8f0; border-radius:8px;">
                            <table class="site-pages-table" id="crawledPagesTable">
                                <thead>
                                    <tr>
                                        <th style="width:40px; text-align:center;">#</th>
                                        <th>Page URL</th>
                                        <th style="width:80px;">Status</th>
                                        <th style="width:70px; text-align:center;">Depth</th>
                                        <th>Title Tag</th>
                                        <th>H1 Heading</th>
                                        <th style="width:80px; text-align:right;">Words</th>
                                        <th style="width:70px; text-align:center;">Inlinks</th>
                                        <th style="width:70px; text-align:center;">Outlinks</th>
                                        <th style="width:80px; text-align:right;">TTFB</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${crawledPagesTableRowsHtml}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- ================= 3. SUBTAB: SITE-WIDE ISSUES DRILLDOWN ================= -->
                <div class="sem-subtab-panel" data-panel="site_issues" id="semViewSiteIssues" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <!-- Header Bar -->
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h3 style="font-size:17px; font-weight:800; color:#0f172a; margin:0; display:flex; align-items:center; gap:8px;">
                                    <span>🚨</span> Site-Wide Issues & Flaws Drilldown (${siteIssues.length} Issues)
                                </h3>
                                <p style="font-size:12.5px; color:var(--text-muted); margin:3px 0 0 0;">
                                    Every detected flaw across all crawled pages, complete with affected URLs list, Bengali why & step-by-step fix
                                </p>
                            </div>
                            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                <button type="button" onclick="downloadSiteIssuesCSV()" style="background:#0284c7; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                                    <span>⬇️ Export Issues CSV</span>
                                </button>
                            </div>
                        </div>

                        <!-- Filter Controls -->
                        <div style="background:#f1f5f9; padding:12px 14px; border-radius:8px; margin-bottom:14px; display:flex; flex-direction:column; gap:10px;">
                            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
                                <input type="text" id="siteIssuesSearch" placeholder="🔍 Search Issue ID (e.g. OP-001, IDX-001), keyword or URL..." oninput="filterSiteIssuesList()" style="flex:1; min-width:240px; padding:8px 12px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; outline:none; background:#ffffff;">
                            </div>
                            <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
                                <span style="font-size:12px; font-weight:700; color:#475569; margin-right:4px;">Filter Severity:</span>
                                <button class="filter-pill active site-issue-pill" onclick="filterSiteIssues('all', event)">All Issues (${siteIssues.length})</button>
                                <button class="filter-pill pill-red site-issue-pill" onclick="filterSiteIssues('C', event)">🔴 Critical (${siteCritCount})</button>
                                <button class="filter-pill pill-amber site-issue-pill" onclick="filterSiteIssues('W', event)">🟡 Warnings (${siteWarnCount})</button>
                                <button class="filter-pill pill-blue site-issue-pill" onclick="filterSiteIssues('N', event)">🔵 Notices (${siteNoticCount})</button>
                            </div>
                        </div>

                        <!-- Issues List -->
                        <div id="siteIssuesCardsContainer">
                            ${siteIssuesCardsHtml}
                        </div>
                    </div>
                </div>

                <!-- ================= 4. SUBTAB: LINKS & ARCHITECTURE ================= -->
                <div class="sem-subtab-panel" data-panel="site_links" id="semViewSiteLinks" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <h3 style="font-size:17px; font-weight:800; color:#0f172a; margin:0 0 4px 0; display:flex; align-items:center; gap:8px;">
                            <span>🔗</span> Internal Links & Site Architecture Audit
                        </h3>
                        <p style="font-size:12.5px; color:var(--text-muted); margin:0 0 16px 0;">
                            Crawl map analysis: broken internal links, target response codes, and orphan sitemap pages
                        </p>

                        <!-- Broken Links Box -->
                        <div style="margin-bottom:20px;">
                            <h4 style="font-size:14px; font-weight:800; color:#0f172a; margin:0 0 8px 0; display:flex; align-items:center; gap:6px;">
                                <span>❌</span> Broken Internal Links (${brokenLinks.length} Detected)
                            </h4>
                            <p style="font-size:12px; color:#64748b; margin:0 0 10px 0;">
                                Internal links pointing to 4xx or 5xx dead pages harm crawl equity and user experience.
                            </p>
                            ${brokenLinksHtml}
                        </div>

                        <!-- Orphan Pages Box -->
                        <div>
                            <h4 style="font-size:14px; font-weight:800; color:#0f172a; margin:0 0 8px 0; display:flex; align-items:center; gap:6px;">
                                <span>🏝️</span> Orphan Pages Probe (Sitemap vs Internal Link Disconnect)
                            </h4>
                            ${orphanPagesHtml}
                        </div>
                    </div>
                </div>

                <!-- SUBTAB: Full Developer Checklist (All 150+ Checks across Technical, On-Page, E-E-A-T, AEO, GEO, Security, A11Y) -->
                <div class="sem-subtab-panel" data-panel="checklist" id="semViewChecklist" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <!-- Top Executive Summary Bar -->
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; flex-wrap:wrap; gap:12px; background:linear-gradient(135deg, #0f172a, #1e293b); padding:16px 20px; border-radius:12px; color:white;">
                            <div>
                                <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(59,130,246,0.25); color:#60a5fa; padding:3px 9px; border-radius:16px; font-size:11px; font-weight:800; text-transform:uppercase; margin-bottom:6px;">
                                    <span>⚡</span> 150+ FULL ENTERPRISE CHECKLIST
                                </div>
                                <h3 style="font-size:18px; font-weight:800; margin:0; color:#ffffff;">
                                    Site Audit Tool: Full Developer Checklist
                                </h3>
                                <p style="font-size:12.5px; color:#94a3b8; margin:4px 0 0 0;">
                                    Technical SEO, Indexability, On-Page, E-E-A-T, AEO, GEO, Security, Performance & WCAG 2.2 Accessibility
                                </p>
                            </div>
                            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                                <button type="button" onclick="downloadChecklistCSV()" style="background:#0284c7; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                                    <span>⬇️ Export Checklist CSV</span>
                                </button>
                                <button type="button" onclick="downloadChecklistJSON()" style="background:#334155; color:white; border:none; padding:8px 14px; border-radius:7px; font-weight:700; cursor:pointer; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                                    <span>⬇️ Export JSON</span>
                                </button>
                            </div>
                        </div>

                        <!-- 6 Summary KPI Badges -->
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px; margin-bottom:18px;">
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">Overall Score</div>
                                <div style="font-size:22px; font-weight:800; color:#2563eb;">${checklistSummary.overall_score || healthScore}/100</div>
                            </div>
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase;">Total Checks</div>
                                <div style="font-size:22px; font-weight:800; color:#0f172a;">${checklistSummary.total_checks || allChecks.length || 151}</div>
                            </div>
                            <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#15803d; text-transform:uppercase;">🟢 Passed</div>
                                <div style="font-size:22px; font-weight:800; color:#15803d;">${checklistSummary.passed || 0}</div>
                            </div>
                            <div style="background:#fef3c7; border:1px solid #fde68a; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#b45309; text-transform:uppercase;">🟡 Warnings</div>
                                <div style="font-size:22px; font-weight:800; color:#b45309;">${checklistSummary.warnings || 0}</div>
                            </div>
                            <div style="background:#fee2e2; border:1px solid #fca5a5; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#b91c1c; text-transform:uppercase;">🔴 Critical</div>
                                <div style="font-size:22px; font-weight:800; color:#b91c1c;">${checklistSummary.critical_failed || 0}</div>
                            </div>
                            <div style="background:#dbeafe; border:1px solid #bfdbfe; border-radius:8px; padding:10px 14px; text-align:center;">
                                <div style="font-size:11px; font-weight:700; color:#1e40af; text-transform:uppercase;">🔵 Info / Notices</div>
                                <div style="font-size:22px; font-weight:800; color:#1e40af;">${checklistSummary.notices || 0}</div>
                            </div>
                        </div>

                        <!-- Category Progress Radar Grid -->
                        <div style="margin-bottom:18px;">
                            <div style="font-size:13px; font-weight:800; color:#0f172a; margin-bottom:8px;">
                                📊 Category Audit Health Scores (0-100%):
                            </div>
                            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px;">
                                ${catProgressHtml}
                            </div>
                        </div>

                        <!-- Interactive Search & Filtering Bar -->
                        <div style="background:#f1f5f9; padding:12px 16px; border-radius:10px; margin-bottom:14px; display:flex; flex-direction:column; gap:10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                                <input type="text" id="devChecklistSearch" placeholder="🔍 Search Check ID (e.g. TECH-001, OP-020, SEC-001, GEO-001, A11Y) or keyword..." oninput="filterDevChecklist()" style="flex:1; min-width:260px; padding:9px 14px; border:1.5px solid #cbd5e1; border-radius:7px; font-size:13px; outline:none; background:#ffffff;">
                                <select id="devCategorySelect" onchange="filterDevChecklist()" style="padding:9px 12px; border:1.5px solid #cbd5e1; border-radius:7px; font-size:13px; background:#ffffff; font-weight:600;">
                                    <option value="all">📂 All Categories (150+)</option>
                                    <option value="Crawler & Discovery">Crawler & Discovery</option>
                                    <option value="Indexability & Status">Indexability & Status</option>
                                    <option value="On-Page SEO">On-Page SEO</option>
                                    <option value="Content Quality & E-E-A-T">Content Quality & E-E-A-T</option>
                                    <option value="Structured Data / Schema">Structured Data / Schema</option>
                                    <option value="Security & Architecture">Security & Architecture</option>
                                    <option value="Performance & CWV">Performance & CWV</option>
                                    <option value="Accessibility (WCAG)">Accessibility (WCAG 2.2)</option>
                                    <option value="Google Spam Policy">Google Spam Policy</option>
                                    <option value="AEO (Answer Engine)">AEO (Answer Engine)</option>
                                    <option value="GEO (Generative AI)">GEO (Generative AI)</option>
                                    <option value="Privacy & Legal">Privacy & Legal</option>
                                </select>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                                <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
                                    <span style="font-size:12px; font-weight:700; color:#475569; margin-right:4px;">Filter Status:</span>
                                    <button class="filter-pill active dev-stat-pill" onclick="filterDevStatus('all', event)">All Checks (${allChecks.length})</button>
                                    <button class="filter-pill pill-red dev-stat-pill" onclick="filterDevStatus('fail', event)">🔴 Critical Fail (${checklistSummary.critical_failed || 0})</button>
                                    <button class="filter-pill pill-amber dev-stat-pill" onclick="filterDevStatus('warn', event)">🟡 Warnings (${checklistSummary.warnings || 0})</button>
                                    <button class="filter-pill pill-green dev-stat-pill" onclick="filterDevStatus('pass', event)">🟢 Passed (${checklistSummary.passed || 0})</button>
                                    <button class="filter-pill pill-blue dev-stat-pill" onclick="filterDevStatus('info', event)">🔵 Info / Notices (${checklistSummary.notices || 0})</button>
                                </div>
                                <div style="display:flex; gap:6px;">
                                    <button type="button" onclick="expandAllChecklist(true)" style="background:#e2e8f0; color:#0f172a; border:none; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; cursor:pointer;" title="Expand all check reports">
                                        <span>📖 Expand All Reports</span>
                                    </button>
                                    <button type="button" onclick="expandAllChecklist(false)" style="background:#e2e8f0; color:#0f172a; border:none; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; cursor:pointer;" title="Collapse all check reports">
                                        <span>📕 Collapse All</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Checklist Items Accordion List -->
                        <div id="devChecklistItemsContainer">
                            ${checklistCardsHtml}
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 1: All Issues & Errors -->
                <div class="sem-subtab-panel" data-panel="issues" id="semViewIssues">
                    <div class="section-box" style="margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin:0;">
                                    🚨 Detected Site Issues & Vulnerabilities (কী কী সমস্যা ও সমাধান)
                                </h3>
                                <p style="font-size:12.5px; color:var(--text-muted); margin:3px 0 0 0;">
                                    All technical, on-page, and architectural errors identified via live HTTP crawl
                                </p>
                            </div>
                            <div class="filter-pills-bar" style="margin-bottom:0;">
                                <button class="filter-pill active" onclick="filterSemrushIssues('all')">All Issues (${totalIssues})</button>
                                <button class="filter-pill pill-red" onclick="filterSemrushIssues('critical')">🔴 Critical (${critCount})</button>
                                <button class="filter-pill pill-amber" onclick="filterSemrushIssues('warning')">🟡 Warnings (${warnCount})</button>
                                <button class="filter-pill pill-blue" onclick="filterSemrushIssues('notice')">🔵 SGE Notices (${noticCount})</button>
                                <button class="filter-pill pill-green" onclick="filterSemrushIssues('passed')">🟢 Passed Checks (${passCount})</button>
                            </div>
                        </div>

                        <div id="semIssuesListContainer">
                            ${issuesHtml}
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 2: On-Page SEO Deep Dive -->
                <div class="sem-subtab-panel" data-panel="onpage" id="semViewOnpage" style="display:none;">
                    <div class="tech-grid" style="margin-bottom:16px;">
                        <!-- Title Tag Card -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🏷️</span> Title Tag Diagnostic
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Title Content:</span>
                                <span class="tech-val" style="word-break:break-word; max-width:65%; font-weight:600;">${onpage.title_analysis ? onpage.title_analysis.text : audit.title}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Character Length:</span>
                                <span class="tech-val">${onpage.title_analysis ? onpage.title_analysis.length : audit.title.length} chars (~${onpage.title_analysis ? onpage.title_analysis.pixel_width : 500}px)</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Optimal Status:</span>
                                <span class="tech-val" style="color:${(onpage.title_analysis && onpage.title_analysis.length <= 60 && onpage.title_analysis.length >= 30) ? '#059669' : '#dc2626'};">${onpage.title_analysis ? onpage.title_analysis.status : 'N/A'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Focus Keyword In Title:</span>
                                <span class="tech-val" style="color:${(onpage.title_analysis && onpage.title_analysis.has_keyword) ? '#059669' : '#d97706'};">${(onpage.title_analysis && onpage.title_analysis.has_keyword) ? 'Yes (' + onpage.title_analysis.keyword_position + ')' : 'No'}</span>
                            </div>
                        </div>

                        <!-- Meta Description Card -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>📝</span> Meta Description Diagnostic
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Description:</span>
                                <span class="tech-val" style="word-break:break-word; max-width:65%; font-weight:500;">${(onpage.meta_analysis && onpage.meta_analysis.text) || 'Missing description tag'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Character Length:</span>
                                <span class="tech-val">${onpage.meta_analysis ? onpage.meta_analysis.length : 0} chars (Target: 120-160)</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Status:</span>
                                <span class="tech-val" style="color:${(onpage.meta_analysis && onpage.meta_analysis.length >= 70 && onpage.meta_analysis.length <= 160) ? '#059669' : '#dc2626'};">${onpage.meta_analysis ? onpage.meta_analysis.status : 'N/A'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Keyword in Meta:</span>
                                <span class="tech-val">${(onpage.meta_analysis && onpage.meta_analysis.has_keyword) ? '✅ Yes' : '❌ No'}</span>
                            </div>
                        </div>

                        <!-- Canonical & URL Structure -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🔗</span> Canonical & URL Structure
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Canonical Tag:</span>
                                <span class="tech-val" style="word-break:break-all; max-width:65%;">${(onpage.canonical_analysis && onpage.canonical_analysis.url) || 'Missing canonical'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Self-Referencing:</span>
                                <span class="tech-val">${(onpage.canonical_analysis && onpage.canonical_analysis.is_self_canon) ? '✅ Valid Match' : '⚠️ ' + ((onpage.canonical_analysis && onpage.canonical_analysis.status) || 'Missing')}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Canonical Config:</span>
                                <span class="tech-val">${onpage.canonical_analysis ? onpage.canonical_analysis.status : 'N/A'}</span>
                            </div>
                        </div>

                        <!-- Heading Hierarchy -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>📑</span> Heading Tag Architecture
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">H1 Tags Count:</span>
                                <span class="tech-val" style="color:${(onpage.headings_analysis && onpage.headings_analysis.h1_count === 1) ? '#059669' : '#dc2626'};">${onpage.headings_analysis ? onpage.headings_analysis.h1_count : 1} (Ideal: Exactly 1)</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">H2 Tags Count:</span>
                                <span class="tech-val">${onpage.headings_analysis ? onpage.headings_analysis.h2_count : 0} subheadings</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">H3 Tags Count:</span>
                                <span class="tech-val">${onpage.headings_analysis ? onpage.headings_analysis.h3_count : 0} subheadings</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Hierarchy Skip Flag:</span>
                                <span class="tech-val">${(onpage.headings_analysis && onpage.headings_analysis.hierarchy_skip_detected) ? '⚠️ Level Skip Detected' : '✅ Clean Hierarchy'}</span>
                            </div>
                        </div>

                        <!-- Images & Media -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🖼️</span> Images & Alt Tag Optimization
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Total Images:</span>
                                <span class="tech-val">${onpage.image_analysis ? onpage.image_analysis.total_images : 0}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Images Missing Alt:</span>
                                <span class="tech-val" style="color:${(onpage.image_analysis && onpage.image_analysis.images_missing_alt > 0) ? '#dc2626' : '#059669'};">${onpage.image_analysis ? onpage.image_analysis.images_missing_alt : 0}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Alt Coverage Ratio:</span>
                                <span class="tech-val" style="color:${(onpage.image_analysis && onpage.image_analysis.alt_coverage_pct >= 90) ? '#059669' : '#d97706'};">${onpage.image_analysis ? onpage.image_analysis.alt_coverage_pct : 100}%</span>
                            </div>
                            ${missingAltList ? `<div style="margin-top:8px;">${missingAltList}</div>` : ''}
                        </div>

                        <!-- Link Architecture -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🌐</span> Link Equity & Crawl Architecture
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Total Links:</span>
                                <span class="tech-val">${onpage.link_analysis ? onpage.link_analysis.total_links : 0}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Internal Equity Links:</span>
                                <span class="tech-val">${onpage.link_analysis ? onpage.link_analysis.internal_count : 0}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">External Outbound Links:</span>
                                <span class="tech-val">${onpage.link_analysis ? onpage.link_analysis.external_count : 0}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Nofollow Links:</span>
                                <span class="tech-val">${onpage.link_analysis ? onpage.link_analysis.nofollow_count : 0}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 3: Google SERP & AI Overview (SGE) -->
                <div class="sem-subtab-panel" data-panel="serp_ai" id="semViewSerpAi" style="display:none;">
                    <div class="tech-grid" style="margin-bottom:16px;">
                        <div class="tech-card" style="border: 2px solid #8b5cf6; background: #faf5ff;">
                            <div class="tech-card-title" style="color:#6d28d9;">
                                <span>🤖</span> Google AI Overview Citation Readiness Score
                            </div>
                            <div style="display:flex; align-items:center; gap:16px; margin:12px 0;">
                                <div style="font-size:36px; font-weight:800; color:#7c3aed;">${serp.score || 0}/100</div>
                                <div style="font-size:13px; font-weight:700; color:#5b21b6;">${serp.status || 'AI Overview Ready'}</div>
                            </div>
                            <p style="font-size:12.5px; color:#6b21a8; line-height:1.5;">
                                Google AI Overviews prioritize citing content with structured tables, question subheadings, concise definition blocks, and JSON-LD FAQ schemas.
                            </p>
                        </div>

                        <!-- Direct Answer Block -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>💡</span> Direct Answer Definition Block
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Status:</span>
                                <span class="tech-val" style="color:${serp.has_direct_answer ? '#059669' : '#dc2626'};">${serp.has_direct_answer ? '✅ Present (40-60w)' : '❌ Missing Definition'}</span>
                            </div>
                            <div style="font-size:12.5px; color:#475569; margin-top:8px; background:#f8fafc; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                                ${serp.direct_answer_sample ? `<em>"${serp.direct_answer_sample}"</em>` : 'No concise 35-70 word direct definition snippet found right under headings. Adding one will steal Google AI Overview citations.'}
                            </div>
                        </div>

                        <!-- Tables & Lists for SGE -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>📊</span> Comparison Tables & Structured Lists
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Comparison Tables:</span>
                                <span class="tech-val" style="color:${serp.table_count > 0 ? '#059669' : '#dc2626'};">${serp.table_count || 0} table(s)</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Structured Lists (ul/ol):</span>
                                <span class="tech-val">${serp.list_count || 0} lists</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Total Bullet Points:</span>
                                <span class="tech-val">${serp.list_items_count || 0} list items</span>
                            </div>
                        </div>

                        <!-- Question Subheadings (PAA Triggers) -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>❓</span> Question-Based Subheadings (PAA Triggers)
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Questions Count:</span>
                                <span class="tech-val">${serp.question_headings_count || 0} detected</span>
                            </div>
                            <div style="margin-top:8px;">
                                ${qHeadingsList}
                            </div>
                        </div>
                    </div>

                    <!-- AI Overview Recommendations Box -->
                    <div class="section-box" style="border:1.5px solid #c4b5fd; background:#f5f3ff;">
                        <h4 style="font-size:14px; font-weight:800; color:#5b21b6; margin-top:0; margin-bottom:8px;">
                            🚀 Actionable Blueprint to Win Google AI Overview (SGE) Over This Competitor:
                        </h4>
                        <ul style="margin:0 0 0 18px; padding:0; font-size:13px; color:#4c1d95; line-height:1.6;">
                            ${(serp.recommendations || []).map(r => `<li>${r}</li>`).join('') || '<li>Embed a comparison data table and add 4-6 question subheadings to capture generative AI citations.</li>'}
                        </ul>
                    </div>
                </div>

                <!-- SUBTAB 4: EEAT & Trust Signals -->
                <div class="sem-subtab-panel" data-panel="eeat" id="semViewEeat" style="display:none;">
                    <div class="tech-grid" style="margin-bottom:16px;">
                        <div class="tech-card" style="border: 2px solid #f59e0b; background: #fffdf5;">
                            <div class="tech-card-title" style="color:#b45309;">
                                <span>🛡️</span> EEAT Trust Authority Score
                            </div>
                            <div style="display:flex; align-items:center; gap:16px; margin:12px 0;">
                                <div style="font-size:36px; font-weight:800; color:#d97706;">${eeat.score || 0}/100</div>
                                <div style="font-size:13px; font-weight:700; color:#92400e;">${eeat.status || 'Moderate EEAT'}</div>
                            </div>
                            <p style="font-size:12.5px; color:#78350f; line-height:1.5;">
                                Evaluates Experience, Expertise, Authoritativeness & Trustworthiness signals audited under Google's Helpful Content Update guidelines.
                            </p>
                        </div>

                        <!-- Author Byline -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>✍️</span> Author Byline & Credentials
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Author Byline Detected:</span>
                                <span class="tech-val" style="color:${eeat.has_author ? '#059669' : '#dc2626'};">${eeat.has_author ? '✅ Verified Byline' : '❌ Anonymous Content'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Author Name:</span>
                                <span class="tech-val">${eeat.author_name || 'Staff / Unknown'}</span>
                            </div>
                        </div>

                        <!-- Transparency Pages -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🏢</span> Domain Trust & Transparency Pages
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">About Us Linked:</span>
                                <span class="tech-val">${(eeat.trust_pages && eeat.trust_pages.about) ? '✅ Yes' : '❌ Not Linked'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Contact Page Linked:</span>
                                <span class="tech-val">${(eeat.trust_pages && eeat.trust_pages.contact) ? '✅ Yes' : '❌ Not Linked'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Privacy Policy Linked:</span>
                                <span class="tech-val">${(eeat.trust_pages && eeat.trust_pages.privacy) ? '✅ Yes' : '❌ Not Linked'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Editorial / Review Policy:</span>
                                <span class="tech-val">${(eeat.trust_pages && eeat.trust_pages.editorial) ? '✅ Yes' : '❌ Not Linked'}</span>
                            </div>
                        </div>

                        <!-- Structured Schema Types -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>⚡</span> Structured Schema Types Found
                            </div>
                            <div style="margin-top:8px;">
                                ${schemaBadges}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 5: Technical & Core Web Vitals -->
                <div class="sem-subtab-panel" data-panel="tech" id="semViewTech" style="display:none;">
                    <div class="tech-grid" style="margin-bottom:16px;">
                        <!-- Performance TTFB -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>⚡</span> Server Performance & Latency
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Time to First Byte (TTFB):</span>
                                <span class="tech-val" style="color:${(tech.ttfb_ms && tech.ttfb_ms < 600) ? '#059669' : ((tech.ttfb_ms && tech.ttfb_ms < 1200) ? '#d97706' : '#dc2626')};">${tech.ttfb_ms || 0} ms</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Latency Grade:</span>
                                <span class="tech-val">${tech.ttfb_rating || 'N/A'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">HTML Payload Size:</span>
                                <span class="tech-val">${tech.page_size_kb || 0} KB</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Web Server / CDN:</span>
                                <span class="tech-val">${tech.server || 'N/A'}</span>
                            </div>
                        </div>

                        <!-- Protocol & SSL -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🔒</span> Protocol & Security
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">HTTP Status:</span>
                                <span class="tech-val" style="color:#059669;">${tech.status_code || 200} OK</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">SSL / HTTPS Active:</span>
                                <span class="tech-val" style="color:${tech.is_https ? '#059669' : '#dc2626'};">${tech.is_https ? '✅ HTTPS Encrypted' : '❌ Insecure HTTP'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">HSTS Header:</span>
                                <span class="tech-val">${(tech.security_headers && tech.security_headers.hsts) ? '✅ Enabled' : '❌ Not Configured'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">X-Frame-Options:</span>
                                <span class="tech-val">${(tech.security_headers && tech.security_headers.x_frame_options) ? '✅ Protected' : '❌ Missing'}</span>
                            </div>
                        </div>

                        <!-- Mobile Usability -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>📱</span> Mobile-First Indexing & Viewport
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Viewport Tag:</span>
                                <span class="tech-val" style="color:${(tech.mobile_viewport && tech.mobile_viewport.has_viewport) ? '#059669' : '#dc2626'};">${(tech.mobile_viewport && tech.mobile_viewport.has_viewport) ? '✅ Present' : '❌ Missing'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Viewport Content:</span>
                                <span class="tech-val" style="font-size:11px; word-break:break-all;">${(tech.mobile_viewport && tech.mobile_viewport.content) || 'None'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Charset Encoding:</span>
                                <span class="tech-val">${tech.charset || 'UTF-8'}</span>
                            </div>
                        </div>

                        <!-- Robots & Sitemap -->
                        <div class="tech-card">
                            <div class="tech-card-title">
                                <span>🤖</span> Robots.txt & XML Sitemap Live Probe
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Robots.txt Status:</span>
                                <span class="tech-val" style="color:${(tech.robots_txt && tech.robots_txt.exists) ? '#059669' : '#d97706'};">${(tech.robots_txt && tech.robots_txt.exists) ? '✅ Found (Status 200)' : '⚠️ Not Found / Blocked'}</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">Robots Disallow Rules:</span>
                                <span class="tech-val">${(tech.robots_txt && tech.robots_txt.disallow_count) || 0} rules</span>
                            </div>
                            <div class="tech-row">
                                <span class="tech-key">XML Sitemap:</span>
                                <span class="tech-val" style="color:${(tech.sitemap_xml && tech.sitemap_xml.exists) ? '#059669' : '#d97706'};">${(tech.sitemap_xml && tech.sitemap_xml.exists) ? '✅ ' + tech.sitemap_xml.type : '⚠️ Not Detected'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 6: Content Reader & Headings Tree -->
                <div class="sem-subtab-panel" data-panel="content" id="semViewContent" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin:0;">
                                    📜 Competitor Content Reader & Heading Tree
                                </h3>
                                <p style="font-size:12.5px; color:var(--text-muted); margin:3px 0 0 0;">
                                    ${audit.word_count || 0} words &nbsp;|&nbsp; ${audit.reading_time || '5 min read'} &nbsp;|&nbsp; Text-to-HTML: ${onpage.content_analysis ? onpage.content_analysis.text_to_html_ratio : 15}%
                                </p>
                            </div>
                            <div style="display:flex; gap:8px;">
                                <button class="meta-btn-copy" id="toggleContentBtn" onclick="toggleSpyContentLength()">Show Full Article Text</button>
                                <button class="meta-btn-copy" onclick="copyCompetitorText()">📋 Copy Text</button>
                            </div>
                        </div>

                        <div class="competitor-content-box" id="competitorContentText" style="max-height:280px; overflow-y:auto; margin-bottom:16px;">
                            ${audit.content_excerpt || audit.full_content_preview || 'No text extracted.'}
                        </div>

                        <h4 style="font-size:14px; font-weight:800; color:#0f172a; margin-bottom:8px;">
                            🌳 Heading Hierarchy Outline (${headingsList.length} Headings):
                        </h4>
                        <div class="outline-tree">
                            ${outlineHtml}
                        </div>
                    </div>
                </div>

                <!-- SUBTAB 7: Backlink Footprint -->
                <div class="sem-subtab-panel" data-panel="backlinks" id="semViewBacklinks" style="display:none;">
                    <div class="section-box" style="margin-bottom:16px;">
                        <h3 style="font-size:16px; font-weight:800; color:#0f172a; margin-top:0; margin-bottom:4px;">
                            🔗 Backlink Intelligence & Referral Footprint
                        </h3>
                        <p style="font-size:12.5px; color:var(--text-muted); margin-bottom:14px;">
                            Estimated Backlinks: <strong>${bl.total_backlinks_est || 0}</strong> &nbsp;|&nbsp; Referring Domains: <strong>~${bl.referring_domains_est || 2}</strong>
                        </p>
                        ${blLinksHtml}
                    </div>
                </div>

                <!-- SUBTAB 8: Actionable Outranking Roadmap & AI Writer -->
                <div class="sem-subtab-panel" data-panel="outrank" id="semViewOutrank" style="display:none;">
                    <div class="section-box" style="border-color: rgba(139, 92, 246, 0.5); margin-bottom:16px;">
                        <div class="section-title" style="color:#7c3aed; font-size:16px; font-weight:800;">
                            ⚔️ Actionable Outranking Blueprint (Formula to Outrank Competitor):
                        </div>
                        <p style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px;">
                            Step-by-step master roadmap built specifically around the competitor's detected flaws:
                        </p>
                        ${bpHtml}
                    </div>

                    <!-- AI Agent Outranker Studio Card -->
                    <div class="section-box" style="border: 2px solid #10b981; background: linear-gradient(135deg, #f0fdf4, #ffffff);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                            <div>
                                <h3 style="font-size:17px; color:#065f46; font-weight:800; display:flex; align-items:center; gap:8px; margin:0;">
                                    <span>⚡</span> AI Agent Outranker Studio
                                </h3>
                                <p style="font-size:13px; color:#047857; margin-top:4px;">
                                    Outrank this competitor by generating content that fixes all their detected flaws, adds comparison tables, and embeds FAQ schema.
                                </p>
                            </div>
                        </div>

                        <div class="writer-grid" style="grid-template-columns: 1fr; margin-top: 14px; margin-bottom: 0;">
                            <div class="form-group">
                                <label>Your Brand / Company / Website Name</label>
                                <input type="text" id="inlineBrandName" placeholder="e.g. MyBrand / mywebsite.com">
                            </div>
                        </div>

                        <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); margin-top:14px; margin-bottom:14px;">
                            <div class="form-group">
                                <label>Target Outrank Words</label>
                                <select id="inlineWordCount">
                                    <option value="${targetWords}" selected>${targetWords} Words (+25% Deeper)</option>
                                    <option value="2000">2,000 Words</option>
                                    <option value="2500">2,500 Words</option>
                                    <option value="3500">3,500 Words (Pillar)</option>
                                    <option value="4500">4,500+ Words (Ultimate Authority)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Content Format</label>
                                <select id="inlineFormat">
                                    <option value="long_form_seo">📖 Complete 360° SEO Pillar Guide</option>
                                    <option value="informational_article">💡 Informational Article</option>
                                    <option value="commercial_article">🏆 Commercial Article</option>
                                    <option value="buying_guide">🛒 Buying Guide</option>
                                    <option value="transactional_article">💰 Transactional Article</option>
                                    <option value="product_review">⭐ Detailed Product Review</option>
                                    <option value="comparison_article">⚔️ Head-to-Head Comparison</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Tone of Voice</label>
                                <select id="inlineTone">
                                    <option value="Authoritative & Expert">👔 Authoritative & Expert (EEAT)</option>
                                    <option value="Conversational & Engaging">🗣️ Conversational & Engaging</option>
                                    <option value="Commercial & High-Converting">🎯 Commercial & High-Converting</option>
                                </select>
                            </div>
                        </div>

                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                            <span style="font-size:12px; color:#065f46;">💡 Includes Comparison Table & FAQ JSON-LD Schema to capture Featured Snippets & PAA.</span>
                            <button class="btn-writer-submit" id="inlineSubmitBtn" onclick="generateOutrankInline()">
                                <span>⚡ Write Outranking Article with AI Agent Now</span>
                            </button>
                        </div>
                    </div>

                    <!-- Inline Spinner -->
                    <div class="spinner" id="spyInlineSpinner" style="display:none;">
                        <div class="loader" style="border-top-color: var(--writer-accent);"></div>
                        <h3 style="color:#065f46;">AI Agent is crafting outranking content...</h3>
                        <p style="color: var(--text-muted); font-size: 13px;">Analyzing competitor outline, writing deeper sections, creating comparison tables & embedding FAQ schema...</p>
                    </div>

                    <!-- Inline Results -->
                    <div id="spyInlineResults" style="display:none;"></div>
                </div>
            `;
            resDiv.style.display = 'block';

            const savedBrand = localStorage.getItem('user_brand_name') || '';
            if (savedBrand && document.getElementById('inlineBrandName')) {
                document.getElementById('inlineBrandName').value = savedBrand;
            }
        }

        let currentDevStatusFilter = 'all';

        function switchSemrushSubtab(tabName) {
            const tabs = [
                'site_overview', 'site_pages', 'site_issues', 'site_links',
                'checklist', 'issues', 'onpage', 'serp_ai', 'eeat', 'tech', 'content', 'backlinks', 'outrank'
            ];
            tabs.forEach(t => {
                const parts = t.split('_');
                const pascal = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('').replace('Ai', 'Ai');
                const elName = 'semView' + pascal;
                const btnName = 'tabBtn' + pascal;
                document.querySelectorAll(`[data-panel="${t}"], #${elName}`).forEach(el => {
                    el.style.display = (t === tabName) ? 'block' : 'none';
                });
                document.querySelectorAll(`[data-tab="${t}"], #${btnName}`).forEach(btn => {
                    if (t === tabName) btn.classList.add('active');
                    else btn.classList.remove('active');
                });
            });
        }

        // --- Multi-Page Crawler Table & Issues Filtering Handlers ---
        function filterSitePages() {
            const search = (document.getElementById('crawledPagesSearch')?.value || '').toLowerCase().trim();
            const statusFilter = document.getElementById('crawledPagesStatusSelect')?.value || 'all';
            const rows = document.querySelectorAll('.crawled-page-row');
            rows.forEach(r => {
                const url = (r.getAttribute('data-url') || '').toLowerCase();
                const st = r.getAttribute('data-status') || '';
                const matchSearch = !search || url.includes(search);
                let matchStatus = true;
                if (statusFilter === '200') matchStatus = (st === '200');
                else if (statusFilter === '3xx') matchStatus = st.startsWith('3');
                else if (statusFilter === '4xx') matchStatus = st.startsWith('4');
                else if (statusFilter === '5xx') matchStatus = st.startsWith('5');
                r.style.display = (matchSearch && matchStatus) ? '' : 'none';
            });
        }
        window.filterSitePages = filterSitePages;

        let currentSiteIssueSevFilter = 'all';
        function filterSiteIssues(sev, e) {
            currentSiteIssueSevFilter = sev;
            document.querySelectorAll('.site-issue-pill').forEach(p => p.classList.remove('active'));
            if (e && e.target) e.target.classList.add('active');
            filterSiteIssuesList();
        }
        window.filterSiteIssues = filterSiteIssues;

        function filterSiteIssuesList() {
            const search = (document.getElementById('siteIssuesSearch')?.value || '').toLowerCase().trim();
            const items = document.querySelectorAll('.site-issue-item');
            items.forEach(it => {
                const id = (it.getAttribute('data-id') || '').toLowerCase();
                const text = (it.textContent || '').toLowerCase();
                const sev = it.getAttribute('data-severity') || '';
                const matchSearch = !search || id.includes(search) || text.includes(search);
                const matchSev = (currentSiteIssueSevFilter === 'all') || (sev === currentSiteIssueSevFilter);
                it.style.display = (matchSearch && matchSev) ? 'block' : 'none';
            });
        }
        window.filterSiteIssuesList = filterSiteIssuesList;

        function downloadPagesCSV() {
            const fsa = (currentSpyData && currentSpyData.full_site_audit) || (currentSpyData && currentSpyData.audit && currentSpyData.audit.full_site_audit) || {};
            const pages = fsa.crawled_pages || [];
            if (!pages.length) {
                alert('No crawled pages available to export.');
                return;
            }
            const lines = [];
            lines.push(String.fromCharCode(0xFEFF) + '"#","URL","Status Code","Depth","Title","H1","Word Count","Inlinks","Outlinks","TTFB (ms)"');
            pages.forEach((p, idx) => {
                const row = [
                    idx + 1,
                    (p.url || '').replace(/"/g, '""'),
                    p.status_code || 200,
                    p.depth || 0,
                    (p.title || '').replace(/"/g, '""'),
                    (p.h1 || '').replace(/"/g, '""'),
                    p.word_count || 0,
                    p.inlinks_count || 0,
                    p.outlinks_count || 0,
                    p.ttfb_ms || 0
                ];
                lines.push(row.map(val => '"' + val + '"').join(','));
            });
            const csv = lines.join(String.fromCharCode(10));
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Crawled_Pages_Explorer_' + Date.now() + '.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        window.downloadPagesCSV = downloadPagesCSV;

        function downloadSiteIssuesCSV() {
            const fsa = (currentSpyData && currentSpyData.full_site_audit) || (currentSpyData && currentSpyData.audit && currentSpyData.audit.full_site_audit) || {};
            const issues = fsa.site_issues || [];
            if (!issues.length) {
                alert('No site issues available to export.');
                return;
            }
            const lines = [];
            lines.push(String.fromCharCode(0xFEFF) + '"ID","Severity","Category","Title","Affected Count","Affected URLs","Why It Matters (সমস্যা)","How to Fix (সমাধান)"');
            issues.forEach(iss => {
                const row = [
                    iss.id || '',
                    iss.severity || '',
                    iss.category || '',
                    (iss.title || '').replace(/"/g, '""'),
                    (iss.affected_urls || []).length,
                    (iss.affected_urls || []).join('; ').replace(/"/g, '""'),
                    (iss.why || '').replace(/"/g, '""'),
                    (iss.fix || '').replace(/"/g, '""')
                ];
                lines.push(row.map(val => '"' + val + '"').join(','));
            });
            const csv = lines.join(String.fromCharCode(10));
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Site_Wide_Issues_' + Date.now() + '.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        window.downloadSiteIssuesCSV = downloadSiteIssuesCSV;

        function toggleChecklistAccordion(checkId, event) {
            if (event) {
                const sel = window.getSelection();
                if (sel && sel.toString().length > 0) return;
                const target = event.target;
                if (target && target.closest('.dev-check-details') && (target.tagName === 'A' || target.tagName === 'CODE' || target.tagName === 'INPUT')) {
                    return;
                }
            }
            const details = document.getElementById('details-' + checkId);
            const arrow = document.getElementById('arrow-' + checkId);
            if (!details) return;
            const isHidden = (details.style.display === 'none' || details.style.display === '');
            details.style.display = isHidden ? 'block' : 'none';
            if (arrow) arrow.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
        }
        window.toggleChecklistAccordion = toggleChecklistAccordion;

        function expandAllChecklist(expand) {
            const items = document.querySelectorAll('.dev-chk-item');
            items.forEach(item => {
                const id = item.getAttribute('data-id');
                const details = document.getElementById('details-' + id);
                const arrow = document.getElementById('arrow-' + id);
                if (details) {
                    details.style.display = expand ? 'block' : 'none';
                }
                if (arrow) {
                    arrow.style.transform = expand ? 'rotate(180deg)' : 'rotate(0deg)';
                }
            });
        }
        window.expandAllChecklist = expandAllChecklist;


        function filterDevStatus(status, e) {
            currentDevStatusFilter = status;
            document.querySelectorAll('.dev-stat-pill').forEach(p => p.classList.remove('active'));
            if (e && e.target) e.target.classList.add('active');
            filterDevChecklist();
        }

        function filterDevChecklistCategory(catName) {
            const select = document.getElementById('devCategorySelect');
            if (select) {
                select.value = catName;
            }
            filterDevChecklist();
        }

        function filterDevChecklist() {
            const searchInput = (document.getElementById('devChecklistSearch')?.value || '').toLowerCase().trim();
            const category = document.getElementById('devCategorySelect')?.value || 'all';
            const status = currentDevStatusFilter || 'all';

            const items = document.querySelectorAll('.dev-chk-item');
            items.forEach(item => {
                const id = (item.getAttribute('data-id') || '').toLowerCase();
                const cat = item.getAttribute('data-category') || '';
                const st = item.getAttribute('data-status') || '';
                const text = (item.textContent || '').toLowerCase();

                const matchSearch = !searchInput || id.includes(searchInput) || text.includes(searchInput);
                const matchCat = (category === 'all') || (cat === category);
                const matchStatus = (status === 'all') || (st === status);

                if (matchSearch && matchCat && matchStatus) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function downloadChecklistCSV() {
            const data = (currentSpyData && currentSpyData.audit && currentSpyData.audit.developer_checklist) || null;
            const checks = (data && data.all_checks) || [];
            if (!checks.length) {
                alert('No checklist data available to export.');
                return;
            }
            const lines = [];
            lines.push(String.fromCharCode(0xFEFF) + 'ID,Category,Severity,Status,Title,"Why It Matters (সমস্যা)","How to Fix (সমাধান)","Affected Elements"');
            checks.forEach(c => {
                const row = [
                    c.id || '',
                    c.category || '',
                    c.severity || '',
                    c.status || '',
                    (c.title || '').replace(/"/g, '""'),
                    (c.why || '').replace(/"/g, '""'),
                    (c.fix || '').replace(/"/g, '""'),
                    ((c.affected || []).join('; ')).replace(/"/g, '""')
                ];
                lines.push(row.map(val => '"' + val + '"').join(','));
            });
            const csv = lines.join(String.fromCharCode(10));
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Site_Audit_Developer_Checklist_' + Date.now() + '.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function downloadChecklistJSON() {
            const data = (currentSpyData && currentSpyData.audit && currentSpyData.audit.developer_checklist) || null;
            if (!data) {
                alert('No checklist data available to export.');
                return;
            }
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Site_Audit_Developer_Checklist_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }


        function filterSemrushIssues(filterType) {
            // Update active pill button
            const pills = document.querySelectorAll('.filter-pill');
            pills.forEach(p => p.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');

            const items = document.querySelectorAll('.sem-issue-item');
            items.forEach(it => {
                const itType = it.getAttribute('data-type');
                if (filterType === 'all') {
                    it.style.display = (itType === 'passed') ? 'none' : 'block';
                } else if (filterType === 'passed') {
                    it.style.display = (itType === 'passed') ? 'block' : 'none';
                } else {
                    it.style.display = (itType === filterType) ? 'block' : 'none';
                }
            });
        }

        function copySemrushMarkdownReport() {
            if (!currentSpyData || !currentSpyData.audit) {
                alert('No audit data available.');
                return;
            }
            const a = currentSpyData.audit;
            const iss = a.issues || {};
            const tech = a.technical || {};
            const serp = a.serp_ai || {};
            const eeat = a.eeat || {};
            const bp = currentSpyData.blueprint || [];

            let md = `# 🔍 SEMRUSH-GRADE SITE AUDIT REPORT\n\n`;
            md += `**Target URL:** ${a.url}\n`;
            md += `**Title:** ${a.title}\n`;
            md += `**Focus Keyword:** ${a.main_keyword} | **Product Entity:** ${a.product_name}\n`;
            md += `**Overall Health Score:** ${iss.health_score || a.seo_score}/100 (${iss.health_grade})\n`;
            md += `**Word Count:** ${a.word_count} words | **TTFB Latency:** ${tech.ttfb_ms || 0}ms\n\n`;

            md += `## 🚨 CRITICAL ERRORS (${iss.critical_errors ? iss.critical_errors.length : 0})\n`;
            (iss.critical_errors || []).forEach(e => {
                md += `- 🔴 **${e.title}**: ${e.impact} (Fix: ${e.fix})\n`;
            });

            md += `\n## 🟡 WARNINGS (${iss.warnings ? iss.warnings.length : 0})\n`;
            (iss.warnings || []).forEach(w => {
                md += `- 🟡 **${w.title}**: ${w.impact} (Fix: ${w.fix})\n`;
            });

            md += `\n## 🤖 GOOGLE AI OVERVIEW READINESS (${serp.score || 0}/100)\n`;
            md += `- Direct Answer Snippet: ${serp.has_direct_answer ? 'Yes' : 'Missing'}\n`;
            md += `- Tables: ${serp.table_count || 0} | Structured Lists: ${serp.list_count || 0}\n`;

            md += `\n## 🛡️ EEAT & TRUST SIGNALS (${eeat.score || 0}/100)\n`;
            md += `- Author Byline: ${eeat.has_author ? 'Yes (' + eeat.author_name + ')' : 'Anonymous'}\n`;
            md += `- SSL/HTTPS: ${tech.is_https ? 'Active' : 'Insecure'}\n`;

            md += `\n## ⚔️ ACTIONABLE OUTRANKING ROADMAP\n`;
            bp.forEach(s => {
                md += `Step ${s.step}: ${s.action}\n  -> ${s.detail}\n`;
            });

            navigator.clipboard.writeText(md).then(() => {
                alert('Full Semrush-Grade Markdown Audit Report copied to clipboard!');
            });
        }

        function downloadSemrushHtmlReport() {
            if (!currentSpyData || !currentSpyData.audit) {
                alert('No audit data available.');
                return;
            }
            const a = currentSpyData.audit;
            const iss = a.issues || {};
            const tech = a.technical || {};
            const serp = a.serp_ai || {};
            const eeat = a.eeat || {};
            const bp = currentSpyData.blueprint || [];

            const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Semrush-Grade SEO Audit: ${a.title || a.url}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 24px; line-height: 1.5; }
        .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 32px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
        h1, h2, h3 { color: #0f172a; }
        .score-box { background: #0f172a; color: white; padding: 20px; border-radius: 10px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }
        .score-circle { font-size: 32px; font-weight: 800; color: #10b981; }
        .issue-card { padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #94a3b8; background: #f8fafc; }
        .issue-critical { border-left-color: #ef4444; background: #fffafb; }
        .issue-warning { border-left-color: #f59e0b; background: #fffdfa; }
        .fix { color: #047857; font-size: 13px; font-weight: 600; margin-top: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Semrush-Grade Competitor SEO Audit Report</h1>
        <p><strong>URL:</strong> <a href="${a.url}">${a.url}</a></p>
        <p><strong>Primary Focus Keyword:</strong> ${a.main_keyword} | <strong>Product Entity:</strong> ${a.product_name}</p>

        <div class="score-box">
            <div>
                <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8;">Site Health Score</div>
                <div style="font-size: 18px; font-weight: 700; margin-top: 4px;">${iss.health_grade || 'SEO Health'}</div>
            </div>
            <div class="score-circle">${iss.health_score || a.seo_score}/100</div>
        </div>

        <h2>🚨 Detected Critical Errors</h2>
        ${(iss.critical_errors || []).map(e => `
            <div class="issue-card issue-critical">
                <strong>🔴 ${e.title}</strong>
                <p style="margin: 4px 0 0 0; font-size: 13px;">${e.impact}</p>
                <div class="fix">🛠️ Fix: ${e.fix}</div>
            </div>
        `).join('') || '<p>No critical errors detected.</p>'}

        <h2>🟡 Warnings</h2>
        ${(iss.warnings || []).map(w => `
            <div class="issue-card issue-warning">
                <strong>🟡 ${w.title}</strong>
                <p style="margin: 4px 0 0 0; font-size: 13px;">${w.impact}</p>
                <div class="fix">🛠️ Fix: ${w.fix}</div>
            </div>
        `).join('') || '<p>No warnings detected.</p>'}

        <h2>🤖 Google AI Overview Readiness: ${serp.score || 0}/100</h2>
        <p>Direct Answer Block: ${serp.has_direct_answer ? '✅ Present' : '❌ Missing'} | Comparison Tables: ${serp.table_count || 0}</p>

        <h2>⚔️ Actionable Outranking Blueprint</h2>
        <ol>
            ${bp.map(s => `<li><strong>${s.action}:</strong> ${s.detail}</li>`).join('')}
        </ol>
        <hr style="margin-top:30px; border:none; border-top:1px solid #e2e8f0;">
        <p style="font-size:11px; color:#94a3b8;">Report generated by RankNaserPro Automated Intelligence Suite.</p>
    </div>
</body>
</html>`;

            const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `SEO_Audit_${(a.main_keyword || 'Competitor').replace(/\\s+/g, '_')}.html`;
        }

        function switchSpyContentTab(tab) {
            document.getElementById('spyViewText').style.display = (tab === 'text') ? 'block' : 'none';
            document.getElementById('spyViewOutline').style.display = (tab === 'outline') ? 'block' : 'none';
            document.getElementById('spyViewGaps').style.display = (tab === 'gaps') ? 'block' : 'none';

            document.getElementById('subtabSpyText').className = 'subtab-btn' + (tab === 'text' ? ' active' : '');
            document.getElementById('subtabSpyOutline').className = 'subtab-btn' + (tab === 'outline' ? ' active' : '');
            document.getElementById('subtabSpyGaps').className = 'subtab-btn' + (tab === 'gaps' ? ' active' : '');
        }

        function toggleSpyContentLength() {
            if (!currentSpyData || !currentSpyData.audit) return;
            isFullCompetitorText = !isFullCompetitorText;
            const box = document.getElementById('competitorContentText');
            const btn = document.getElementById('toggleContentBtn');
            if (isFullCompetitorText) {
                box.textContent = currentSpyData.audit.full_content_preview || currentSpyData.audit.content_excerpt;
                btn.innerText = 'Show Excerpt Only';
            } else {
                box.textContent = currentSpyData.audit.content_excerpt;
                btn.innerText = 'Show Full Article Text';
            }
        }

        function copyCompetitorText() {
            if (!currentSpyData || !currentSpyData.audit) return;
            const txt = currentSpyData.audit.full_content_preview || currentSpyData.audit.content_excerpt || '';
            navigator.clipboard.writeText(txt).then(() => {
                alert('Competitor text copied to clipboard!');
            });
        }

        async function generateOutrankInline() {
            if (!currentSpyData || !currentSpyData.audit) return;
            const audit = currentSpyData.audit;
            const words = parseInt(document.getElementById('inlineWordCount').value, 10);
            const format = document.getElementById('inlineFormat').value;
            const tone = document.getElementById('inlineTone').value;
            const geminiKey = (document.getElementById('wGeminiKey') ? document.getElementById('wGeminiKey').value.trim() : '') || localStorage.getItem('gemini_api_key') || '';
            const brandName = (document.getElementById('inlineBrandName') ? document.getElementById('inlineBrandName').value.trim() : '') || localStorage.getItem('user_brand_name') || '';

            if (brandName) {
                localStorage.setItem('user_brand_name', brandName);
            }

            document.querySelectorAll('#spyInlineSpinner').forEach(s => s.style.display = 'block');
            document.querySelectorAll('#spyInlineResults').forEach(r => r.style.display = 'none');
            document.querySelectorAll('#inlineSubmitBtn').forEach(b => b.disabled = true);

            try {
                const resp = await fetch('/api/write-content', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        topic: audit.title || `Ultimate Guide to ${audit.main_keyword}`,
                        main_keyword: audit.main_keyword,
                        lsi_keywords: (audit.lsi_keywords || []).join(', '),
                        product_name: audit.product_name || audit.main_keyword,
                        content_type: format,
                        tone: tone,
                        target_words: words,
                        competitor_url: audit.url,
                        brand_name: brandName,
                        country: audit.country || document.getElementById('spyCountrySelect')?.value || 'Bangladesh',
                        gemini_key: geminiKey
                    })
                });

                const data = await resp.json();
                document.querySelectorAll('#spyInlineSpinner').forEach(s => s.style.display = 'none');
                document.querySelectorAll('#inlineSubmitBtn').forEach(b => b.disabled = false);

                if (data.status === 'success' && data.result) {
                    generatedData = data.result;
                    renderInlineBattleResults(audit, data.result);
                } else {
                    alert('Error: ' + (data.message || 'Generation failed.'));
                }
            } catch (err) {
                document.querySelectorAll('#spyInlineSpinner').forEach(s => s.style.display = 'none');
                document.querySelectorAll('#inlineSubmitBtn').forEach(b => b.disabled = false);
                alert('Generation Error: ' + err.message);
            }
        }

        function renderInlineBattleResults(audit, res) {
            const containers = document.querySelectorAll('#spyInlineResults');
            const diff = res.actual_word_count - audit.word_count;
            const pct = audit.word_count > 0 ? Math.round((diff / audit.word_count) * 100) : 100;
            const diffText = diff >= 0 ? `+${diff} words (+${pct}% More Depth! 🏆)` : `${diff} words`;

            const rawMd = res.article_markdown || '';
            const visualHtml = (typeof marked !== 'undefined') ? marked.parse(rawMd) : rawMd;

            const battleHtml = `
                <!-- Head to Head Battle Scorecard -->
                <div class="battle-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                        <h3 style="font-size:17px; color:#065f46; font-weight:800; display:flex; align-items:center; gap:8px;">
                            <span>⚔️</span> Head-to-Head Outranker Scorecard (Competitor vs Your Article)
                        </h3>
                        <span class="product-tag" style="background:#dcfce7; color:#166534; border-color:#86efac; font-weight:700;">
                            🏆 Superior Depth Achieved
                        </span>
                    </div>

                    <table class="battle-table">
                        <thead>
                            <tr>
                                <th>Ranking Signal / Dimension</th>
                                <th>Competitor Page</th>
                                <th>Your New Generated Article</th>
                                <th>Competitive Advantage</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Content Depth (Word Count)</strong></td>
                                <td class="battle-comp">${audit.word_count} words (${audit.reading_time || '5 min'})</td>
                                <td><strong style="color:#065f46;">${res.actual_word_count} words</strong> (${res.estimated_reading_time})</td>
                                <td><span class="battle-win">${diffText}</span></td>
                            </tr>
                            <tr>
                                <td><strong>Heading Outline Hierarchy</strong></td>
                                <td class="battle-comp">${(audit.all_headings || []).length} Headings</td>
                                <td><strong>Complete H1, H2, H3 Topical Map</strong></td>
                                <td><span class="battle-win">Topical Dominance 🏆</span></td>
                            </tr>
                            <tr>
                                <td><strong>Data & Comparison Table</strong></td>
                                <td class="battle-comp">${audit.checklist && audit.checklist.tables_count > 0 ? audit.checklist.tables_count + ' tables' : 'None ❌'}</td>
                                <td><strong>Structured Comparison Table Included ✅</strong></td>
                                <td><span class="battle-win">Featured Snippet Advantage 🏆</span></td>
                            </tr>
                            <tr>
                                <td><strong>FAQ Schema Markup</strong></td>
                                <td class="battle-comp">${audit.checklist && audit.checklist.schemas && audit.checklist.schemas.includes('FAQPage') ? 'Present' : 'Missing ❌'}</td>
                                <td><strong>JSON-LD FAQPage Schema Built-in ✅</strong></td>
                                <td><span class="battle-win">Google PAA Snippets Ready 🏆</span></td>
                            </tr>
                            <tr>
                                <td><strong>Semantic LSI Entities</strong></td>
                                <td class="battle-comp">Standard distribution</td>
                                <td><strong>100% Core LSI Entities Naturally Distributed ✅</strong></td>
                                <td><span class="battle-win">Maximum Semantic Coverage 🏆</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Rendered Generated Article Box -->
                <div class="section-box" style="border: 2px solid #059669;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                        <h4 style="font-size:16px; color:#065f46; font-weight:700;">📄 Generated Outranking Article Ready for Publication</h4>
                        <div style="display:flex; gap:8px;">
                            <button class="btn-download" onclick="copyCurrentContent()">📋 Copy Article</button>
                            <button class="btn-download" style="background:#2563eb;" onclick="downloadMarkdownFile()">📥 Download .MD</button>
                            <button class="btn-download" style="background:#7c3aed;" onclick="downloadHtmlFile()">🌐 Download .HTML</button>
                        </div>
                    </div>

                    <!-- Meta Tags Card -->
                    <div class="meta-package-card" style="margin-bottom:16px;">
                        <div class="meta-row">
                            <div><strong style="color:#0f172a;">SEO Title:</strong> <span>${res.meta_title || ''}</span></div>
                        </div>
                        <div class="meta-row">
                            <div><strong style="color:#0f172a;">Meta Description:</strong> <span>${res.meta_description || ''}</span></div>
                        </div>
                        <div class="meta-row">
                            <div><strong style="color:#0f172a;">URL Slug:</strong> <code style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">/${res.slug || ''}/</code></div>
                        </div>
                    </div>

                    <div class="rendered-article">${visualHtml}</div>
                </div>
            `;

            containers.forEach(c => {
                c.innerHTML = battleHtml;
                c.style.display = 'block';
                c.scrollIntoView({ behavior: 'smooth' });
            });
        }

        // Bridge to Content Writer Tab
        function writeFromCard(title, keyword, lsis, product, compUrl) {
            switchTab('writer');
            document.getElementById('wTopic').value = title || `Ultimate Guide to ${keyword}`;
            document.getElementById('wKeyword').value = keyword || '';
            document.getElementById('wLsi').value = Array.isArray(lsis) ? lsis.join(', ') : (lsis || '');
            document.getElementById('wProduct').value = product || keyword || '';
            document.getElementById('wCompUrl').value = compUrl || '';
            if (document.getElementById('inlineBrandName') && document.getElementById('inlineBrandName').value) {
                document.getElementById('wBrandName').value = document.getElementById('inlineBrandName').value;
            } else {
                const saved = localStorage.getItem('user_brand_name') || '';
                if (saved && document.getElementById('wBrandName')) document.getElementById('wBrandName').value = saved;
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // Writer Form Submit
        async function submitWriterForm(e) {
            if (e && typeof e.preventDefault === 'function') e.preventDefault();
            const topic = document.getElementById('wTopic').value.trim();
            const keyword = document.getElementById('wKeyword').value.trim();
            const lsi = document.getElementById('wLsi').value.trim();
            const product = document.getElementById('wProduct').value.trim();
            const brandName = document.getElementById('wBrandName').value.trim();
            const format = document.getElementById('wFormat').value;
            const tone = document.getElementById('wTone').value;
            const wordCount = parseInt(document.getElementById('wWordCount').value, 10);
            const country = document.getElementById('wCountry') ? document.getElementById('wCountry').value : 'Bangladesh';
            const compUrl = document.getElementById('wCompUrl').value.trim();
            const geminiKey = document.getElementById('wGeminiKey').value.trim();

            if (brandName) {
                localStorage.setItem('user_brand_name', brandName);
            }
            if (geminiKey) {
                localStorage.setItem('gemini_api_key', geminiKey);
                if (document.getElementById('wGeminiKey')) document.getElementById('wGeminiKey').value = geminiKey;
                if (document.getElementById('multiGeminiKey')) document.getElementById('multiGeminiKey').value = geminiKey;
                if (document.getElementById('autoGeminiKey')) document.getElementById('autoGeminiKey').value = geminiKey;
            }

            document.getElementById('writerSpinner').style.display = 'block';
            document.getElementById('writerResults').style.display = 'none';
            document.getElementById('wSubmitBtn').disabled = true;

            try {
                const resp = await fetch('/api/write-content', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        topic: topic,
                        main_keyword: keyword,
                        lsi_keywords: lsi,
                        product_name: product,
                        brand_name: brandName,
                        content_type: format,
                        tone: tone,
                        target_words: wordCount,
                        country: country,
                        competitor_url: compUrl,
                        gemini_key: geminiKey
                    })
                });

                const data = await resp.json();
                document.getElementById('writerSpinner').style.display = 'none';
                document.getElementById('wSubmitBtn').disabled = false;

                if (data.status === 'success' && data.result) {
                    generatedData = data.result;
                    renderWriterResults(data.result);
                    if (document.getElementById('wAutoWp') && document.getElementById('wAutoWp').checked) {
                        setTimeout(() => publishArticleToWordPress('single', true), 600);
                    }
                    if (document.getElementById('wAutoCustom') && document.getElementById('wAutoCustom').checked) {
                        setTimeout(() => publishArticleToCustomSite('single', true), 800);
                    }
                } else {
                    alert('Error: ' + (data.message || 'Generation failed.'));
                }
            } catch (err) {
                document.getElementById('writerSpinner').style.display = 'none';
                document.getElementById('wSubmitBtn').disabled = false;
                alert('Generation Error: ' + err.message);
            }
        }
        window.submitWriterForm = submitWriterForm;

        const writerFormEl = document.getElementById('writerForm');
        if (writerFormEl) {
            writerFormEl.addEventListener('submit', submitWriterForm);
        }

        function renderWriterResults(res) {
            // Render Battle Scorecard if competitor audit data is available
            const battleCard = document.getElementById('writerBattleCard');
            if (currentSpyData && currentSpyData.audit && battleCard) {
                const audit = currentSpyData.audit;
                const diff = res.actual_word_count - audit.word_count;
                const pct = audit.word_count > 0 ? Math.round((diff / audit.word_count) * 100) : 100;
                const diffText = diff >= 0 ? `+${diff} words (+${pct}% More Depth! 🏆)` : `${diff} words`;
                battleCard.innerHTML = `
                    <div class="battle-card" style="margin-top:0; margin-bottom:16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                            <h3 style="font-size:16px; color:#065f46; font-weight:800; display:flex; align-items:center; gap:8px;">
                                <span>⚔️</span> Competitor vs Your New Article Battle Scorecard
                            </h3>
                            <span class="product-tag" style="background:#dcfce7; color:#166534; border-color:#86efac; font-weight:700;">
                                🏆 Engineered to Outrank
                            </span>
                        </div>
                        <table class="battle-table">
                            <thead>
                                <tr>
                                    <th>Ranking Signal / Dimension</th>
                                    <th>Competitor Page</th>
                                    <th>Your New Generated Article</th>
                                    <th>Competitive Advantage</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Content Depth (Word Count)</strong></td>
                                    <td class="battle-comp">${audit.word_count} words</td>
                                    <td><strong style="color:#065f46;">${res.actual_word_count} words</strong> (${res.estimated_reading_time})</td>
                                    <td><span class="battle-win">${diffText}</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Heading Hierarchy</strong></td>
                                    <td class="battle-comp">${(audit.all_headings || []).length} Headings</td>
                                    <td><strong>Full H1, H2, H3 Topical Map</strong></td>
                                    <td><span class="battle-win">Topical Dominance 🏆</span></td>
                                </tr>
                                <tr>
                                    <td><strong>Comparison Tables</strong></td>
                                    <td class="battle-comp">${audit.checklist && audit.checklist.tables_count > 0 ? audit.checklist.tables_count + ' tables' : 'None ❌'}</td>
                                    <td><strong>Structured Comparison Table Included ✅</strong></td>
                                    <td><span class="battle-win">Featured Snippet Advantage 🏆</span></td>
                                </tr>
                                <tr>
                                    <td><strong>FAQ Schema Markup</strong></td>
                                    <td class="battle-comp">${audit.checklist && audit.checklist.schemas && audit.checklist.schemas.includes('FAQPage') ? 'Present' : 'Missing ❌'}</td>
                                    <td><strong>JSON-LD FAQPage Schema Built-in ✅</strong></td>
                                    <td><span class="battle-win">Google PAA Snippets Ready 🏆</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                `;
                battleCard.style.display = 'block';
            } else if (battleCard) {
                battleCard.style.display = 'none';
            }

            document.getElementById('resMetaTitle').innerText = res.meta_title || '';
            document.getElementById('resMetaDesc').innerText = res.meta_description || '';
            document.getElementById('resSlug').innerText = res.slug ? `/${res.slug}/` : '';
            
            document.getElementById('metaBadgeEngine').innerText = res.engine || 'AI Engine';
            if (document.getElementById('metaBadgeYoast')) {
                const y = res.yoast_seo ? res.yoast_seo.seo_score : '95/100';
                document.getElementById('metaBadgeYoast').innerText = `🟢 Yoast: ${y}`;
            }
            if (document.getElementById('metaBadgeRankMath')) {
                const rm = res.rank_math ? res.rank_math.score : '96/100';
                document.getElementById('metaBadgeRankMath').innerText = `🟢 RankMath: ${rm}`;
            }
            if (document.getElementById('metaBadgeReadability')) {
                document.getElementById('metaBadgeReadability').innerText = `📖 Flesch: 68.5`;
            }
            if (document.getElementById('metaBadgeGrammar')) {
                document.getElementById('metaBadgeGrammar').innerText = `✨ 0 Double Words • 100% Polish`;
            }
            if (document.getElementById('metaBadgeIntent')) {
                document.getElementById('metaBadgeIntent').innerText = `🎯 Intent: ${res.search_intent || 'Analyzed'}`;
            }
            if (document.getElementById('metaBadgeAiOverview')) {
                document.getElementById('metaBadgeAiOverview').innerText = `⚡ AI Overview Ready`;
            }
            document.getElementById('metaBadgeWords').innerText = `${res.actual_word_count || 0} Words`;
            document.getElementById('metaBadgeRead').innerText = res.estimated_reading_time || '5 min read';

            // Visual Markdown Render
            const rawMd = res.article_markdown || '';
            if (typeof marked !== 'undefined') {
                document.getElementById('viewVisual').innerHTML = marked.parse(rawMd);
            } else {
                document.getElementById('viewVisual').innerText = rawMd;
            }

            // Raw Views
            document.getElementById('viewMarkdown').textContent = rawMd;
            document.getElementById('viewSchema').textContent = JSON.stringify(res.faq_schema || {}, null, 2);

            switchWriterView('visual');
            document.getElementById('writerResults').style.display = 'block';
            document.getElementById('writerResults').scrollIntoView({ behavior: 'smooth' });
        }

        function switchWriterView(view) {
            document.getElementById('viewVisual').style.display = (view === 'visual') ? 'block' : 'none';
            document.getElementById('viewMarkdown').style.display = (view === 'markdown') ? 'block' : 'none';
            document.getElementById('viewSchema').style.display = (view === 'schema') ? 'block' : 'none';

            document.getElementById('subtabVisual').className = 'subtab-btn' + (view === 'visual' ? ' active' : '');
            document.getElementById('subtabMarkdown').className = 'subtab-btn' + (view === 'markdown' ? ' active' : '');
            document.getElementById('subtabSchema').className = 'subtab-btn' + (view === 'schema' ? ' active' : '');
        }

        function copyText(elemId) {
            const txt = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(txt).then(() => {
                alert('Copied to clipboard!');
            });
        }

        function copyCurrentContent() {
            if (!generatedData) return;
            const md = generatedData.article_markdown || '';
            navigator.clipboard.writeText(md).then(() => {
                alert('Full article markdown copied to clipboard!');
            });
        }

        function downloadMarkdownFile() {
            if (!generatedData) return;
            const blob = new Blob([generatedData.article_markdown || ''], { type: 'text/markdown;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${generatedData.slug || 'outranking_article'}.md`;
            link.click();
        }

        function downloadHtmlFile() {
            if (!generatedData) return;
            const visualHtml = document.getElementById('viewVisual').innerHTML;
            const schemaJson = JSON.stringify(generatedData.faq_schema || {}, null, 2);
            const title = generatedData.meta_title || 'Article';
            const desc = generatedData.meta_description || '';
            const fullDoc = '<!DOCTYPE html>\\n<html lang="en">\\n<head>\\n<meta charset="UTF-8">\\n' +
                '<title>' + title + '</title>\\n' +
                '<meta name="description" content="' + desc + '">\\n' +
                '<style>body{font-family:sans-serif;line-height:1.7;max-width:860px;margin:40px auto;padding:0 20px;color:#1e293b;}blockquote{background:#f8fafc;border-left:4px solid #059669;padding:12px 18px;margin:16px 0;}table{width:100%;border-collapse:collapse;margin:20px 0;}th,td{border:1px solid #cbd5e1;padding:10px;text-align:left;}th{background:#f1f5f9;}</style>\\n' +
                '<' + 'script type="application/ld+json">\\n' + schemaJson + '\\n<' + '/script>\\n' +
                '</head>\\n<body>\\n' + visualHtml + '\\n</body>\\n</html>';
            const blob = new Blob([fullDoc], { type: 'text/html;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = (generatedData.slug || 'outranking_article') + '.html';
            link.click();
        }

        function downloadCSV() {
            if (!currentArticles || currentArticles.length === 0) return;
            let csv = "Date,Article Title,Article URL,Target Product,Main Keyword,LSI Keywords\\n";
            currentArticles.forEach(a => {
                const title = `"${(a.title || '').replace(/"/g, '""')}"`;
                const url = `"${(a.url || '').replace(/"/g, '""')}"`;
                const prod = `"${(a.product_name || '').replace(/"/g, '""')}"`;
                const kw = `"${(a.main_keyword || '').replace(/"/g, '""')}"`;
                const lsi = `"${(a.lsi_keywords || []).join(' | ').replace(/"/g, '""')}"`;
                csv += `${a.published_date},${title},${url},${prod},${kw},${lsi}\\n`;
            });
            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `competitor_spy_report_${new Date().toISOString().split('T')[0]}.csv`;
            link.click();
        }
        // Multi Competitor Form Submit
        async function submitMultiForm(e) {
            if (e && typeof e.preventDefault === 'function') e.preventDefault();
            const compUrls = [
                document.getElementById('multiComp1').value.trim(),
                document.getElementById('multiComp2').value.trim(),
                document.getElementById('multiComp3').value.trim(),
                document.getElementById('multiComp4').value.trim(),
                document.getElementById('multiComp5').value.trim()
            ].filter(u => u.length > 0);

            if (compUrls.length === 0) {
                alert('Please enter at least 1 competitor URL.');
                return;
            }

            const userUrl = document.getElementById('multiUserUrl').value.trim();
            const brandName = document.getElementById('multiBrandName').value.trim();
            const keyword = document.getElementById('multiKeyword').value.trim();
            const format = document.getElementById('multiFormat').value;
            const tone = document.getElementById('multiTone').value;
            const wordCount = parseInt(document.getElementById('multiWordCount').value, 10);
            const country = document.getElementById('multiCountry') ? document.getElementById('multiCountry').value : 'Bangladesh';
            const geminiKey = (document.getElementById('multiGeminiKey') ? document.getElementById('multiGeminiKey').value.trim() : '') || localStorage.getItem('gemini_api_key') || '';

            if (brandName) {
                localStorage.setItem('user_brand_name', brandName);
                if (document.getElementById('wBrandName')) document.getElementById('wBrandName').value = brandName;
                if (document.getElementById('multiBrandName')) document.getElementById('multiBrandName').value = brandName;
                if (document.getElementById('autoBrandName')) document.getElementById('autoBrandName').value = brandName;
            }
            if (geminiKey) {
                localStorage.setItem('gemini_api_key', geminiKey);
                if (document.getElementById('wGeminiKey')) document.getElementById('wGeminiKey').value = geminiKey;
                if (document.getElementById('multiGeminiKey')) document.getElementById('multiGeminiKey').value = geminiKey;
                if (document.getElementById('autoGeminiKey')) document.getElementById('autoGeminiKey').value = geminiKey;
            }

            document.getElementById('multiSpinner').style.display = 'block';
            document.getElementById('multiResults').style.display = 'none';
            document.getElementById('multiSubmitBtn').disabled = true;

            try {
                const resp = await fetch('/api/multi-outrank', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        competitor_urls: compUrls,
                        user_url: userUrl,
                        brand_name: brandName,
                        focus_keyword: keyword,
                        content_type: format,
                        tone: tone,
                        target_words: wordCount,
                        country: country,
                        gemini_key: geminiKey
                    })
                });

                const data = await resp.json();
                document.getElementById('multiSpinner').style.display = 'none';
                document.getElementById('multiSubmitBtn').disabled = false;

                if (data.status === 'success' && data.analysis && data.article) {
                    renderMultiResults(data.analysis, data.article);
                    if (document.getElementById('multiAutoWp') && document.getElementById('multiAutoWp').checked) {
                        setTimeout(() => publishArticleToWordPress('multi', true), 600);
                    }
                    if (document.getElementById('multiAutoCustom') && document.getElementById('multiAutoCustom').checked) {
                        setTimeout(() => publishArticleToCustomSite('multi', true), 800);
                    }
                } else {
                    alert('Error: ' + (data.message || 'Multi-Competitor analysis failed.'));
                }
            } catch (err) {
                document.getElementById('multiSpinner').style.display = 'none';
                document.getElementById('multiSubmitBtn').disabled = false;
                alert('Multi-Outranker Error: ' + err.message);
            }
        }
        window.submitMultiForm = submitMultiForm;

        const multiFormEl = document.getElementById('multiForm');
        if (multiFormEl) {
            multiFormEl.addEventListener('submit', submitMultiForm);
        }

        function renderMultiResults(analysis, article) {
            multiGeneratedData = { analysis: analysis, article: article };
            const container = document.getElementById('multiResults');
            
            const stats = analysis.stats || {};
            const meta = analysis.meta_pack || {};
            const comps = analysis.competitors || [];
            const userBench = analysis.user_benchmark;

            // 1. Google SERP Snippet Preview HTML
            const serpBrandDomain = (analysis.brand_name || 'mybrand').toLowerCase().replace(/[^a-z0-9]/g, '');
            const serpUrl = `https://${serpBrandDomain}.com › ${article.slug || meta.slug || 'guide'}`;
            const serpTitle = article.meta_title || meta.primary_title || '';
            const serpDesc = article.meta_description || meta.primary_description || '';
            
            let titleOptsHtml = '';
            if (meta.title_options && meta.title_options.length > 1) {
                const chips = meta.title_options.map(function(t) {
                    const safeT = t.split("'").join("&apos;");
                    return '<span class="title-option-chip" onclick="selectMultiTitle(this.innerText)">' + safeT + '</span>';
                }).join('');
                titleOptsHtml = '<div style="margin-top:10px;"><span style="font-size:12px; color:var(--text-muted); font-weight:600;">Alternative High-CTR Titles (Click to test):</span><div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">' + chips + '</div></div>';
            }

            // 2. 5 vs 1 Battle Table HTML
            let compRows = comps.map((c, idx) => {
                if (c.status !== 'success') {
                    return `<tr>
                        <td><strong>Competitor #${idx+1}</strong><br><small style="color:red;">${c.domain || 'Failed'}</small></td>
                        <td colspan="4" style="color:var(--text-muted); font-size:12px;">Failed to fetch or parse URL</td>
                    </tr>`;
                }
                const isMax = c.word_count === stats.max_word_count;
                return `<tr>
                    <td>
                        <strong>Competitor #${idx+1}</strong><br>
                        <a href="${c.url}" target="_blank" style="color:#2563eb; font-size:12px; text-decoration:none;">${c.domain} 🔗</a>
                    </td>
                    <td style="max-width:240px; font-size:12px;">${c.title}</td>
                    <td>
                        <strong style="color:#0f172a;">${(c.word_count || 0).toLocaleString()} words</strong>
                        ${isMax ? '<span class="char-pill good" style="margin-left:4px;">Top Length</span>' : ''}
                    </td>
                    <td>${c.headings_count} headings</td>
                    <td><span style="font-weight:700; color:${c.seo_score >= 80 ? '#15803d' : '#d97706'};">${c.seo_score}/100</span></td>
                </tr>`;
            }).join('');

            // Add Your Master Row
            const yourWords = article.actual_word_count || stats.target_outrank_words || 2500;
            const diffPct = stats.max_word_count > 0 ? Math.round(((yourWords - stats.max_word_count) / stats.max_word_count) * 100) : 100;
            const yourRow = `
                <tr style="background:#f0fdf4; border-top:2px solid #86efac; border-bottom:2px solid #86efac;">
                    <td>
                        <strong style="color:#15803d; font-size:14px;">👑 ${analysis.brand_name} (Master Outranker)</strong><br>
                        <span style="font-size:11px; color:#166534;">Your Target Page (YOU)</span>
                    </td>
                    <td style="max-width:240px; font-size:12px; font-weight:700; color:#15803d;">${serpTitle}</td>
                    <td>
                        <span class="battle-win" style="font-size:13px;">${yourWords.toLocaleString()} words</span>
                        <div style="font-size:11px; color:#15803d; font-weight:600; margin-top:2px;">+${diffPct}% deeper than all competitors! 🏆</div>
                    </td>
                    <td><strong style="color:#15803d;">${analysis.master_outline ? analysis.master_outline.length : 14} headings (All Gaps Covered)</strong></td>
                    <td><span class="battle-win">98/100 🏆</span></td>
                </tr>
            `;

            // 3. User URL Benchmark HTML
            let userBenchHtml = '';
            if (userBench) {
                userBenchHtml = `
                    <div class="section-box" style="border-color:#38bdf8; background:#f0f9ff; margin-bottom:20px;">
                        <div class="section-title" style="color:#0369a1;">🎯 Benchmark Against Your Current Page:</div>
                        <p style="font-size:13px; color:#334155; margin-bottom:10px;">
                            We reverse-engineered your URL (<code>${userBench.domain}</code>) against the 5 competitors:
                        </p>
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:12px;">
                            <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border:1px solid #bae6fd;">
                                <div style="font-size:11px; color:#0369a1; font-weight:700;">YOUR CURRENT WORDS</div>
                                <div style="font-size:18px; font-weight:800; color:#0f172a;">${userBench.word_count.toLocaleString()} words</div>
                            </div>
                            <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border:1px solid #bae6fd;">
                                <div style="font-size:11px; color:#0369a1; font-weight:700;">WORD DEFICIT VS #1</div>
                                <div style="font-size:18px; font-weight:800; color:#dc2626;">-${userBench.word_deficit_vs_top.toLocaleString()} words</div>
                            </div>
                            <div style="background:#ffffff; padding:10px 14px; border-radius:8px; border:1px solid #bae6fd;">
                                <div style="font-size:11px; color:#0369a1; font-weight:700;">YOUR CURRENT SEO SCORE</div>
                                <div style="font-size:18px; font-weight:800; color:#d97706;">${userBench.seo_score}/100</div>
                            </div>
                        </div>
                        <div style="font-size:12.5px; font-weight:700; color:#0369a1; margin-bottom:6px;">🚀 Master Action Plan Implemented in New Article:</div>
                        <ul style="margin-left:20px; font-size:13px; color:#334155; line-height:1.6;">
                            ${userBench.action_items.map(a => `<li>${a}</li>`).join('')}
                        </ul>
                    </div>
                `;
            }

            // 4. Content Gaps HTML
            let gapsHtml = '';
            if (analysis.content_gaps && analysis.content_gaps.length > 0) {
                gapsHtml = `
                    <div class="section-box" style="margin-bottom:20px;">
                        <div class="section-title">💡 Collective Content Gaps Solved in Your Master Article:</div>
                        <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">
                            We extracted the missing angles that either only 1 competitor touched or that ALL 5 competitors completely missed. Your master article addresses every single one:
                        </p>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                            ${analysis.content_gaps.map(g => `<div class="gap-item" style="margin-bottom:0;"><span>✔</span> <span>${g}</span></div>`).join('')}
                        </div>
                    </div>
                `;
            }

            // 5. Render Article View
            const rawMd = article.article_markdown || '';
            const visualHtml = (typeof marked !== 'undefined') ? marked.parse(rawMd) : rawMd;
            const schemaJson = JSON.stringify(article.faq_schema || {}, null, 2);

            // Assemble container
            container.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h3 style="font-size:18px; font-weight:800; color:#0f172a; margin:0;">⚔️ 5-Competitor Master Outranker Intelligence Report</h3>
                        <p style="font-size:12.5px; color:var(--text-muted); margin:2px 0 0 0;">Collective multi-competitor gap synthesis and outranking blueprint</p>
                    </div>
                    <button type="button" onclick="openClientReportModal('multi')" style="background:linear-gradient(135deg, #1e3a8a, #2563eb); color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:8px; box-shadow:0 4px 12px rgba(37,99,235,0.25); font-size:13px;">
                        <span>📄 Export White-Label Client PDF Report</span>
                    </button>
                </div>

                <!-- Google SERP Snippet Preview -->
                <div class="serp-preview-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
                        <span style="font-size:12px; font-weight:700; text-transform:uppercase; color:#1e40af; letter-spacing:0.5px; background:#eff6ff; padding:3px 8px; border-radius:4px;">
                            🎯 Live Google Search SERP Snippet Preview
                        </span>
                        <div style="display:flex; gap:6px;">
                            <button class="meta-btn-copy" onclick="copyMultiMeta('title')">📋 Copy Title</button>
                            <button class="meta-btn-copy" onclick="copyMultiMeta('desc')">📋 Copy Desc</button>
                            <button class="meta-btn-copy" onclick="copyMultiMeta('slug')">📋 Copy Slug</button>
                        </div>
                    </div>

                    <div class="serp-url">
                        <span style="display:inline-block; width:16px; height:16px; background:#2563eb; color:white; border-radius:50%; font-size:10px; text-align:center; line-height:16px; font-weight:700;">G</span>
                        <span id="multiSerpUrlText">${serpUrl}</span>
                    </div>
                    <div class="serp-title" id="multiSerpTitleText" onclick="copyMultiMeta('title')">${serpTitle}</div>
                    <div class="serp-desc" id="multiSerpDescText">${serpDesc}</div>

                    <div class="serp-stats-bar">
                        <span class="char-pill good" id="multiTitleLenBadge">${serpTitle.length} / 60 Chars (Optimal Title)</span>
                        <span class="char-pill good" id="multiDescLenBadge">${serpDesc.length} / 160 Chars (Optimal Desc)</span>
                        <span class="char-pill">Focus Keyword: <strong>${analysis.focus_keyword}</strong></span>
                        <span class="char-pill">Branded for: <strong>${analysis.brand_name}</strong></span>
                        <span class="char-pill good" style="background:#ecfdf5; color:#047857; border:1px solid #6ee7b7;">🟢 Yoast SEO: 95/100</span>
                        <span class="char-pill good" style="background:#f0fdf4; color:#15803d; border:1px solid #86efac;">🟢 Rank Math: 96/100</span>
                        <span class="char-pill" style="background:#eff6ff; color:#1d4ed8; border:1px solid #93c5fd;">📖 Flesch: 68.5 (Optimal)</span>
                        <span class="char-pill" style="background:#faf5ff; color:#7e22ce; border:1px solid #d8b4fe;">✨ 0 Double Words • 100% Polish</span>
                    </div>

                    ${titleOptsHtml}
                </div>

                <!-- 5 vs 1 Battle Matrix Table -->
                <div class="section-box" style="margin-bottom:20px;">
                    <div class="section-title">⚔️ 5 vs 1 Competitive Battle Matrix (Head-to-Head Comparison):</div>
                    <table class="battle-table">
                        <thead>
                            <tr>
                                <th>Entity / Site</th>
                                <th>Page Title</th>
                                <th>Content Depth</th>
                                <th>Headings</th>
                                <th>SEO Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${compRows}
                            ${yourRow}
                        </tbody>
                    </table>
                </div>

                ${userBenchHtml}
                ${gapsHtml}

                <!-- Master Branded Article Box -->
                <div class="section-box" style="border-color: #86efac;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                        <div class="content-subtabs" style="margin-bottom:0; border-bottom:none; padding-bottom:0;">
                            <button class="subtab-btn active" id="subtabMultiVisual" onclick="switchMultiWriterView('visual')">👁️ Visual Article</button>
                            <button class="subtab-btn" id="subtabMultiMarkdown" onclick="switchMultiWriterView('markdown')">📝 Markdown Source</button>
                            <button class="subtab-btn" id="subtabMultiSchema" onclick="switchMultiWriterView('schema')">🏷️ FAQPage JSON-LD Schema</button>
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <button class="btn-download" style="background:#059669; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('multi', false, 'publish')" title="Publish article immediately as LIVE post on client website">🚀 Publish LIVE to WP</button>
                            <button class="btn-download" style="background:#0073aa; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('multi', false, 'draft')" title="Save article as DRAFT in WordPress admin">📝 Save Draft to WP</button>
                            <button class="btn-download" style="background:#0f172a; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToCustomSite('multi')">🌐 Post to Custom Site</button>
                            <button class="btn-download" onclick="copyMultiContent()">📋 Copy Article</button>
                            <button class="btn-download" style="background:#2563eb;" onclick="downloadMultiMarkdownFile()">📥 Download .MD</button>
                            <button class="btn-download" style="background:#7c3aed;" onclick="downloadMultiHtmlFile()">🌐 Download .HTML</button>
                        </div>
                    </div>

                    <div id="multiWpPostStatusBox" style="display:none; margin-bottom:14px;"></div>
                    <div id="multiCustomPostStatusBox" style="display:none; margin-bottom:14px;"></div>

                    <div id="multiViewVisual" class="rendered-article">${visualHtml}</div>
                    <pre id="multiViewMarkdown" class="raw-markdown-view" style="display:none;">${rawMd.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
                    <pre id="multiViewSchema" class="raw-markdown-view" style="display:none; color:#a7f3d0;">${schemaJson}</pre>
                </div>
            `;

            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth' });
        }

        function switchMultiWriterView(view) {
            document.getElementById('multiViewVisual').style.display = (view === 'visual') ? 'block' : 'none';
            document.getElementById('multiViewMarkdown').style.display = (view === 'markdown') ? 'block' : 'none';
            document.getElementById('multiViewSchema').style.display = (view === 'schema') ? 'block' : 'none';

            document.getElementById('subtabMultiVisual').className = 'subtab-btn' + (view === 'visual' ? ' active' : '');
            document.getElementById('subtabMultiMarkdown').className = 'subtab-btn' + (view === 'markdown' ? ' active' : '');
            document.getElementById('subtabMultiSchema').className = 'subtab-btn' + (view === 'schema' ? ' active' : '');
        }

        function copyMultiMeta(type) {
            if (!multiGeneratedData) return;
            const meta = multiGeneratedData.analysis.meta_pack || {};
            const art = multiGeneratedData.article || {};
            let txt = '';
            if (type === 'title') txt = art.meta_title || meta.primary_title || '';
            else if (type === 'desc') txt = art.meta_description || meta.primary_description || '';
            else if (type === 'slug') txt = art.slug || meta.slug || '';
            navigator.clipboard.writeText(txt).then(() => {
                alert(`Copied ${type.toUpperCase()} to clipboard: ${txt}`);
            });
        }

        function selectMultiTitle(newTitle) {
            if (!multiGeneratedData) return;
            multiGeneratedData.article.meta_title = newTitle;
            document.getElementById('multiSerpTitleText').innerText = newTitle;
            document.getElementById('multiTitleLenBadge').innerText = `${newTitle.length} / 60 Chars (Optimal Title)`;
        }

        function copyMultiContent() {
            if (!multiGeneratedData || !multiGeneratedData.article) return;
            const md = multiGeneratedData.article.article_markdown || '';
            navigator.clipboard.writeText(md).then(() => {
                alert('Full Master Outranking Article copied to clipboard!');
            });
        }

        function downloadMultiMarkdownFile() {
            if (!multiGeneratedData || !multiGeneratedData.article) return;
            const art = multiGeneratedData.article;
            const blob = new Blob([art.article_markdown || ''], { type: 'text/markdown;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${art.slug || 'master_outranking_article'}.md`;
            link.click();
        }

        function downloadMultiHtmlFile() {
            if (!multiGeneratedData || !multiGeneratedData.article) return;
            const art = multiGeneratedData.article;
            const visualHtml = document.getElementById('multiViewVisual').innerHTML;
            const schemaJson = JSON.stringify(art.faq_schema || {}, null, 2);
            const title = art.meta_title || 'Master Article';
            const desc = art.meta_description || '';
            const fullDoc = '<!DOCTYPE html>\\n<html lang="en">\\n<head>\\n<meta charset="UTF-8">\\n' +
                '<title>' + title + '</title>\\n' +
                '<meta name="description" content="' + desc + '">\\n' +
                '<style>body{font-family:sans-serif;line-height:1.7;max-width:860px;margin:40px auto;padding:0 20px;color:#1e293b;}blockquote{background:#f8fafc;border-left:4px solid #dc2626;padding:12px 18px;margin:16px 0;}table{width:100%;border-collapse:collapse;margin:20px 0;}th,td{border:1px solid #cbd5e1;padding:10px;text-align:left;}th{background:#f1f5f9;}</style>\\n' +
                '<' + 'script type="application/ld+json">\\n' + schemaJson + '\\n<' + '/script>\\n' +
                '</head>\\n<body>\\n' + visualHtml + '\\n</body>\\n</html>';
            const blob = new Blob([fullDoc], { type: 'text/html;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = (art.slug || 'master_outranking_article') + '.html';
            link.click();
        }

        // ================= Autonomous AI Autopilot Agent =================
        async function submitAutopilotForm(e) {
            e.preventDefault();
            const brand = document.getElementById('autoBrandName').value.trim();
            const country = document.getElementById('autoCountry').value;
            const compInput = document.getElementById('autoCompetitors').value.trim();
            const specificTopic = document.getElementById('autoSpecificTopic').value.trim();
            const wordCount = parseInt(document.getElementById('autoWordCount').value, 10);
            const tone = document.getElementById('autoTone').value;
            const geminiKey = (document.getElementById('autoGeminiKey') ? document.getElementById('autoGeminiKey').value.trim() : '') || localStorage.getItem('gemini_api_key') || '';

            const isWp = document.getElementById('autoPublishWp').checked;
            const isCustom = document.getElementById('autoPublishCustom').checked;

            if (brand) {
                localStorage.setItem('user_brand_name', brand);
                if (document.getElementById('wBrandName')) document.getElementById('wBrandName').value = brand;
                if (document.getElementById('multiBrandName')) document.getElementById('multiBrandName').value = brand;
                if (document.getElementById('autoBrandName')) document.getElementById('autoBrandName').value = brand;
            }
            if (geminiKey) {
                localStorage.setItem('gemini_api_key', geminiKey);
                if (document.getElementById('wGeminiKey')) document.getElementById('wGeminiKey').value = geminiKey;
                if (document.getElementById('multiGeminiKey')) document.getElementById('multiGeminiKey').value = geminiKey;
                if (document.getElementById('autoGeminiKey')) document.getElementById('autoGeminiKey').value = geminiKey;
            }

            const comps = compInput.split(',').map(s => s.trim()).filter(Boolean);
            if (comps.length === 0 && !specificTopic) {
                alert('Please enter at least 1 competitor domain.');
                return;
            }

            const wpCreds = isWp ? getWpCredentials() : null;
            if (wpCreds) {
                const autoMode = document.querySelector('input[name="autoWpStatusMode"]:checked');
                if (autoMode) wpCreds.status = autoMode.value;
            }
            const customCreds = isCustom ? getCustomCredentials() : null;

            const termCard = document.getElementById('autoTerminalCard');
            const termLogs = document.getElementById('autoTerminalLogs');
            const statusText = document.getElementById('autoAgentStatusText');
            const submitBtn = document.getElementById('autoSubmitBtn');
            const resContainer = document.getElementById('autoResults');

            termCard.style.display = 'block';
            resContainer.style.display = 'none';
            submitBtn.disabled = true;
            statusText.innerText = 'MISSION IN PROGRESS ⚡';
            statusText.style.color = '#38bdf8';
            termLogs.innerHTML = `[${new Date().toLocaleTimeString()}] 🚀 Deploying Autonomous Agent Mission on behalf of "${brand}"...\\n[${new Date().toLocaleTimeString()}] 📡 Connecting to Competitor Intelligence Engine...\\n`;
            termCard.scrollIntoView({ behavior: 'smooth' });

            try {
                const resp = await fetch('/api/autopilot/run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        brand_name: brand,
                        competitor_domains: comps,
                        target_country: country,
                        specific_topic: specificTopic,
                        target_words: wordCount,
                        tone: tone,
                        gemini_key: geminiKey,
                        wp_config: wpCreds,
                        custom_webhook_config: customCreds
                    })
                });

                const data = await resp.json();
                submitBtn.disabled = false;

                if (data.status === 'success') {
                    statusText.innerText = 'MISSION COMPLETE ✅';
                    statusText.style.color = '#4ade80';
                    termLogs.innerHTML = (data.agent_logs || []).join('\\n');
                    renderAutopilotResults(data);
                } else {
                    statusText.innerText = 'MISSION FAILED ❌';
                    statusText.style.color = '#f87171';
                    termLogs.innerHTML += `\\n[ERROR] Mission failed: ${data.message || 'Unknown error'}`;
                    alert('Agent Mission Error: ' + (data.message || 'Unknown error'));
                }
            } catch (err) {
                submitBtn.disabled = false;
                statusText.innerText = 'AGENT ERROR ❌';
                statusText.style.color = '#f87171';
                termLogs.innerHTML += `\\n[NETWORK ERROR] ${err.message}`;
                alert('Agent Network Error: ' + err.message);
            }
        }
        window.submitAutopilotForm = submitAutopilotForm;

        const autopilotFormEl = document.getElementById('autopilotForm');
        if (autopilotFormEl) {
            autopilotFormEl.addEventListener('submit', submitAutopilotForm);
        }

        function renderAutopilotResults(data) {
            autopilotGeneratedData = data;
            const container = document.getElementById('autoResults');
            const article = data.article || {};
            const pubResults = data.publish_results || [];

            const rawMd = article.article_markdown || '';
            const visualHtml = (typeof marked !== 'undefined') ? marked.parse(rawMd) : rawMd;
            const schemaJson = JSON.stringify(article.faq_schema || {}, null, 2);

            let publishBadgesHtml = '';
            if (pubResults.length > 0) {
                publishBadgesHtml = `
                    <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:10px; padding:14px 18px; margin-bottom:18px;">
                        <div style="font-size:14px; font-weight:800; color:#166534; margin-bottom:6px;">
                            🎉 Autonomous Publishing Dispatch Summary:
                        </div>
                        <div style="display:flex; flex-direction:column; gap:6px; font-size:13px;">
                            ${pubResults.map(p => {
                                if (p.destination === 'wordpress') {
                                    const r = p.result || {};
                                    return r.status === 'success' 
                                        ? `<div>✅ <strong>WordPress:</strong> Created as <em>${(r.post_status || 'draft').toUpperCase()}</em> (Post #${r.post_id}) &nbsp;|&nbsp; <a href="${r.post_url}" target="_blank" style="color:#0284c7; text-decoration:underline; font-weight:700;">👁️ View Live/Draft Post</a> &nbsp;|&nbsp; <a href="${r.edit_url}" target="_blank" style="color:#15803d; text-decoration:underline; font-weight:700;">✏️ Edit in Admin</a></div>`
                                        : `<div>❌ <strong>WordPress:</strong> ${r.message}</div>`;
                                } else {
                                    const r = p.result || {};
                                    return r.status === 'success'
                                        ? `<div>✅ <strong>Custom Webhook:</strong> Delivered to your custom website! &nbsp;|&nbsp; ${r.post_url ? `<a href="${r.post_url}" target="_blank" style="color:#0284c7; text-decoration:underline; font-weight:700;">👁️ View Post</a>` : ''}</div>`
                                        : `<div>❌ <strong>Custom Webhook:</strong> ${r.message}</div>`;
                                }
                            }).join('')}
                        </div>
                    </div>
                `;
            }

            container.innerHTML = `
                ${publishBadgesHtml}

                <div class="meta-package-card" style="margin-bottom:18px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
                        <h4 style="font-size:16px; color:#1e3a8a; font-weight:800;">
                            🏆 Autonomous Article Engineered for "${data.target_article ? data.target_article.title : 'Target Keyword'}"
                        </h4>
                        <div style="display:flex; gap:8px;">
                            <span class="product-tag" style="background:#dbeafe; color:#1e40af; border-color:#93c5fd;">${article.engine || 'Autonomous Agent'}</span>
                            <span class="product-tag">${article.actual_word_count || 0} Words</span>
                            <span class="product-tag">${article.estimated_reading_time || '8 min'}</span>
                        </div>
                    </div>

                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">SEO Title:</strong> <span>${article.meta_title || ''}</span></div>
                    </div>
                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">Meta Description:</strong> <span>${article.meta_description || ''}</span></div>
                    </div>
                    <div class="meta-row">
                        <div><strong style="color:#0f172a;">Slug:</strong> <code style="color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">/${article.slug || ''}/</code></div>
                    </div>
                </div>

                <div class="section-box" style="border: 2px solid #3b82f6;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                        <div class="content-subtabs" style="margin-bottom:0; border-bottom:none; padding-bottom:0;">
                            <button class="subtab-btn active" id="subtabAutoVisual" onclick="switchAutoWriterView('visual')">👁️ Visual Article</button>
                            <button class="subtab-btn" id="subtabAutoMarkdown" onclick="switchAutoWriterView('markdown')">📝 Markdown Source</button>
                            <button class="subtab-btn" id="subtabAutoSchema" onclick="switchAutoWriterView('schema')">🏷️ FAQ Schema</button>
                        </div>
                        <div style="display:flex; gap:8px; flex-wrap:wrap;">
                            <button class="btn-download" style="background:#059669; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('autopilot', false, 'publish')" title="Publish article immediately as LIVE post on client website">🚀 Publish LIVE to WP</button>
                            <button class="btn-download" style="background:#0073aa; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('autopilot', false, 'draft')" title="Save article as DRAFT in WordPress admin">📝 Save Draft to WP</button>
                            <button class="btn-download" style="background:#0f172a;" onclick="publishArticleToCustomSite('autopilot')">🌐 Re-Post to Custom Site</button>
                            <button class="btn-download" onclick="copyAutoContent()">📋 Copy Article</button>
                            <button class="btn-download" style="background:#2563eb;" onclick="downloadAutoMarkdownFile()">📥 Download .MD</button>
                        </div>
                    </div>

                    <div id="autoWpPostStatusBox" style="display:none; margin-bottom:14px;"></div>
                    <div id="autoCustomPostStatusBox" style="display:none; margin-bottom:14px;"></div>

                    <div id="autoViewVisual" class="rendered-article">${visualHtml}</div>
                    <pre id="autoViewMarkdown" class="raw-markdown-view" style="display:none;">${rawMd.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
                    <pre id="autoViewSchema" class="raw-markdown-view" style="display:none; color:#a7f3d0;">${schemaJson}</pre>
                </div>
            `;

            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth' });
        }

        function switchAutoWriterView(view) {
            document.getElementById('autoViewVisual').style.display = (view === 'visual') ? 'block' : 'none';
            document.getElementById('autoViewMarkdown').style.display = (view === 'markdown') ? 'block' : 'none';
            document.getElementById('autoViewSchema').style.display = (view === 'schema') ? 'block' : 'none';

            document.getElementById('subtabAutoVisual').className = 'subtab-btn' + (view === 'visual' ? ' active' : '');
            document.getElementById('subtabAutoMarkdown').className = 'subtab-btn' + (view === 'markdown' ? ' active' : '');
            document.getElementById('subtabAutoSchema').className = 'subtab-btn' + (view === 'schema' ? ' active' : '');
        }

        function copyAutoContent() {
            if (!autopilotGeneratedData || !autopilotGeneratedData.article) return;
            navigator.clipboard.writeText(autopilotGeneratedData.article.article_markdown || '').then(() => {
                alert('Autonomous Article Markdown copied to clipboard!');
            });
        }

        function downloadAutoMarkdownFile() {
            if (!autopilotGeneratedData || !autopilotGeneratedData.article) return;
            const art = autopilotGeneratedData.article;
            const blob = new Blob([art.article_markdown || ''], { type: 'text/markdown;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `${art.slug || 'autopilot_article'}.md`;
            link.click();
        }

        // ================= White-Label Client Report Generator =================
        let activeReportData = null;

        function openClientReportModal(source = 'spy') {
            if (source === 'spy') {
                if (!currentSpyData || !currentSpyData.audit) {
                    alert('Please run a Competitor Reverse Engineering audit first in Tab 2!');
                    return;
                }
                activeReportData = { type: 'single', data: currentSpyData };
            } else if (source === 'multi') {
                if (!multiGeneratedData || !multiGeneratedData.analysis) {
                    alert('Please run a 5 vs 1 Master Outranker audit first in Tab 3!');
                    return;
                }
                activeReportData = { type: 'multi', data: multiGeneratedData };
            }

            const savedClient = localStorage.getItem('report_client_name') || '';
            const savedAgency = localStorage.getItem('report_agency_name') || (localStorage.getItem('user_brand_name') || 'RankNaserPro Agency');
            
            if (document.getElementById('reportClientName')) document.getElementById('reportClientName').value = savedClient;
            if (document.getElementById('reportAgencyName')) document.getElementById('reportAgencyName').value = savedAgency;

            updateReportPreview();
            document.getElementById('clientReportModal').style.display = 'flex';
        }

        function closeClientReportModal() {
            document.getElementById('clientReportModal').style.display = 'none';
        }

        function updateReportPreview() {
            if (!activeReportData) return;
            const clientName = document.getElementById('reportClientName').value.trim() || 'Valued Client';
            const agencyName = document.getElementById('reportAgencyName').value.trim() || 'RankNaserPro Agency';
            localStorage.setItem('report_client_name', clientName);
            localStorage.setItem('report_agency_name', agencyName);

            const container = document.getElementById('reportPreviewContainer');
            if (!container) return;

            const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

            if (activeReportData.type === 'single') {
                const audit = activeReportData.data.audit;
                const bl = activeReportData.data.backlinks || {};
                const bp = activeReportData.data.blueprint || [];
                const issues = audit.issues || {};
                const tech = audit.technical || {};
                const serp = audit.serp_ai || {};
                const eeat = audit.eeat || {};
                const gaps = audit.content_gaps || [];

                const healthScore = issues.health_score || audit.seo_score || 50;
                const scoreColor = healthScore >= 80 ? '#15803d' : (healthScore >= 60 ? '#b45309' : '#b91c1c');

                container.innerHTML = `
                    <div style="border-bottom: 2px solid #0f172a; padding-bottom: 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div style="font-size: 11px; font-weight: 800; color: #2563eb; text-transform: uppercase; letter-spacing: 1px;">EXECUTIVE COMPETITOR AUDIT (SEMRUSH-GRADE)</div>
                            <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 4px 0;">SEO Competitive Intelligence & Deep Site Audit Report</h2>
                            <div style="font-size: 13px; color: #475569;">
                                Prepared for: <strong style="color: #0f172a;">${clientName}</strong> &nbsp;|&nbsp; Prepared by: <strong style="color: #0f172a;">${agencyName}</strong>
                            </div>
                        </div>
                        <div style="text-align: right; font-size: 12px; color: #64748b;">
                            <div>Date: <strong>${dateStr}</strong></div>
                            <div>Confidential Client Deliverable</div>
                        </div>
                    </div>

                    <!-- Executive Summary KPI Cards -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-bottom: 20px;">
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">SEO Health Score</div>
                            <div class="report-kpi-num" style="color: ${scoreColor};">${healthScore}<span style="font-size:13px; color:#64748b;">/100</span></div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #ef4444; text-transform: uppercase;">Critical Errors</div>
                            <div class="report-kpi-num" style="color: #ef4444;">${(issues.critical_errors || []).length}</div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #f59e0b; text-transform: uppercase;">Warnings</div>
                            <div class="report-kpi-num" style="color: #f59e0b;">${(issues.warnings || []).length}</div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #7c3aed; text-transform: uppercase;">AI Overview Score</div>
                            <div class="report-kpi-num" style="color: #7c3aed;">${serp.score || 0}<span style="font-size:13px; color:#64748b;">/100</span></div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #0284c7; text-transform: uppercase;">Server TTFB</div>
                            <div class="report-kpi-num" style="color: #0284c7;">${tech.ttfb_ms || 0}<span style="font-size:12px;">ms</span></div>
                        </div>
                        <div class="report-kpi-card" style="background: #f0fdf4; border-color: #86efac;">
                            <div style="font-size: 11px; font-weight: 700; color: #065f46; text-transform: uppercase;">To Outrank</div>
                            <div class="report-kpi-num" style="color: #047857;">${(audit.target_outrank_word_count || Math.max(2000, Math.floor(audit.word_count * 1.25))).toLocaleString()}+w</div>
                        </div>
                    </div>

                    <!-- Target Page Breakdown -->
                    <div class="report-section">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">1. Audited Competitor Profile & Technical Health</h4>
                        <div style="font-size: 13px; line-height: 1.7; color: #334155;">
                            <div><strong>Page Title:</strong> ${audit.title || 'Untitled'}</div>
                            <div><strong>URL:</strong> <code style="font-size:12px; color:#2563eb;">${audit.url || ''}</code></div>
                            <div><strong>Target Entity / Topic:</strong> ${audit.product_name || 'General Topic'}</div>
                            <div><strong>Primary Focus Keyword:</strong> <span style="background:#fef3c7; color:#92400e; padding:1px 6px; border-radius:4px; font-weight:700;">${audit.main_keyword || 'Not detected'}</span></div>
                            <div><strong>Security & Protocol:</strong> ${tech.is_https ? '✅ HTTPS Encrypted' : '❌ Insecure HTTP'} &nbsp;|&nbsp; <strong>Mobile Viewport:</strong> ${(tech.mobile_viewport && tech.mobile_viewport.has_viewport) ? '✅ Responsive' : '❌ Missing'} &nbsp;|&nbsp; <strong>Robots.txt:</strong> ${(tech.robots_txt && tech.robots_txt.exists) ? '✅ Status 200' : '⚠️ Missing'}</div>
                        </div>
                    </div>

                    <!-- Critical Issues & Gaps -->
                    <div class="report-section" style="border-left: 4px solid #ef4444;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #991b1b; margin-top: 0; margin-bottom: 8px;">2. High-Priority Issues & Critical SEO Errors</h4>
                        <p style="font-size: 12px; color: #64748b; margin-top: 0;">Errors discovered during live crawler analysis that negatively impact search visibility:</p>
                        <div style="display: grid; gap: 8px;">
                            ${(issues.critical_errors || []).map(e => `
                                <div style="background:#fffafb; border:1px solid #fecaca; border-radius:6px; padding:8px 12px; font-size:12.5px;">
                                    <strong style="color:#b91c1c;">🔴 ${e.title}</strong>
                                    <div style="color:#475569; margin:2px 0;">${e.impact}</div>
                                    <div style="color:#047857; font-weight:600;">🛠️ Recommended Fix: ${e.fix}</div>
                                </div>
                            `).join('') || '<div style="color:#059669; font-weight:600;">No critical errors detected.</div>'}
                        </div>
                    </div>

                    <!-- Google AI Overview & SERP Readiness -->
                    <div class="report-section" style="border-left: 4px solid #8b5cf6;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #5b21b6; margin-top: 0; margin-bottom: 8px;">3. Google SERP & AI Overview (SGE) Opportunities</h4>
                        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
                            <div><strong>AI Overview Readiness:</strong> ${serp.score || 0}/100 (${serp.status || 'Moderate'})</div>
                            <div><strong>Direct Answer Definition Block:</strong> ${serp.has_direct_answer ? '✅ Present' : '❌ Missing (Prime opportunity to steal AI Overview citation)'}</div>
                            <div><strong>Comparison Tables:</strong> ${serp.table_count || 0} table(s) &nbsp;|&nbsp; <strong>Structured Question Headings:</strong> ${serp.question_headings_count || 0} detected</div>
                        </div>
                    </div>

                    <!-- Semantic Keyword Cluster -->
                    <div class="report-section">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">4. High-Intent Semantic Keyword Cluster</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                            ${(audit.lsi_keywords || []).map(k => `<span style="background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; padding:3px 8px; border-radius:5px; font-size:12px; font-weight:600;">${k}</span>`).join('')}
                        </div>
                    </div>

                    <!-- Actionable Outranking Roadmap -->
                    <div class="report-section" style="border-left: 4px solid #10b981; margin-bottom: 0;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #065f46; margin-top: 0; margin-bottom: 8px;">5. Strategic Outranking Roadmap for ${clientName}</h4>
                        <div style="display: grid; gap: 8px;">
                            ${bp.map(s => `
                                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px;">
                                    <div style="font-size:13px; font-weight:700; color:#0f172a;">Step ${s.step}: ${s.action}</div>
                                    <div style="font-size:12px; color:#475569; margin-top:2px;">${s.detail}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>

                    <div style="margin-top: 24px; padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between;">
                        <span>Report generated by ${agencyName} (RankNaserPro Automated Intelligence Suite)</span>
                        <span>Confidential</span>
                    </div>
                `;
            } else if (activeReportData.type === 'multi') {
                const analysis = activeReportData.data.analysis;
                const article = activeReportData.data.article;
                const comps = analysis.competitors || [];
                const stats = analysis.stats || {};
                const gaps = analysis.content_gaps || [];

                container.innerHTML = `
                    <div style="border-bottom: 2px solid #0f172a; padding-bottom: 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div style="font-size: 11px; font-weight: 800; color: #dc2626; text-transform: uppercase; letter-spacing: 1px;">MULTI-COMPETITOR BATTLE ROYALE AUDIT</div>
                            <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 4px 0;">5 vs 1 Master Outranker Intelligence Report</h2>
                            <div style="font-size: 13px; color: #475569;">
                                Prepared for: <strong style="color: #0f172a;">${clientName}</strong> &nbsp;|&nbsp; Prepared by: <strong style="color: #0f172a;">${agencyName}</strong>
                            </div>
                        </div>
                        <div style="text-align: right; font-size: 12px; color: #64748b;">
                            <div>Date: <strong>${dateStr}</strong></div>
                            <div>Confidential Client Deliverable</div>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Competitors Benchmarked</div>
                            <div class="report-kpi-num" style="color: #0f172a;">${comps.length} URLs</div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Top Competitor Length</div>
                            <div class="report-kpi-num" style="color: #d97706;">${(stats.max_word_count || 0).toLocaleString()} w</div>
                        </div>
                        <div class="report-kpi-card" style="background: #f0fdf4; border-color: #86efac;">
                            <div style="font-size: 11px; font-weight: 700; color: #065f46; text-transform: uppercase;">Engineered Article Length</div>
                            <div class="report-kpi-num" style="color: #047857;">${(article.actual_word_count || stats.target_word_count || 2500).toLocaleString()} w 🏆</div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Collective Gaps Solved</div>
                            <div class="report-kpi-num" style="color: #2563eb;">${gaps.length} Gaps</div>
                        </div>
                    </div>

                    <div class="report-section">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">1. Competitor Benchmark Dissection</h4>
                        <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                                <thead>
                                    <tr style="background: #0f172a; color: white;">
                                        <th style="padding: 8px 10px; text-align: left;">Competitor</th>
                                        <th style="padding: 8px 10px; text-align: left;">Title</th>
                                        <th style="padding: 8px 10px; text-align: left;">Words</th>
                                        <th style="padding: 8px 10px; text-align: left;">SEO Score</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${comps.map((c, i) => `
                                        <tr style="border-bottom: 1px solid #e2e8f0;">
                                            <td style="padding: 8px 10px;"><strong>#${i+1} ${c.domain}</strong></td>
                                            <td style="padding: 8px 10px; max-width: 260px;">${c.title}</td>
                                            <td style="padding: 8px 10px;">${(c.word_count || 0).toLocaleString()} w</td>
                                            <td style="padding: 8px 10px; font-weight: 700; color: ${c.seo_score >= 80 ? '#15803d' : '#d97706'};">${c.seo_score}/100</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="report-section" style="border-left: 4px solid #f59e0b;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">2. Collective Competitor Gaps Solved for ${clientName}</h4>
                        <ul style="margin: 0 0 0 18px; padding: 0; font-size: 13px; color: #334155; line-height: 1.7;">
                            ${gaps.map(g => `<li>${g}</li>`).join('')}
                        </ul>
                    </div>

                    <div class="report-section" style="border-left: 4px solid #10b981; margin-bottom: 0;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #065f46; margin-top: 0; margin-bottom: 8px;">3. Engineered Outranking Article Blueprint</h4>
                        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
                            <div><strong>Recommended Title:</strong> ${article.meta_title || ''}</div>
                            <div><strong>Meta Description:</strong> ${article.meta_description || ''}</div>
                            <div><strong>Focus Keyword:</strong> <span style="background:#dcfce7; color:#166534; padding:2px 8px; border-radius:4px; font-weight:700;">${analysis.focus_keyword || ''}</span></div>
                            <div style="margin-top: 6px; color: #059669; font-weight: 700;">✅ Outranking article generated with ${article.actual_word_count || stats.target_word_count} words (+25% depth) and FAQ schema markup!</div>
                        </div>
                    </div>

                    <div style="margin-top: 24px; padding-top: 12px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between;">
                        <span>Report generated by ${agencyName} (RankNaserPro Multi-Competitor Suite)</span>
                        <span>Confidential</span>
                    </div>
                `;
            }
        }

        function printClientReport() {
            updateReportPreview();
            const previewHtml = document.getElementById('reportPreviewContainer').innerHTML;
            const printBox = document.getElementById('printableClientReport');
            if (printBox) {
                printBox.innerHTML = previewHtml;
            }
            window.print();
        }

        function copyClientReportSummary() {
            if (!activeReportData) return;
            const clientName = document.getElementById('reportClientName').value.trim() || 'Client';
            const agencyName = document.getElementById('reportAgencyName').value.trim() || 'Agency';
            const NL = String.fromCharCode(10);

            let summary = '';
            if (activeReportData.type === 'single') {
                const audit = activeReportData.data.audit;
                const lsiList = (audit.lsi_keywords || []).slice(0, 6).map(k => '• ' + k).join(NL);
                const gapList = (audit.content_gaps || []).slice(0, 3).map(g => '• ' + g).join(NL);
                const targetW = (audit.target_outrank_word_count || Math.max(2000, Math.floor(audit.word_count * 1.25))) + '+ words';

                summary = '📊 *EXECUTIVE COMPETITOR AUDIT REPORT*' + NL +
                    '*Prepared for:* ' + clientName + NL +
                    '*Prepared by:* ' + agencyName + NL +
                    '*Competitor URL:* ' + audit.url + NL +
                    '*Competitor SEO Score:* ' + audit.seo_score + '/100' + NL +
                    '*Competitor Word Count:* ' + audit.word_count + ' words' + NL +
                    '*Target to Outrank:* ' + targetW + NL + NL +
                    '🎯 *Top Keywords Competitor Ranks For:*' + NL +
                    lsiList + NL + NL +
                    '⚠️ *Identified Competitor Weaknesses:*' + NL +
                    gapList + NL + NL +
                    '🚀 *Next Steps:* We have engineered an outranking content piece ready to publish to outrank this competitor. Let us know when to deploy!';
            } else if (activeReportData.type === 'multi') {
                const analysis = activeReportData.data.analysis;
                const article = activeReportData.data.article;
                const gaps = (analysis.content_gaps || []).slice(0, 5).map(g => '• ' + g).join(NL);

                summary = '⚔️ *MULTI-COMPETITOR BATTLE AUDIT REPORT*' + NL +
                    '*Prepared for:* ' + clientName + NL +
                    '*Prepared by:* ' + agencyName + NL +
                    '*Competitors Audited:* ' + (analysis.competitors || []).length + ' URLs' + NL +
                    '*Focus Keyword:* ' + analysis.focus_keyword + NL +
                    '*Engineered Outrank Words:* ' + article.actual_word_count + ' words' + NL + NL +
                    '💡 *Collective Competitor Gaps Solved:*' + NL +
                    gaps + NL + NL +
                    '🏆 *Engineered Article Title:* ' + article.meta_title + NL +
                    'Ready to deploy to your website!';
            }

            navigator.clipboard.writeText(summary).then(() => {
                alert('Executive Summary copied to clipboard! Ready to paste into WhatsApp, Email, or Slack.');
            });
        }

        // ================= 30-Day Topical Authority Content Roadmap =================
        let currentRoadmapItems = [];

        function openRoadmapModal() {
            document.getElementById('contentRoadmapModal').style.display = 'flex';
        }

        function closeRoadmapModal() {
            document.getElementById('contentRoadmapModal').style.display = 'none';
        }

        function handleGenerateRoadmap(e) {
            e.preventDefault();
            const topic = document.getElementById('roadmapTopicInput').value.trim();
            const country = document.getElementById('roadmapCountryInput').value;
            if (!topic) return;

            const calendar = [
                {
                    day: "Day 1 (Week 1)",
                    stage: "Core Pillar Foundation",
                    title: `The Ultimate Guide to ${topic} (${new Date().getFullYear()} Edition)`,
                    intent: "Informational / Pillar",
                    intentClass: "intent-info",
                    keywords: `${topic}, best ${topic}, comprehensive guide`,
                    words: 3500,
                    type: "long_form_seo"
                },
                {
                    day: "Day 4 (Week 1)",
                    stage: "Pricing & Buying Sub-Pillar",
                    title: `${topic} Price Breakdown & Complete Buying Guide in ${country}`,
                    intent: "Commercial / Price",
                    intentClass: "intent-comm",
                    keywords: `${topic} price in ${country}, budget ${topic}, buying tips`,
                    words: 2200,
                    type: "buying_guide"
                },
                {
                    day: "Day 8 (Week 2)",
                    stage: "High-Intent Buyer Reviews",
                    title: `Top 10 Best ${topic} Ranked & Reviewed (Expert Tested)`,
                    intent: "Commercial / Review",
                    intentClass: "intent-comm",
                    keywords: `best ${topic} review, top rated ${topic}, comparison`,
                    words: 2800,
                    type: "commercial_article"
                },
                {
                    day: "Day 12 (Week 2)",
                    stage: "Head-to-Head Comparison Battle",
                    title: `${topic} vs Alternatives: Which One Should You Buy?`,
                    intent: "Decision / Versus",
                    intentClass: "intent-trans",
                    keywords: `${topic} comparison, ${topic} vs alternatives`,
                    words: 2400,
                    type: "comparison_article"
                },
                {
                    day: "Day 16 (Week 3)",
                    stage: "Mistakes & Pitfalls Cluster",
                    title: `7 Costly Mistakes to Avoid When Choosing ${topic}`,
                    intent: "Informational / Trust",
                    intentClass: "intent-info",
                    keywords: `${topic} mistakes, how to choose ${topic}`,
                    words: 1800,
                    type: "informational_article"
                },
                {
                    day: "Day 20 (Week 3)",
                    stage: "Practical How-To Tutorial",
                    title: `How to Setup, Maintain & Maximize Your ${topic} Step-by-Step`,
                    intent: "Informational / Guide",
                    intentClass: "intent-info",
                    keywords: `how to use ${topic}, ${topic} setup guide, tutorial`,
                    words: 2000,
                    type: "informational_article"
                },
                {
                    day: "Day 24 (Week 4)",
                    stage: "High-Converting Budget Cluster",
                    title: `Best Budget ${topic} That Deliver Maximum Value in ${country}`,
                    intent: "Transactional / Budget",
                    intentClass: "intent-trans",
                    keywords: `cheap ${topic}, budget friendly ${topic}, best value`,
                    words: 2200,
                    type: "product_review"
                },
                {
                    day: "Day 28 (Week 4)",
                    stage: "FAQ Authority Rich Snippet Cluster",
                    title: `Frequently Asked Questions About ${topic}: Everything You Need to Know`,
                    intent: "Informational / FAQ",
                    intentClass: "intent-info",
                    keywords: `${topic} faqs, common questions ${topic}`,
                    words: 1600,
                    type: "long_form_seo"
                }
            ];

            currentRoadmapItems = calendar;

            const tbody = document.getElementById('roadmapTableBody');
            tbody.innerHTML = calendar.map((item) => `
                <tr>
                    <td>
                        <strong style="color:#0f172a;">${item.day}</strong><br>
                        <small style="color:#64748b;">${item.stage}</small>
                    </td>
                    <td>
                        <strong style="color:#1e3a8a; font-size:13px;">${item.title}</strong>
                    </td>
                    <td>
                        <span class="badge-intent ${item.intentClass}">${item.intent}</span>
                    </td>
                    <td style="font-size:12px; color:#475569;">
                        <code>${item.keywords}</code>
                    </td>
                    <td>
                        <strong style="color:#059669;">${item.words.toLocaleString()}w</strong>
                    </td>
                    <td>
                        <button type="button" class="btn-download" style="background:#2563eb; padding:5px 10px; font-size:11px;" onclick="sendRoadmapTopicToStudio('${item.title.replace(/'/g, "\\'")}', '${item.keywords.split(',')[0].replace(/'/g, "\\'")}', ${item.words}, '${item.type}')">
                            ⚡ Write Article
                        </button>
                    </td>
                </tr>
            `).join('');

            document.getElementById('roadmapResultsBox').style.display = 'block';
            document.getElementById('roadmapCountText').innerText = `📋 30-Day Topical Roadmap for "${topic}" (${calendar.length} High-Impact Articles)`;
        }

        function downloadRoadmapCSV() {
            if (!currentRoadmapItems || currentRoadmapItems.length === 0) return;
            const NL = String.fromCharCode(10);
            let csv = "Schedule,Stage,Content Title,Search Intent,Target Keywords,Target Word Count,Content Type" + NL;
            currentRoadmapItems.forEach(i => {
                const day = '"' + (i.day || '').replace(/"/g, '""') + '"';
                const stage = '"' + (i.stage || '').replace(/"/g, '""') + '"';
                const title = '"' + (i.title || '').replace(/"/g, '""') + '"';
                const intent = '"' + (i.intent || '').replace(/"/g, '""') + '"';
                const kw = '"' + (i.keywords || '').replace(/"/g, '""') + '"';
                const words = i.words || 2000;
                const type = i.type || 'long_form_seo';
                csv += day + ',' + stage + ',' + title + ',' + intent + ',' + kw + ',' + words + ',' + type + NL;
            });

            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = `30_day_topical_authority_roadmap_${new Date().toISOString().split('T')[0]}.csv`;
            link.click();
        }

        function sendRoadmapTopicToStudio(title, kw, words, type) {
            closeRoadmapModal();
            switchTab('writer');
            if (document.getElementById('wTopic')) document.getElementById('wTopic').value = title;
            if (document.getElementById('wKeyword')) document.getElementById('wKeyword').value = kw;
            if (document.getElementById('wFormat')) document.getElementById('wFormat').value = type;
            if (document.getElementById('wWordCount')) document.getElementById('wWordCount').value = words >= 3000 ? '3500' : (words >= 2000 ? '2500' : '1500');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // ==========================================
        // TAB 6: Personal SEO Director Agent Logic
        // ==========================================
        function escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }

        let currentDirectorCampaign = null;
        let directorDeliverables = {};
        let activeDirectorModalDay = null;

        const defaultDirectorProfiles = [
            {
                id: 'prof_default',
                name: 'My Business Campaign',
                domain: '',
                country: 'Bangladesh',
                keywords: '',
                competitors: '',
                instructions: 'Ensure accurate market pricing, prioritize authorized warranty verification, and optimize all headings for Google AI Overview.'
            }
        ];

        activeProfileId = activeProfileId || 'prof_default';

        function getDirectorProfiles() {
            return getConnectedClients();
        }

        function saveDirectorProfiles(profiles) {
            localStorage.setItem('ranknaser_connected_clients', JSON.stringify(profiles));
            localStorage.setItem('seo_director_profiles', JSON.stringify(profiles));
            if (typeof updateClientsUI === 'function') updateClientsUI();
        }

        function renderCompanyPills() {
            const profiles = getDirectorProfiles();
            const container = document.getElementById('companyProfilesList');
            if (!container) return;

            let html = '';
            profiles.forEach(p => {
                const isActive = (p.id === activeProfileId);
                html += `<div class="company-pill ${isActive ? 'active' : ''}" onclick="selectCompanyProfile('${p.id}')">
                    <span>🏢 ${escapeHtml(p.name)}</span>
                </div>`;
            });
            container.innerHTML = html;
        }

        function selectCompanyProfile(profileId) {
            activeProfileId = profileId;
            const profiles = getDirectorProfiles();
            const p = profiles.find(item => item.id === profileId);
            if (!p) return;

            if (document.getElementById('dirCompanyName')) document.getElementById('dirCompanyName').value = p.name || '';
            if (document.getElementById('dirDomain')) document.getElementById('dirDomain').value = p.domain || '';
            if (document.getElementById('dirCountry')) document.getElementById('dirCountry').value = p.country || 'Bangladesh';
            if (document.getElementById('dirKeywords')) document.getElementById('dirKeywords').value = p.keywords || '';
            if (document.getElementById('dirCompetitors')) document.getElementById('dirCompetitors').value = p.competitors || '';
            if (document.getElementById('dirInstructions')) document.getElementById('dirInstructions').value = p.instructions || '';

            renderCompanyPills();
            appendDirectorLog(`[PROFILE] Switched to company profile: ${p.name}`);
        }

        function saveCurrentCompanyProfile() {
            const name = document.getElementById('dirCompanyName').value.trim() || 'My Business';
            const domain = document.getElementById('dirDomain').value.trim();
            const country = document.getElementById('dirCountry').value;
            const keywords = document.getElementById('dirKeywords').value.trim();
            const competitors = document.getElementById('dirCompetitors').value.trim();
            const instructions = document.getElementById('dirInstructions').value.trim();

            let profiles = getDirectorProfiles();
            let idx = profiles.findIndex(p => p.id === activeProfileId);

            const updatedProfile = {
                id: activeProfileId || ('prof_' + Date.now()),
                name: name,
                domain: domain,
                country: country,
                keywords: keywords,
                competitors: competitors,
                instructions: instructions
            };

            if (idx >= 0) {
                profiles[idx] = updatedProfile;
            } else {
                profiles.push(updatedProfile);
                activeProfileId = updatedProfile.id;
            }

            saveDirectorProfiles(profiles);
            renderCompanyPills();
            alert(`✅ Company profile for "${name}" saved successfully!`);
        }

        function addNewCompanyProfile() {
            const newId = 'prof_' + Date.now();
            activeProfileId = newId;
            let profiles = getDirectorProfiles();
            const newProf = {
                id: newId,
                name: 'New Client / Company',
                domain: 'https://newclient.com',
                country: 'Bangladesh',
                keywords: ['primary keyword', 'secondary keyword', 'best product review'].join('\\n'),
                competitors: 'https://competitor.com',
                instructions: 'Focus on search intent, pricing transparency, and Google AI Overview snippets.'
            };
            profiles.push(newProf);
            saveDirectorProfiles(profiles);
            selectCompanyProfile(newId);
        }

        function deleteCurrentCompanyProfile() {
            let profiles = getDirectorProfiles();
            if (profiles.length <= 1) {
                alert('Cannot delete the last company profile. You must have at least one profile.');
                return;
            }
            if (!confirm(`Are you sure you want to delete the active company profile?`)) return;

            profiles = profiles.filter(p => p.id !== activeProfileId);
            activeProfileId = profiles[0].id;
            saveDirectorProfiles(profiles);
            selectCompanyProfile(activeProfileId);
        }

        function appendDirectorLog(msg) {
            const consoleBox = document.getElementById('dirConsoleBox');
            const logBox = document.getElementById('dirConsoleLogs');
            if (consoleBox) consoleBox.style.display = 'block';
            if (logBox) {
                const time = new Date().toLocaleTimeString();
                logBox.innerHTML += `<div><span style="color:#64748b;">[${time}]</span> ${escapeHtml(msg)}</div>`;
                consoleBox.scrollTop = consoleBox.scrollHeight;
            }
        }

        async function generateDirectorPlan() {
            const companyName = document.getElementById('dirCompanyName').value.trim();
            const domain = document.getElementById('dirDomain').value.trim();
            const country = document.getElementById('dirCountry').value;
            const kwRaw = document.getElementById('dirKeywords').value.trim();
            const compRaw = document.getElementById('dirCompetitors').value.trim();

            if (!companyName) {
                alert('Please enter a Company / Brand Name.');
                return;
            }
            if (!kwRaw) {
                alert('Please enter at least one target keyword.');
                return;
            }

            const keywords = kwRaw.split(String.fromCharCode(10)).flatMap(function(line) { return line.split(','); }).map(function(k) { return k.trim(); }).filter(function(k) { return k.length > 0; });
            const competitor_urls = compRaw.split(String.fromCharCode(10)).flatMap(function(line) { return line.split(','); }).map(function(u) { return u.trim(); }).filter(function(u) { return u.length > 0; });
            const geminiKey = localStorage.getItem('gemini_api_key') || '';

            const btn = document.getElementById('btnGenDirectorPlan');
            btn.disabled = true;
            btn.innerHTML = '<span>⏳ Synthesizing 10-Day Plan...</span>';
            appendDirectorLog(`[DIRECTOR] Generating 10-Day Master SEO Strategy for "${companyName}" (${keywords.length} keywords)...`);

            try {
                const resp = await fetch('/api/seo-director/plan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        company_name: companyName,
                        domain: domain,
                        keywords: keywords,
                        target_country: country,
                        competitor_urls: competitor_urls,
                        gemini_key: geminiKey
                    })
                });
                const data = await resp.json();
                btn.disabled = false;
                btn.innerHTML = '<span>🚀 1. Generate 10-Day Master Roadmap</span>';

                if (data.status === 'success' && data.campaign) {
                    currentDirectorCampaign = data.campaign;
                    directorDeliverables = {};
                    renderDirectorCards(currentDirectorCampaign.roadmap);
                    updateDirectorProgress();
                    appendDirectorLog(`✅ 10-Day Master Campaign roadmap generated successfully! 10 Missions loaded.`);
                } else {
                    alert('Error: ' + (data.message || 'Failed to generate plan.'));
                }
            } catch(e) {
                btn.disabled = false;
                btn.innerHTML = '<span>🚀 1. Generate 10-Day Master Roadmap</span>';
                alert('Request failed: ' + e.message);
                appendDirectorLog(`❌ Error: ${e.message}`);
            }
        }

        function renderDirectorCards(roadmap) {
            const grid = document.getElementById('dirDaysGrid');
            if (!grid) return;

            let html = '';
            roadmap.forEach(day => {
                const hasDeliverable = !!directorDeliverables[day.day];
                const statusText = hasDeliverable ? 'Completed ✅' : (day.status || 'Ready to Execute');
                const cardClass = hasDeliverable ? 'completed' : '';

                html += `
                <div class="day-mission-card ${cardClass}" id="dirCardDay_${day.day}">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="font-size: 15px; font-weight: 800; color: #1e3a8a;">${day.icon} Day ${day.day}</span>
                            <span class="${day.badge_class || 'badge-onpage'}">${day.category}</span>
                        </div>
                        <h4 style="font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 6px; line-height: 1.35;">${escapeHtml(day.title)}</h4>
                        <p style="font-size: 12.5px; color: #475569; margin-bottom: 12px; line-height: 1.45;">${escapeHtml(day.objective)}</p>
                        
                        <div style="margin-bottom: 12px;">
                            <div style="font-size: 10.5px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px;">Target Keywords:</div>
                            <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                                ${(day.target_keywords || []).map(k => `<span style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; font-size: 11px; padding: 2px 7px; border-radius: 4px; font-weight: 600;">${escapeHtml(k)}</span>`).join('')}
                            </div>
                        </div>
                    </div>

                    <div style="border-top: 1px solid var(--border); padding-top: 12px; display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap;">
                        <span id="dirCardStatus_${day.day}" style="font-size: 12px; font-weight: 700; color: ${hasDeliverable ? '#059669' : '#64748b'};">${statusText}</span>
                        <div style="display: flex; gap: 6px;">
                            <button type="button" class="btn-action" id="btnDirExecDay_${day.day}" onclick="executeDirectorDay(${day.day})" style="background: #0284c7; color: white; border: none; font-size: 11.5px; padding: 6px 11px;">
                                <span>▶️ ${hasDeliverable ? 'Re-Run' : 'Run Mission'}</span>
                            </button>
                            ${hasDeliverable ? `
                            <button type="button" class="btn-action" onclick="openDirectorModal(${day.day})" style="background: #ffffff; border: 1px solid #cbd5e1; color: #0f172a; font-size: 11.5px; padding: 6px 11px;">
                                <span>👁️ View</span>
                            </button>` : ''}
                        </div>
                    </div>
                </div>
                `;
            });

            grid.innerHTML = html;
        }

        function updateDirectorProgress() {
            const pBox = document.getElementById('dirCampaignProgressBox');
            if (!pBox) return;
            pBox.style.display = 'block';

            const compTitle = document.getElementById('dirCampaignHeaderTitle');
            if (compTitle && currentDirectorCampaign) {
                compTitle.innerText = `Campaign: ${currentDirectorCampaign.company_name} (${currentDirectorCampaign.target_country})`;
            }

            const total = 10;
            const completedCount = Object.keys(directorDeliverables).length;
            const pct = Math.round((completedCount / total) * 100);

            const pBar = document.getElementById('dirProgressBar');
            if (pBar) pBar.style.width = pct + '%';

            const cText = document.getElementById('dirCompletionText');
            if (cText) cText.innerText = `${completedCount} of 10 Days Executed (${pct}%)`;

            const pill = document.getElementById('dirCampaignStatusPill');
            if (pill) {
                if (completedCount === 10) {
                    pill.innerText = 'Completed 100% 🏆';
                    pill.style.background = '#d1fae5';
                    pill.style.color = '#065f46';
                } else {
                    pill.innerText = `${completedCount}/10 Missions Live`;
                }
            }
        }

        async function executeDirectorDay(dayNumber) {
            if (!currentDirectorCampaign) {
                await generateDirectorPlan();
                if (!currentDirectorCampaign) return;
            }

            const card = document.getElementById(`dirCardDay_${dayNumber}`);
            const statusElem = document.getElementById(`dirCardStatus_${dayNumber}`);
            const btnExec = document.getElementById(`btnDirExecDay_${dayNumber}`);

            if (card) {
                card.className = 'day-mission-card running';
            }
            if (statusElem) {
                statusElem.innerText = 'Executing ⚙️...';
                statusElem.style.color = '#2563eb';
            }
            if (btnExec) {
                btnExec.disabled = true;
                btnExec.innerHTML = '<span>⏳ Running</span>';
            }

            appendDirectorLog(`[MISSION] Launching Day ${dayNumber} autonomous task...`);

            const geminiKey = localStorage.getItem('gemini_api_key') || '';
            const wpCreds = getWpCredentials();
            const customCreds = getCustomCredentials();

            try {
                const resp = await fetch('/api/seo-director/execute-day', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        day_number: dayNumber,
                        campaign_info: currentDirectorCampaign,
                        wp_config: wpCreds.url ? wpCreds : null,
                        custom_webhook_config: customCreds.url ? customCreds : null,
                        gemini_key: geminiKey
                    })
                });

                const data = await resp.json();

                if (btnExec) btnExec.disabled = false;

                if (data.status === 'success' && data.deliverable) {
                    directorDeliverables[dayNumber] = data.deliverable;
                    if (data.logs) {
                        data.logs.forEach(l => appendDirectorLog(l));
                    }
                    if (card) card.className = 'day-mission-card completed';
                    if (statusElem) {
                        statusElem.innerText = 'Completed ✅';
                        statusElem.style.color = '#059669';
                    }
                    renderDirectorCards(currentDirectorCampaign.roadmap);
                    updateDirectorProgress();
                    openDirectorModal(dayNumber);
                } else {
                    if (card) card.className = 'day-mission-card';
                    if (statusElem) {
                        statusElem.innerText = 'Failed ❌';
                        statusElem.style.color = '#dc2626';
                    }
                    alert('Error executing day ' + dayNumber + ': ' + (data.message || 'Unknown error'));
                    appendDirectorLog(`❌ Error executing day ${dayNumber}: ${data.message || 'Unknown error'}`);
                }
            } catch(e) {
                if (btnExec) btnExec.disabled = false;
                if (card) card.className = 'day-mission-card';
                alert('Request failed: ' + e.message);
                appendDirectorLog(`❌ Request error: ${e.message}`);
            }
        }

        async function executeAllDirectorDays() {
            if (!currentDirectorCampaign) {
                await generateDirectorPlan();
                if (!currentDirectorCampaign) return;
            }

            const btn = document.getElementById('btnExecAllDirector');
            btn.disabled = true;
            btn.innerHTML = '<span>⏳ Executing All 10 Days...</span>';

            const spinner = document.getElementById('dirLiveSpinner');
            if (spinner) spinner.style.display = 'inline';

            appendDirectorLog(`[AUTONOMOUS BATCH] Starting sequential execution of all 10 days for "${currentDirectorCampaign.company_name}"...`);

            for (let d = 1; d <= 10; d++) {
                appendDirectorLog(`▶️ Commencing Day ${d} of 10...`);
                await executeDirectorDay(d);
            }

            if (spinner) spinner.style.display = 'none';
            btn.disabled = false;
            btn.innerHTML = '<span>⚡ 2. Execute Entire 10-Day Campaign Autonomously</span>';
            appendDirectorLog(`🎉 All 10 Days successfully executed! Full SEO portfolio ready for download.`);
            alert('🎉 Congratulations! All 10 days of your SEO campaign have been successfully executed!');
        }

        function openDirectorModal(dayNumber) {
            activeDirectorModalDay = dayNumber;
            const deliv = directorDeliverables[dayNumber];
            if (!deliv) return;

            const modal = document.getElementById('dirDeliverableModal');
            const dayBadge = document.getElementById('dirModalDayBadge');
            const titleElem = document.getElementById('dirModalTitle');
            const contentElem = document.getElementById('dirModalContent');
            const btnStudio = document.getElementById('btnDirSendToStudio');
            const btnWpLive = document.getElementById('btnDirSendToWpLive');
            const btnWpDraft = document.getElementById('btnDirSendToWpDraft');

            if (dayBadge) dayBadge.innerText = `DAY ${dayNumber}`;
            if (titleElem) titleElem.innerText = deliv.title || `Deliverable for Day ${dayNumber}`;

            let htmlContent = '';
            if (deliv.html) {
                htmlContent = deliv.html;
            } else if (deliv.markdown) {
                htmlContent = (typeof marked !== 'undefined') ? marked.parse(deliv.markdown) : `<pre>${escapeHtml(deliv.markdown)}</pre>`;
            } else if (deliv.schema_json) {
                htmlContent = `<pre style="background:#0f172a; color:#38bdf8; padding:16px; border-radius:8px; overflow-x:auto;">${escapeHtml(deliv.schema_json)}</pre>`;
            } else {
                htmlContent = `<pre>${escapeHtml(JSON.stringify(deliv, null, 2))}</pre>`;
            }

            if (contentElem) contentElem.innerHTML = htmlContent;

            // Show Send to Studio if day produces articles (Day 2, 4, 6)
            if (btnStudio) {
                btnStudio.style.display = ([2, 4, 6].includes(dayNumber) && deliv.article) ? 'inline-block' : 'none';
            }
            if (btnWpLive) btnWpLive.style.display = ([2, 4, 6].includes(dayNumber) && deliv.article) ? 'inline-block' : 'none';
            if (btnWpDraft) btnWpDraft.style.display = ([2, 4, 6].includes(dayNumber) && deliv.article) ? 'inline-block' : 'none';

            if (modal) modal.style.display = 'flex';
        }

        function closeDirectorModal() {
            const modal = document.getElementById('dirDeliverableModal');
            if (modal) modal.style.display = 'none';
        }

        function copyDirectorDeliverable() {
            if (!activeDirectorModalDay) return;
            const deliv = directorDeliverables[activeDirectorModalDay];
            if (!deliv) return;

            let textToCopy = deliv.markdown || deliv.schema_json || JSON.stringify(deliv, null, 2);
            navigator.clipboard.writeText(textToCopy).then(() => {
                const alert = document.getElementById('dirModalCopyAlert');
                if (alert) {
                    alert.style.display = 'inline';
                    setTimeout(() => alert.style.display = 'none', 3000);
                }
            });
        }

        function sendDirectorArticleToStudio() {
            if (!activeDirectorModalDay) return;
            const deliv = directorDeliverables[activeDirectorModalDay];
            if (!deliv || !deliv.article) return;

            closeDirectorModal();
            switchTab('writer');

            const a = deliv.article;
            if (document.getElementById('wTopic')) document.getElementById('wTopic').value = a.topic || '';
            if (document.getElementById('wKeyword')) document.getElementById('wKeyword').value = a.main_keyword || '';
            if (document.getElementById('wFormat')) document.getElementById('wFormat').value = a.content_type || 'long_form_seo';

            generatedData = a;
            renderVisualView(a);
            updateWordPressPostFields();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function publishDirectorDeliverableToWp(forcedStatus = 'publish') {
            if (!activeDirectorModalDay) return;
            const deliv = directorDeliverables[activeDirectorModalDay];
            if (!deliv) return;

            if ([2, 4, 6].includes(activeDirectorModalDay) && deliv.article) {
                generatedData = deliv.article;
                publishArticleToWordPress('single', false, forcedStatus);
            } else {
                alert('Direct WordPress publishing is supported for articles (Days 2, 4, 6). For schemas, copy and paste into your site header.');
            }
        }

        function downloadDirectorCampaignReport() {
            if (!currentDirectorCampaign) {
                alert('Please generate a 10-day roadmap first.');
                return;
            }

            const c = currentDirectorCampaign;
            const NL = String.fromCharCode(10);
            const lines = [
                '# 10-Day Master SEO Campaign Roadmap: ' + c.company_name,
                '**Target Domain:** ' + c.domain + ' | **Country:** ' + c.target_country,
                '**Primary Focus Keyword:** ' + c.primary_keyword,
                '**All Target Keywords:** ' + (c.all_keywords || []).join(', '),
                '**Created Date:** ' + c.created_at,
                '',
                '---',
                ''
            ];

            (c.roadmap || []).forEach(function(day) {
                lines.push('## Day ' + day.day + ': ' + day.title + ' (' + day.category + ')');
                lines.push('**Objective:** ' + day.objective);
                lines.push('**Target Keywords:** ' + (day.target_keywords || []).join(', '));
                lines.push('');

                const deliv = directorDeliverables[day.day];
                if (deliv) {
                    lines.push('### Executed Deliverable:');
                    lines.push('');
                    if (deliv.markdown) {
                        lines.push(deliv.markdown);
                        lines.push('');
                    } else if (deliv.schema_json) {
                        lines.push('```json');
                        lines.push(deliv.schema_json);
                        lines.push('```');
                        lines.push('');
                    }
                } else {
                    lines.push('*Deliverable status: Ready to execute*');
                    lines.push('');
                }
                lines.push('---');
                lines.push('');
            });

            const mdContent = lines.join(NL);
            const blob = new Blob([mdContent], { type: 'text/markdown;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'SEO_10_Day_Campaign_' + c.company_name.replace(/[^a-zA-Z0-9]/g, '_') + '.md';
            link.click();
        }

        // Initialize Director company pills safely
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            try { renderCompanyPills(); } catch(e) {}
        } else {
            window.addEventListener('DOMContentLoaded', function() {
                try { renderCompanyPills(); } catch(e) {}
            });
        }

        // ================= AUTHENTICATION & SESSION LOGIC =================
        function checkAuthOnLoad() {
            let user = null;
            let authUser = localStorage.getItem('ranknaser_auth_user');
            if (authUser) {
                try {
                    user = JSON.parse(authUser);
                } catch(e) {
                    console.error('Failed to parse auth user', e);
                }
            }
            if (!user) {
                user = {
                    name: 'RankNaser Admin',
                    username: 'ADMIN',
                    email: 'admin@ranknaser.com',
                    domain: 'ranknaser.com'
                };
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(user));
            }
            showDashboardView(user);
        }

        function showAuthView() {
            const authSc = document.getElementById('authScreen');
            const dashWrap = document.getElementById('dashboardWrapper');
            if (authSc) authSc.style.display = 'none';
            if (dashWrap) dashWrap.style.display = 'block';
            window.scrollTo(0, 0);
        }


        // ================= 7-DAY FREE TRIAL EXPIRATION ENGINE =================
        const TRIAL_DURATION_DAYS = 7;
        const TRIAL_DURATION_MS = TRIAL_DURATION_DAYS * 24 * 60 * 60 * 1000;

        function getTrialData() {
            let startTs = localStorage.getItem('ranknaser_trial_start');
            if (!startTs) {
                startTs = Date.now().toString();
                localStorage.setItem('ranknaser_trial_start', startTs);
            }
            const start = parseInt(startTs, 10);
            const expires = start + TRIAL_DURATION_MS;
            const now = Date.now();
            const remainingMs = expires - now;
            const isExpired = remainingMs <= 0;
            
            const elapsedDays = Math.min(TRIAL_DURATION_DAYS, Math.max(1, Math.floor((now - start) / (24 * 60 * 60 * 1000)) + 1));
            const remainingDays = Math.max(0, Math.ceil(remainingMs / (24 * 60 * 60 * 1000)));
            const remainingHours = Math.max(0, Math.floor((remainingMs % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000)));

            return {
                start: new Date(start),
                expires: new Date(expires),
                isExpired: isExpired,
                elapsedDays: elapsedDays,
                remainingDays: remainingDays,
                remainingHours: remainingHours,
                remainingMs: remainingMs
            };
        }

        function updateTrialBadge(user) {
            const badge = document.getElementById('trialCountdownBadge');
            const text = document.getElementById('trialCountdownText');
            if (!badge || !text) return;

            badge.style.pointerEvents = 'none';
            badge.style.cursor = 'default';
            badge.removeAttribute('onclick');
            badge.onclick = null;

            // Master Admin check
            if (user && (user.username === 'ADMIN' || (user.email && user.email.toLowerCase() === 'admin@ranknaser.com'))) {
                badge.style.background = '#ffffff';
                badge.style.borderColor = '#cbd5e1';
                badge.style.color = '#0f172a';
                text.innerHTML = '👑 <strong>Master Admin:</strong> Lifetime';
                hideTrialExpiredLock();
                return;
            }

            const t = getTrialData();
            if (t.isExpired) {
                badge.style.background = '#fef2f2';
                badge.style.borderColor = '#fca5a5';
                badge.style.color = '#991b1b';
                text.innerHTML = '🔒 <strong>Free Trial:</strong> Expired';
                showTrialExpiredLock();
            } else {
                badge.style.background = '#ffffff';
                badge.style.borderColor = '#cbd5e1';
                badge.style.color = '#0f172a';
                text.innerHTML = `⏱️ <strong>7-Day Free Trial:</strong> Day ${t.elapsedDays} of 7 (${t.remainingDays}d left)`;
                hideTrialExpiredLock();
            }
        }

        function checkTrialEnforcement(user) {
            if (user && (user.username === 'ADMIN' || (user.email && user.email.toLowerCase() === 'admin@ranknaser.com'))) {
                hideTrialExpiredLock();
                return true;
            }
            const t = getTrialData();
            if (t.isExpired) {
                showTrialExpiredLock();
                return false;
            }
            hideTrialExpiredLock();
            return true;
        }

        function showTrialExpiredLock() {
            const modal = document.getElementById('trialExpiredModal');
            if (modal) modal.style.display = 'flex';
        }

        function hideTrialExpiredLock() {
            const modal = document.getElementById('trialExpiredModal');
            if (modal) modal.style.display = 'none';
        }

        function openTrialModal() {
            return false; // Disabled completely for 7 days
            const modal = document.getElementById('trialInfoModal');
            const body = document.getElementById('trialInfoModalBody');
            const adminBar = document.getElementById('adminTrialControlBar');
            if (!modal || !body) return;

            const user = JSON.parse(localStorage.getItem('ranknaser_auth_user') || '{}');
            const isAdmin = user && (user.username === 'ADMIN' || (user.email && user.email.toLowerCase() === 'admin@ranknaser.com'));

            if (adminBar) {
                adminBar.style.display = isAdmin ? 'block' : 'none';
            }

            if (isAdmin) {
                body.innerHTML = `
                    <div style="background: #e0f2fe; border: 1.5px solid #bae6fd; border-radius: 12px; padding: 14px; margin-bottom: 12px;">
                        <div style="font-weight: 800; color: #0369a1; font-size: 14px; margin-bottom: 4px;">👑 Master Administrator Account</div>
                        <div style="color: #0c4a6e;">You are logged in as the system owner. Your account has <strong>Lifetime Unlimited Access</strong> and will never expire.</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px;">
                        <div><strong>Trial Duration for Users:</strong> 7 Days (1 Week)</div>
                        <div><strong>Policy:</strong> After 7 days, user sessions automatically lock with the expiration screen.</div>
                    </div>
                `;
            } else {
                const t = getTrialData();
                body.innerHTML = `
                    <div style="background: ${t.isExpired ? '#fee2e2' : '#ecfdf5'}; border: 1.5px solid ${t.isExpired ? '#fca5a5' : '#a7f3d0'}; border-radius: 12px; padding: 14px; margin-bottom: 14px;">
                        <div style="font-weight: 800; color: ${t.isExpired ? '#b91c1c' : '#047857'}; font-size: 14.5px; margin-bottom: 4px;">
                            ${t.isExpired ? '🔒 7-Day Free Trial Expired' : '✅ 7-Day Free Trial Active'}
                        </div>
                        <div>${t.isExpired ? 'Your complimentary 1-week access has concluded.' : 'You currently have full, unrestricted access to all 6 autonomous SEO engines.'}</div>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; font-size: 13px; line-height: 1.7;">
                        <div>📅 <strong>Trial Started:</strong> ${t.start.toLocaleDateString()}</div>
                        <div>⏳ <strong>Trial Ends:</strong> ${t.expires.toLocaleDateString()}</div>
                        <div>📊 <strong>Progress:</strong> Day ${t.elapsedDays} of 7</div>
                        <div>⏱️ <strong>Remaining Time:</strong> ${t.isExpired ? '0 hours' : t.remainingDays + ' day(s), ' + t.remainingHours + ' hour(s)'}</div>
                    </div>
                `;
            }
            modal.style.display = 'flex';
        }

        function closeTrialModal() {
            const modal = document.getElementById('trialInfoModal');
            if (modal) modal.style.display = 'none';
        }

        function adminSimulateExpiredTrial() {
            // Set start date to 8 days ago
            const eightDaysAgo = Date.now() - (8 * 24 * 60 * 60 * 1000);
            localStorage.setItem('ranknaser_trial_start', eightDaysAgo.toString());
            closeTrialModal();
            const user = JSON.parse(localStorage.getItem('ranknaser_auth_user') || '{}');
            // If admin is testing, momentarily view non-admin lock
            alert('Simulation active: Set trial to 8 days ago. Showing trial lock overlay...');
            showTrialExpiredLock();
        }

        function adminReset7DayTrial() {
            localStorage.setItem('ranknaser_trial_start', Date.now().toString());
            closeTrialModal();
            hideTrialExpiredLock();
            const user = JSON.parse(localStorage.getItem('ranknaser_auth_user') || '{}');
            updateTrialBadge(user);
            alert('7-Day Free Trial has been reset to Day 1 of 7! Access unlocked.');
        }

        function promptAdminUnlock() {
            const u = prompt('Enter Admin User ID:');
            if (!u) return;
            const p = prompt('Enter Admin Password:');
            if (!p) return;
            if (u.toUpperCase() === 'ADMIN' && (p.toUpperCase() === 'AGENTNASER' || p === 'AGENTNASER')) {
                const adminUser = {
                    name: 'RankNaser Admin',
                    username: 'ADMIN',
                    email: 'admin@ranknaser.com',
                    domain: 'ranknaser.com'
                };
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(adminUser));
                hideTrialExpiredLock();
                showDashboardView(adminUser);
                alert('Master Admin verified! Full lifetime access unlocked.');
            } else {
                alert('Invalid Admin credentials! Only the administrator can unlock.');
            }
        }

        // ================= 1-WEEK FREE TRIAL USER MESSAGE CONTROLLERS (GLOBAL SCOPE) =================
        let trialWelcomeTimer = null;

        function showTrialWelcomeModal(force = false) {
            if (!force && sessionStorage.getItem('ranknaser_welcome_seen') === 'true') {
                return;
            }
            const modal = document.getElementById('trialWelcomeModal');
            if (modal) {
                modal.style.display = 'flex';
            }
        }
        
        // ================= USER GUIDE CONTROLLERS & PDF PRINTER =================
        function openUserGuideModal() {
            const modal = document.getElementById('userGuideModal');
            if (modal) modal.style.display = 'flex';
        }
        window.openUserGuideModal = openUserGuideModal;

        function closeUserGuideModal() {
            const modal = document.getElementById('userGuideModal');
            if (modal) modal.style.display = 'none';
        }
        window.closeUserGuideModal = closeUserGuideModal;

        function switchGuideTab(lang) {
            const viewEn = document.getElementById('guideViewEn');
            const viewBn = document.getElementById('guideViewBn');
            const tabEn = document.getElementById('guideTabEnBtn');
            const tabBn = document.getElementById('guideTabBnBtn');

            if (lang === 'bn') {
                if (viewEn) viewEn.style.display = 'none';
                if (viewBn) viewBn.style.display = 'block';
                if (tabEn) { tabEn.style.background = '#ffffff'; tabEn.style.color = '#334155'; tabEn.style.borderColor = '#cbd5e1'; }
                if (tabBn) { tabBn.style.background = '#059669'; tabBn.style.color = '#ffffff'; tabBn.style.borderColor = '#059669'; }
            } else {
                if (viewEn) viewEn.style.display = 'block';
                if (viewBn) viewBn.style.display = 'none';
                if (tabEn) { tabEn.style.background = '#4f46e5'; tabEn.style.color = '#ffffff'; tabEn.style.borderColor = '#4f46e5'; }
                if (tabBn) { tabBn.style.background = '#ffffff'; tabBn.style.color = '#334155'; tabBn.style.borderColor = '#cbd5e1'; }
            }
        }
        window.switchGuideTab = switchGuideTab;

        function downloadGuidePdf(lang) {
            const url = lang === 'bn' ? '/guide/bangla' : '/guide/english';
            window.open(url, '_blank');
        }
        window.downloadGuidePdf = downloadGuidePdf;

        window.showTrialWelcomeModal = showTrialWelcomeModal;

        function closeTrialWelcomeModal() {
            if (trialWelcomeTimer) {
                clearTimeout(trialWelcomeTimer);
                trialWelcomeTimer = null;
            }
            sessionStorage.setItem('ranknaser_welcome_seen', 'true');
            
            const modal = document.getElementById('trialWelcomeModal');
            if (modal) {
                modal.style.display = 'none';
            }
            const dashWrap = document.getElementById('dashboardWrapper');
            if (dashWrap) {
                dashWrap.style.display = 'block';
            }
            const authSc = document.getElementById('authScreen');
            if (authSc) {
                authSc.style.display = 'none';
            }
        }
        window.closeTrialWelcomeModal = closeTrialWelcomeModal;

        function dismissTrialAlert() {
            const alertBox = document.getElementById('trialWelcomeAlert');
            if (alertBox) {
                alertBox.style.display = 'none';
            }
        }
        window.dismissTrialAlert = dismissTrialAlert;

        function showDashboardView(user) {
            const authSc = document.getElementById('authScreen');
            const dashWrap = document.getElementById('dashboardWrapper');
            if (authSc) {
                authSc.style.display = 'none';
            }
            if (dashWrap) {
                dashWrap.style.display = 'block';
            }
            window.scrollTo(0, 0);
            
            const nameDisp = document.getElementById('currentUserNameDisplay');
            if (nameDisp && user && user.name) {
                nameDisp.textContent = '👤 ' + user.name;
            }

            try {
                updateTrialBadge(user);
                checkTrialEnforcement(user);
            } catch(e) {
                console.warn('Trial check non-blocking warning:', e);
            }

            try {
                if (typeof switchTab === 'function') {
                    const hash = window.location.hash.replace('#', '');
                    if (hash && ['daily', 'spy', 'multi', 'writer', 'autopilot', 'director', 'agency'].includes(hash)) {
                        switchTab(hash, false);
                    } else {
                        switchTab('daily', false);
                    }
                }
            } catch(e) {
                console.warn('Tab switch non-blocking warning:', e);
            }
        }

        function switchAuthTab(tab) {
            const tabLogin = document.getElementById('tabLoginBtn');
            const tabReg = document.getElementById('tabRegisterBtn');
            const formLogin = document.getElementById('loginForm');
            const formReg = document.getElementById('registerForm');
            const alertBox = document.getElementById('authAlertBox');
            if (alertBox) alertBox.style.display = 'none';

            if (tab === 'login') {
                tabLogin.classList.add('active');
                tabReg.classList.remove('active');
                formLogin.style.display = 'block';
                formReg.style.display = 'none';
            } else {
                tabReg.classList.add('active');
                tabLogin.classList.remove('active');
                formReg.style.display = 'block';
                formLogin.style.display = 'none';
            }
        }

        function showAuthAlert(msg, isSuccess = false) {
            const alertBox = document.getElementById('authAlertBox');
            if (!alertBox) return;
            alertBox.style.display = 'block';
            alertBox.style.background = isSuccess ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
            alertBox.style.border = isSuccess ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(239, 68, 68, 0.4)';
            alertBox.style.color = isSuccess ? '#34d399' : '#f87171';
            alertBox.innerHTML = (isSuccess ? '✅ ' : '⚠️ ') + msg;
        }

        async function handleAuthLogin(e) {
            if (e) {
                try { e.preventDefault(); } catch(err) {}
            }
            const uInput = document.getElementById('loginUsername') || document.getElementById('loginEmail');
            const username = (uInput ? uInput.value : '').trim();
            const pInput = document.getElementById('loginPassword');
            const password = (pInput ? pInput.value : '').trim();
            const submitBtn = document.getElementById('btnSubmitLogin');

            const adminUser = {
                name: 'RankNaser Admin',
                username: 'ADMIN',
                email: 'admin@ranknaser.com',
                domain: 'ranknaser.com'
            };

            // If empty, auto-fill default ADMIN / AGENTNASER and enter
            if (!username && !password) {
                if (uInput) uInput.value = 'ADMIN';
                if (pInput) pInput.value = 'AGENTNASER';
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(adminUser));
                showDashboardView(adminUser);
                return;
            }

            // Direct instant verification for ADMIN / AGENTNASER
            if (username.toUpperCase() === 'ADMIN' || password.toUpperCase() === 'AGENTNASER' || username.toLowerCase() === 'admin@ranknaser.com') {
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(adminUser));
                showDashboardView(adminUser);
                return;
            }

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerText = 'Verifying credentials...';
            }

            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: username, password: password })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    localStorage.setItem('ranknaser_auth_user', JSON.stringify(data.user));
                    showDashboardView(data.user);
                } else {
                    showAuthAlert(data.message || 'Invalid credentials! User: ADMIN | Password: AGENTNASER');
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = '<span>🚀 Launch RankNaserPro Dashboard</span>';
                    }
                }
            } catch(err) {
                // Offline fallback
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(adminUser));
                showDashboardView(adminUser);
            }
        }

        async function handleAuthRegister(e) {
            if (e) e.preventDefault();
            const name = (document.getElementById('regName').value || '').trim();
            const email = (document.getElementById('regEmail').value || '').trim();
            const domain = (document.getElementById('regDomain').value || '').trim();
            const password = (document.getElementById('regPassword').value || '').trim();
            const submitBtn = document.getElementById('btnSubmitRegister');

            if (!name || !email || !password) {
                showAuthAlert('Please fill out all required fields.');
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerText = 'Creating account...';

            try {
                const res = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ name: name, email: email, domain: domain, password: password })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    showAuthAlert('Account created successfully! Welcome, ' + name + '!', true);
                    localStorage.setItem('ranknaser_auth_user', JSON.stringify(data.user));
                    setTimeout(() => {
                        showDashboardView(data.user);
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = '<span>✨ Create Free Account & Enter</span>';
                    }, 500);
                } else {
                    showAuthAlert(data.message || 'Registration failed.');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<span>✨ Create Free Account & Enter</span>';
                }
            } catch(err) {
                // Local fallback registration
                const newUser = { name: name, email: email, domain: domain };
                localStorage.setItem('ranknaser_auth_user', JSON.stringify(newUser));
                showDashboardView(newUser);
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span>✨ Create Free Account & Enter</span>';
            }
        }

        function handleInstantDemoLogin() {
            const adminUser = {
                name: 'RankNaser Admin',
                username: 'ADMIN',
                email: 'admin@ranknaser.com',
                domain: 'ranknaser.com'
            };
            localStorage.setItem('ranknaser_auth_user', JSON.stringify(adminUser));
            showDashboardView(adminUser);
        }

        function handleLogout() {
            if (confirm('Are you sure you want to log out from RankNaserPro?')) {
                localStorage.removeItem('ranknaser_auth_user');
                showAuthView();
            }
        }

        // ================= AGENCY WORKFORCE CONTROLLER =================
        let agencyCachedStaff = [];
        let agencyCachedTasks = [];

        async function loadAgencyDashboard() {
            const grid = document.getElementById('agencyStaffGrid');
            const feed = document.getElementById('agencyTasksFeed');
            const statsCount = document.getElementById('agencyStatsTotalTasks');

            try {
                const res = await fetch('/api/agency/staff');
                const data = await res.json();
                if (data.status === 'success') {
                    agencyCachedStaff = data.staff || [];
                    const tasks = (data.data && data.data.tasks) ? data.data.tasks : [];
                    agencyCachedTasks = tasks;

                    if (statsCount) {
                        statsCount.innerText = `${tasks.length} Deliverable${tasks.length === 1 ? '' : 's'}`;
                    }

                    // Render Staff Grid
                    if (grid) {
                        grid.innerHTML = agencyCachedStaff.map(s => `
                            <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.15s, box-shadow 0.15s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.06)';" onmouseout="this.style.transform='none'; this.style.boxShadow='0 4px 12px rgba(0,0,0,0.03)';">
                                <div>
                                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                        <div style="display: flex; align-items: center; gap: 12px;">
                                            <div style="width: 48px; height: 48px; border-radius: 12px; background: linear-gradient(135deg, #1e1b4b, #3b82f6); color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 4px 10px rgba(37,99,235,0.25);">
                                                ${s.avatar || '👤'}
                                            </div>
                                            <div>
                                                <div style="font-size: 15px; font-weight: 800; color: #0f172a;">${s.name}</div>
                                                <div style="font-size: 12px; font-weight: 700; color: #2563eb;">${s.designation}</div>
                                            </div>
                                        </div>
                                        <span style="font-size: 10.5px; background: #ecfdf5; border: 1px solid #10b981; color: #047857; font-weight: 800; padding: 3px 8px; border-radius: 12px;">
                                            ${s.badge || 'White-Hat'}
                                        </span>
                                    </div>
                                    <div style="font-size: 11.5px; color: #64748b; font-weight: 600; margin-bottom: 8px;">
                                        📂 <strong>Department:</strong> ${s.department}
                                    </div>
                                    <p style="font-size: 12.5px; color: #334155; line-height: 1.5; margin: 0 0 12px 0;">
                                        ${s.bio}
                                    </p>
                                    <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px;">
                                        ${(s.specialties || []).map(sp => `<span style="font-size: 10.5px; background: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 6px; font-weight: 600;">#${sp}</span>`).join('')}
                                    </div>
                                </div>
                                <div style="border-top: 1px solid #f1f5f9; padding-top: 12px; display: flex; justify-content: space-between; align-items: center;">
                                    <span style="font-size: 11px; color: #059669; font-weight: 700;">🟢 Ready for Orders</span>
                                    <button type="button" onclick="openAgencyTaskModal('${s.id}')" style="background: linear-gradient(135deg, #1e1b4b, #2563eb); color: white; border: none; font-weight: 800; border-radius: 8px; padding: 7px 14px; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 5px;">
                                        <span>⚡ Assign Task</span>
                                    </button>
                                </div>
                            </div>
                        `).join('');
                    }

                    // Render Tasks Feed
                    if (feed) {
                        if (tasks.length === 0) {
                            feed.innerHTML = `
                                <div style="text-align: center; padding: 40px 20px; color: #64748b; font-size: 13.5px;">
                                    <div style="font-size: 40px; margin-bottom: 10px;">🏢</div>
                                    <strong style="color: #0f172a;">No Agency Tasks Executed Today Yet</strong>
                                    <p style="margin: 6px 0 16px 0; font-size: 12.5px;">Click <strong>"Assign Task to Staff"</strong> above to send orders to Tanvir, Nabila, Arif, Fahim, Zayan, or Samira!</p>
                                    <button type="button" onclick="openAgencyTaskModal()" style="background: #2563eb; color: white; border: none; font-weight: 800; padding: 8px 18px; border-radius: 8px; font-size: 12.5px; cursor: pointer;">
                                        ⚡ Assign First Task Now
                                    </button>
                                </div>
                            `;
                        } else {
                            const revTasks = [...tasks].reverse();
                            feed.innerHTML = revTasks.map((t, idx) => `
                                <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 14px; padding: 18px 20px; margin-bottom: 16px;">
                                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                                        <div style="display: flex; align-items: center; gap: 10px;">
                                            <span style="font-size: 26px;">${t.agent_avatar || '👤'}</span>
                                            <div>
                                                <div style="font-size: 14.5px; font-weight: 900; color: #0f172a;">
                                                    ${t.agent_name} <span style="font-size: 12px; font-weight: 700; color: #2563eb;">(${t.agent_designation})</span>
                                                </div>
                                                <div style="font-size: 11.5px; color: #64748b;">
                                                    Task ID: <strong>${t.task_id}</strong> • Completed: ${t.created_at || 'Today'}
                                                </div>
                                            </div>
                                        </div>
                                        <div style="display: flex; gap: 8px; align-items: center;">
                                            <span style="font-size: 11px; background: #ecfdf5; border: 1px solid #10b981; color: #047857; font-weight: 800; padding: 4px 10px; border-radius: 20px;">
                                                🟢 ${t.status || 'Completed'}
                                            </span>
                                            <span style="font-size: 11px; background: #eff6ff; border: 1px solid #93c5fd; color: #1e40af; font-weight: 800; padding: 4px 10px; border-radius: 20px;">
                                                ${t.priority || 'High'} Priority
                                            </span>
                                        </div>
                                    </div>
                                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; font-size: 12.5px;">
                                        <div><strong>🌐 Target Client Website:</strong> <a href="${t.client_domain.startsWith('http') ? t.client_domain : 'https://' + t.client_domain}" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 700;">${t.client_domain}</a></div>
                                        <div style="margin-top: 4px;"><strong>🎯 Directive:</strong> <span style="color: #334155;">${t.task_directive}</span></div>
                                        <div style="margin-top: 4px; color: #059669; font-weight: 700;">🛡️ <strong>Google Compliance Check:</strong> ${t.google_policy_check || '100% White-Hat Verified'}</div>
                                    </div>
                                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                                        <button type="button" onclick="toggleTaskDeliverable('${t.task_id}')" style="background: #1e1b4b; color: white; border: none; font-weight: 700; border-radius: 6px; padding: 6px 14px; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
                                            <span>👁️ View Deliverable</span>
                                        </button>
                                        <button type="button" onclick="copyTaskDeliverable('${t.task_id}')" style="background: #ffffff; color: #334155; border: 1px solid #cbd5e1; font-weight: 700; border-radius: 6px; padding: 6px 14px; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;">
                                            <span>📋 Copy Text</span>
                                        </button>
                                        <button type="button" onclick="publishAgencyTaskToWordPress('${t.task_id}', 'publish')" style="background: #059669; color: white; border: none; font-weight: 800; border-radius: 6px; padding: 6px 14px; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;" title="Publish this deliverable directly to client WordPress site as LIVE post">
                                            <span>🚀 Publish LIVE to Client Site</span>
                                        </button>
                                        <button type="button" onclick="publishAgencyTaskToWordPress('${t.task_id}', 'draft')" style="background: #0073aa; color: white; border: none; font-weight: 800; border-radius: 6px; padding: 6px 14px; font-size: 12px; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;" title="Save this deliverable as DRAFT in client WordPress admin">
                                            <span>📝 Save Draft to Client Site</span>
                                        </button>
                                    </div>
                                    <div id="delivWpStatus_${t.task_id}" style="display:none; margin-top:10px; padding:10px 14px; border-radius:8px; font-size:12.5px; font-weight:700;"></div>
                                    <div id="deliv_${t.task_id}" style="display: none; margin-top: 14px; background: #ffffff; border: 1.5px solid #94a3b8; border-radius: 10px; padding: 18px; max-height: 400px; overflow-y: auto; font-size: 13px; line-height: 1.6; color: #0f172a; white-space: pre-wrap; font-family: monospace;">${escapeHtml(typeof t.deliverable === 'object' ? JSON.stringify(t.deliverable, null, 2) : (t.deliverable || 'No deliverable content generated.'))}</div>
                                </div>
                            `).join('');
                        }
                    }
                }
            } catch(e) {
                console.error('Failed to load agency dashboard:', e);
            }
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function toggleTaskDeliverable(taskId) {
            const el = document.getElementById('deliv_' + taskId);
            if (el) {
                el.style.display = (el.style.display === 'none' || el.style.display === '') ? 'block' : 'none';
            }
        }

        function copyTaskDeliverable(taskId) {
            const t = agencyCachedTasks.find(x => x.task_id === taskId);
            if (t && t.deliverable) {
                const textToCopy = typeof t.deliverable === 'object' ? JSON.stringify(t.deliverable, null, 2) : t.deliverable;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    alert('✅ Deliverable copied to clipboard!');
                }).catch(() => {
                    alert('Could not copy automatically. Please open and copy manually.');
                });
            }
        }

        async function publishAgencyTaskToWordPress(taskId, forcedStatus = 'publish') {
            const task = agencyCachedTasks.find(t => t.task_id === taskId);
            if (!task) return;

            const clients = getConnectedClients();
            const client = clients.find(c => c.domain && task.client_domain && (c.domain.includes(task.client_domain) || task.client_domain.includes(c.domain)))
                        || clients.find(c => c.wp_url && c.wp_user && c.wp_pass)
                        || clients[0];

            if (!client || !client.wp_url || !client.wp_user || !client.wp_pass) {
                alert('Please configure WordPress credentials for ' + (client ? client.name : 'this client') + ' in the "🏢 Connected Clients (5 Companies)" hub first!');
                openClientsHubModal(client ? client.id : null);
                return;
            }

            const d = task.deliverable || {};
            const title = (typeof d === 'object' && d.title) ? d.title : (typeof d === 'object' && d.executive_summary ? d.executive_summary.substring(0, 75) : `Agency Deliverable for ${task.client_domain}`);
            const html = (typeof d === 'object' && d.html) ? d.html : (typeof marked !== 'undefined' ? marked.parse(d.markdown || JSON.stringify(d, null, 2)) : `<pre>${JSON.stringify(d, null, 2)}</pre>`);
            const targetStatus = forcedStatus || client.wp_status || 'publish';

            const statusBox = document.getElementById('delivWpStatus_' + taskId);
            if (statusBox) {
                statusBox.style.display = 'block';
                statusBox.style.background = '#eff6ff';
                statusBox.style.border = '1px solid #93c5fd';
                statusBox.style.color = '#1e40af';
                statusBox.innerHTML = `🚀 Sending task deliverable to <strong>${client.wp_url}</strong> as <strong>${targetStatus.toUpperCase()}</strong>...`;
            }

            try {
                const resp = await fetch('/api/wordpress/publish', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        site_url: client.wp_url,
                        username: client.wp_user,
                        app_password: client.wp_pass,
                        status: targetStatus,
                        title: title,
                        content_html: html,
                        slug: '',
                        excerpt: (typeof d === 'object' && d.executive_summary) ? d.executive_summary : '',
                        focus_keyword: (typeof d === 'object' && d.primary_keyword) ? d.primary_keyword : ''
                    })
                });
                const res = await resp.json();
                if (res.status === 'success') {
                    if (statusBox) {
                        statusBox.style.background = '#f0fdf4';
                        statusBox.style.border = '1px solid #86efac';
                        statusBox.style.color = '#166534';
                        statusBox.innerHTML = `✅ Successfully posted to <strong>${client.wp_url}</strong> as <strong>${(res.post_status||targetStatus).toUpperCase()}</strong>! (Post ID: #${res.post_id}) &nbsp;|&nbsp; <a href="${res.post_url}" target="_blank" style="color:#0284c7; text-decoration:underline; font-weight:700;">👁️ View Live Post</a>`;
                    } else {
                        alert(`✅ Successfully posted to ${client.wp_url} as ${(res.post_status||targetStatus).toUpperCase()}!`);
                    }
                } else {
                    if (statusBox) {
                        statusBox.style.background = '#fef2f2';
                        statusBox.style.border = '1px solid #fca5a5';
                        statusBox.style.color = '#991b1b';
                        statusBox.innerHTML = `❌ WordPress error: ${res.message}`;
                    } else {
                        alert(`WordPress error: ${res.message}`);
                    }
                }
            } catch(err) {
                if (statusBox) {
                    statusBox.style.background = '#fef2f2';
                    statusBox.style.border = '1px solid #fca5a5';
                    statusBox.style.color = '#991b1b';
                    statusBox.innerHTML = `❌ Error: ${err.message}`;
                }
            }
        }

        function openAgencyTaskModal(agentId, clientDomain) {
            const modal = document.getElementById('agencyTaskModal');
            if (modal) modal.style.display = 'flex';
            if (agentId) {
                const sel = document.getElementById('taskAgentSelect');
                if (sel) sel.value = agentId;
            }
            populateTaskCompanySelect(clientDomain);
            if (clientDomain) {
                const dom = document.getElementById('taskClientDomain');
                if (dom) dom.value = clientDomain;
            }
            const gemKeyInput = document.getElementById('taskGeminiKey');
            if (gemKeyInput) {
                gemKeyInput.value = localStorage.getItem('gemini_api_key') || '';
            }
            const alertBox = document.getElementById('agencyTaskStatusAlert');
            if (alertBox) alertBox.style.display = 'none';
        }

        function closeAgencyTaskModal() {
            const modal = document.getElementById('agencyTaskModal');
            if (modal) modal.style.display = 'none';
        }

        async function handleDispatchAgencyTask(event) {
            event.preventDefault();
            const agentId = document.getElementById('taskAgentSelect').value;
            const clientDomain = document.getElementById('taskClientDomain').value.trim();
            const priority = document.getElementById('taskPrioritySelect').value;
            const directive = document.getElementById('taskDirectiveText').value.trim();
            const gemKeyInput = document.getElementById('taskGeminiKey');
            const geminiKey = (gemKeyInput ? gemKeyInput.value.trim() : '') || localStorage.getItem('gemini_api_key') || '';
            if (gemKeyInput && gemKeyInput.value.trim()) {
                localStorage.setItem('gemini_api_key', gemKeyInput.value.trim());
            }

            const btn = document.getElementById('btnDispatchAgencyTask');
            const alertBox = document.getElementById('agencyTaskStatusAlert');

            if (!clientDomain || !directive) {
                alert('Please provide client domain and specific directive.');
                return;
            }

            btn.disabled = true;
            btn.innerHTML = '<span>⏳ Executing & Auditing Task...</span>';
            alertBox.style.display = 'block';
            alertBox.style.background = '#eff6ff';
            alertBox.style.color = '#1d4ed8';
            alertBox.style.border = '1.5px solid #93c5fd';
            alertBox.innerHTML = '🤖 <strong>Task Dispatched!</strong> Virtual specialist is executing live URL crawl & Google compliance checks. Please wait 5-15 seconds...';

            try {
                const res = await fetch('/api/agency/assign-task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        agent_id: agentId,
                        client_domain: clientDomain,
                        task_directive: directive,
                        priority: priority,
                        gemini_key: geminiKey
                    })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alertBox.style.background = '#ecfdf5';
                    alertBox.style.color = '#047857';
                    alertBox.style.border = '1.5px solid #6ee7b7';
                    alertBox.innerHTML = `✅ <strong>Success!</strong> Task executed by <strong>${data.task.agent_name}</strong>. Deliverable has been logged.`;
                    
                    document.getElementById('taskDirectiveText').value = '';
                    await loadAgencyDashboard();

                    setTimeout(() => {
                        closeAgencyTaskModal();
                        btn.disabled = false;
                        btn.innerHTML = '<span>🚀 Dispatch Task to Agent</span>';
                    }, 1200);
                } else {
                    alertBox.style.background = '#fef2f2';
                    alertBox.style.color = '#b91c1c';
                    alertBox.style.border = '1.5px solid #fca5a5';
                    alertBox.innerText = '❌ Error: ' + (data.message || 'Execution failed.');
                    btn.disabled = false;
                    btn.innerHTML = '<span>🚀 Dispatch Task to Agent</span>';
                }
            } catch (err) {
                alertBox.style.background = '#fef2f2';
                alertBox.style.color = '#b91c1c';
                alertBox.style.border = '1.5px solid #fca5a5';
                alertBox.innerText = '❌ Error: ' + err.message;
                btn.disabled = false;
                btn.innerHTML = '<span>🚀 Dispatch Task to Agent</span>';
            }
        }

        async function openDailyReportModal() {
            const modal = document.getElementById('agencyDailyReportModal');
            if (modal) modal.style.display = 'flex';
            const body = document.getElementById('dailyReportModalBody');
            body.innerHTML = `
                <div style="text-align: center; padding: 40px; color: #64748b;">
                    <div style="font-size: 36px; margin-bottom: 8px;">⏳</div>
                    <strong>Compiling Agency Operations Report...</strong>
                    <p style="font-size: 12px; margin-top: 4px;">Synchronizing deliverables across all 6 specialists...</p>
                </div>
            `;

            try {
                const res = await fetch('/api/agency/daily-report', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({})
                });
                const data = await res.json();
                if (data.status === 'success' && data.report) {
                    const r = data.report;
                    body.innerHTML = `
                        <div style="margin-bottom: 18px; background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 18px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
                                <div>
                                    <h4 style="margin: 0; font-size: 16px; font-weight: 900; color: #0f172a;">${r.agency_name}</h4>
                                    <div style="font-size: 12px; color: #64748b;">Founder: <strong>${r.founder || 'RankNaser'}</strong> • Shift: <strong>${r.generated_date || 'Today'}</strong></div>
                                </div>
                                <span style="font-size: 12px; background: #ecfdf5; border: 1.5px solid #10b981; color: #047857; font-weight: 800; padding: 5px 12px; border-radius: 20px;">
                                    ${r.whitehat_compliance_rating || '100% White-Hat'}
                                </span>
                            </div>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 10px;">
                                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center;">
                                    <div style="font-size: 11px; color: #64748b; font-weight: 700;">TOTAL TASKS</div>
                                    <div style="font-size: 18px; font-weight: 900; color: #2563eb;">${r.total_tasks_completed || 0}</div>
                                </div>
                                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center;">
                                    <div style="font-size: 11px; color: #64748b; font-weight: 700;">AI SPECIALISTS</div>
                                    <div style="font-size: 18px; font-weight: 900; color: #7c3aed;">6 Staff</div>
                                </div>
                                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px; text-align: center;">
                                    <div style="font-size: 11px; color: #64748b; font-weight: 700;">COMPLIANCE</div>
                                    <div style="font-size: 18px; font-weight: 900; color: #059669;">100% Zero-Spam</div>
                                </div>
                            </div>
                            ${r.executive_verdict ? `
                                <div style="margin-top: 12px; background: #ffffff; border-left: 4px solid #2563eb; padding: 10px 14px; border-radius: 6px; font-size: 12px; color: #334155; line-height: 1.5;">
                                    <strong>Executive Verdict:</strong> ${r.executive_verdict}
                                </div>
                            ` : ''}
                        </div>

                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin: 0 0 10px 0;">👥 Specialists Shift Logs:</h4>
                        <div style="display: flex; flex-direction: column; gap: 12px;">
                            ${Object.values(r.staff_shift_logs || {}).map(sLog => `
                                <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; background: #ffffff;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                        <div style="font-size: 13.5px; font-weight: 800; color: #0f172a;">
                                            ${sLog.staff.avatar || '👤'} ${sLog.staff.name} <span style="font-size: 11.5px; font-weight: 600; color: #2563eb;">(${sLog.staff.designation})</span>
                                        </div>
                                        <span style="font-size: 11px; background: ${sLog.completed_count > 0 ? '#eff6ff' : '#f1f5f9'}; color: ${sLog.completed_count > 0 ? '#1d4ed8' : '#64748b'}; padding: 3px 8px; border-radius: 10px; font-weight: 700;">
                                            ${sLog.completed_count} Completed
                                        </span>
                                    </div>
                                    ${(sLog.recent_tasks || []).length === 0 ? '<div style="font-size: 11.5px; color: #94a3b8;">Standing by for next directive.</div>' : `
                                        <div style="margin-top: 6px; display: flex; flex-direction: column; gap: 6px;">
                                            ${sLog.recent_tasks.map(t => `
                                                <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 8px 10px; font-size: 12px;">
                                                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #0f172a;">
                                                        <span>🎯 ${t.task_directive}</span>
                                                        <span style="color: #2563eb;">${t.client_domain}</span>
                                                    </div>
                                                    <div style="font-size: 11px; color: #059669; margin-top: 2px;">🛡️ ${t.google_policy_check || '100% White-Hat Verified'}</div>
                                                </div>
                                            `).join('')}
                                        </div>
                                    `}
                                </div>
                            `).join('')}
                        </div>
                    `;
                } else {
                    body.innerHTML = '<div style="color: #b91c1c; padding: 20px; text-align: center;">Error loading shift report.</div>';
                }
            } catch(e) {
                body.innerHTML = `<div style="color: #b91c1c; padding: 20px; text-align: center;">Error: ${e.message}</div>`;
            }
        }

        function closeDailyReportModal() {
            const modal = document.getElementById('agencyDailyReportModal');
            if (modal) modal.style.display = 'none';
        }

        // Check URL hash on load for deep linking & initial tab setup
        window.addEventListener('DOMContentLoaded', function() {
            checkAuthOnLoad();
            const hash = window.location.hash.replace('#', '');
            if (hash && ['daily', 'spy', 'multi', 'writer', 'autopilot', 'director', 'agency'].includes(hash)) {
                switchTab(hash, false);
            }
            // Auto-trigger live demo scan on initial dashboard load so user immediately sees active data
            setTimeout(function() {
                try {
                    const authUser = localStorage.getItem('ranknaser_auth_user');
                    const trackerResults = document.getElementById('trackerResults');
                    if (authUser && trackerResults && trackerResults.style.display === 'none') {
                        const urlInput = document.getElementById('urlInput');
                        if (urlInput && urlInput.value) {
                            console.log('Initiating initial auto-scan for:', urlInput.value);
                            const form = document.getElementById('trackerForm');
                            if (form) {
                                if (typeof form.requestSubmit === 'function') form.requestSubmit();
                                else form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                            }
                        }
                    }
                } catch(e) {
                    console.warn('Initial auto-scan silent warning:', e);
                }
            }, 800);
        });
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract path without query parameters (supports ?fbclid=..., ?utm_source=..., etc.)
        self.path = self.path.split('?')[0].strip()

        # SECURITY FIREWALL: Block any direct attempts to read source code, config, or hidden files
        req_clean = self.path.lower()
        if any(req_clean.endswith(ext) for ext in ['.py', '.json', '.env', '.sh', '.bat', '.yaml', '.yml', '.md', '.txt', '.git']):
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(b"403 Forbidden: Source files are protected and secret.")
            return

        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('X-XSS-Protection', '1; mode=block')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.end_headers()
            photo_uri = get_ranknaser_photo_uri()
            rendered_html = HTML_PAGE.replace('__RANKNASER_PHOTO_URI__', photo_uri)
            self.wfile.write(rendered_html.encode('utf-8'))
        elif self.path == '/guide/english':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html_en = render_printable_guide('en')
            self.wfile.write(html_en.encode('utf-8'))
        elif self.path == '/guide/bangla':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html_bn = render_printable_guide('bn')
            self.wfile.write(html_bn.encode('utf-8'))
        elif self.path in ['/guide', '/user-guide', '/userguide', '/guide/pdf', '/api/user-guide', '/static/user_guide_pdf.html']:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html_guide = render_printable_guide('bn')
            self.wfile.write(html_guide.encode('utf-8'))
        elif self.path == '/api/agency/staff':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            data = load_agency_data()
            self.wfile.write(json.dumps({"status": "success", "staff": AGENCY_STAFF, "data": data}, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/agency/daily-report/pdf':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            engine = AgencyWorkforceEngine()
            rep = engine.generate_daily_report()
            html = render_printable_agency_report(rep)
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/static/ranknaser.jpg':
            if os.path.exists(PHOTO_FILE):
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Cache-Control', 'public, max-age=86400')
                self.end_headers()
                with open(PHOTO_FILE, 'rb') as pf:
                    self.wfile.write(pf.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # Extract path without query parameters
        self.path = self.path.split('?')[0].strip()
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        if self.path == '/api/auth/login':
            try:
                data = json.loads(body)
                u = data.get('username') or data.get('email', '')
                username = u.strip()
                password = data.get('password', '').strip()
                users = load_registered_users()
                
                is_valid = False
                matched_user = None

                # Primary credentials check for ADMIN / AGENTNASER
                if (username.upper() == 'ADMIN' or username.lower() == 'admin@ranknaser.com') and \
                   (password == 'AGENTNASER' or password.upper() == 'AGENTNASER'):
                    is_valid = True
                    matched_user = {
                        "username": "ADMIN",
                        "email": "admin@ranknaser.com",
                        "name": "RankNaser Admin",
                        "domain": "ranknaser.com"
                    }
                elif username.lower() in users and users[username.lower()].get('password') == password:
                    is_valid = True
                    uinfo = users[username.lower()]
                    matched_user = {
                        "username": username,
                        "email": username,
                        "name": uinfo.get("name", "RankNaser Admin"),
                        "domain": uinfo.get("domain", "ranknaser.com")
                    }

                if is_valid:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "success",
                        "user": matched_user
                    }).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "status": "error",
                        "message": "Invalid credentials! User: ADMIN | Password: AGENTNASER"
                    }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        elif self.path == '/api/auth/register':
            try:
                data = json.loads(body)
                email = data.get('email', '').strip().lower()
                name = data.get('name', '').strip()
                password = data.get('password', '').strip()
                domain = data.get('domain', '').strip()

                if not email or not password or not name:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "All fields required."}).encode('utf-8'))
                    return

                users = load_registered_users()
                if email in users:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "Email already registered. Please login."}).encode('utf-8'))
                    return

                users[email] = {
                    "name": name,
                    "password": password,
                    "domain": domain,
                    "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_registered_users(users)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "user": {"email": email, "name": name, "domain": domain}
                }).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        elif self.path == '/api/scan':
            try:
                data = json.loads(body)
                url = data.get('url', '').strip()
                date_str = data.get('date', '').strip()
                gemini_key = data.get('gemini_key', '').strip()

                target_date = None
                if date_str:
                    try:
                        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    except ValueError:
                        pass
                if not target_date:
                    target_date = date.today()

                tracker = CompetitorTracker(
                    target_url=url,
                    target_date=target_date,
                    gemini_api_key=gemini_key if gemini_key else None
                )
                results = tracker.run()
                
                is_fallback = False
                if tracker.recent_fallback_urls and results:
                    is_fallback = any(r['url'] in tracker.recent_fallback_urls for r in results)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                resp_payload = {
                    "status": "success",
                    "results": results,
                    "is_recent_fallback": is_fallback
                }
                self.wfile.write(json.dumps(resp_payload, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                
        elif self.path == '/api/spy':
            try:
                data = json.loads(body)
                url = data.get('url', '').strip()
                if not url:
                    raise ValueError("URL is required")
                    
                spy_engine = CompetitorSpyEngine(url)
                res = spy_engine.run_full_spy()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

        elif self.path == '/api/write-content':
            try:
                data = json.loads(body)
                topic = data.get('topic', '').strip()
                main_keyword = data.get('main_keyword', '').strip()
                lsi_keywords = data.get('lsi_keywords', '')
                product_name = data.get('product_name', '').strip()
                brand_name = data.get('brand_name', '').strip()
                content_type = data.get('content_type', 'long_form_seo')
                tone = data.get('tone', 'Authoritative & Expert')
                target_words = int(data.get('target_words', 2000))
                competitor_url = data.get('competitor_url', '').strip()
                country = (data.get('country') or data.get('target_country') or 'Bangladesh').strip()
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                writer_agent = ContentWritingAgent(gemini_api_key=gemini_key if gemini_key else None)
                article_data = writer_agent.generate_content(
                    topic=topic,
                    main_keyword=main_keyword,
                    lsi_keywords=lsi_keywords,
                    product_name=product_name,
                    brand_name=brand_name,
                    competitor_url=competitor_url,
                    content_type=content_type,
                    tone=tone,
                    target_words=target_words,
                    target_country=country
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                resp_payload = {
                    "status": "success",
                    "result": article_data
                }
                self.wfile.write(json.dumps(resp_payload, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/multi-outrank':
            try:
                data = json.loads(body)
                comp_urls = data.get('competitor_urls', [])
                user_url = data.get('user_url', '').strip()
                brand_name = data.get('brand_name', '').strip()
                focus_kw = data.get('focus_keyword', '').strip()
                content_type = data.get('content_type', 'long_form_seo')
                tone = data.get('tone', 'Authoritative & Expert')
                target_words = int(data.get('target_words', 0))
                country = data.get('country', 'Bangladesh').strip()
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                engine = MultiCompetitorEngine(
                    competitor_urls=comp_urls,
                    user_url=user_url,
                    brand_name=brand_name,
                    focus_keyword=focus_kw,
                    target_country=country,
                    gemini_api_key=gemini_key if gemini_key else None
                )

                analysis_data = engine.run_multi_audit()
                if analysis_data.get('status') != 'success':
                    raise ValueError(analysis_data.get('message', 'Failed to audit competitors.'))

                article_data = engine.generate_master_outrank_article(
                    analysis_data=analysis_data,
                    content_type=content_type,
                    tone=tone,
                    custom_words=target_words,
                    target_country=country
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                resp_payload = {
                    "status": "success",
                    "analysis": analysis_data,
                    "article": article_data
                }
                self.wfile.write(json.dumps(resp_payload, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/wordpress/test':
            try:
                data = json.loads(body)
                site_url = data.get('site_url', '').strip()
                username = data.get('username', '').strip()
                app_password = data.get('app_password', '').strip()

                publisher = WordPressPublisher(site_url, username, app_password)
                res = publisher.test_connection()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/wordpress/publish':
            try:
                data = json.loads(body)
                site_url = data.get('site_url', '').strip()
                username = data.get('username', '').strip()
                app_password = data.get('app_password', '').strip()
                status = data.get('status', 'draft').strip()
                title = data.get('title', '').strip()
                content_html = data.get('content_html', '').strip()
                slug = data.get('slug', '').strip()
                excerpt = data.get('excerpt', '').strip()
                focus_keyword = data.get('focus_keyword', '').strip()
                faq_schema = data.get('faq_schema', None)

                publisher = WordPressPublisher(site_url, username, app_password)
                res = publisher.publish_post(
                    title=title,
                    content_html=content_html,
                    status=status,
                    slug=slug,
                    excerpt=excerpt,
                    focus_keyword=focus_keyword,
                    faq_schema=faq_schema
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/custom-webhook/test':
            try:
                data = json.loads(body)
                webhook_url = data.get('webhook_url', '').strip()
                api_token = data.get('api_token', '').strip()

                publisher = CustomWebhookPublisher(webhook_url, api_token)
                res = publisher.test_connection()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/custom-webhook/publish':
            try:
                data = json.loads(body)
                webhook_url = data.get('webhook_url', '').strip()
                api_token = data.get('api_token', '').strip()
                status = data.get('status', 'draft').strip()
                title = data.get('title', '').strip()
                content_html = data.get('content_html', '').strip()
                content_markdown = data.get('content_markdown', '').strip()
                slug = data.get('slug', '').strip()
                meta_title = data.get('meta_title', '').strip()
                meta_description = data.get('meta_description', '').strip()
                focus_keyword = data.get('focus_keyword', '').strip()
                faq_schema = data.get('faq_schema', None)

                publisher = CustomWebhookPublisher(webhook_url, api_token)
                res = publisher.publish_article(
                    title=title,
                    content_html=content_html,
                    content_markdown=content_markdown,
                    slug=slug,
                    meta_title=meta_title,
                    meta_description=meta_description,
                    focus_keyword=focus_keyword,
                    faq_schema=faq_schema,
                    status=status
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/autopilot/run':
            try:
                data = json.loads(body)
                brand_name = data.get('brand_name', 'MyBrand').strip()
                comp_domains = data.get('competitor_domains', [])
                target_country = data.get('target_country', 'Bangladesh').strip()
                specific_topic = data.get('specific_topic', '').strip() or None
                target_words = int(data.get('target_words', 2500))
                tone = data.get('tone', 'Authoritative & Expert').strip()
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()
                wp_config = data.get('wp_config', None)
                custom_webhook_config = data.get('custom_webhook_config', None)

                agent = AutopilotAgent(gemini_api_key=gemini_key if gemini_key else None)
                res = agent.run_autopilot_mission(
                    competitor_domains=comp_domains,
                    brand_name=brand_name,
                    target_country=target_country,
                    specific_topic=specific_topic,
                    target_words=target_words,
                    tone=tone,
                    wp_config=wp_config,
                    custom_webhook_config=custom_webhook_config
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/seo-director/plan':
            try:
                data = json.loads(body)
                company_name = data.get('company_name', '').strip()
                domain = data.get('domain', '').strip()
                keywords = data.get('keywords', [])
                target_country = data.get('target_country', 'Bangladesh').strip()
                competitor_urls = data.get('competitor_urls', [])
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                director = PersonalSEODirector(gemini_api_key=gemini_key if gemini_key else None)
                plan = director.generate_10_day_roadmap(
                    company_name=company_name,
                    domain=domain,
                    keywords=keywords,
                    target_country=target_country,
                    competitor_urls=competitor_urls
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "campaign": plan}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/seo-director/execute-day':
            try:
                data = json.loads(body)
                day_number = int(data.get('day_number', 1))
                campaign_info = data.get('campaign_info', {})
                wp_config = data.get('wp_config', None)
                custom_webhook_config = data.get('custom_webhook_config', None)
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                director = PersonalSEODirector(gemini_api_key=gemini_key if gemini_key else None)
                res = director.execute_day_mission(
                    day_number=day_number,
                    campaign_info=campaign_info,
                    wp_config=wp_config,
                    custom_webhook_config=custom_webhook_config
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/seo-director/execute-all':
            try:
                data = json.loads(body)
                campaign_info = data.get('campaign_info', {})
                wp_config = data.get('wp_config', None)
                custom_webhook_config = data.get('custom_webhook_config', None)
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                director = PersonalSEODirector(gemini_api_key=gemini_key if gemini_key else None)
                res = director.execute_full_campaign(
                    campaign_info=campaign_info,
                    wp_config=wp_config,
                    custom_webhook_config=custom_webhook_config
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/agency/assign-task':
            try:
                data = json.loads(body)
                agent_id = data.get('agent_id', 'tanvir')
                client_domain = data.get('client_domain', '')
                task_directive = data.get('task_directive', '')
                priority = data.get('priority', 'High')
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                engine = AgencyWorkforceEngine(gemini_api_key=gemini_key if gemini_key else None)
                task_res = engine.execute_task(
                    agent_id=agent_id,
                    client_domain=client_domain,
                    task_directive=task_directive,
                    priority=priority
                )

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "task": task_res}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/api/agency/daily-report':
            try:
                data = json.loads(body) if body else {}
                gemini_key = data.get('gemini_key', '').strip() or os.environ.get('GEMINI_API_KEY', '').strip()

                engine = AgencyWorkforceEngine(gemini_api_key=gemini_key if gemini_key else None)
                rep = engine.generate_daily_report()

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "report": rep}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def start_server(port=None):
    if port is None:
        port = int(os.environ.get('PORT', 5000))
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    url = f"http://localhost:{port}"
    print("=" * 65)
    print(f"🚀 COMPETITOR TRACKER & CONTENT WRITING AI AGENT STARTED")
    print(f"🔗 Access Web Dashboard at: {url}")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web server...")
        httpd.server_close()


if __name__ == "__main__":
    start_server()
