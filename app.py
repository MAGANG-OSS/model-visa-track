import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import os
import base64
from pathlib import Path
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import streamlit.components.v1 as components

# =============================================================
# 1. KONFIGURASI HALAMAN
# =============================================================
st.set_page_config(
    page_title="Visa Track - Prediksi Student Visa Australia",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================
# TYPOGRAPHY & REFINED STYLING (POPPINS - LMS OSS BALI AESTHETIC)
# =============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography - Poppins (Identik dengan LMS OSS Bali) */
    html, body, p, label, input, select, textarea, button,
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stDateInputField"] input,
    div[data-testid="stDateInputField"] span,
    div[data-testid="stDateInputField"] div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] div,
    div[data-testid="stSelectbox"] span,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] span,
    div.stButton button,
    div.stButton button p,
    div.stButton button span {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: #17324D;
    }

    /* Pertahankan font icon bawaan Streamlit agar tidak rusak */
    [class*="material-symbols"], [class*="material-icons"], .material-symbols-rounded, .material-icons, svg, svg * {
        font-family: inherit !important;
    }

    /* Background halaman lembut kebiruan: #F4F9FD */
    .stApp {
        background-color: #F4F9FD !important;
    }

    /* Streamlit Expander Icon & Header Fix */
    div[data-testid="stExpander"] details summary {
        font-family: 'Poppins', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #075985 !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    div[data-testid="stExpander"] details summary svg {
        margin-right: 8px !important;
    }

    .block-container {
        max-width: 1240px !important;
        margin: 0 auto !important;
        padding-top: 1.8rem !important;
        padding-bottom: 14rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* =========================================================
       HEADER UTAMA APLIKASI (GRADASI BIRU ELEGAN MEMBULAT)
       ========================================================= */
    .banner-header {
        background: linear-gradient(135deg, #025a85 0%, #0284c7 100%) !important;
        border-radius: 16px !important;
        padding: 22px 30px !important;
        margin-top: 10px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 8px 24px rgba(2, 90, 133, 0.14) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        overflow: hidden;
    }
    .banner-left {
        display: flex;
        flex-direction: column;
    }
    .banner-accent {
        width: 36px;
        height: 4.5px;
        background-color: #f59e0b;
        border-radius: 3px;
        margin-bottom: 10px;
    }
    .banner-title {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.015em;
        text-shadow: 0 1px 2px rgba(0,0,0,0.12);
    }
    .banner-right {
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }

    /* =========================================================
       STEPPER PROGRESS INDICATOR (SESUAI DESAIN CARD MINIMALIS RAMPING)
       ========================================================= */
    .stepper-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 10px 18px 8px 18px !important;
        margin-top: 2px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .stepper-container {
        display: flex !important;
        align-items: flex-start !important;
        justify-content: space-between !important;
        width: 100% !important;
    }
    .stepper-item {
        flex: 1 1 0% !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        position: relative !important;
        min-width: 0 !important;
    }
    .stepper-top {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        height: 22px !important;
    }
    .stepper-line {
        flex: 1 1 0% !important;
        height: 0 !important;
    }
    .stepper-line.completed {
        border-top: 2px solid #0284C7 !important;
    }
    .stepper-line.pending {
        border-top: 1.5px dashed #CBD5E1 !important;
    }
    .stepper-line.hidden {
        visibility: hidden !important;
        border-top: 2px solid transparent !important;
    }
    .stepper-node {
        flex: 0 0 22px !important;
        width: 22px !important;
        height: 22px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-sizing: border-box !important;
        transition: all 0.2s ease !important;
        z-index: 2 !important;
    }
    .stepper-node.active,
    .stepper-node.completed {
        background-color: #0284C7 !important;
        background: #0284C7 !important;
        color: #FFFFFF !important;
        box-shadow: 0 1px 4px rgba(2, 132, 199, 0.22) !important;
    }
    .stepper-node.pending {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 2px solid #CBD5E1 !important;
        box-shadow: inset 0 0 0 2px #FFFFFF, inset 0 0 0 4.5px #CBD5E1 !important;
    }
    .stepper-label {
        font-size: 11px !important;
        margin-top: 5px !important;
        line-height: 1.25 !important;
        letter-spacing: -0.01em !important;
        text-align: center !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
    }
    .stepper-label.active {
        font-weight: 700 !important;
        color: #0F172A !important;
    }
    .stepper-label.completed {
        font-weight: 600 !important;
        color: #1E293B !important;
    }
    .stepper-label.pending {
        font-weight: 500 !important;
        color: #94A3B8 !important;
    }
    @media (max-width: 640px) {
        .stepper-label {
            font-size: 10px !important;
            white-space: normal !important;
        }
        .stepper-card {
            padding: 8px 6px 6px 6px !important;
        }
    }

    /* =========================================================
       STRUKTUR KARTU SECTION (OUTER CARD, HEADER BIRU MUDA, INNER FORM)
       ========================================================= */
    /* Matikan border bawaan stVerticalBlockBorderWrapper jika ada agar tidak double border */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[class*="st-key-outer_card_"]),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[class*="st-key-inner_card_"]) {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* 1. Container Utama Section */
    div[class*="st-key-outer_card_"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 24px 30px !important;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04) !important;
        gap: 12px !important;
        overflow: visible !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    /* Outer Card Khusus Section 1 & 2: Sedikit diperpanjang ke bawah (1-2 cm) proporsional */
    div[class*="st-key-outer_card_sec1"],
    div[class*="st-key-outer_card_sec2"] {
        padding: 26px 32px 38px 32px !important;
    }

        /* =========================================================
       SIDEBAR KIRI SESUAI CONTOH MOCKUP (BLUE GRADIENT ELEGAN)
       ========================================================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0072CE 0%, #005696 55%, #0A486D 100%) !important;
        min-width: 290px !important;
        max-width: 320px !important;
        border-right: none !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.08) !important;
        overflow: hidden !important;
        height: 100dvh !important;
        max-height: 100dvh !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        overflow: hidden !important;
        height: 100dvh !important;
        max-height: 100dvh !important;
        display: flex !important;
        flex-direction: column !important;
    }
    /* Sembunyikan default header streamlit */
    [data-testid="stSidebarHeader"] {
        display: none !important;
        height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    /* stSidebarContent mengambil tinggi penuh tanpa scrollbar terpotong */
    [data-testid="stSidebarContent"] {
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        height: 100dvh !important;
        max-height: 100dvh !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 100% !important;
    }
    [data-testid="stSidebarUserContent"] {
        overflow: hidden !important;
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 auto !important;
    }
    /* Hilangkan scrollbar default Streamlit di wrapper luar */
    [data-testid="stSidebar"]::-webkit-scrollbar,
    [data-testid="stSidebar"] > div::-webkit-scrollbar,
    [data-testid="stSidebarContent"]::-webkit-scrollbar {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
    }

    /* Container wrapper flexbox vertikal penuh (100dvh) */
    .sidebar-root {
        height: 100dvh;
        max-height: 100dvh;
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
        overflow: hidden;
        position: relative;
    }

    /* Area scrollable body tunggal, responsif, memanjang sepanjang sidebar */
    .sidebar-scrollable-body {
        flex: 1 1 auto;
        width: 100%;
        overflow-y: auto;
        overflow-x: hidden;
        display: flex;
        flex-direction: column;
        padding: 24px 20px 16px 20px;
        box-sizing: border-box;
        scrollbar-width: thin;
        scrollbar-color: rgba(255, 255, 255, 0.25) transparent;
    }
    /* 1 Scrollbar vertikal tunggal yang tipis, bersih, dan responsif memanjang */
    .sidebar-scrollable-body::-webkit-scrollbar {
        width: 4px !important;
    }
    .sidebar-scrollable-body::-webkit-scrollbar-track {
        background: transparent !important;
    }
    .sidebar-scrollable-body::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.25) !important;
        border-radius: 4px !important;
    }
    .sidebar-scrollable-body::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.45) !important;
    }
    .sidebar-scrollable-body::-webkit-scrollbar:horizontal {
        display: none !important;
        height: 0px !important;
    }

    /* Kelompok logo dan stepper menu diturunkan dan dipusatkan seimbang secara vertikal */
    .sidebar-center-group {
        margin: auto 0;
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    /* Matikan celah vertikal Streamlit bawaan di sidebar & set tinggi penuh */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        row-gap: 0px !important;
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 auto !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebar"] div[data-testid="stElementContainer"] {
        margin: 0px !important;
        padding: 0px !important;
    }
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:first-child {
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 auto !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:first-child > div[data-testid="stMarkdownContainer"] {
        height: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        flex: 1 1 auto !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:nth-child(n+2) {
        display: none !important;
        height: 0px !important;
        min-height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Sidebar Brand (Posisi lebih turun dan seimbang) */
    .sidebar-brand-wrapper {
        margin-top: 0 !important;
        margin-bottom: 20px !important;
    }
    .sidebar-brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .sidebar-brand-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar-brand-title {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.01em;
        font-family: 'Poppins', sans-serif;
    }
    .sidebar-brand-sub {
        color: rgba(255, 255, 255, 0.82);
        font-size: 12px;
        line-height: 1.45;
        margin-top: 6px;
        font-family: 'Poppins', sans-serif;
    }

    /* Sidebar Stepper Menu */
    .sidebar-stepper-menu {
        display: flex;
        flex-direction: column;
        margin-top: 6px;
        margin-bottom: 10px;
    }

    /* Sidebar Stepper Rows - 100% Identik Gambar User */
    .sidebar-step-row {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        position: relative;
        text-decoration: none !important;
        user-select: none !important;
        transition: all 0.15s ease;
        padding: 2px 4px;
        border-radius: 8px;
    }
    .sidebar-step-row.clickable {
        cursor: pointer !important;
    }
    .sidebar-step-row.clickable:hover {
        background: rgba(255, 255, 255, 0.08) !important;
    }
    .sidebar-step-row.clickable:hover .sidebar-step-title {
        color: #FFFFFF !important;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
    }
    .sidebar-step-row.clickable:hover .sidebar-step-circle {
        border-color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.22) !important;
    }
    .sidebar-step-row,
    .sidebar-step-row *,
    .sidebar-step-title,
    .sidebar-step-desc {
        text-decoration: none !important;
    }
    .sidebar-step-row.locked {
        cursor: not-allowed !important;
        opacity: 0.55 !important;
    }
    .sidebar-step-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 30px;
        min-width: 30px;
        flex-shrink: 0;
    }
    .sidebar-step-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.75);
        background: rgba(255, 255, 255, 0.12);
        border: 1.5px solid rgba(255, 255, 255, 0.35);
        transition: all 0.2s ease;
    }
    .sidebar-step-row.active .sidebar-step-circle {
        background: #0088FF;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        box-shadow: 0 0 12px rgba(0, 136, 255, 0.55);
    }
    .sidebar-step-row.completed .sidebar-step-circle {
        background: #0284C7;
        color: #FFFFFF;
        border: 1.5px solid #FFFFFF;
    }
    /* Tinggi connector 20px pas dan nyaman di layar */
    .sidebar-step-connector {
        width: 2px;
        height: 20px;
        border-left: 2px dashed rgba(255, 255, 255, 0.35);
        margin: 2px 0;
    }
    .sidebar-step-content {
        display: flex;
        flex-direction: column;
        padding-top: 2px;
        padding-bottom: 4px;
        flex: 1;
        overflow: hidden;
    }
    .sidebar-step-title {
        color: rgba(255, 255, 255, 0.75);
        font-size: 13.5px;
        font-weight: 600;
        line-height: 1.25;
        font-family: 'Poppins', sans-serif;
    }
    .sidebar-step-row.active .sidebar-step-title {
        color: #FFFFFF;
        font-weight: 700;
    }
    .sidebar-step-row.completed .sidebar-step-title {
        color: #FFFFFF;
        font-weight: 600;
    }
    .sidebar-step-desc {
        color: rgba(255, 255, 255, 0.55);
        font-size: 11px;
        margin-top: 2px;
        line-height: 1.25;
        font-family: 'Poppins', sans-serif;
    }
    .sidebar-step-row.active .sidebar-step-desc {
        color: rgba(255, 255, 255, 0.88);
    }

        /* Sidebar Footer selalu menempel di area paling bawah */
    .sidebar-footer-container {
        margin-top: auto;
        flex-shrink: 0;
        width: 100%;
        padding: 14px 20px 20px 20px;
        box-sizing: border-box;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .sidebar-footer-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 11px;
        white-space: normal !important;
        word-break: break-word !important;
        margin: 0 !important;
        padding: 0px !important;
        line-height: 1.4 !important;
        font-family: 'Poppins', sans-serif;
        text-align: left;
    }

    /* Invisible Sidebar Action Buttons */
    div[class*="st-key-sb_nav_btn_"] {
        position: fixed !important;
        left: -9999px !important;
        top: -9999px !important;
        width: 1px !important;
        height: 1px !important;
        opacity: 0 !important;
        pointer-events: none !important;
        overflow: hidden !important;
    }

    /* Main Area Header Above Card */
    .main-page-header {
        margin-top: 4px;
        margin-bottom: 16px;
    }
    .main-step-eyebrow {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 4px;
        font-family: 'Poppins', sans-serif;
    }
    .main-step-title {
        font-size: 20px;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.015em;
        margin-bottom: 4px;
        line-height: 1.25;
        font-family: 'Poppins', sans-serif;
    }
    .main-step-desc {
        font-size: 13px;
        color: #64748B;
        line-height: 1.4;
        font-family: 'Poppins', sans-serif;
    }

    /* 2. Inner Card (Sekat Putih Area Form) */
    div[class*="st-key-inner_card_"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D6EAFA !important;
        border-radius: 10px !important;
        padding: 16px 20px 16px 20px !important;
        box-shadow: none !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
        gap: 10px !important;
    }
    /* Khusus Inner Card Section 1 & 2: Proporsional, rapi & tidak mepet */
    div[class*="st-key-inner_card_sec1"],
    div[class*="st-key-inner_card_sec2"] {
        padding: 18px 22px 18px 22px !important;
        border: 1px solid #D6EAFA !important;
        border-radius: 10px !important;
        margin-top: 6px !important;
        margin-bottom: 12px !important;
    }

    /* 3. Header Section: Membentang penuh di bagian atas kartu, spasi judul & deskripsi rapat! */
    .card-section-header {
        background-color: #EAF5FD !important;
        border-bottom: 1px solid #CBE8FA !important;
        border-radius: 14px 14px 0 0 !important;
        margin: -20px -24px 16px -24px !important;
        padding: 16px 24px !important;
        display: flex !important;
        align-items: center !important;
        gap: 14px !important;
    }
    .card-header-icon {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        border-radius: 50% !important;
        background-color: #D6ECFA !important;
        border: 1px solid #B9E0F7 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #0284C7 !important;
    }
    .card-header-text {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        gap: 2px !important;
    }
    div[data-testid="stMarkdownContainer"] h2.card-title,
    div[data-testid="stMarkdownContainer"] div.card-title,
    .stMarkdown h2.card-title,
    .card-header-text .card-title,
    .card-title {
        font-size: 18.5px !important;
        font-weight: 700 !important;
        color: #075985 !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
        letter-spacing: -0.01em !important;
    }
    div[data-testid="stMarkdownContainer"] p.card-subtitle,
    div[data-testid="stMarkdownContainer"] div.card-subtitle,
    .stMarkdown p.card-subtitle,
    .card-header-text .card-subtitle,
    .card-subtitle {
        font-size: 13px !important;
        font-weight: 400 !important;
        color: #64809F !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.35 !important;
    }

    /* =========================================================
       LABEL WIDGET & TOOLTIP: SERAGAM 100% UNTUK SEMUA JENIS INPUT (11.5PX)
       ========================================================= */
    div[data-testid="stWidgetLabel"] {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stWidgetLabel"] *,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span,
    .stNumberInput label,
    .stSelectbox label,
    .stRadio label,
    .stDateInput label,
    .stTextInput label {
        font-size: 11.5px !important;
        font-weight: 600 !important;
        color: #0284C7 !important;
        margin: 0 !important;
        letter-spacing: -0.01em !important;
        line-height: 1.3 !important;
    }
    /* Ikon tanda tanya bulat di pojok kanan atas masing-masing kotak fill form */
    div[data-testid="stTooltipIcon"] {
        margin-left: auto !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    div[data-testid="stTooltipIcon"] svg {
        color: #0284C7 !important;
        width: 13.5px !important;
        height: 13.5px !important;
    }

    /* =========================================================
       DESAIN FIELD INPUT: MURNI PUTIH (#FFFFFF) & PINGGIRAN ABU-ABU (#CBD5E1)
       UKURAN COMPACT RAMPING (HEIGHT: 40PX, RADIUS: 7PX)
       SESUAI DOM STREAMLIT 1.66 (DATEINPUT, TEXTINPUT, SELECTBOX, NUMBERINPUT)
       ========================================================= */
    div[data-testid="stDateInputField"],
    [data-testid="stDateInputField"],
    div[data-testid="stDateInput"] [data-testid="stDateInputField"],
    div[data-testid="stDateInput"] div[data-baseweb="input"],
    [data-testid="stTextInputRootElement"],
    div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] div.react-aria-Group,
    div[data-testid="stTextInput"] div[class*="e1bh1cux2"],
    div[data-testid="stTextInput"] div:has(> input),
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stSelectbox"] div.react-aria-Group,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"],
    div[data-testid="stSelectbox"] div[role="group"],
    div[data-testid="stSelectbox"] div:has(> input),
    div[data-testid="stSelectbox"] > div:nth-child(2),
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] div:has(> input),
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-color: #CBD5E1 !important;
        border-width: 1.5px !important;
        border-style: solid !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        height: 42px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        box-sizing: border-box !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stDateInputField"] [data-testid="stDateInputFieldsScroller"],
    div[data-testid="stDateInputField"] div {
        background-color: transparent !important;
        background: transparent !important;
    }
    div[data-baseweb="base-input"],
    div[data-testid="stDateInput"] div[data-baseweb="base-input"],
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    div[data-baseweb="input"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stDateInputField"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] input,
    input[data-testid="stTextInputField"],
    [data-testid="stTextInputField"] {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        height: 100% !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        color: #17324D !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        caret-color: #0284C7 !important;
    }

    /* Teks nilai di dalam field input & selectbox */
    div[data-baseweb="input"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] input,
    div[data-baseweb="select"] [role="combobox"] span,
    div[data-baseweb="select"] [role="combobox"] div,
    div[data-testid="stSelectbox"] [role="combobox"] span,
    div[data-testid="stSelectbox"] [role="combobox"] div,
    div[data-testid="stSelectbox"] div.react-aria-Group span,
    div[data-testid="stSelectbox"] div.react-aria-Group div {
        color: #17324D !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        caret-color: #0284C7 !important;
    }

    /* Placeholder (#8AA6C1) */
    div[data-testid="stDateInput"] input::placeholder,
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stSelectbox"] input::placeholder,
    div[data-baseweb="input"] input::placeholder,
    input[data-testid="stTextInputField"]::placeholder {
        color: #8AA6C1 !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        opacity: 1 !important;
    }

    /* Hover & Focus State */
    div[data-testid="stDateInputField"]:hover,
    [data-testid="stDateInputField"]:hover,
    div[data-testid="stDateInput"] [data-testid="stDateInputField"]:hover,
    div[data-testid="stDateInput"] div[data-baseweb="input"]:hover,
    [data-testid="stTextInputRootElement"]:hover,
    div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"]:hover,
    div[data-testid="stTextInput"] div.react-aria-Group:hover,
    div[data-testid="stTextInput"] div[class*="e1bh1cux2"]:hover,
    div[data-testid="stTextInput"] div:has(> input):hover,
    div[data-testid="stTextInput"] div[data-baseweb="input"]:hover,
    div[data-testid="stSelectbox"] div.react-aria-Group:hover,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"]:hover,
    div[data-testid="stSelectbox"] div[role="group"]:hover,
    div[data-testid="stSelectbox"] div:has(> input):hover,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
        border: 1.5px solid #94A3B8 !important;
        border-color: #94A3B8 !important;
        box-shadow: 0 0 0 2px rgba(148, 163, 184, 0.15) !important;
    }

    div[data-testid="stDateInputField"]:focus-within,
    [data-testid="stDateInputField"]:focus-within,
    div[data-testid="stDateInput"] [data-testid="stDateInputField"]:focus-within,
    div[data-testid="stDateInput"] div[data-baseweb="input"]:focus-within,
    [data-testid="stTextInputRootElement"]:focus-within,
    div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"]:focus-within,
    div[data-testid="stTextInput"] div.react-aria-Group:focus-within,
    div[data-testid="stTextInput"] div[class*="e1bh1cux2"]:focus-within,
    div[data-testid="stTextInput"] div:has(> input):focus-within,
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stSelectbox"] div.react-aria-Group:focus-within,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"]:focus-within,
    div[data-testid="stSelectbox"] div[role="group"]:focus-within,
    div[data-testid="stSelectbox"] div:has(> input):focus-within,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border: 1.5px solid #0284C7 !important;
        border-color: #0284C7 !important;
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.18) !important;
    }

    /* Ikon Kalender & Dropdown */
    div[data-testid="stDateInput"] svg,
    div[data-testid="stSelectbox"] svg,
    div[data-baseweb="select"] svg {
        color: #0284C7 !important;
        width: 16px !important;
        height: 16px !important;
    }

    /* State Border Invalid (#DC2626) */
    div[data-baseweb="input"].input-invalid-border,
    div[data-baseweb="select"] > div.input-invalid-border,
    [data-testid="stTextInputRootElement"].input-invalid-border {
        border: 1.5px solid #DC2626 !important;
        border-color: #DC2626 !important;
        background-color: #FFFFFF !important;
    }

    /* =========================================================
       RADIO BUTTONS: PILL ELEGAN DENGAN TEKS HORIZONTAL RAPI
       ========================================================= */
    div[data-testid="stRadioGroup"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 14px !important;
        flex-wrap: wrap !important;
        margin-top: 4px !important;
        margin-bottom: 6px !important;
    }
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] {
        display: inline-flex !important;
        align-items: center !important;
        gap: 10px !important;
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 7px !important;
        padding: 7px 16px !important;
        margin: 0 !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        user-select: none !important;
        width: auto !important;
        min-width: fit-content !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:hover {
        border-color: #94A3B8 !important;
        background-color: #F8FAFC !important;
        background: #F8FAFC !important;
    }
    div[data-testid="stRadio"] label[data-testid="stRadioOption"][data-selected="true"],
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #0284C7 !important;
        box-shadow: 0 1px 3px rgba(2, 132, 199, 0.12) !important;
    }
    /* Pastikan kontainer teks radio dan teks p selalu horizontal rapi tanpa patah huruf */
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] div[data-testid="stMarkdownContainer"],
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] [data-testid="stMarkdownContainer"] {
        width: auto !important;
        max-width: none !important;
        white-space: nowrap !important;
        background-color: transparent !important;
        background: transparent !important;
    }
    div[data-testid="stRadio"] label[data-testid="stRadioOption"] p {
        font-size: 13.5px !important;
        font-weight: 500 !important;
        color: #17324D !important;
        white-space: nowrap !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.4 !important;
        display: inline-block !important;
    }
    div[data-testid="stRadio"] label[data-testid="stRadioOption"][data-selected="true"] p,
    div[data-testid="stRadio"] label[data-testid="stRadioOption"]:has(input:checked) p {
        color: #0078D4 !important;
        font-weight: 600 !important;
    }

    /* =========================================================
       SECTION 2: PERHITUNGAN GAP CARD
       ========================================================= */
    .gap-boxes-row {
        display: flex;
        align-items: stretch;
        gap: 16px;
        width: 100%;
        margin-top: 4px;
    }
    .gap-white-box {
        background-color: #FFFFFF;
        border: 1.5px solid #CBE8FA;
        border-radius: 12px;
        padding: 16px 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        flex: 1;
    }
    .gap-stat-block {
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
    }
    .gap-stat-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;
        border-radius: 9px;
        background-color: #EAF5FD;
        border: 1px solid #CBE8FA;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0284C7;
    }
    .gap-stat-info {
        display: flex;
        flex-direction: column;
    }
    .gap-stat-label {
        font-size: 12px;
        color: #64809F;
        font-weight: 500;
        margin-bottom: 2px;
    }
    .gap-stat-value {
        font-size: 17px;
        font-weight: 700;
        color: #075985;
        line-height: 1.15;
    }
    .gap-stat-divider {
        width: 1px;
        height: 36px;
        background-color: #CBE8FA;
        margin: 0 8px;
    }
    .gap-badge-terisi {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #059669;
        font-size: 11.5px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        margin-left: auto;
        white-space: nowrap;
    }

    /* =========================================================
       HINT / PESAN VALIDASI DI BAWAH INPUT
       ========================================================= */
    .field-hint {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        margin-top: 5px;
        margin-bottom: 4px;
        line-height: 1.35;
    }
    .field-hint.hint-muted {
        color: #64809F;
    }
    .field-hint.hint-success {
        color: #059669;
        font-weight: 500;
    }
    .field-hint.hint-error {
        color: #EF4444 !important;
        font-weight: 500;
    }
    .field-error-text {
        color: #EF4444 !important;
        font-size: 11.5px !important;
        font-weight: 500 !important;
        margin-top: 5px !important;
        margin-bottom: 2px !important;
        line-height: 1.3 !important;
        display: block !important;
        padding-left: 1px !important;
    }
    .field-error-banner {
        display: flex !important;
        align-items: center !important;
        gap: 7px !important;
        background-color: #FEF2F2 !important;
        border: 1px solid #FECACA !important;
        border-left: 3px solid #DC2626 !important;
        border-radius: 6px !important;
        padding: 5px 10px !important;
        margin-top: -6px !important;
        margin-bottom: 2px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .field-error-banner .error-badge-icon {
        width: 15px !important;
        height: 15px !important;
        min-width: 15px !important;
        border-radius: 50% !important;
        background-color: #DC2626 !important;
        color: #FFFFFF !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        line-height: 1 !important;
    }
    .field-error-banner .error-badge-text {
        color: #DC2626 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        line-height: 1.3 !important;
    }
    /* Otomatis border merah pada kotak input saat ada pesan eror di kolomnya */
    div:has(> .field-error-banner) [data-testid="stTextInputRootElement"],
    div:has(> .field-error-banner) div.react-aria-Group,
    div:has(> .field-error-banner) [data-baseweb="input"],
    div:has(> div .field-error-banner) [data-testid="stTextInputRootElement"],
    div:has(> div .field-error-banner) div.react-aria-Group,
    div:has(> div .field-error-banner) [data-baseweb="input"],
    div[data-testid="stColumn"]:has(.field-error-banner) [data-testid="stTextInputRootElement"],
    div[data-testid="stColumn"]:has(.field-error-banner) div.react-aria-Group,
    div[data-testid="stColumn"]:has(.field-error-banner) [data-baseweb="input"],
    div[data-testid="column"]:has(.field-error-banner) [data-baseweb="input"],
    /* Section 1 & General Error Border */
    div[data-testid="column"]:has(.field-error-sec1) div[data-baseweb="input"],
    div[data-testid="column"]:has(.field-error-sec1) [data-testid="stDateInputField"],
    div[data-testid="column"]:has(.field-error-sec1) div[data-testid="stDateInput"] div[data-baseweb="input"],
    div[data-testid="stColumn"]:has(.field-error-sec1) div[data-baseweb="input"],
    div[data-testid="stColumn"]:has(.field-error-sec1) [data-testid="stDateInputField"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:first-child:has(.field-error-sec1) div[data-baseweb="input"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:first-child:has(.field-error-sec1) [data-testid="stDateInputField"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:last-child:has(.field-error-sec1) div[data-baseweb="input"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:last-child:has(.field-error-sec1) [data-testid="stDateInputField"],
    div[data-testid="column"]:has(.field-error-text) [data-testid="stDateInputField"],
    div[data-testid="stColumn"]:has(.field-error-text) div[data-testid="stDateInput"] div[data-baseweb="input"],
    div[data-testid="stColumn"]:has(.field-error-text) [data-testid="stTextInputRootElement"],
    div[data-testid="stColumn"]:has(.field-error-text) div.react-aria-Group,
    div[data-testid="stColumn"]:has(.field-error-text) [data-baseweb="input"],
    div[data-testid="stColumn"]:has(.field-error-text) [data-baseweb="input"] > div,
    div[data-testid="column"]:has(.field-error-text) [data-baseweb="input"],
    div[data-testid="column"]:has(.field-error-text) [data-testid="stDateInputField"] {
        border: 1.5px solid #EF4444 !important;
        border-color: #EF4444 !important;
        box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important;
    }

    /* Penyesuaian Pesan Error Section 1 Tepat di Bawah Input */
    div[class*="st-key-inner_card_sec1"] div[data-testid="column"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="stColumn"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec1"] div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        row-gap: 0px !important;
    }
    div[class*="st-key-inner_card_sec1"] div[data-testid="stDateInput"] {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    div[class*="st-key-inner_card_sec1"] div[data-testid="element-container"]:has(.field-error-sec1),
    div[class*="st-key-inner_card_sec1"] div[data-testid="stElementContainer"]:has(.field-error-sec1) {
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    .field-error-sec1,
    .field-error-sec2 {
        color: #EF4444 !important;
        font-size: 11.5px !important;
        font-weight: 500 !important;
        margin-top: 6px !important;
        margin-bottom: 2px !important;
        line-height: 1.25 !important;
        display: block !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Penyesuaian Pesan Error Section 2 Tepat di Bawah Input */
    div[class*="st-key-inner_card_sec2"] div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec2"] div[data-testid="column"] div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        row-gap: 0px !important;
    }
    div[class*="st-key-inner_card_sec2"] div[data-testid="stHorizontalBlock"] {
        gap: 16px !important;
        column-gap: 16px !important;
    }
    div[class*="st-key-inner_card_sec2"] div[data-testid="stTextInput"],
    div[class*="st-key-inner_card_sec2"] div[data-testid="stSelectbox"] {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    div[class*="st-key-inner_card_sec2"] div[data-testid="element-container"]:has(.field-error-sec2),
    div[class*="st-key-inner_card_sec2"] div[data-testid="stElementContainer"]:has(.field-error-sec2) {
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }

    /* Penyesuaian Pesan Error & Sejajarkan Input Section 4 */
    div[class*="st-key-inner_card_sec4"] div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="column"] div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        row-gap: 0px !important;
    }
    div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"] {
        gap: 16px !important;
        column-gap: 16px !important;
    }
    div[class*="st-key-inner_card_sec4"] div[data-testid="stTextInput"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    div[class*="st-key-inner_card_sec4"] div[data-testid="element-container"]:has(.field-error-sec4),
    div[class*="st-key-inner_card_sec4"] div[data-testid="stElementContainer"]:has(.field-error-sec4) {
        margin-top: 0px !important;
        margin-bottom: 2px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    .field-error-sec4 {
        color: #EF4444 !important;
        font-size: 11.5px !important;
        font-weight: 500 !important;
        margin-top: 6px !important;
        margin-bottom: 2px !important;
        line-height: 1.25 !important;
        display: block !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Sembunyikan 'Press Enter to apply' bawaan Streamlit agar form bersih */
    div[data-testid="InputInstructions"],
    div[data-testid="stInputInstructions"],
    div[class*="stInputInstructions"] {
        display: none !important;
    }

    /* Tombol Clear (x) Biru pada Text Input Section 2 & 4 */
    .st-custom-clear-btn {
        position: absolute !important;
        right: 11px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        cursor: pointer !important;
        z-index: 10 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 20px !important;
        height: 20px !important;
        transition: opacity 0.15s ease !important;
        user-select: none !important;
    }
    .st-custom-clear-btn:hover {
        opacity: 0.8 !important;
    }

    /* Penyelarasan Tinggi Label 3 Selectbox Row 2 Section 4 */
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] div[data-testid="stWidgetLabel"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] label[data-testid="stWidgetLabel"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] label {
        min-height: 22px !important;
        height: auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    .hint-icon {
        width: 14px;
        height: 14px;
        min-width: 14px;
    }

    /* =========================================================
       KOTAK INFORMASI USIA OTOMATIS (SECTION 1) — RAMPING & BOLD
       ========================================================= */
    .calc-box-placeholder {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 9px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 14px !important;
        margin-bottom: 6px !important;
    }
    .calc-placeholder-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 15px;
        width: 15px;
        height: 15px;
        color: #1D4ED8;
    }
    .calc-placeholder-text {
        font-size: 11.5px !important;
        color: #1D4ED8 !important;
        font-weight: 700 !important;
        line-height: 1.35 !important;
    }

    .calc-box-result {
        background-color: #F8FAFC;
        border: 1px solid #D6EAFA;
        border-radius: 10px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        margin-top: 8px !important;
        margin-bottom: 8px !important;
    }
    .calc-avatar-icon {
        width: 32px;
        height: 32px;
        min-width: 32px;
        border-radius: 50%;
        background-color: #FFFFFF;
        border: 1px solid #CBE8FA;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0284C7;
        margin-right: 14px;
    }
    .calc-col-age {
        display: flex;
        flex-direction: column;
    }
    .calc-label {
        font-size: 11px;
        color: #64809F;
        font-weight: 500;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    .calc-val-age {
        font-size: 16px;
        font-weight: 700;
        color: #075985;
        line-height: 1.2;
    }
    .calc-divider {
        width: 1px;
        height: 26px;
        background-color: #D6EAFA;
        margin: 0 16px;
    }
    .calc-col-detail {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .calc-date-range {
        font-size: 12.5px;
        font-weight: 600;
        color: #17324D;
        line-height: 1.3;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }
    .calc-subdetail-badge {
        font-size: 11.5px;
        color: #64809F;
        font-weight: 400;
    }

    /* =========================================================
       TOMBOL NAVIGASI SELANJUTNYA (#0078D4) & KEMBALI
       ========================================================= */
    div.st-key-btn_next_1,
    div.st-key-btn_next_2,
    div.st-key-btn_next_3,
    div.st-key-btn_back_2,
    div.st-key-btn_back_3,
    div.st-key-btn_back_4,
    div.st-key-btn_submit {
        margin-top: 6px !important;
    }

    div.st-key-btn_next_1 button,
    div.st-key-btn_next_2 button,
    div.st-key-btn_next_3 button {
        background-color: #0078D4 !important;
        color: #FFFFFF !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 9px !important;
        padding: 10px 24px !important;
        min-height: 42px !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0, 120, 212, 0.22) !important;
        transition: all 0.15s ease !important;
    }
    div.st-key-btn_next_1 button p, div.st-key-btn_next_1 button span,
    div.st-key-btn_next_2 button p, div.st-key-btn_next_2 button span,
    div.st-key-btn_next_3 button p, div.st-key-btn_next_3 button span {
        color: #FFFFFF !important;
    }
    div.st-key-btn_next_1 button:hover,
    div.st-key-btn_next_2 button:hover,
    div.st-key-btn_next_3 button:hover {
        background-color: #0284C7 !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.32) !important;
    }

    /* Tombol Kembali (Outline Biru) */
    div.st-key-btn_back_2 button,
    div.st-key-btn_back_3 button,
    div.st-key-btn_back_4 button {
        background-color: #FFFFFF !important;
        color: #0284C7 !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 9px !important;
        padding: 9px 24px !important;
        min-height: 42px !important;
        border: 1.5px solid #0284C7 !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }
    div.st-key-btn_back_2 button p, div.st-key-btn_back_2 button span,
    div.st-key-btn_back_3 button p, div.st-key-btn_back_3 button span,
    div.st-key-btn_back_4 button p, div.st-key-btn_back_4 button span {
        color: #0284C7 !important;
        font-weight: 600 !important;
    }
    div.st-key-btn_back_2 button:hover,
    div.st-key-btn_back_3 button:hover,
    div.st-key-btn_back_4 button:hover {
        background-color: #EAF5FD !important;
        border-color: #0078D4 !important;
        color: #0078D4 !important;
    }
    div.st-key-btn_back_2 button:hover p, div.st-key-btn_back_2 button:hover span,
    div.st-key-btn_back_3 button:hover p, div.st-key-btn_back_3 button:hover span,
    div.st-key-btn_back_4 button:hover p, div.st-key-btn_back_4 button:hover span {
        color: #0078D4 !important;
    }

    div.st-key-btn_edit_submission button {
        background-color: #075985 !important;
        color: #FFFFFF !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 9px !important;
        padding: 10px 24px !important;
        border: none !important;
        box-shadow: 0 3px 10px rgba(7, 89, 133, 0.2) !important;
        transition: all 0.15s ease !important;
    }
    div.st-key-btn_edit_submission button p, div.st-key-btn_edit_submission button span {
        color: #FFFFFF !important;
    }

    /* Hijau Solid (#059669) untuk Tombol Prediksi & Selesai */
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"],
    div.st-key-btn_finish_submission button {
        background-color: #059669 !important;
        color: #FFFFFF !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 9px !important;
        padding: 10px 24px !important;
        min-height: 42px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span,
    div.stButton > button[data-testid="baseButton-primary"] p,
    div.stButton > button[data-testid="baseButton-primary"] span,
    div.st-key-btn_finish_submission button p,
    div.st-key-btn_finish_submission button span {
        color: #FFFFFF !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover,
    div.st-key-btn_finish_submission button:hover {
        background-color: #047857 !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.35) !important;
    }

    /* Warning / Reminder & Error Banner (#DC2626) */
    .reminder-box-prev {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 6px;
        margin-bottom: 20px;
        padding: 10px 14px;
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-radius: 8px;
    }
    .reminder-circle-icon {
        width: 18px;
        height: 18px;
        min-width: 18px;
        border-radius: 50%;
        border: 1.5px solid #DC2626;
        color: #DC2626;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        font-family: inherit;
    }
    .reminder-content-text {
        color: #DC2626;
        font-size: 12.5px;
        font-weight: 600;
        line-height: 1.35;
    }

    .form-error-banner {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background-color: #FEF2F2 !important;
        border: 1px solid #FECACA !important;
        border-left: 3px solid #DC2626 !important;
        border-radius: 6px !important;
        padding: 5px 12px !important;
        margin-top: 6px !important;
        margin-bottom: 8px !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .form-error-icon {
        width: 15px !important;
        height: 15px !important;
        min-width: 15px !important;
        border-radius: 50% !important;
        background-color: #DC2626 !important;
        color: #FFFFFF !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 9.5px !important;
        font-weight: 800 !important;
        line-height: 1 !important;
    }
    .form-error-text {
        font-size: 11.5px !important;
        font-weight: 500 !important;
        color: #DC2626 !important;
        line-height: 1.35 !important;
    }

    /* CARD GRANT & REFUSAL */
    div.st-key-direct_card_grant button,
    div[data-testid="stButton"].st-key-direct_card_grant button {
        background-color: #f0fdf4 !important;
        background: #f0fdf4 !important;
        border: 2px solid #86efac !important;
        border-radius: 16px !important;
        min-height: 125px !important;
        padding: 22px 18px !important;
        white-space: pre-line !important;
        line-height: 1.45 !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.08) !important;
        transition: all 0.2s ease !important;
    }
    div.st-key-direct_card_grant button p,
    div.st-key-direct_card_grant button span,
    div.st-key-direct_card_grant button div,
    div[data-testid="stButton"].st-key-direct_card_grant button p,
    div[data-testid="stButton"].st-key-direct_card_grant button span,
    div[data-testid="stButton"].st-key-direct_card_grant button div {
        color: #059669 !important;
        font-size: 21px !important;
        font-weight: 800 !important;
        white-space: pre-line !important;
    }
    div.st-key-direct_card_grant button:hover,
    div[data-testid="stButton"].st-key-direct_card_grant button:hover {
        background-color: #dcfce7 !important;
        background: #dcfce7 !important;
        border-color: #059669 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.18) !important;
    }

    div.st-key-direct_card_refusal button,
    div[data-testid="stButton"].st-key-direct_card_refusal button {
        background-color: #fef2f2 !important;
        background: #fef2f2 !important;
        border: 2px solid #fca5a5 !important;
        border-radius: 16px !important;
        min-height: 125px !important;
        padding: 22px 18px !important;
        white-space: pre-line !important;
        line-height: 1.45 !important;
        box-shadow: 0 4px 14px rgba(220, 38, 38, 0.08) !important;
        transition: all 0.2s ease !important;
    }
    div.st-key-direct_card_refusal button p,
    div.st-key-direct_card_refusal button span,
    div.st-key-direct_card_refusal button div,
    div[data-testid="stButton"].st-key-direct_card_refusal button p,
    div[data-testid="stButton"].st-key-direct_card_refusal button span,
    div[data-testid="stButton"].st-key-direct_card_refusal button div {
        color: #DC2626 !important;
        font-size: 21px !important;
        font-weight: 800 !important;
        white-space: pre-line !important;
    }
    div.st-key-direct_card_refusal button:hover,
    div[data-testid="stButton"].st-key-direct_card_refusal button:hover {
        background-color: #fee2e2 !important;
        background: #fee2e2 !important;
        border-color: #DC2626 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.18) !important;
    }

    .recom-item-clean {
        background-color: #FFFFFF;
        border: 1px solid #CBE8FA;
        border-left: 3.5px solid #075985;
        border-radius: 6px;
        padding: 11px 14px;
        margin-bottom: 9px;
        font-size: 13px;
        line-height: 1.5;
        color: #17324D;
    }
    .recom-item-clean.grant-item {
        border-left-color: #059669;
    }
    .recom-item-clean.refusal-item {
        border-left-color: #DC2626;
    }
    .recom-title-clean {
        font-weight: 700;
        color: #075985;
    }
    .result-breakdown-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 18px;
        margin-bottom: 12px;
    }
    .result-breakdown-icon {
        width: 38px;
        height: 38px;
        min-width: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .result-breakdown-icon.grant-icon {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #059669;
    }
    .result-breakdown-icon.refusal-icon {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        color: #DC2626;
    }
    .result-breakdown-titles {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .result-breakdown-title {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.01em;
        line-height: 1.25;
    }
    .result-breakdown-subtitle {
        font-size: 12.5px;
        color: #64748B;
        font-family: 'Poppins', sans-serif;
        line-height: 1.35;
    }




    /* Calendar & Floating UI Popover Protection: Mencegah kalender & dropdown tahun glitch/tertutup sendiri */
    #stFloatingOverlayPortal {
        z-index: 99999999 !important;
        pointer-events: auto !important;
    }
    div[data-testid="stDateInputCalendar"],
    div[data-testid="stDateInputHeaderPickerPopover"],
    div[data-testid="stDateInputQuickSelectPopover"],
    div[data-baseweb="popover"],
    div[data-baseweb="calendar"] {
        z-index: 99999999 !important;
        pointer-events: auto !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stDateInputHeaderPickerPopover"] {
        max-height: 220px !important;
        overflow-y: auto !important;
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12) !important;
    }
    div[data-testid="stDateInputCalendar"] {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    div[data-testid="stDateInputCalendar"] button,
    div[data-testid="stDateInputCalendar"] div {
        min-height: unset !important;
    }
    div[data-testid="stDateInputClearButton"] {
        cursor: pointer !important;
        pointer-events: auto !important;
    }
    div[data-testid="stDateInputClearButton"] svg {
        color: #0284C7 !important;
        fill: #0284C7 !important;
    }
    div[data-testid="stDateInputCalendarButton"] svg {
        color: #0284C7 !important;
    }
    div[data-baseweb="popover"] div[data-baseweb="select"] > div,
    div[data-baseweb="calendar"] div[data-baseweb="select"] > div,
    div[data-baseweb="calendar"] div[data-baseweb="input"],
    div[data-baseweb="calendar"] input,
    div[data-baseweb="calendar"] button,
    div[data-baseweb="calendar"] div {
        min-height: unset !important;
        height: auto !important;
        border-radius: 4px !important;
    }
    div[data-baseweb="popover"] {
        z-index: 9999999 !important;
    }
    div[data-baseweb="calendar"] {
        background-color: #FFFFFF !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* Clean, Modern Input & Selectbox Styling (Zero JS delay) */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] div.react-aria-Group,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"],
    div[data-testid="stSelectbox"] div[role="group"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        height: 42px !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] div.react-aria-Group,
    div[data-testid="stTextInput"] div[class*="e1bh1cux2"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        box-sizing: border-box !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stSelectbox"] input {
        color: #17324D !important;
        font-size: 13px !important;
    }
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
    div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] label {
        min-height: 22px !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Card & Button Direktori Kampus Mitra OSS Bali (True Modern Button) */
    div[class*="st-key-card_oss_directory"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #38BDF8 !important;
        border-left: 5px solid #0284C7 !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.08) !important;
    }
    div[class*="st-key-card_oss_directory"] div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 16px !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-card_oss_directory"] div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
    }
    div[class*="st-key-card_oss_directory"] [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] a {
        background-color: #0284C7 !important;
        background: linear-gradient(180deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #0284C7 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 10px 20px !important;
        min-height: 42px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        box-shadow: 0 2px 5px rgba(2, 132, 199, 0.25) !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        width: 100% !important;
    }
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] a:hover {
        background-color: #0369A1 !important;
        background: linear-gradient(180deg, #0369A1 0%, #075985 100%) !important;
        border-color: #0369A1 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.38) !important;
        transform: translateY(-1px) !important;
    }
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] a p,
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] a span,
    div[class*="st-key-card_oss_directory"] [data-testid="stLinkButton"] a * {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        text-decoration: none !important;
    }

</style>
""", unsafe_allow_html=True)

# Inject Poppins into parent document head & Attach Sidebar Navbar Click Listener + Global Scroll-to-Top
components.html("""
<script>
try {
    const doc = window.parent.document;
    if (!doc.getElementById('poppins-font-link')) {
        const link = doc.createElement('link');
        link.id = 'poppins-font-link';
        link.rel = 'stylesheet';
        link.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap';
        doc.head.appendChild(link);
    }
    if (!doc.getElementById('poppins-font-style')) {
        const style = doc.createElement('style');
        style.id = 'poppins-font-style';
        style.innerHTML = `
            html, body, .stApp, [class*="st-"], p, span, label, input, select, textarea, button, h1, h2, h3, h4 {
                font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }
            [class*="material-symbols"], [class*="material-icons"], svg, svg * {
                font-family: inherit !important;
            }
        `;
        doc.head.appendChild(style);
    }

    window.parent.__visaTrackScrollToTop = function() {
        try {
            const win = window.parent;
            const d = win.document;
            const appView = d.querySelector('[data-testid="stAppViewContainer"]');
            if (appView) appView.scrollTop = 0;
            const mainSec = d.querySelector('section.main') || d.querySelector('.main');
            if (mainSec) mainSec.scrollTop = 0;
            win.scrollTo(0, 0);
        } catch(e) {}
    };

    if (!window.parent.__visaTrackNavAttached) {
        window.parent.__visaTrackNavAttached = true;
        doc.addEventListener('click', function(e) {
            // Klik baris stepbar navigasi sidebar
            const row = e.target.closest('.sidebar-step-row.clickable');
            if (row) {
                const step = row.getAttribute('data-step');
                if (step) {
                    const btnWrap = doc.querySelector('.st-key-sb_nav_btn_' + step);
                    if (btnWrap) {
                        const btn = btnWrap.querySelector('button');
                        if (btn) {
                            window.parent.__visaTrackScrollToTop();
                            btn.click();
                        }
                    }
                }
                return;
            }

            // Klik tombol navigasi antar section (Lanjut, Selanjutnya, Kembali, Prediksi, Edit Data)
            const navBtn = e.target.closest('button');
            if (navBtn) {
                const txt = (navBtn.innerText || '').toLowerCase();
                if (txt.includes('lanjut') || txt.includes('selanjutnya') || txt.includes('kembali') || txt.includes('prediksi') || txt.includes('edit data') || txt.includes('analisis')) {
                    window.parent.__visaTrackScrollToTop();
                }
            }
        });
    }
} catch (e) {}
</script>
""", height=0, width=0)

# =============================================================
# LOAD ASSETS
# =============================================================
def load_assets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'model_random_forest.pkl')
    features_path = os.path.join(base_dir, 'model_features.pkl')
    
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    explainer = shap.TreeExplainer(model)
    return model, features, explainer

try:
    model, model_features, explainer = load_assets()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

# State Management
if "current_section" not in st.session_state:
    st.session_state.current_section = 1

if "max_unlocked_step" not in st.session_state:
    st.session_state.max_unlocked_step = 1

# Check if URL parameter ?sec=X is requested (via sidebar link click)
if "sec" in st.query_params:
    try:
        req_sec = int(st.query_params.get("sec", 1))
        max_allowed = st.session_state.get("max_unlocked_step", 1)
        if 1 <= req_sec <= max_allowed:
            st.session_state.current_section = req_sec
    except (ValueError, TypeError):
        pass

st.session_state.max_unlocked_step = max(
    st.session_state.get("max_unlocked_step", 1),
    st.session_state.current_section
)

if "fin_input_str" not in st.session_state:
    st.session_state.fin_input_str = ""

if "ielts_input_str" not in st.session_state:
    st.session_state.ielts_input_str = ""

if "active_result_view" not in st.session_state:
    st.session_state.active_result_view = "grant"

today = date.today()
current_year = today.year

# Helper Callbacks
def on_ielts_change():
    val = st.session_state.ielts_raw_input.strip().replace(",", ".")
    if val:
        if val.isdigit() and len(val) == 2 and int(val) >= 10 and int(val) <= 90:
            val = f"{int(val)/10:.1f}"
            st.session_state.ielts_raw_input = val
        else:
            try:
                num = float(val)
                if num.is_integer() and 1 <= num <= 9:
                    st.session_state.ielts_raw_input = f"{num:.1f}"
            except ValueError:
                pass
    st.session_state.ielts_input_str = st.session_state.ielts_raw_input

def on_financial_change():
    val = st.session_state.fin_raw_input
    clean_digits = "".join([c for c in str(val) if c.isdigit()])
    if clean_digits:
        num = int(clean_digits)
        formatted = f"{num:,}".replace(",", ".")
        st.session_state.fin_input_str = formatted
        st.session_state.fin_raw_input = formatted
        st.session_state.financial_nominal = float(num)
    else:
        st.session_state.fin_input_str = ""
        st.session_state.fin_raw_input = ""
        st.session_state.financial_nominal = None

def on_campus_level_change():
    val = str(st.session_state.get("select_campus_level", ""))
    if "Level 1" in val:
        st.session_state["campus_level_idx"] = 0
        st.session_state["level_kampus"] = 1.0
    elif "Level 2" in val:
        st.session_state["campus_level_idx"] = 1
        st.session_state["level_kampus"] = 2.0
    else:
        st.session_state["campus_level_idx"] = 2
        st.session_state["level_kampus"] = 3.0

# Helper Stepper UI (Design ala Image 1: White Card + Connected Nodes + Checkmarks)
def render_stepper(current_step):
    steps = [
        (1, "1. Data Pengajuan"), 
        (2, "2. Pendidikan & Jeda Studi"), 
        (3, "3. Jalur Studi (Pathway) & Kampus"), 
        (4, "4. Profil & Riwayat")
    ]
    parts = []
    total_steps = len(steps)
    for idx, (num, title) in enumerate(steps):
        # Node & label status
        if num < current_step:
            node_state = "completed"
            label_state = "completed"
            icon_html = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
        elif num == current_step:
            node_state = "active"
            label_state = "active"
            icon_html = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
        else:
            node_state = "pending"
            label_state = "pending"
            icon_html = ''

        # Left track line
        if idx == 0:
            left_line_class = "stepper-line hidden"
        else:
            if num <= current_step:
                left_line_class = "stepper-line completed"
            else:
                left_line_class = "stepper-line pending"

        # Right track line
        if idx == total_steps - 1:
            right_line_class = "stepper-line hidden"
        else:
            if num < current_step:
                right_line_class = "stepper-line completed"
            else:
                right_line_class = "stepper-line pending"

        step_html = f'''<div class="stepper-item">
            <div class="stepper-top">
                <div class="{left_line_class}"></div>
                <div class="stepper-node {node_state}">{icon_html}</div>
                <div class="{right_line_class}"></div>
            </div>
            <div class="stepper-label {label_state}">{title}</div>
        </div>'''
        parts.append(step_html)

    return f'<div class="stepper-card"><div class="stepper-container">{"".join(parts)}</div></div>'

# =============================================================
# DETEKSI PERPINDAHAN SECTION
# =============================================================
_prev_rendered_sec = st.session_state.get("_active_rendered_section", None)
_curr_rendered_sec = st.session_state.current_section
_sec_changed = (_prev_rendered_sec != _curr_rendered_sec)
st.session_state["_active_rendered_section"] = _curr_rendered_sec

# =============================================================
# SIDEBAR KIRI (100% IDENTIK MOCKUP GAMBAR USER + DIRECT NATIVE CLICK)
# =============================================================
with st.sidebar:
    current_step = st.session_state.current_section
    max_unlocked = st.session_state.get("max_unlocked_step", 1)
    if current_step == 5:
        max_unlocked = 5
        st.session_state.max_unlocked_step = 5

    steps_data = [
        (1, "Data Pengajuan", "Informasi dasar pemohon"),
        (2, "Pendidikan & Jeda Studi", "Riwayat pendidikan & jeda"),
        (3, "Jalur Studi (Pathway)", "Pilihan jenjang & kampus"),
        (4, "Profil & Riwayat", "Pengalaman dan latar belakang")
    ]
    if max_unlocked >= 5:
        steps_data.append((5, "Hasil Prediksi", "Evaluasi & rekomendasi visa"))

    step_rows = []
    total_steps = len(steps_data)
    for idx, (num, title, desc) in enumerate(steps_data):
        is_active = (current_step == num)
        is_completed = (num < current_step) or (current_step == 5 and num < 5)
        is_unlocked = (num <= max_unlocked)
        is_last = (idx == total_steps - 1)

        if num == 5:
            state_class = "active" if is_active else "completed"
            circle_inner = "★"
        elif is_completed:
            state_class = "completed"
            circle_inner = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        elif is_active:
            state_class = "active"
            circle_inner = str(num)
        else:
            state_class = "pending"
            circle_inner = str(num)

        clickable_class = "clickable" if (is_unlocked and not is_active) else ("active" if is_active else "locked")
        connector_html = '<div class="sidebar-step-connector"></div>' if not is_last else ''

        step_row_html = (
            f'<div class="sidebar-step-row {state_class} {clickable_class}" data-step="{num}">'
            f'<div class="sidebar-step-node">'
            f'<div class="sidebar-step-circle">{circle_inner}</div>'
            f'{connector_html}'
            f'</div>'
            f'<div class="sidebar-step-content">'
            f'<div class="sidebar-step-title">{title}</div>'
            f'<div class="sidebar-step-desc">{desc}</div>'
            f'</div>'
            f'</div>'
        )
        step_rows.append(step_row_html)

    stepper_html = "".join(step_rows)

    sidebar_full_html = (
        '<div class="sidebar-root">'
        '<div class="sidebar-scrollable-body">'
        '<div class="sidebar-center-group">'
        '<div class="sidebar-brand-wrapper">'
        '<div class="sidebar-brand-header">'
        '<div class="sidebar-brand-icon">'
        '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="9.5"></circle>'
        '<path d="M3 12h18M12 2.5a14 14 0 0 1 0 19M12 2.5a14 14 0 0 0 0 19"></path>'
        '<polygon points="18 5 22 3 20 7" fill="#FFFFFF"></polygon>'
        '</svg>'
        '</div>'
        '<div class="sidebar-brand-title">Visa Track</div>'
        '</div>'
        '<div class="sidebar-brand-sub">Prediksi Keberhasilan<br>Student Visa Australia</div>'
        '</div>'
        f'<div class="sidebar-stepper-menu">{stepper_html}</div>'
        '</div>'
        '</div>'
        '<div class="sidebar-footer-container">'
        '<div class="sidebar-footer-text">&copy; 2026 Visa Track. All rights reserved.</div>'
        '</div>'
        '</div>'
    )
    st.markdown(sidebar_full_html, unsafe_allow_html=True)

    # Invisible action buttons for sidebar navbar navigation
    for n in range(1, 6):
        if st.button(" ", key=f"sb_nav_btn_{n}"):
            st.session_state.current_section = n
            st.rerun()

# =============================================================
# JIKA SEDANG DI TAHAP FORM INPUT (SECTION 1 s/d 4)
# =============================================================
if st.session_state.current_section in [1, 2, 3, 4]:
    # ---------------------------------------------------------
    # SECTION 1: DATA PENGAJUAN STUDENT
    # ---------------------------------------------------------
    if st.session_state.current_section == 1:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 01 / 04</div>'
            '<div class="main-step-title">Data Pengajuan</div>'
            '<div class="main-step-desc">Masukkan data dasar untuk menghitung usia serta informasi dasar lainnya.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec1"):

            with st.container(border=True, key="inner_card_sec1"):
                d1, d2 = st.columns(2)
                with d1:
                    saved_birth = st.session_state.get("birth_date", None)
                    if "input_birth_date" not in st.session_state and saved_birth is not None:
                        st.session_state["input_birth_date"] = saved_birth

                    birth_date = st.date_input(
                        "Tanggal Lahir Student :red[*]",
                        value=None,
                        min_value=date(1960, 1, 1),
                        max_value=date(current_year - 14, 12, 31),
                        format="DD/MM/YYYY",
                        key="input_birth_date",
                        persist_state="session",
                        help="Pilih tanggal lahir student sesuai identitas paspor."
                    )
                    st.session_state["birth_date"] = birth_date
                    if birth_date is not None:
                        st.session_state["sec1_birth_err"] = False

                    if st.session_state.get("sec1_birth_err") and birth_date is None:
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:first-child div[data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:first-child [data-testid="stDateInputField"], '
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:first-child div[data-testid="stDateInput"] > div { '
                            '    border: 1.5px solid #EF4444 !important; '
                            '    border-color: #EF4444 !important; '
                            '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                            '} '
                            '</style>'
                            '<div class="field-error-sec1">'
                            'Silahkan masukkan tanggal lahir'
                            '</div>',
                            unsafe_allow_html=True
                        )

                with d2:
                    saved_apply = st.session_state.get("apply_date", None)
                    if "input_apply_date" not in st.session_state and saved_apply is not None:
                        st.session_state["input_apply_date"] = saved_apply

                    apply_date = st.date_input(
                        "Waktu Pengajuan Visa :red[*]",
                        value=None,
                        min_value=date(2015, 1, 1),
                        max_value=date(current_year + 2, 12, 31),
                        format="DD/MM/YYYY",
                        key="input_apply_date",
                        persist_state="session",
                        help="Pilih tanggal pengajuan aplikasi visa student."
                    )
                    st.session_state["apply_date"] = apply_date
                    if apply_date is not None and (birth_date is None or apply_date >= birth_date):
                        st.session_state["sec1_apply_err"] = False
                        st.session_state["sec1_apply_err_msg"] = None

                    if st.session_state.get("sec1_apply_err") and (apply_date is None or (birth_date and apply_date < birth_date)):
                        err_msg = st.session_state.get("sec1_apply_err_msg", "Silahkan masukkan waktu pengajuan visa")
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:nth-child(2) div[data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:nth-child(2) [data-testid="stDateInputField"], '
                            'div[class*="st-key-inner_card_sec1"] div[data-testid="column"]:nth-child(2) div[data-testid="stDateInput"] > div { '
                            '    border: 1.5px solid #EF4444 !important; '
                            '    border-color: #EF4444 !important; '
                            '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                            '} '
                            '</style>'
                            f'<div class="field-error-sec1">'
                            f'{err_msg}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                if birth_date is None or apply_date is None:
                    sec1_placeholder_html = (
                        '<div class="calc-box-placeholder">'
                        '<div class="calc-placeholder-icon">'
                        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1D4ED8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
                        '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
                        '</svg></div>'
                        '<div class="calc-placeholder-text">'
                        'Usia dan tahun pengajuan akan dihitung otomatis setelah kedua tanggal diisi.'
                        '</div></div>'
                    )
                    st.markdown(sec1_placeholder_html, unsafe_allow_html=True)

            if birth_date is not None and apply_date is not None:
                if apply_date < birth_date:
                    st.session_state["sec1_apply_err"] = True
                    st.session_state["sec1_apply_err_msg"] = "Waktu Pengajuan Visa tidak boleh lebih awal dari Tanggal Lahir Student."
                else:
                    st.session_state["sec1_apply_err"] = False
                    st.session_state["sec1_apply_err_msg"] = None
                    st.session_state["sec1_error"] = None
                    diff = relativedelta(apply_date, birth_date)
                    diff_years = diff.years
                    diff_months = diff.months
                    diff_days = diff.days

                    calculated_age = apply_date.year - birth_date.year - ((apply_date.month, apply_date.day) < (birth_date.month, birth_date.day))
                    age_val = max(15, min(65, calculated_age))
                    app_year = apply_date.year
                    st.session_state["age_val"] = age_val
                    st.session_state["app_year"] = app_year

                    b_str = birth_date.strftime("%d/%m/%Y")
                    a_str = apply_date.strftime("%d/%m/%Y")

                    sec1_result_html = (
                        '<div class="calc-box-result">'
                        '<div class="calc-avatar-icon">'
                        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
                        '<circle cx="12" cy="12" r="9"></circle><polyline points="12 6 12 12 16 14"></polyline>'
                        '</svg></div>'
                        '<div class="calc-col-age">'
                        '<div class="calc-label">Usia Saat Pengajuan</div>'
                        f'<div class="calc-val-age">{age_val} Tahun</div>'
                        '</div>'
                        '<div class="calc-divider"></div>'
                        '<div class="calc-col-age">'
                        '<div class="calc-label">Tahun Pengajuan</div>'
                        f'<div class="calc-val-age">{app_year}</div>'
                        '</div>'
                        '<div class="calc-divider"></div>'
                        '<div class="calc-col-detail">'
                        '<div class="calc-label">Rincian Perhitungan Usia</div>'
                        f'<div class="calc-date-range">{b_str} &rarr; {a_str} <span class="calc-subdetail-badge">({diff_years} thn, {diff_months} bln, {diff_days} hr)</span></div>'
                        '</div></div>'
                    )
                    st.markdown(sec1_result_html, unsafe_allow_html=True)

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            c_btn1, c_btn2 = st.columns([4.4, 1.2])
            with c_btn2:
                if st.button("Selanjutnya", key="btn_next_1", use_container_width=True):
                    eff_birth = birth_date or st.session_state.get("birth_date")
                    eff_apply = apply_date or st.session_state.get("apply_date")
                    has_err = False
                    if eff_birth is None:
                        st.session_state["sec1_birth_err"] = True
                        has_err = True
                    else:
                        st.session_state["sec1_birth_err"] = False

                    if eff_apply is None:
                        st.session_state["sec1_apply_err"] = True
                        st.session_state["sec1_apply_err_msg"] = "Silahkan masukkan waktu pengajuan visa"
                        has_err = True
                    elif eff_birth and eff_apply < eff_birth:
                        st.session_state["sec1_apply_err"] = True
                        st.session_state["sec1_apply_err_msg"] = "Waktu Pengajuan Visa tidak boleh lebih awal dari Tanggal Lahir Student."
                        has_err = True
                    else:
                        st.session_state["sec1_apply_err"] = False
                        st.session_state["sec1_apply_err_msg"] = None

                    if eff_birth is not None:
                        st.session_state["birth_date"] = eff_birth
                    if eff_apply is not None:
                        st.session_state["apply_date"] = eff_apply

                    if has_err:
                        st.session_state["sec1_error"] = None
                        st.rerun()
                    else:
                        st.session_state["sec1_error"] = None
                        st.session_state["sec1_birth_err"] = False
                        st.session_state["sec1_apply_err"] = False
                        st.session_state["sec1_apply_err_msg"] = None
                        st.session_state.current_section = 2
                        st.rerun()

        birth_err_val = "true" if (st.session_state.get("sec1_birth_err") and birth_date is None) else "false"
        apply_err_val = "true" if (st.session_state.get("sec1_apply_err") and (apply_date is None or (birth_date and apply_date < birth_date))) else "false"



    # ---------------------------------------------------------
    # SECTION 2: INFORMASI PENDIDIKAN TERAKHIR & GAP
    # ---------------------------------------------------------
    elif st.session_state.current_section == 2:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 02 / 04</div>'
            '<div class="main-step-title">Informasi Pendidikan Terakhir & Jeda Studi (Gap)</div>'
            '<div class="main-step-desc">Kelompokkan informasi tahun kelulusan terakhir dan durasi jeda studi student.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec2"):
            with st.container(border=True, key="inner_card_sec2"):
                degree_options = [
                    "SMA / SMK",
                    "Diploma Satu (D1)",
                    "Diploma Dua (D2)",
                    "Diploma Tiga (D3)",
                    "Diploma Empat (D4)",
                    "S1 (Strata 1)",
                    "S2 (Strata 2)"
                ]
                saved_degree_idx = st.session_state.get("last_edu_degree_idx", 0)
                if saved_degree_idx >= len(degree_options):
                    saved_degree_idx = 0
                last_edu_degree = st.selectbox(
                    "Kualifikasi Pendidikan Terakhir",
                    options=degree_options,
                    index=saved_degree_idx,
                    key="select_last_edu_degree",
                    help="Pilih jenjang pendidikan formal terakhir yang telah diselesaikan oleh student."
                )
                st.session_state["last_edu_degree"] = last_edu_degree
                st.session_state["last_edu_degree_idx"] = degree_options.index(last_edu_degree) if last_edu_degree in degree_options else 0

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                gap_options = ["Mengetahui Bulan dan Tahun", "Hanya Mengetahui Tahun"]
                saved_gap_mode = st.session_state.get("gap_mode", gap_options[0])
                gap_idx = gap_options.index(saved_gap_mode) if saved_gap_mode in gap_options else 0
                gap_mode = st.radio(
                    "Perhitungan Jeda Studi (Gap)",
                    options=gap_options,
                    index=gap_idx,
                    key="radio_gap_mode",
                    horizontal=True,
                    label_visibility="visible"
                )
                if gap_mode != saved_gap_mode:
                    st.session_state["gap_mode"] = gap_mode
                    st.session_state["sec2_year_err"] = False
                    st.session_state["sec2_month_err"] = False

                app_year = st.session_state.get("app_year", current_year)
                apply_date = st.session_state.get("apply_date", today)
                bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

                if "input_last_edu_year" not in st.session_state:
                    st.session_state["input_last_edu_year"] = str(st.session_state.get("last_edu_year") or "")

                last_edu_year = None
                clean_edu_digits = ""
                raw_edu_year = ""
                total_months = 0
                gap_year = 0.0
                bulan_lulus = None
                bulan_lulus_idx = None
                bulan_app_idx = apply_date.month if apply_date else today.month

                if gap_mode == "Mengetahui Bulan dan Tahun":
                    g1, g2 = st.columns(2)
                    with g1:
                        raw_edu_year = st.text_input(
                            "Tahun Terakhir Pendidikan / Kelulusan :red[*]",
                            placeholder="Contoh: 2022",
                            key="input_last_edu_year",
                            max_chars=4,
                            help=f"Masukkan 4 digit tahun kelulusan terakhir (1990 – {current_year})."
                        )
                        clean_edu_digits = "".join([c for c in raw_edu_year if c.isdigit()])
                        last_edu_year = int(clean_edu_digits) if len(clean_edu_digits) == 4 else None
                        st.session_state["last_edu_year"] = last_edu_year

                        if last_edu_year is not None and 1990 <= last_edu_year <= current_year:
                            st.session_state["sec2_year_err"] = False

                        if st.session_state.get("sec2_year_err") and (last_edu_year is None or last_edu_year < 1990 or last_edu_year > current_year):
                            st.markdown(
                                '<style>'
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child [data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:first-child div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:first-child [data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:first-child div:has(> input) { '
                                '    border: 1.5px solid #EF4444 !important; '
                                '    border-color: #EF4444 !important; '
                                '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                                '} '
                                '</style>'
                                '<div class="field-error-sec2">'
                                'Silahkan masukkan tahun terakhir pendidikan/kelulusan'
                                '</div>',
                                unsafe_allow_html=True
                            )

                    with g2:
                        saved_bulan_idx = st.session_state.get("bulan_lulus_idx", None)
                        bulan_lulus = st.selectbox(
                            "Bulan Kelulusan Pendidikan Terakhir :red[*]",
                            options=bulan_list,
                            index=saved_bulan_idx,
                            placeholder="Pilih bulan kelulusan",
                            key="select_bulan_lulus",
                            help="Pilih bulan kelulusan pendidikan terakhir."
                        )
                        if bulan_lulus is not None:
                            bulan_lulus_idx = bulan_list.index(bulan_lulus) + 1
                            st.session_state["bulan_lulus_idx"] = bulan_lulus_idx - 1
                            st.session_state["sec2_month_err"] = False
                        else:
                            bulan_lulus_idx = None
                            st.session_state["bulan_lulus_idx"] = None

                        if st.session_state.get("sec2_month_err") and bulan_lulus is None:
                            st.markdown(
                                '<style>'
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] > div:nth-child(2), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] div[role="group"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) div[data-testid="stSelectbox"] div[class*="e1oobldh0"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) [data-baseweb="select"] > div, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:nth-child(2) div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) div[data-testid="stSelectbox"] > div:nth-child(2), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) div[data-testid="stSelectbox"] div[role="group"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) div[data-testid="stSelectbox"] div[class*="e1oobldh0"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) [data-baseweb="select"] > div, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:nth-child(2) div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div[data-testid="stSelectbox"] > div:nth-child(2), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div[data-testid="stSelectbox"] div[role="group"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div[data-testid="stSelectbox"] div[class*="e1oobldh0"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child [data-baseweb="select"] > div, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child div[data-testid="stSelectbox"] > div:nth-child(2), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child div[data-testid="stSelectbox"] div[role="group"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child div[data-testid="stSelectbox"] div[class*="e1oobldh0"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child [data-baseweb="select"] > div, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"]:last-child div:has(> input) { '
                                '    border: 1.5px solid #EF4444 !important; '
                                '    border-color: #EF4444 !important; '
                                '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                                '} '
                                '</style>'
                                '<div class="field-error-sec2">'
                                'Silahkan pilih bulan kelulusan pendidikan terakhir'
                                '</div>',
                                unsafe_allow_html=True
                            )

                    bulan_app_idx = apply_date.month if apply_date else today.month

                    if last_edu_year is not None and 1990 <= last_edu_year <= current_year and bulan_lulus_idx is not None:
                        total_months = (app_year - int(last_edu_year)) * 12 + (bulan_app_idx - bulan_lulus_idx)
                        total_months = max(0, total_months)
                        gap_year = round(total_months / 12.0, 1)
                        st.session_state["gap_year"] = gap_year

                else:  # Hanya Mengetahui Tahun
                    col_year, = st.columns(1)
                    with col_year:
                        raw_edu_year = st.text_input(
                            "Tahun Terakhir Pendidikan / Kelulusan :red[*]",
                            placeholder="Contoh: 2021",
                            key="input_last_edu_year",
                            max_chars=4,
                            help=f"Masukkan 4 digit tahun kelulusan terakhir (1990 – {current_year})."
                        )
                        clean_edu_digits = "".join([c for c in raw_edu_year if c.isdigit()])
                        last_edu_year = int(clean_edu_digits) if len(clean_edu_digits) == 4 else None
                        st.session_state["last_edu_year"] = last_edu_year

                        if last_edu_year is not None and 1990 <= last_edu_year <= current_year:
                            st.session_state["sec2_year_err"] = False
                            gap_year = float(max(0, app_year - int(last_edu_year)))
                            st.session_state["gap_year"] = gap_year
                        else:
                            st.session_state["gap_year"] = 0.0

                        if st.session_state.get("sec2_year_err") and (last_edu_year is None or last_edu_year < 1990 or last_edu_year > current_year):
                            st.markdown(
                                '<style>'
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] [data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"] [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"] div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"] [data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stColumn"] div:has(> input) { '
                                '    border: 1.5px solid #EF4444 !important; '
                                '    border-color: #EF4444 !important; '
                                '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                                '} '
                                '</style>'
                                '<div class="field-error-sec2">'
                                'Silahkan masukkan tahun terakhir pendidikan/kelulusan'
                                '</div>',
                                unsafe_allow_html=True
                            )

                # Status apakah input tahun dan bulan sudah lengkap
                if gap_mode == "Mengetahui Bulan dan Tahun":
                    data_ok = (last_edu_year is not None and 1990 <= last_edu_year <= current_year and bulan_lulus is not None)
                else:
                    data_ok = (last_edu_year is not None and 1990 <= last_edu_year <= current_year)

                if not data_ok:
                    sec2_placeholder_html = (
                        '<div class="calc-box-placeholder">'
                        '<div class="calc-placeholder-icon">'
                        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1D4ED8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
                        '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>'
                        '</svg></div>'
                        '<div class="calc-placeholder-text">'
                        'Durasi jeda studi (gap) akan dihitung otomatis setelah data kelulusan diisi.'
                        '</div></div>'
                    )
                    st.markdown(sec2_placeholder_html, unsafe_allow_html=True)
            # DI LUAR inner_card_sec2, DI DALAM outer_card_sec2 (HASIL KALKULASI GAP TERPISAH)
            if data_ok:
                if gap_mode == "Mengetahui Bulan dan Tahun":
                    gap_val_text = f"{gap_year} Tahun"
                    gap_sub_badge = f'<span class="calc-subdetail-badge">({total_months} Bulan)</span>'
                    lulus_info = f"{bulan_lulus} {int(last_edu_year)}"
                else:
                    gap_val_text = f"{gap_year:.0f} Tahun"
                    gap_sub_badge = ""
                    lulus_info = f"Tahun {int(last_edu_year)}"

                sec2_result_html = (
                    '<div class="calc-box-result">'
                    '<div class="calc-avatar-icon">'
                    '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
                    '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>'
                    '</svg></div>'
                    '<div class="calc-col-age">'
                    '<div class="calc-label">Durasi Jeda Studi (Gap)</div>'
                    f'<div class="calc-val-age">{gap_val_text} {gap_sub_badge}</div>'
                    '</div>'
                    '<div class="calc-divider"></div>'
                    '<div class="calc-col-age">'
                    '<div class="calc-label">Kelulusan Terakhir</div>'
                    f'<div class="calc-val-age">{lulus_info}</div>'
                    '</div>'
                    '</div>'
                )
                st.markdown(sec2_result_html, unsafe_allow_html=True)

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            c_btn1, _, c_btn3 = st.columns([1.2, 3.2, 1.2])
            with c_btn1:
                if st.button("Kembali", key="btn_back_2", use_container_width=True):
                    st.session_state["sec2_year_err"] = False
                    st.session_state["sec2_month_err"] = False
                    st.session_state["sec2_error"] = None
                    st.session_state.current_section = 1
                    st.rerun()
            with c_btn3:
                if st.button("Selanjutnya", key="btn_next_2", use_container_width=True):
                    has_err = False
                    edu_yr = st.session_state.get("last_edu_year")
                    if edu_yr is None or edu_yr < 1990 or edu_yr > current_year:
                        st.session_state["sec2_year_err"] = True
                        has_err = True
                    else:
                        st.session_state["sec2_year_err"] = False

                    if gap_mode == "Mengetahui Bulan dan Tahun":
                        sel_bln = st.session_state.get("select_bulan_lulus") or bulan_lulus
                        if sel_bln is None:
                            st.session_state["sec2_month_err"] = True
                            has_err = True
                        else:
                            st.session_state["sec2_month_err"] = False
                    else:
                        st.session_state["sec2_month_err"] = False

                    if has_err:
                        st.rerun()
                    else:
                        st.session_state["sec2_year_err"] = False
                        st.session_state["sec2_month_err"] = False
                        st.session_state["sec2_error"] = None
                        st.session_state.current_section = 3
                        st.rerun()

        components.html("""
        <script>
        function bindSec2() {
            try {
                const doc = window.parent.document;
                const inputs = doc.querySelectorAll('div[class*="st-key-inner_card_sec2"] div[data-testid="stTextInput"] input');
                inputs.forEach(inp => {
                    const wrap = inp.closest('[data-testid="stTextInputRootElement"]') || inp.closest('div.react-aria-Group') || inp.closest('[data-baseweb="input"]') || inp.parentElement;
                    if (!wrap) return;

                    wrap.style.setProperty('position', 'relative', 'important');
                    inp.style.setProperty('padding-right', '36px', 'important');

                    let btn = wrap.querySelector('.st-custom-clear-btn');
                    if (!btn) {
                        btn = doc.createElement('div');
                        btn.className = 'st-custom-clear-btn';
                        btn.setAttribute('role', 'button');
                        btn.setAttribute('title', 'Hapus input');
                        btn.style.setProperty('display', 'none', 'important');
                        btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="display:block; pointer-events:none;">
                            <circle cx="12" cy="12" r="10" fill="#0284C7"></circle>
                            <path d="M15 9L9 15M9 9l6 6" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"></path>
                        </svg>`;
                        btn.addEventListener('mousedown', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                            nativeSetter.call(inp, '');
                            inp.dispatchEvent(new Event('input', { bubbles: true }));
                            inp.dispatchEvent(new Event('change', { bubbles: true }));
                            btn.style.setProperty('display', 'none', 'important');
                            inp.focus();
                        });
                        wrap.appendChild(btn);
                    }

                    const updateVisibility = () => {
                        const val = inp.value || "";
                        if (val.trim().length > 0) {
                            btn.style.setProperty('display', 'flex', 'important');
                        } else {
                            btn.style.setProperty('display', 'none', 'important');
                        }
                    };

                    if (!inp.dataset.sec2Bound) {
                        inp.dataset.sec2Bound = "true";
                        let timer = null;
                        inp.addEventListener('input', function() {
                            updateVisibility();
                            if (timer) clearTimeout(timer);
                            const digits = (this.value || "").replace(/\\D/g, "");
                            if (digits.length === 4) {
                                timer = setTimeout(() => {
                                    this.dispatchEvent(new Event('change', { bubbles: true }));
                                    this.blur();
                                }, 150);
                            }
                        });
                        inp.addEventListener('change', updateVisibility);
                        inp.addEventListener('keyup', updateVisibility);
                    }
                    updateVisibility();
                });
            } catch(e) {}
        }
        bindSec2();
        setTimeout(bindSec2, 50);
        setTimeout(bindSec2, 200);
        </script>
        """, height=0, width=0)

    # ---------------------------------------------------------
    # SECTION 3: JALUR STUDI (PATHWAY) & PILIHAN KAMPUS
    # ---------------------------------------------------------
    elif st.session_state.current_section == 3:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 03 / 04</div>'
            '<div class="main-step-title">Jalur Studi (Pathway) & Kampus Pilihan</div>'
            '<div class="main-step-desc">Pilih jenjang studi, kampus di Australia, dan durasi rencana studi.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec3"):
            with st.container(border=True, key="inner_card_sec3"):
                p1, p2 = st.columns(2)
                with p1:
                    campus_options = [
                        "Level 1 — University",
                        "Level 2 — Vocational / Polytechnic / TAFE",
                        "Level 3 — College / Private Institute"
                    ]
                    saved_c_idx = st.session_state.get("campus_level_idx", 0)
                    if saved_c_idx >= len(campus_options):
                        saved_c_idx = 0
                    campus_level_str = st.selectbox(
                        "Tingkat / Level Institusi",
                        options=campus_options,
                        index=saved_c_idx,
                        key="select_campus_level",
                        help="Kategori level institusi pendidikan di Australia (Level 1: University, Level 2: Vocational/Polytechnic/TAFE, Level 3: College/Private Institute).",
                        on_change=on_campus_level_change
                    )
                    if "Level 1" in campus_level_str:
                        st.session_state["campus_level_idx"] = 0
                        level_kampus = 1.0
                    elif "Level 2" in campus_level_str:
                        st.session_state["campus_level_idx"] = 1
                        level_kampus = 2.0
                    else:
                        st.session_state["campus_level_idx"] = 2
                        level_kampus = 3.0
                    st.session_state["level_kampus"] = level_kampus

                with p2:
                    _elicos_opts = ["Tidak", "Ya"]
                    _elicos_idx = st.session_state.get("has_elicos_idx", 0)
                    has_elicos = st.selectbox(
                        "Mengambil Kursus Bahasa (ELICOS)?",
                        options=_elicos_opts,
                        index=_elicos_idx,
                        key="select_has_elicos",
                        help="Pilih 'Ya' jika student mengambil kursus persiapan bahasa Inggris (ELICOS) sebelum memulai program studi utama."
                    )
                    st.session_state["has_elicos_idx"] = 1 if has_elicos == "Ya" else 0
                    st.session_state["has_elicos"] = has_elicos

                p3, p4 = st.columns(2)
                with p3:
                    _voc_opts = ["Tidak", "Ya"]
                    _voc_idx = st.session_state.get("has_vocational_idx", 0)
                    has_vocational = st.selectbox(
                        "Mengambil Jalur Kejuruan (Vocational/VET)?",
                        options=_voc_opts,
                        index=_voc_idx,
                        key="select_has_vocational",
                        help="Pilih 'Ya' jika student mengambil program kejuruan praktis seperti Certificate atau Diploma vokasi."
                    )
                    st.session_state["has_vocational_idx"] = 1 if has_vocational == "Ya" else 0
                    st.session_state["has_vocational"] = has_vocational

                with p4:
                    _higher_opts = ["Tidak", "Ya"]
                    _higher_idx = st.session_state.get("has_higher_idx", 1)
                    if _higher_idx >= len(_higher_opts):
                        _higher_idx = 1
                    has_higher = st.selectbox(
                        "Mengambil Pendidikan Tinggi (Higher Education)?",
                        options=_higher_opts,
                        index=_higher_idx,
                        key="select_has_higher",
                        help="Pilih 'Ya' jika student mengambil program gelar seperti Bachelor (S1), Master (S2), atau Doctoral (S3)."
                    )
                    st.session_state["has_higher_idx"] = 1 if has_higher == "Ya" else 0
                    st.session_state["has_higher"] = has_higher

            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            c_btn1, c_btn2, c_btn3 = st.columns([1.2, 3.2, 1.2])
            with c_btn1:
                if st.button("Kembali", key="btn_back_3", use_container_width=True):
                    st.session_state.current_section = 2
                    st.rerun()
            with c_btn3:
                if st.button("Selanjutnya", key="btn_next_3", use_container_width=True):
                    st.session_state.current_section = 4
                    st.rerun()

    # ---------------------------------------------------------
    # SECTION 4: PROFIL LATAR BELAKANG & RIWAYAT VISA
    # ---------------------------------------------------------
    elif st.session_state.current_section == 4:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 04 / 04</div>'
            '<div class="main-step-title">Latar Belakang Pendidikan & Riwayat Visa</div>'
            '<div class="main-step-desc">Lengkapi informasi kemampuan bahasa Inggris, kesiapan finansial, dan riwayat pengajuan visa.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec4"):
            with st.container(border=True, key="inner_card_sec4"):
                c1, c2 = st.columns(2)
                with c1:
                    ielts_val = st.text_input(
                        "Kemampuan Bahasa Inggris (Skor IELTS)",
                        value=st.session_state.get("ielts_input_str", ""),
                        key="ielts_raw_input",
                        placeholder="Contoh: 6.0",
                        help="Masukkan skor keseluruhan (Overall Band Score) IELTS student (skala 1.0 - 9.0).",
                        on_change=on_ielts_change
                    )
                    st.session_state["ielts_input_str"] = ielts_val
                    raw_ielts_str = str(ielts_val).strip()
                    try:
                        clean_ielts = raw_ielts_str.replace(",", ".")
                        english_prof = float(clean_ielts) if clean_ielts else None
                    except ValueError:
                        english_prof = None
                    st.session_state["english_prof"] = english_prof

                    is_ielts_invalid = st.session_state.get("ielts_show_error", False) and (english_prof is None or english_prof < 1.0 or english_prof > 9.0)
                    if not is_ielts_invalid and raw_ielts_str and (english_prof is None or english_prof < 1.0 or english_prof > 9.0):
                        is_ielts_invalid = True
                    if is_ielts_invalid:
                        ielts_err_text = "Silahkan masukkan skor IELTS" if not raw_ielts_str else "Skor resmi IELTS harus berada pada rentang 1.0 hingga 9.0"
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-ielts_raw_input"] [data-baseweb="input"], '
                            'div[class*="st-key-ielts_raw_input"] [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-ielts_raw_input"] div:has(> input), '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:first-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:first-child [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="stColumn"]:first-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="stColumn"]:first-child [data-testid="stTextInputRootElement"] { '
                            '    border: 1.5px solid #EF4444 !important; '
                            '    border-color: #EF4444 !important; '
                            '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                            '} '
                            '</style>'
                            f'<div class="field-error-sec4">{ielts_err_text}</div>',
                            unsafe_allow_html=True
                        )
                    elif english_prof and 1.0 <= english_prof <= 9.0:
                        st.session_state["ielts_show_error"] = False

                with c2:
                    fin_ret = st.text_input(
                        "Kesiapan Finansial / Tabungan (Rupiah)",
                        value=st.session_state.fin_input_str,
                        key="fin_raw_input",
                        placeholder="Contoh: 500.000.000",
                        help="Estimasi dana tabungan atau bukti kesiapan finansial yang dimiliki untuk mendukung biaya studi dan hidup di Australia (dalam Rupiah).",
                        on_change=on_financial_change
                    )
                    fin_src = fin_ret if fin_ret is not None else st.session_state.get("fin_raw_input", st.session_state.get("fin_input_str", ""))
                    digits_only = "".join([c for c in str(fin_src) if c.isdigit()])
                    financial_nominal = float(digits_only) if digits_only else None
                    st.session_state["financial_nominal"] = financial_nominal

                    raw_fin = str(st.session_state.get("fin_input_str", "")).strip()
                    is_fin_invalid = st.session_state.get("fin_show_error", False) and (financial_nominal is None or financial_nominal < 10_000_000)
                    if not is_fin_invalid and raw_fin and (financial_nominal is None or financial_nominal < 10_000_000):
                        is_fin_invalid = True
                    if is_fin_invalid:
                        fin_err_text = "Silahkan masukkan nominal tabungan/finansial" if not raw_fin else "Format belum lengkap, contoh: 500.000.000 (minimal Rp 10.000.000)"
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-fin_raw_input"] [data-baseweb="input"], '
                            'div[class*="st-key-fin_raw_input"] [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-fin_raw_input"] div:has(> input), '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:last-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:last-child [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="stColumn"]:last-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="stColumn"]:last-child [data-testid="stTextInputRootElement"] { '
                            '    border: 1.5px solid #EF4444 !important; '
                            '    border-color: #EF4444 !important; '
                            '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                            '} '
                            '</style>'
                            f'<div class="field-error-sec4">{fin_err_text}</div>',
                            unsafe_allow_html=True
                        )
                    elif financial_nominal and financial_nominal >= 10_000_000:
                        st.session_state["fin_show_error"] = False

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                r1, r2, r3 = st.columns(3)
                with r1:
                    _rm_opts = ["Sesuai / Linier", "Tidak / Lintas Jurusan"]
                    _rm_idx = st.session_state.get("related_major_idx", 0)
                    related_major = st.selectbox(
                        "Kesesuaian Jurusan",
                        options=_rm_opts,
                        index=_rm_idx,
                        key="select_related_major",
                        help="Kesesuaian program studi yang dituju di Australia dengan latar belakang pendidikan atau riwayat kerja sebelumnya."
                    )
                    st.session_state["related_major_idx"] = 0 if "Sesuai" in related_major else 1
                    st.session_state["related_major"] = related_major

                with r2:
                    _ec_opts = ["Iya", "Tidak"]
                    _ec_idx = st.session_state.get("emp_continuity_idx", 0)
                    emp_continuity = st.selectbox(
                        "Aktivitas Selama Gap",
                        options=_ec_opts,
                        index=_ec_idx,
                        key="select_emp_continuity",
                        help="Apakah student memiliki aktivitas kerja, magang, atau pengalaman profesional yang jelas selama jeda studi (gap)."
                    )
                    st.session_state["emp_continuity_idx"] = 0 if emp_continuity == "Iya" else 1
                    st.session_state["emp_continuity"] = emp_continuity

                with r3:
                    _hr_opts = ["Tidak", "Pernah"]
                    _hr_idx = st.session_state.get("has_refusal_idx", 0)
                    has_refusal = st.selectbox(
                        "Riwayat Penolakan Visa",
                        options=_hr_opts,
                        index=_hr_idx,
                        key="select_has_refusal",
                        help="Apakah student pernah memiliki riwayat penolakan visa Australia atau visa negara lain sebelumnya."
                    )
                    st.session_state["has_refusal_idx"] = 0 if has_refusal == "Tidak" else 1
                    st.session_state["has_refusal"] = has_refusal

            c_btn1, c_btn2, c_btn3 = st.columns([1.2, 3.2, 1.4])
            with c_btn1:
                if st.button("Kembali", key="btn_back_4", use_container_width=True):
                    st.session_state["sec4_error"] = None
                    st.session_state["ielts_show_error"] = False
                    st.session_state["fin_show_error"] = False
                    st.session_state.current_section = 3
                    st.rerun()
            with c_btn3:
                if st.button("Prediksi", key="btn_submit", type="primary", use_container_width=True):
                    eng_val = st.session_state.get("english_prof")
                    fin_val = st.session_state.get("financial_nominal")

                    has_err = False
                    if eng_val is None or eng_val < 1.0 or eng_val > 9.0:
                        st.session_state["ielts_show_error"] = True
                        has_err = True
                    else:
                        st.session_state["ielts_show_error"] = False

                    if not fin_val or fin_val < 10_000_000:
                        st.session_state["fin_show_error"] = True
                        has_err = True
                    else:
                        st.session_state["fin_show_error"] = False

                    if has_err:
                        st.session_state["sec4_error"] = None
                        st.rerun()
                    else:
                        st.session_state["sec4_error"] = None
                        st.session_state["ielts_show_error"] = False
                        st.session_state["fin_show_error"] = False
                        st.session_state.current_section = 5
                        st.rerun()

        components.html("""
        <script>
        function bindSec4Clear() {
            try {
                const doc = window.parent.document;
                const inputs = doc.querySelectorAll('div[class*="st-key-inner_card_sec4"] div[data-testid="stTextInput"] input');
                inputs.forEach(inp => {
                    const wrap = inp.closest('[data-testid="stTextInputRootElement"]') || inp.closest('div.react-aria-Group') || inp.closest('[data-baseweb="input"]') || inp.parentElement;
                    if (!wrap) return;

                    wrap.style.setProperty('position', 'relative', 'important');
                    inp.style.setProperty('padding-right', '36px', 'important');

                    let btn = wrap.querySelector('.st-custom-clear-btn');
                    if (!btn) {
                        btn = doc.createElement('div');
                        btn.className = 'st-custom-clear-btn';
                        btn.setAttribute('role', 'button');
                        btn.setAttribute('title', 'Hapus input');
                        btn.style.setProperty('display', 'none', 'important');
                        btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="display:block; pointer-events:none;">
                            <circle cx="12" cy="12" r="10" fill="#0284C7"></circle>
                            <path d="M15 9L9 15M9 9l6 6" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"></path>
                        </svg>`;
                        btn.addEventListener('mousedown', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                            nativeSetter.call(inp, '');
                            inp.dispatchEvent(new Event('input', { bubbles: true }));
                            inp.dispatchEvent(new Event('change', { bubbles: true }));
                            btn.style.setProperty('display', 'none', 'important');
                            inp.focus();
                        });
                        wrap.appendChild(btn);
                    }

                    const updateVisibility = () => {
                        const val = inp.value || "";
                        if (val.trim().length > 0) {
                            btn.style.setProperty('display', 'flex', 'important');
                        } else {
                            btn.style.setProperty('display', 'none', 'important');
                        }
                    };

                    if (!inp.dataset.sec4ClearBound) {
                        inp.dataset.sec4ClearBound = "true";
                        inp.addEventListener('input', updateVisibility);
                        inp.addEventListener('change', updateVisibility);
                        inp.addEventListener('keyup', updateVisibility);
                    }
                    updateVisibility();
                });
            } catch(e) {}
        }
        bindSec4Clear();
        setTimeout(bindSec4Clear, 50);
        setTimeout(bindSec4Clear, 200);
        </script>
        """, height=0, width=0)

# =============================================================
# SECTION 5: HASIL PREDIKSI & EVALUASI PROFIL
# =============================================================
elif st.session_state.current_section == 5:
    # 1. Pastikan usia & tahun pengajuan dihitung dari tanggal lahir & apply terkini
    birth_date = st.session_state.get("birth_date")
    apply_date = st.session_state.get("apply_date")
    if birth_date and apply_date and apply_date >= birth_date:
        calculated_age = apply_date.year - birth_date.year - ((apply_date.month, apply_date.day) < (birth_date.month, birth_date.day))
        age_val = max(15, min(65, calculated_age))
        app_year = apply_date.year
        st.session_state["age_val"] = age_val
        st.session_state["app_year"] = app_year
    else:
        age_val = float(st.session_state.get("age_val", 24.0))
        app_year = float(st.session_state.get("app_year", current_year))

    # 2. Pastikan jeda studi (gap) dihitung dari tahun kelulusan & mode terkini
    last_edu_year = st.session_state.get("last_edu_year")
    gap_mode = st.session_state.get("gap_mode", "Mengetahui Bulan dan Tahun")
    bulan_lulus_idx = st.session_state.get("bulan_lulus_idx")
    if last_edu_year is not None:
        if gap_mode == "Mengetahui Bulan dan Tahun" and bulan_lulus_idx is not None and apply_date:
            total_months = (int(app_year) - int(last_edu_year)) * 12 + (apply_date.month - (int(bulan_lulus_idx) + 1))
            gap_year = round(max(0, total_months) / 12.0, 1)
        else:
            gap_year = float(max(0, int(app_year) - int(last_edu_year)))
        st.session_state["gap_year"] = gap_year
    else:
        gap_year = float(st.session_state.get("gap_year", 1.0))
        last_edu_year = 2022.0

    # 3. Ambil seluruh input profil terkini dengan resolusi ganda (widget key & session state)
    campus_sel = str(st.session_state.get("select_campus_level", ""))
    if "Level 1" in campus_sel:
        level_kampus = 1.0
        st.session_state["campus_level_idx"] = 0
    elif "Level 2" in campus_sel:
        level_kampus = 2.0
        st.session_state["campus_level_idx"] = 1
    elif "Level 3" in campus_sel:
        level_kampus = 3.0
        st.session_state["campus_level_idx"] = 2
    else:
        c_idx = st.session_state.get("campus_level_idx")
        if c_idx is not None:
            level_kampus = float(int(c_idx) + 1)
        else:
            level_kampus = float(st.session_state.get("level_kampus", 1.0) or 1.0)
    st.session_state["level_kampus"] = level_kampus

    elicos_sel = str(st.session_state.get("select_has_elicos", ""))
    has_elicos = elicos_sel if elicos_sel in ["Ya", "Tidak"] else str(st.session_state.get("has_elicos", "Tidak"))
    st.session_state["has_elicos"] = has_elicos

    voc_sel = str(st.session_state.get("select_has_vocational", ""))
    has_vocational = voc_sel if voc_sel in ["Ya", "Tidak"] else str(st.session_state.get("has_vocational", "Tidak"))
    st.session_state["has_vocational"] = has_vocational

    higher_sel = str(st.session_state.get("select_has_higher", ""))
    has_higher = higher_sel if higher_sel in ["Ya", "Tidak"] else str(st.session_state.get("has_higher", "Ya"))
    st.session_state["has_higher"] = has_higher

    rm_sel = str(st.session_state.get("select_related_major", ""))
    related_major = rm_sel if ("Sesuai" in rm_sel or "Tidak" in rm_sel) else str(st.session_state.get("related_major", "Sesuai / Linier"))
    st.session_state["related_major"] = related_major

    ec_sel = str(st.session_state.get("select_emp_continuity", ""))
    emp_continuity = ec_sel if ec_sel in ["Iya", "Tidak"] else str(st.session_state.get("emp_continuity", "Iya"))
    st.session_state["emp_continuity"] = emp_continuity

    hr_sel = str(st.session_state.get("select_has_refusal", ""))
    has_refusal = hr_sel if hr_sel in ["Pernah", "Tidak"] else str(st.session_state.get("has_refusal", "Tidak"))
    st.session_state["has_refusal"] = has_refusal

    financial_nominal = float(st.session_state.get("financial_nominal", 500000000.0) or 500000000.0)
    english_prof = float(st.session_state.get("english_prof", 6.0) or 6.0)

    input_payload = {
        'Financial': float(financial_nominal),
        'Age': float(age_val),
        'Gap_Year': float(gap_year),
        'Last_Education_Year': float(last_edu_year),
        'Application_Year': float(app_year),
        'Level_Kampus': float(level_kampus),
        'English_Proficiency': float(english_prof),
        'English_Proficiency_Cleaned': float(english_prof),
        'Related_Major': 1 if "Sesuai" in related_major else 0,
        'Has_Refusal': 1 if "Pernah" in has_refusal else 0,
        'Employment_Continuity': 1 if emp_continuity == "Iya" else 0,
        'Has_ELICOS': 1 if has_elicos == "Ya" else 0,
        'Has_Vocational': 1 if has_vocational == "Ya" else 0,
        'Has_Higher': 1 if has_higher == "Ya" else 0
    }

    input_df = pd.DataFrame([input_payload])[model_features]
    pred_proba = model.predict_proba(input_df)[0]
    p_refusal = pred_proba[0] * 100
    p_grant = pred_proba[1] * 100

    if p_grant > 99.0:
        p_grant = 99.0
        p_refusal = 1.0
    elif p_refusal > 99.0:
        p_refusal = 99.0
        p_grant = 1.0

    # Auto-sinkronisasi tab aktif sesuai dengan hasil prediksi dominan terbaru
    current_winner = "grant" if p_grant >= p_refusal else "refusal"
    if "last_pred_winner" not in st.session_state or st.session_state["last_pred_winner"] != current_winner:
        st.session_state["last_pred_winner"] = current_winner
        st.session_state.active_result_view = current_winner

    # Analisis SHAP
    shap_out = explainer(input_df)
    if len(shap_out.values.shape) == 3:
        raw_shap = shap_out.values[0, :, 1]
    else:
        raw_shap = shap_out.values[0]

    total_abs_shap = np.sum(np.abs(raw_shap))
    if total_abs_shap == 0:
        total_abs_shap = 1e-6
    shap_percentages = (raw_shap / total_abs_shap) * 100

    friendly_names = {
        'Financial': 'Kondisi finansial',
        'Employment_Continuity': 'Aktivitas selama masa jeda studi',
        'Age': 'Usia',
        'Related_Major': 'Kesesuaian latar belakang pendidikan dengan jurusan',
        'Level_Kampus': 'Pilihan level institusi',
        'Has_Refusal': 'Riwayat penolakan visa',
        'Gap_Year': 'Durasi jeda studi (gap)',
        'English_Proficiency': 'Kemahiran bahasa Inggris',
        'English_Proficiency_Cleaned': 'Kemahiran bahasa Inggris',
        'Has_Higher': 'Jalur Higher Education',
        'Has_Vocational': 'Jalur Vocational',
        'Has_ELICOS': 'Jalur ELICOS',
        'Last_Education_Year': 'Tahun kelulusan terakhir',
        'Application_Year': 'Waktu pengajuan aplikasi'
    }

    df_shap_all = pd.DataFrame({
        'Faktor': [friendly_names.get(col, col) for col in model_features],
        'Dampak': np.abs(raw_shap),
        'Raw_SHAP': raw_shap,
        'Persen': shap_percentages
    })

    # Penjelasan dinamis yang menyesuaikan dengan profil yang dipilih
    if level_kampus == 1.0:
        campus_grant_reason = "Pilihan institusi Level 1 (University) memiliki reputasi prima dan profil risiko imigrasi yang sangat rendah, sehingga sangat memperkuat peluang persetujuan visa."
        campus_refusal_reason = "Meskipun memilih institusi Level 1 (University), pastikan seluruh dokumen pendukung dan Genuine Student Statement disusun secara meyakinkan."
    elif level_kampus == 2.0:
        campus_grant_reason = "Pilihan institusi Level 2 (Vocational / TAFE) memiliki jalur kejuruan terstruktur dengan rekam jejak kepatuhan visa yang baik."
        campus_refusal_reason = "Pilihan institusi Level 2 (Vocational / TAFE) memerlukan justifikasi rencana studi yang konkret agar selaras dengan riwayat pendidikan dan tujuan karier."
    else:
        campus_grant_reason = "Pilihan institusi Level 3 (College) tetap dapat disetujui selama didukung bukti pembiayaan dan kualifikasi akademik yang lengkap."
        campus_refusal_reason = "Pilihan kampus Level 3 (College / Private Institute) memiliki risiko pengawasan imigrasi yang lebih ketat, sehingga memerlukan pemenuhan dokumen finansial dan bukti Genuine Student yang sangat kuat."

    reason_explanations_grant = {
        'Kondisi finansial': f"Kondisi finansial dinilai memadai (Rp {financial_nominal:,.0f}) untuk menopang biaya pendidikan dan kebutuhan hidup selama studi di Australia.",
        'Aktivitas selama masa jeda studi': "Kesinambungan aktivitas selama masa jeda terisi dengan baik melalui pekerjaan atau kegiatan produktif yang relevan.",
        'Usia': f"Usia student ({age_val:.0f} tahun) berada dalam rentang yang wajar dan didukung profil studi yang konsisten.",
        'Kesesuaian latar belakang pendidikan dengan jurusan': "Latar belakang pendidikan atau pengalaman kerja sebelumnya selaras dan konsisten dengan program studi yang dituju di Australia.",
        'Pilihan level institusi': campus_grant_reason,
        'Riwayat penolakan visa': "Student tidak memiliki catatan penolakan visa sebelumnya, yang memberikan nilai positif terhadap profil pengajuan.",
        'Kemahiran bahasa Inggris': f"Kemampuan bahasa Inggris (IELTS {english_prof:.1f}) memenuhi standar persyaratan minimum studi yang dituju.",
        'Durasi jeda studi (gap)': f"Durasi jeda studi ({gap_year:.1f} tahun) tergolong moderat dan dapat dipertanggungjawabkan dengan baik.",
        'Jalur ELICOS': "Program persiapan bahasa (ELICOS) mendukung kesiapan akademik sebelum menempuh program utama.",
        'Jalur Vocational': "Program kejuruan yang dipilih relevan dengan jalur pengembangan karier terapan.",
        'Jalur Higher Education': "Jalur Higher Education (S1/S2) memberikan nilai akademis yang kuat dan meyakinkan bagi imigrasi.",
        'Waktu pengajuan aplikasi': "Waktu pengajuan visa relatif dekat dengan masa kelulusan, mencerminkan kesinambungan rencana studi yang konsisten.",
        'Tahun kelulusan terakhir': "Tahun kelulusan terakhir tergolong segar dan mendukung kontinuitas rekam jejak akademik student."
    }

    reason_explanations_refusal = {
        'Kondisi finansial': f"Kondisi finansial (Rp {financial_nominal:,.0f}) masih perlu diperkuat dengan memastikan dana yang tersedia memadai untuk biaya hidup dan tuition fee (patokan minimum acuan ~Rp450 juta) serta didukung bukti sumber dana yang jelas.",
        'Aktivitas selama masa jeda studi': "Apabila terdapat masa jeda (gap), pengalaman kerja, usaha, atau aktivitas produktif perlu didokumentasikan dengan bukti tertulis agar tidak menjadi celah kecurigaan imigrasi.",
        'Usia': f"Usia student ({age_val:.0f} tahun) perlu diselaraskan dengan alasan kuat melanjutkan studi, riwayat pendidikan, dan prospek karier saat kembali ke negara asal.",
        'Kesesuaian latar belakang pendidikan dengan jurusan': "Kesesuaian jurusan perlu diperkuat dengan penjelasan tertulis (Genuine Student Statement) mengenai alasan berpindah bidang studi.",
        'Pilihan level institusi': campus_refusal_reason,
        'Riwayat penolakan visa': "Adanya riwayat penolakan visa sebelumnya merupakan faktor risiko signifikan. Wajib melampirkan penjelasan perbaikan profil yang substansial.",
        'Kemahiran bahasa Inggris': f"Kemampuan bahasa Inggris (IELTS {english_prof:.1f}) masih perlu ditingkatkan atau dilengkapi dengan paket kursus ELICOS sebelum memulai perkuliahan utama.",
        'Durasi jeda studi (gap)': f"Jeda studi ({gap_year:.1f} tahun) yang cukup panjang tanpa dokumentasi aktivitas yang jelas berpotensi menurunkan tingkat keyakinan petugas visa terhadap kriteria Genuine Student.",
        'Jalur ELICOS': "Perlu memastikan durasi ELICOS proporsional dan tidak terkesan hanya memperpanjang masa tinggal di Australia.",
        'Jalur Vocational': "Pilihan diploma/vokasi untuk pelamar dengan latar belakang yang sudah tinggi rentan dinilai non-genuine student.",
        'Jalur Higher Education': "Perlu memastikan rencana pembiayaan program Higher Education terjamin hingga masa akhir studi.",
        'Waktu pengajuan aplikasi': "Jarak waktu antara kelulusan dan tahun pengajuan aplikasi memerlukan klarifikasi tertulis mengenai aktivitas yang dilakukan selama masa tunggu.",
        'Tahun kelulusan terakhir': "Jeda waktu yang cukup lama sejak tahun kelulusan terakhir memerlukan pembuktian komitmen studi kembali (Genuine Student)."
    }

    st.markdown(
        '<div class="main-page-header">'
        '<div class="main-step-eyebrow">HASIL EVALUASI</div>'
        '<div class="main-step-title">Hasil Prediksi & Evaluasi Profil</div>'
        '<div class="main-step-desc">Klik salah satu card di bawah untuk melihat rincian faktor pendukung secara terpisah.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="reminder-box-prev">
<div class="reminder-circle-icon">!</div>
<div class="reminder-content-text">
<strong>Reminder:</strong> Keputusan akhir visa sepenuhnya merupakan hak prerogatif Department of Home Affairs (Imigrasi Australia).
</div>
</div>
""", unsafe_allow_html=True)

    card_col1, card_col2 = st.columns(2)
    active_tab = st.session_state.active_result_view

    grant_fmt = f"{p_grant:.1f}%" if (p_grant % 1 != 0) else f"{p_grant:.0f}%"
    refusal_fmt = f"{p_refusal:.1f}%" if (p_refusal % 1 != 0) else f"{p_refusal:.0f}%"

    with card_col1:
        grant_btn_content = f"{grant_fmt}\nDISETUJUI (GRANT)"
        if st.button(
            grant_btn_content,
            key="direct_card_grant",
            use_container_width=True
        ):
            st.session_state.active_result_view = "grant"
            st.rerun()

    with card_col2:
        refusal_btn_content = f"{refusal_fmt}\nDITOLAK (REFUSAL)"
        if st.button(
            refusal_btn_content,
            key="direct_card_refusal",
            use_container_width=True
        ):
            st.session_state.active_result_view = "refusal"
            st.rerun()

    if active_tab == "grant":
        st.markdown(
            '<div class="result-breakdown-header">'
            '<div class="result-breakdown-icon grant-icon">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="20 6 9 17 4 12"></polyline>'
            '</svg>'
            '</div>'
            '<div class="result-breakdown-titles">'
            '<div class="result-breakdown-title">Faktor Pendukung Prediksi Disetujui (Grant)</div>'
            '<div class="result-breakdown-subtitle">Daftar atribut pelamar yang berkontribusi positif memperkuat profil persetujuan visa:</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Exclude 'Pilihan level institusi' dari loop SHAP — ditampilkan secara eksplisit berdasarkan level
        shap_positives = df_shap_all[
            (df_shap_all['Raw_SHAP'] > 0.001) &
            (df_shap_all['Faktor'] != 'Pilihan level institusi')
        ].sort_values(by='Raw_SHAP', ascending=False)
        shown_count = 0
        for _, row in shap_positives.iterrows():
            faktor = row['Faktor']
            pct = row['Persen']
            shown_count += 1
            expl = reason_explanations_grant.get(faktor, "Faktor ini memberikan pengaruh positif terhadap profil pengajuan.")
            st.markdown(
                f'<div class="recom-item-clean grant-item"><span class="recom-title-clean">{faktor} (+{pct:.0f}%):</span> {expl}</div>',
                unsafe_allow_html=True
            )

        # Tampilkan card Pilihan level institusi berdasarkan level kampus yang dipilih (bukan dari arah SHAP)
        # Level 1 & 2 = mendukung grant → tampil di Grant tab
        # Level 3 = risiko lebih tinggi → tampil di Refusal tab
        campus_level_row = df_shap_all[df_shap_all['Faktor'] == 'Pilihan level institusi']
        campus_pct_val = abs(campus_level_row['Persen'].values[0]) if len(campus_level_row) > 0 else 0
        if level_kampus in (1.0, 2.0):
            st.markdown(
                f'<div class="recom-item-clean grant-item"><span class="recom-title-clean">Pilihan level institusi (+{campus_pct_val:.0f}%):</span> {campus_grant_reason}</div>',
                unsafe_allow_html=True
            )

        if input_payload['Has_Refusal'] == 0 and 'Riwayat penolakan visa' not in shap_positives['Faktor'].values:
            st.markdown(
                f'<div class="recom-item-clean grant-item"><span class="recom-title-clean">Riwayat Bersih:</span> {reason_explanations_grant["Riwayat penolakan visa"]}</div>',
                unsafe_allow_html=True
            )

        if shown_count == 0:
            st.info("Peluang grant didukung oleh kombinasi rata-rata atribut profil yang memenuhi syarat dasar.")

    else:
        st.markdown(
            '<div class="result-breakdown-header">'
            '<div class="result-breakdown-icon refusal-icon">'
            '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"></circle>'
            '<line x1="12" y1="8" x2="12" y2="12"></line>'
            '<line x1="12" y1="16" x2="12.01" y2="16"></line>'
            '</svg>'
            '</div>'
            '<div class="result-breakdown-titles">'
            '<div class="result-breakdown-title">Faktor Risiko Prediksi Ditolak (Refusal)</div>'
            '<div class="result-breakdown-subtitle">Daftar atribut pelamar yang menjadi faktor risiko atau area yang memerlukan perbaikan dokumen:</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        # Exclude 'Pilihan level institusi' dari loop SHAP — ditampilkan secara eksplisit berdasarkan level
        shap_negatives = df_shap_all[
            (df_shap_all['Raw_SHAP'] < -0.001) &
            (df_shap_all['Faktor'] != 'Pilihan level institusi')
        ].sort_values(by='Raw_SHAP', ascending=True)
        shown_risk_count = 0
        for _, row in shap_negatives.iterrows():
            faktor = row['Faktor']
            pct = row['Persen']
            shown_risk_count += 1
            expl = reason_explanations_refusal.get(faktor, "Faktor ini berkontribusi terhadap potensi risiko penolakan visa.")
            st.markdown(
                f'<div class="recom-item-clean refusal-item"><span class="recom-title-clean">{faktor} ({pct:.0f}%):</span> {expl}</div>',
                unsafe_allow_html=True
            )

        # Tampilkan card Pilihan level institusi berdasarkan level kampus yang dipilih (bukan dari arah SHAP)
        # Level 3 = risiko lebih tinggi → tampil di Refusal tab
        # Level 1 & 2 sudah ditampilkan di Grant tab
        campus_level_row_r = df_shap_all[df_shap_all['Faktor'] == 'Pilihan level institusi']
        campus_pct_val_r = abs(campus_level_row_r['Persen'].values[0]) if len(campus_level_row_r) > 0 else 0
        if level_kampus == 3.0:
            st.markdown(
                f'<div class="recom-item-clean refusal-item"><span class="recom-title-clean">Pilihan level institusi (-{campus_pct_val_r:.0f}%):</span> {campus_refusal_reason}</div>',
                unsafe_allow_html=True
            )

        if input_payload['Financial'] < 450000000 and 'Kondisi finansial' not in shap_negatives['Faktor'].values:
            st.markdown(
                f'<div class="recom-item-clean refusal-item"><span class="recom-title-clean">Kondisi Finansial (Perhatian Khusus):</span> {reason_explanations_refusal["Kondisi finansial"]}</div>',
                unsafe_allow_html=True
            )

        if input_payload['Has_Refusal'] == 1 and 'Riwayat penolakan visa' not in shap_negatives['Faktor'].values:
            st.markdown(
                f'<div class="recom-item-clean refusal-item"><span class="recom-title-clean">Riwayat Penolakan Visa (Perhatian Khusus):</span> {reason_explanations_refusal["Riwayat penolakan visa"]}</div>',
                unsafe_allow_html=True
            )

        if input_payload['Related_Major'] == 0 and 'Kesesuaian latar belakang dengan jurusan' not in shap_negatives['Faktor'].values:
            st.markdown(
                f'<div class="recom-item-clean refusal-item"><span class="recom-title-clean">Kesesuaian Jurusan (Lintas Bidang):</span> {reason_explanations_refusal["Kesesuaian latar belakang dengan jurusan"]}</div>',
                unsafe_allow_html=True
            )

        if shown_risk_count == 0 and input_payload['Financial'] >= 450000000 and input_payload['Has_Refusal'] == 0:
            st.success("Tidak terdeteksi faktor risiko penolakan yang signifikan pada profil pengajuan ini.")


    # ==============================================================================
    # DIREKTORI KAMPUS MITRA OSS BALI (COLORED BORDER - BLUE ACCENT)
    # ==============================================================================
    oss_college_url = "https://onestepsolutionbali.com/user/college"
    
    with st.container(border=True, key="card_oss_directory"):
        col_dir_txt, col_dir_btn = st.columns([3.3, 1.7])
        with col_dir_txt:
            st.markdown(
                '<div style="padding: 6px 0 4px 0;">'
                '<div style="font-size: 14px; font-weight: 700; color: #0284C7; margin-bottom: 6px; display: flex; align-items: center; gap: 7px; line-height: 1.4;">'
                'Direktori Kampus Mitra OSS Bali'
                '</div>'
                '<div style="font-size: 12.5px; color: #334155; line-height: 1.55; margin: 0; padding-bottom: 4px;">'
                'Untuk mengeksplorasi alternatif institusi pendidikan atau mencari program studi lain yang sesuai dengan minat calon mahasiswa, Anda dapat meninjau katalog mitra resmi One Step Solution Bali.'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with col_dir_btn:
            st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
            st.link_button("Buka Direktori Kampus ↗", url=oss_college_url, use_container_width=True)

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
    c_rst1, c_rst2 = st.columns(2)
    with c_rst1:
        if st.button("✎  Edit Data Pengajuan", key="btn_edit_submission", use_container_width=True):
            st.session_state.max_unlocked_step = 5
            st.session_state.current_section = 1
            st.rerun()
    with c_rst2:
        if st.button("✓  Selesai / Pengajuan Baru", key="btn_finish_submission", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.current_section = 1
            st.session_state.fin_input_str = ""
            st.session_state.ielts_input_str = ""
            st.session_state.active_result_view = "grant"
            st.rerun()
