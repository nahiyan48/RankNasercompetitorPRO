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


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RankNaserPro - Autonomous SEO Intelligence & Outranking Suite</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Hind+Siliguri:wght@400;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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
            display: inline-block;
            background: linear-gradient(135deg, #1d4ed8, #2563eb);
            color: white;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 5px 16px;
            border-radius: 20px;
            margin-bottom: 8px;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        }
        h1 {
            font-size: 30px;
            font-weight: 800;
            background: linear-gradient(90deg, #0f172a, #2563eb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        p.subtitle { color: var(--text-muted); font-size: 14px; }

        /* Tabs Navigation - 5 Symmetrical Equal Columns */
        .tabs-nav {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 11px;
            margin-bottom: 22px;
            border-bottom: 2px solid var(--border);
            padding-bottom: 14px;
            width: 100%;
        }
        .tab-btn {
            width: 100%;
            height: 48px;
            box-sizing: border-box;
            border: 1px solid var(--border);
            padding: 0 8px;
            border-radius: 10px;
            font-weight: 700;
            cursor: pointer;
            font-size: 13.5px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            gap: 6px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap;
            user-select: none;
        }
        .tab-btn:hover {
            transform: translateY(-1px);
        }
        @media (max-width: 1024px) {
            .tabs-nav {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }
        }
        @media (max-width: 640px) {
            .tabs-nav {
                grid-template-columns: 1fr;
            }
        }
        /* Unified Light Blue Theme for All Tab Buttons */
        .tab-btn,
        .tab-btn.daily,
        .tab-btn.spy,
        .tab-btn.multi,
        .tab-btn.writer,
        .tab-btn.autopilot {
            background: linear-gradient(135deg, #38bdf8, #0ea5e9);
            border: 1px solid #0284c7;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.28);
        }
        .tab-btn:hover,
        .tab-btn.daily:hover,
        .tab-btn.spy:hover,
        .tab-btn.multi:hover,
        .tab-btn.writer:hover,
        .tab-btn.autopilot:hover {
            background: linear-gradient(135deg, #0ea5e9, #0284c7);
            border-color: #0369a1;
            color: #ffffff;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.38);
        }
        .tab-btn.active,
        .tab-btn.active.daily,
        .tab-btn.active.spy,
        .tab-btn.active.multi,
        .tab-btn.active.writer,
        .tab-btn.active.autopilot {
            background: linear-gradient(135deg, #0284c7, #1d4ed8) !important;
            color: #ffffff !important;
            border-color: #0369a1 !important;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.45) !important;
            outline: 2px solid #bae6fd !important;
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
            border: 1.5px solid #38bdf8;
            color: #0f172a;
            padding: 11px 14px;
            width: 100%;
        }
        input[type="text"]:hover, input[type="date"]:hover, select:hover, textarea:hover {
            border-color: #0ea5e9;
            box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.15);
        }
        input:focus, select:focus, textarea:focus {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.25) !important;
        }
        button.btn-scan {
            background: var(--accent);
            color: white;
            border: none;
            padding: 12px 24px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
        }
        button.btn-scan:hover { background: var(--accent-hover); }
        button.btn-spy {
            background: var(--spy-accent);
            color: white;
            border: none;
            padding: 12px 24px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.25);
        }
        button.btn-spy:hover { background: var(--spy-hover); }
        button.btn-writer-submit {
            background: linear-gradient(135deg, #059669, #10b981);
            color: white;
            border: none;
            padding: 13px 28px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            border-radius: 10px;
            box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        button.btn-writer-submit:hover { background: #047857; }

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
    </style>
</head>
<body>
    <div class="container">
        <header style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px; flex-wrap: wrap; gap: 16px;">
            <div style="text-align: left;">
                <span class="logo-badge" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; font-weight: 800; letter-spacing: 1px; padding: 5px 16px; border-radius: 20px; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                    <span>🚀</span> RANKNASERPRO
                </span>
                <h1 style="font-size: 28px; font-weight: 800; margin: 4px 0 3px 0; color: #0f172a; letter-spacing: -0.5px;">RankNaserPro Intelligence Suite</h1>
                <p class="subtitle" style="margin: 0; color: #64748b; font-size: 13.5px;">Autonomous Competitor Spy, 5 vs 1 SERP Outranker & AI Content Publishing Machine</p>
            </div>
            <div style="display: flex; gap: 9px; align-items: center; flex-wrap: wrap;">
                <button type="button" id="roadmapBtn" onclick="openRoadmapModal()" style="background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; font-weight: 700; border-radius: 10px; padding: 10px 15px; cursor: pointer; display: flex; align-items: center; gap: 7px; box-shadow: 0 2px 8px rgba(2,132,199,0.3); font-size: 12.5px;">
                    <span>🗺️ 30-Day Content Roadmap</span>
                </button>
                <button type="button" id="wpSetupBtn" onclick="openWpModal()" style="background: #0073aa; color: white; border: none; font-weight: 700; border-radius: 10px; padding: 10px 15px; cursor: pointer; display: flex; align-items: center; gap: 7px; box-shadow: 0 2px 8px rgba(0,115,170,0.25); font-size: 12.5px;">
                    <span>🔌 WordPress</span>
                    <span id="wpStatusBadge" style="font-size: 10.5px; background: rgba(255,255,255,0.22); padding: 2px 6px; border-radius: 4px; font-weight: 600;">Not Configured</span>
                </button>
                <button type="button" id="customApiBtn" onclick="openCustomApiModal()" style="background: #0f172a; color: white; border: none; font-weight: 700; border-radius: 10px; padding: 10px 15px; cursor: pointer; display: flex; align-items: center; gap: 7px; box-shadow: 0 2px 8px rgba(15,23,42,0.25); font-size: 12.5px;">
                    <span>🌐 Custom Site API</span>
                    <span id="customApiBadge" style="font-size: 10.5px; background: rgba(255,255,255,0.22); padding: 2px 6px; border-radius: 4px; font-weight: 600;">Not Configured</span>
                </button>
            </div>
        </header>

        <!-- Tab Nav: 5 Equal Columns Grid -->
        <div class="tabs-nav">
            <button class="tab-btn active daily" id="tabDailyBtn" onclick="switchTab('daily')">
                <span>📅 1. Daily Keyword Tracker</span>
            </button>
            <button class="tab-btn spy" id="tabSpyBtn" onclick="switchTab('spy')">
                <span>🕵️‍♂️ 2. 360° Deep Spy</span>
            </button>
            <button class="tab-btn multi" id="tabMultiBtn" onclick="switchTab('multi')">
                <span>⚔️ 3. 5 vs 1 Master Outranker</span>
            </button>
            <button class="tab-btn writer" id="tabWriterBtn" onclick="switchTab('writer')">
                <span>✍️ 4. AI Content Studio</span>
            </button>
            <button class="tab-btn autopilot" id="tabAutopilotBtn" onclick="switchTab('autopilot')">
                <span>🤖 5. Autopilot AI Agent</span>
            </button>
        </div>

        <!-- TAB 1: Daily Tracker -->
        <div id="tabDaily">
            <div class="search-card">
                <form id="trackerForm">
                    <div class="form-grid-tracker">
                        <input type="text" id="urlInput" placeholder="Enter Competitor Domain OR Specific Page (e.g. https://www.startech.com.bd or https://theverge.com)" required>
                        <input type="date" id="dateInput">
                        <button type="submit" class="btn-scan" id="scanBtn">
                            <span>🔍 Scan Competitor Pages</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="spinner" id="trackerSpinner">
                <div class="loader"></div>
                <h3>Scanning competitor website & articles...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Extracting newly published articles, targeted products, and LSI entities in real-time...</p>
            </div>

            <div id="trackerResults" style="display: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px;">
                    <h2 id="trackerCount" style="font-size: 18px;">Analysis Results</h2>
                    <button class="btn-download" onclick="downloadCSV()">⬇️ Download CSV</button>
                </div>
                <div id="trackerCards"></div>
            </div>
        </div>

        <!-- TAB 2: Competitor Deep Spy -->
        <div id="tabSpy" style="display: none;">
            <div class="search-card" style="border-color: rgba(139, 92, 246, 0.4);">
                <form id="spyForm">
                    <div class="form-grid">
                        <input type="text" id="spyUrlInput" placeholder="Enter Competitor Specific Ranking URL (e.g. https://www.startech.com.bd/blog/...)" required>
                        <button type="submit" class="btn-spy" id="spyBtn">
                            <span>🕵️‍♂️ Reverse Engineer</span>
                        </button>
                    </div>
                </form>
            </div>

            <div class="spinner" id="spySpinner">
                <div class="loader" style="border-top-color: var(--spy-accent);"></div>
                <h3>Performing 360° Reverse Engineering...</h3>
                <p style="color: var(--text-muted); font-size: 13px;">Auditing Google ranking signals, heading hierarchy, structured schemas, and backlink footprints...</p>
            </div>

            <div id="spyResults" style="display: none;">
                <!-- Content injected dynamically -->
            </div>
        </div>

        <!-- TAB 3: 5 vs 1 Master Outranker -->
        <div id="tabMulti" style="display: none;">
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

                <form id="multiForm">
                    <!-- Competitor URLs Grid -->
                    <div style="margin-bottom: 16px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                            <label style="font-size: 13px; font-weight: 700; color: #0f172a;">
                                🥊 Competitor Ranking URLs (Up to 5 URLs):
                            </label>
                            <span style="font-size: 11px; color: var(--text-muted);">Audited in parallel (fast)</span>
                        </div>
                        <div style="display: grid; gap: 8px;">
                            <input type="text" id="multiComp1" placeholder="Competitor 1 URL (Required - e.g. https://competitor1.com/best-model)" required>
                            <input type="text" id="multiComp2" placeholder="Competitor 2 URL (Optional - e.g. https://competitor2.com/review)">
                            <input type="text" id="multiComp3" placeholder="Competitor 3 URL (Optional)">
                            <input type="text" id="multiComp4" placeholder="Competitor 4 URL (Optional)">
                            <input type="text" id="multiComp5" placeholder="Competitor 5 URL (Optional)">
                        </div>
                    </div>

                    <!-- User Website & Branding Grid -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 4px;">
                                🌐 Your Website / Target URL (Optional Benchmark):
                            </label>
                            <input type="text" id="multiUserUrl" placeholder="e.g. https://mysite.com/page (Agent will benchmark against the 5)">
                        </div>
                        <div>
                            <label style="font-size: 12px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 4px;">
                                🏷️ Your Brand / Company / Website Name:
                            </label>
                            <input type="text" id="multiBrandName" placeholder="e.g. RankNaserPro / MyBrand" required>
                        </div>
                    </div>

                    <!-- Keywords & Preferences Grid -->
                    <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-bottom: 16px;">
                        <div class="form-group">
                            <label>Target Focus Keyword (Optional)</label>
                            <input type="text" id="multiKeyword" placeholder="Auto-extracted from 5 competitors if blank">
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
                                🚀 Automatically Post to WordPress Site as Draft upon generation
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

                    <button type="submit" class="btn-multi-submit" id="multiSubmitBtn" style="width: 100%; padding: 14px; font-size: 15px; font-weight: 800; background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; border: none; border-radius: 10px; cursor: pointer; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.25);">
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
            <div class="search-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <div style="margin-bottom: 16px;">
                    <h3 style="font-size: 18px; color: #065f46; display: flex; align-items: center; gap: 8px;">
                        <span>✍️</span> Autonomous Content Writing Studio
                    </h3>
                    <p style="font-size: 13px; color: var(--text-muted);">
                        Transform competitor keyword clusters into comprehensive, human-grade, Google-outranking articles.
                    </p>
                </div>

                <form id="writerForm">
                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Target Topic / Article Working Title</label>
                            <input type="text" id="wTopic" placeholder="e.g. Best Phones Under 40000 in Bangladesh (2026 Ultimate Guide)" required>
                        </div>
                        <div class="form-group">
                            <label>Primary Focus Keyword</label>
                            <input type="text" id="wKeyword" placeholder="e.g. Best Phones Under 40000" required>
                        </div>
                    </div>

                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Semantic LSI Keywords Cluster (comma separated)</label>
                            <input type="text" id="wLsi" placeholder="e.g. AMOLED display, 5G phone price, battery life, camera review">
                        </div>
                        <div class="form-group">
                            <label>Target Product / Entity Name</label>
                            <input type="text" id="wProduct" placeholder="e.g. Smartphones Under 40000">
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
                                <option value="long_form_seo">📖 Long-Form SEO Guide (1,500-3,500w)</option>
                                <option value="product_review">⭐ In-Depth Product Review & Rating</option>
                                <option value="comparison_article">⚔️ Head-to-Head Comparison (A vs B)</option>
                                <option value="viral_social_post">🚀 Viral Social Media / Facebook Post</option>
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
                            <input type="text" id="wBrandName" placeholder="e.g. RankNaserPro / mywebsite.com (Woven naturally into recommendations & CTA)">
                        </div>
                        <div class="form-group">
                            <label>Competitor URL to Outrank (Optional)</label>
                            <input type="text" id="wCompUrl" placeholder="e.g. https://www.startech.com.bd/blog/best-phones-under-40000-in-bangladesh">
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
                                🚀 Automatically Post to WordPress Site as Draft upon generation
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
                        <button type="submit" class="btn-writer-submit" id="wSubmitBtn">
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
                        <div style="display:flex; gap:8px;">
                            <span class="product-tag" id="metaBadgeEngine" style="background:#dcfce7; color:#166534; border-color:#86efac;">AI Engine</span>
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
                            <button class="btn-download" style="background:#0073aa; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('single')">🚀 Post to WordPress</button>
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

                <form id="autopilotForm">
                    <div class="writer-grid">
                        <div class="form-group">
                            <label>Your Brand / Website Name</label>
                            <input type="text" id="autoBrandName" placeholder="e.g. TechBazaar BD / MyWebsite" required>
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
                        <input type="text" id="autoCompetitors" placeholder="e.g. https://www.startech.com.bd, https://ryans.com" required>
                        <div style="font-size: 11.5px; color: #64748b; margin-top: 3px;">
                            💡 Separate multiple domains with commas (,). The agent scans these domains and autonomously selects today's best ranking opportunity.
                        </div>
                    </div>

                    <div class="writer-grid" style="grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));">
                        <div class="form-group">
                            <label>Optional: Specific Topic / Mission Focus (Leave blank for autonomous detection)</label>
                            <input type="text" id="autoSpecificTopic" placeholder="Leave empty for autonomous opportunity selection">
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
                        <div style="font-size: 11.5px; color: #64748b; margin-top: 6px;">
                            💡 If credentials are configured in the "🔌 WordPress" or "🌐 Custom Site API" buttons above, the agent will publish automatically.
                        </div>
                    </div>

                    <!-- Gemini Key -->
                    <div style="margin-bottom: 16px;">
                        <input type="text" id="autoGeminiKey" placeholder="Optional: Gemini API Key (Leave empty to use 100% Free Offline Heuristic Writer)">
                    </div>

                    <button type="submit" class="btn-scan" id="autoSubmitBtn" style="background: linear-gradient(135deg, #1e3a8a, #2563eb); font-size: 16px; padding: 15px; width: 100%;">
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

    <script>
        document.getElementById('dateInput').value = new Date().toISOString().split('T')[0];
        
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

        // WordPress Sync Settings and Helpers
        function getWpCredentials() {
            return {
                url: localStorage.getItem('wp_site_url') || '',
                user: localStorage.getItem('wp_username') || '',
                appPass: localStorage.getItem('wp_app_password') || '',
                status: localStorage.getItem('wp_default_status') || 'draft'
            };
        }

        function updateWpBadge() {
            const creds = getWpCredentials();
            const badge = document.getElementById('wpStatusBadge');
            if (!badge) return;
            if (creds.url && creds.user && creds.appPass) {
                badge.innerText = 'Connected';
                badge.style.background = '#dcfce7';
                badge.style.color = '#15803d';
            } else {
                badge.innerText = 'Not Configured';
                badge.style.background = 'rgba(255,255,255,0.22)';
                badge.style.color = 'white';
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

        async function publishArticleToWordPress(source, isAuto = false) {
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

            statusBox.style.display = 'block';
            statusBox.style.background = '#eff6ff';
            statusBox.style.border = '1px solid #93c5fd';
            statusBox.style.borderRadius = '8px';
            statusBox.style.padding = '12px 16px';
            statusBox.style.color = '#1e40af';
            statusBox.innerHTML = `🚀 Sending article to WordPress (${creds.url})... Please wait.`;

            try {
                const resp = await fetch('/api/wordpress/publish', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        site_url: creds.url,
                        username: creds.user,
                        app_password: creds.appPass,
                        status: creds.status || 'draft',
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

        // Initialize WordPress sync badge status
        updateWpBadge();

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
            } else {
                badge.innerText = 'Not Configured';
                badge.style.background = 'rgba(255,255,255,0.22)';
                badge.style.color = 'white';
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
                alert('Built-in API Token copied to clipboard:\\n' + tok);
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

        function switchTab(tab) {
            document.getElementById('tabDaily').style.display = (tab === 'daily') ? 'block' : 'none';
            document.getElementById('tabSpy').style.display = (tab === 'spy') ? 'block' : 'none';
            document.getElementById('tabMulti').style.display = (tab === 'multi') ? 'block' : 'none';
            document.getElementById('tabWriter').style.display = (tab === 'writer') ? 'block' : 'none';
            document.getElementById('tabAutopilot').style.display = (tab === 'autopilot') ? 'block' : 'none';

            document.getElementById('tabDailyBtn').className = 'tab-btn daily' + (tab === 'daily' ? ' active' : '');
            document.getElementById('tabSpyBtn').className = 'tab-btn spy' + (tab === 'spy' ? ' active' : '');
            document.getElementById('tabMultiBtn').className = 'tab-btn multi' + (tab === 'multi' ? ' active' : '');
            document.getElementById('tabWriterBtn').className = 'tab-btn writer' + (tab === 'writer' ? ' active' : '');
            document.getElementById('tabAutopilotBtn').className = 'tab-btn autopilot' + (tab === 'autopilot' ? ' active' : '');
        }

        // Tracker Form Submit
        document.getElementById('trackerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const url = document.getElementById('urlInput').value.trim();
            const targetDate = document.getElementById('dateInput').value;

            document.getElementById('trackerSpinner').style.display = 'block';
            document.getElementById('trackerResults').style.display = 'none';
            document.getElementById('scanBtn').disabled = true;

            try {
                const resp = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url, date: targetDate })
                });
                const data = await resp.json();
                document.getElementById('trackerSpinner').style.display = 'none';
                document.getElementById('scanBtn').disabled = false;

                if (data.status === 'success' && data.results && data.results.length > 0) {
                    currentArticles = data.results;
                    renderTrackerCards(data.results, data.is_recent_fallback);
                } else {
                    alert('No articles found! Please check the competitor website URL.');
                }
            } catch (err) {
                document.getElementById('trackerSpinner').style.display = 'none';
                document.getElementById('scanBtn').disabled = false;
                alert('Error: ' + err.message);
            }
        });

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
                            <button class="btn-spy" style="padding:7px 16px; font-size:13px; font-weight:600;" onclick="spySingleUrl('${art.url}')">🕵️‍♂️ 360° Deep Spy</button>
                            <button class="btn-download" style="padding:7px 16px; font-size:13px; font-weight:600;" onclick='writeFromCard(${JSON.stringify(art.title)}, ${JSON.stringify(art.main_keyword)}, ${JSON.stringify(lsiList)}, ${JSON.stringify(art.product_name)}, ${JSON.stringify(art.url)})'>✍️ Write Outranking Article</button>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
            document.getElementById('trackerResults').style.display = 'block';
        }

        // Spy Form Submit
        document.getElementById('spyForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const url = document.getElementById('spyUrlInput').value.trim();
            runDeepSpy(url);
        });

        function spySingleUrl(url) {
            switchTab('spy');
            document.getElementById('spyUrlInput').value = url;
            runDeepSpy(url);
        }

        async function runDeepSpy(url) {
            if (!url) return;
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

        function renderSpyResults(data) {
            currentSpyData = data;
            const audit = data.audit;
            const bl = data.backlinks;
            const bp = data.blueprint;
            const resDiv = document.getElementById('spyResults');

            const reasonsHtml = (audit.ranking_reasons || []).map(r => `<div class="reason-item">✔ ${r}</div>`).join('');
            const bpHtml = (bp || []).map(s => `
                <div class="blueprint-item">
                    <div class="bp-step">Step ${s.step}: ${s.action}</div>
                    <div class="bp-desc">${s.detail}</div>
                </div>
            `).join('');

            const blLinksHtml = (bl.external_backlink_sources || []).map(s => `
                <div style="margin-bottom:8px; font-size:13px;">
                    <a href="${s.source_url || s.url}" target="_blank" style="color:var(--accent); text-decoration:underline; font-weight:600;">${s.anchor_or_title || s.title || s.source_url || s.url}</a>
                    <span style="font-size:11px; background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px; margin-left:6px;">${s.type || 'Backlink'}</span>
                </div>
            `).join('');

            const lsiChips = (audit.lsi_keywords || []).map(k => `<span class="lsi-chip">${k}</span>`).join('');

            // Outline Tree HTML
            const headingsList = audit.all_headings || [];
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

            // Content Gaps HTML
            const gapsList = audit.content_gaps || [];
            let gapsHtml = '';
            if (gapsList.length > 0) {
                gapsHtml = gapsList.map(g => `
                    <div class="gap-item">
                        <span style="font-size:16px;">⚠️</span>
                        <div>${g}</div>
                    </div>
                `).join('');
            } else {
                gapsHtml = '<div class="reason-item">✔ Competitor has a balanced on-page structure. Match word count and add richer schemas to beat them.</div>';
            }

            const targetWords = audit.target_outrank_word_count || Math.max(2000, Math.floor(audit.word_count * 1.25));

            resDiv.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                    <div>
                        <h3 style="font-size:18px; font-weight:800; color:#0f172a; margin:0;">360° Competitor Dissection Report</h3>
                        <p style="font-size:12.5px; color:var(--text-muted); margin:2px 0 0 0;">In-depth reverse engineering of on-page signals and ranking secrets</p>
                    </div>
                    <button type="button" onclick="openClientReportModal('spy')" style="background:linear-gradient(135deg, #1e3a8a, #2563eb); color:white; border:none; padding:10px 18px; border-radius:8px; font-weight:700; cursor:pointer; display:flex; align-items:center; gap:8px; box-shadow:0 4px 12px rgba(37,99,235,0.25); font-size:13px;">
                        <span>📄 Export White-Label Client PDF Report</span>
                    </button>
                </div>

                <!-- Metric Header -->
                <div class="spy-header-metrics">
                    <div class="metric-box">
                        <div class="metric-label">Competitor SEO Score</div>
                        <div class="metric-val" style="color:#059669;">${audit.seo_score}/100</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Competitor Word Count</div>
                        <div class="metric-val">${audit.word_count} <span style="font-size:12px; color:var(--text-muted); font-weight:500;">(${audit.reading_time || '5 min'})</span></div>
                    </div>
                    <div class="metric-box" style="border: 1.5px solid #86efac; background: #f0fdf4;">
                        <div class="metric-label" style="color:#065f46;">Target to Outrank</div>
                        <div class="metric-val" style="color:#047857;">${targetWords}+ <span style="font-size:12px; font-weight:700;">words 🎯</span></div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Estimated Backlinks</div>
                        <div class="metric-val" style="color:#0284c7;">${bl.total_backlinks_est} <span style="font-size:12px; color:var(--text-muted); font-weight:500;">(~${bl.referring_domains_est} Domains)</span></div>
                    </div>
                </div>

                <!-- Page Identity -->
                <div class="section-box">
                    <div class="card-top">
                        <a href="${audit.url}" target="_blank" class="card-title" style="font-size:19px;">${audit.title} ↗</a>
                        <span class="product-tag">📦 ${audit.product_name}</span>
                    </div>
                    <div style="margin: 6px 0 12px 0; font-size: 13px; color: var(--text-muted); word-break: break-all;">
                        <strong style="color: var(--text-main);">🔗 Competitor URL:</strong> <a href="${audit.url}" target="_blank" style="color: var(--accent); text-decoration: underline; font-weight: 500;">${audit.url}</a>
                    </div>
                    <div class="keyword-box">
                        <div>
                            <div class="kw-label">🎯 Target Focus Keyword</div>
                            <div class="main-kw" style="font-size:16px;">${audit.main_keyword}</div>
                        </div>
                        <div>
                            <div class="kw-label">🏷️ Clean LSI Keywords Cluster</div>
                            <div class="lsi-container">${lsiChips}</div>
                        </div>
                    </div>
                </div>

                <!-- Competitor Content & Outline Dissection Box -->
                <div class="section-box" style="border-color: #cbd5e1;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                        <div class="content-subtabs" style="margin-bottom:0; border-bottom:none; padding-bottom:0;">
                            <button class="subtab-btn active" id="subtabSpyText" onclick="switchSpyContentTab('text')">📜 Competitor Content Reader</button>
                            <button class="subtab-btn" id="subtabSpyOutline" onclick="switchSpyContentTab('outline')">🌳 Heading Hierarchy Outline (${headingsList.length})</button>
                            <button class="subtab-btn" id="subtabSpyGaps" onclick="switchSpyContentTab('gaps')">⚠️ Content Gaps & Vulnerabilities (${gapsList.length})</button>
                        </div>
                    </div>

                    <!-- Panel 1: Content Reader -->
                    <div id="spyViewText">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
                            <span style="font-size:12px; color:var(--text-muted);">
                                📖 Showing competitor article text (${audit.word_count} words, ${audit.reading_time || '5 min read'})
                            </span>
                            <div style="display:flex; gap:8px;">
                                <button class="meta-btn-copy" id="toggleContentBtn" onclick="toggleSpyContentLength()">Show Full Article Text</button>
                                <button class="meta-btn-copy" onclick="copyCompetitorText()">📋 Copy Text</button>
                            </div>
                        </div>
                        <div class="competitor-content-box" id="competitorContentText">${audit.content_excerpt || audit.full_content_preview || 'No text extracted.'}</div>
                    </div>

                    <!-- Panel 2: Heading Tree -->
                    <div id="spyViewOutline" style="display:none;">
                        <div style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">
                            📌 Exact heading hierarchy used by the competitor to rank on Google search:
                        </div>
                        <div class="outline-tree">
                            ${outlineHtml}
                        </div>
                    </div>

                    <!-- Panel 3: Content Gaps -->
                    <div id="spyViewGaps" style="display:none;">
                        <div style="font-size:12px; color:var(--text-muted); margin-bottom:10px;">
                            🚨 Actionable opportunities to beat this competitor on Google's Helpful Content update:
                        </div>
                        ${gapsHtml}
                    </div>
                </div>

                <!-- AI Agent Outranker Studio Card -->
                <div class="section-box" style="border: 2px solid #10b981; background: linear-gradient(135deg, #f0fdf4, #ffffff);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
                        <div>
                            <h3 style="font-size:17px; color:#065f46; font-weight:800; display:flex; align-items:center; gap:8px;">
                                <span>⚡</span> AI Agent Outranker Studio
                            </h3>
                            <p style="font-size:13px; color:#047857; margin-top:2px;">
                                Outrank this competitor by publishing a more authoritative article covering all missing LSI entities, comparison tables, and FAQ schema.
                            </p>
                        </div>
                        <button class="btn-download" style="background:#2563eb;" onclick='writeFromCard(${JSON.stringify(audit.title)}, ${JSON.stringify(audit.main_keyword)}, ${JSON.stringify(audit.lsi_keywords || [])}, ${JSON.stringify(audit.product_name)}, ${JSON.stringify(audit.url)})'>
                            ✏️ Customize in Tab 3 Studio
                        </button>
                    </div>

                    <div class="writer-grid" style="grid-template-columns: 1fr; margin-top: 14px; margin-bottom: 0;">
                        <div class="form-group">
                            <label>Your Brand / Company / Website Name</label>
                            <input type="text" id="inlineBrandName" placeholder="e.g. MyBrand / mywebsite.com (Woven naturally into recommendations, testing authority & CTA)">
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
                                <option value="long_form_seo">📖 Long-Form SEO Guide</option>
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

                <!-- Inline Spinner for Tab 2 Generation -->
                <div class="spinner" id="spyInlineSpinner" style="display:none;">
                    <div class="loader" style="border-top-color: var(--writer-accent);"></div>
                    <h3 style="color:#065f46;">AI Agent is crafting outranking content...</h3>
                    <p style="color: var(--text-muted); font-size: 13px;">Analyzing competitor outline, writing deeper sections, creating comparison tables & embedding FAQ schema...</p>
                </div>

                <!-- Inline Battle Results in Tab 2 -->
                <div id="spyInlineResults" style="display:none;"></div>

                <!-- Why it Ranked -->
                <div class="section-box">
                    <div class="section-title">💡 Secret Ranking Factors (Why This Page Ranked on Google):</div>
                    ${reasonsHtml}
                </div>

                <!-- Backlink Footprint -->
                <div class="section-box">
                    <div class="section-title">🔗 Backlink Intelligence & Referral Footprint (Sources & URLs):</div>
                    <p style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">Identified external citation sources, referral domains, social mentions, and community backlink footprints:</p>
                    ${blLinksHtml}
                </div>

                <!-- Outranking Blueprint -->
                <div class="section-box" style="border-color: rgba(139, 92, 246, 0.5);">
                    <div class="section-title" style="color:#7c3aed;">⚔️ Actionable Outranking Blueprint (Formula to Outrank Competitor):</div>
                    ${bpHtml}
                </div>
            `;
            resDiv.style.display = 'block';

            const savedBrand = localStorage.getItem('user_brand_name') || '';
            if (savedBrand && document.getElementById('inlineBrandName')) {
                document.getElementById('inlineBrandName').value = savedBrand;
            }
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

            document.getElementById('spyInlineSpinner').style.display = 'block';
            document.getElementById('spyInlineResults').style.display = 'none';
            document.getElementById('inlineSubmitBtn').disabled = true;

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
                        gemini_key: geminiKey
                    })
                });

                const data = await resp.json();
                document.getElementById('spyInlineSpinner').style.display = 'none';
                document.getElementById('inlineSubmitBtn').disabled = false;

                if (data.status === 'success' && data.result) {
                    generatedData = data.result;
                    renderInlineBattleResults(audit, data.result);
                } else {
                    alert('Error: ' + (data.message || 'Generation failed.'));
                }
            } catch (err) {
                document.getElementById('spyInlineSpinner').style.display = 'none';
                document.getElementById('inlineSubmitBtn').disabled = false;
                alert('Generation Error: ' + err.message);
            }
        }

        function renderInlineBattleResults(audit, res) {
            const container = document.getElementById('spyInlineResults');
            const diff = res.actual_word_count - audit.word_count;
            const pct = audit.word_count > 0 ? Math.round((diff / audit.word_count) * 100) : 100;
            const diffText = diff >= 0 ? `+${diff} words (+${pct}% More Depth! 🏆)` : `${diff} words`;

            const rawMd = res.article_markdown || '';
            const visualHtml = (typeof marked !== 'undefined') ? marked.parse(rawMd) : rawMd;

            container.innerHTML = `
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

            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth' });
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
        document.getElementById('writerForm').addEventListener('submit', async function(e) {
            e.preventDefault();
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
        });

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
        document.getElementById('multiForm').addEventListener('submit', async function(e) {
            e.preventDefault();
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
        });

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
                titleOptsHtml = `
                    <div style="margin-top:10px;">
                        <span style="font-size:12px; color:var(--text-muted); font-weight:600;">Alternative High-CTR Titles (Click to test):</span>
                        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                            ${meta.title_options.map(t => `<span class="title-option-chip" onclick="selectMultiTitle('${t.replace(/'/g, "\\'")}')">${t}</span>`).join('')}
                        </div>
                    </div>
                `;
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
                            <button class="btn-download" style="background:#0073aa; border:none; display:flex; align-items:center; gap:6px;" onclick="publishArticleToWordPress('multi')">🚀 Post to WordPress</button>
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
        document.getElementById('autopilotForm').addEventListener('submit', async function(e) {
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
        });

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
                            <button class="btn-download" style="background:#0073aa;" onclick="publishArticleToWordPress('autopilot')">🚀 Re-Post to WordPress</button>
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
                const gaps = audit.content_gaps || [];

                const scoreColor = audit.seo_score >= 80 ? '#15803d' : (audit.seo_score >= 60 ? '#b45309' : '#b91c1c');

                container.innerHTML = `
                    <div style="border-bottom: 2px solid #0f172a; padding-bottom: 14px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                        <div>
                            <div style="font-size: 11px; font-weight: 800; color: #3b82f6; text-transform: uppercase; letter-spacing: 1px;">EXECUTIVE COMPETITOR AUDIT</div>
                            <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; margin: 4px 0;">SEO Competitive Intelligence & Gap Report</h2>
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
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px;">
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Competitor SEO Score</div>
                            <div class="report-kpi-num" style="color: ${scoreColor};">${audit.seo_score}<span style="font-size:14px; color:#64748b;">/100</span></div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Competitor Word Count</div>
                            <div class="report-kpi-num" style="color: #0f172a;">${(audit.word_count || 0).toLocaleString()}</div>
                        </div>
                        <div class="report-kpi-card" style="background: #f0fdf4; border-color: #86efac;">
                            <div style="font-size: 11px; font-weight: 700; color: #065f46; text-transform: uppercase;">Required To Outrank</div>
                            <div class="report-kpi-num" style="color: #047857;">${(audit.target_outrank_word_count || Math.max(2000, Math.floor(audit.word_count * 1.25))).toLocaleString()}+</div>
                        </div>
                        <div class="report-kpi-card">
                            <div style="font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase;">Estimated Backlinks</div>
                            <div class="report-kpi-num" style="color: #0284c7;">${bl.total_backlinks_est || 0}</div>
                        </div>
                    </div>

                    <!-- Target Page Breakdown -->
                    <div class="report-section">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">1. Audited Competitor Profile</h4>
                        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
                            <div><strong>Page Title:</strong> ${audit.title || 'Untitled'}</div>
                            <div><strong>URL:</strong> <code style="font-size:12px; color:#2563eb;">${audit.url || ''}</code></div>
                            <div><strong>Target Entity / Product:</strong> ${audit.product_name || 'General Topic'}</div>
                            <div><strong>Primary Focus Keyword:</strong> <span style="background:#fef3c7; color:#92400e; padding:1px 6px; border-radius:4px; font-weight:700;">${audit.main_keyword || 'Not detected'}</span></div>
                        </div>
                    </div>

                    <!-- Semantic Keyword Cluster -->
                    <div class="report-section">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">2. High-Intent Semantic Keyword Cluster</h4>
                        <p style="font-size: 12px; color: #64748b; margin-top: 0;">Keywords your competitor is leveraging to win organic impressions on search engines:</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                            ${(audit.lsi_keywords || []).map(k => `<span style="background:#eff6ff; color:#1e40af; border:1px solid #bfdbfe; padding:3px 8px; border-radius:5px; font-size:12px; font-weight:600;">${k}</span>`).join('')}
                        </div>
                    </div>

                    <!-- Content Gaps & Critical Vulnerabilities -->
                    <div class="report-section" style="border-left: 4px solid #f59e0b;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 8px;">3. Competitor Vulnerabilities & Content Gaps</h4>
                        <p style="font-size: 12px; color: #64748b; margin-top: 0;">Critical ranking deficiencies identified in the competitor's on-page architecture:</p>
                        <ul style="margin: 0 0 0 18px; padding: 0; font-size: 13px; color: #334155; line-height: 1.7;">
                            ${gaps.length > 0 ? gaps.map(g => `<li>${g}</li>`).join('') : '<li>Competitor lacks in-depth topical coverage and structured FAQ schema markup.</li>'}
                        </ul>
                    </div>

                    <!-- Actionable 5-Step Outranking Roadmap -->
                    <div class="report-section" style="border-left: 4px solid #10b981; margin-bottom: 0;">
                        <h4 style="font-size: 14px; font-weight: 800; color: #065f46; margin-top: 0; margin-bottom: 8px;">4. Recommended Outranking Action Plan for ${clientName}</h4>
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
                    type: "long_form_seo"
                },
                {
                    day: "Day 8 (Week 2)",
                    stage: "High-Intent Buyer Reviews",
                    title: `Top 10 Best ${topic} Ranked & Reviewed (Expert Tested)`,
                    intent: "Commercial / Review",
                    intentClass: "intent-comm",
                    keywords: `best ${topic} review, top rated ${topic}, comparison`,
                    words: 2800,
                    type: "product_review"
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
                    type: "long_form_seo"
                },
                {
                    day: "Day 20 (Week 3)",
                    stage: "Practical How-To Tutorial",
                    title: `How to Setup, Maintain & Maximize Your ${topic} Step-by-Step`,
                    intent: "Informational / Guide",
                    intentClass: "intent-info",
                    keywords: `how to use ${topic}, ${topic} setup guide, tutorial`,
                    words: 2000,
                    type: "long_form_seo"
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
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        if self.path == '/api/scan':
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
                country = data.get('country', 'Bangladesh').strip()
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
