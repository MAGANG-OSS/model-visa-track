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
        padding-bottom: 3rem !important;
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
        overflow: hidden !important;
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
        overflow-y: hidden !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
        overflow: hidden !important;
        overflow-y: hidden !important;
    }
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background: transparent !important;
        padding-top: 14px !important;
        padding-bottom: 14px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
        overflow-y: hidden !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Sidebar Brand */
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
        color: rgba(255, 255, 255, 0.8);
        font-size: 12px;
        line-height: 1.45;
        margin-top: 8px;
        font-family: 'Poppins', sans-serif;
    }

    /* Sidebar Stepper Menu */
    .sidebar-stepper-menu {
        display: flex;
        flex-direction: column;
        gap: 0;
        margin-top: 10px;
    }
    .sidebar-step-row {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        position: relative;
    }
    .sidebar-step-node {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 30px;
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
    .sidebar-step-connector {
        width: 2px;
        height: 28px;
        border-left: 2px dashed rgba(255, 255, 255, 0.35);
        margin: 3px 0;
    }
    .sidebar-step-content {
        display: flex;
        flex-direction: column;
        padding-top: 3px;
        padding-bottom: 10px;
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

    /* Sidebar Footer */
    .sidebar-footer-text {
        color: rgba(255, 255, 255, 0.45);
        font-size: 11px;
        white-space: nowrap !important;
        margin-top: 64px;
        padding-top: 8px;
        font-family: 'Poppins', sans-serif;
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
    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-baseweb="input"],
    div[data-baseweb="select"] > div {
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
    div[data-baseweb="input"]:hover,
    div[data-testid="stSelectbox"] div.react-aria-Group:hover,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"]:hover,
    div[data-testid="stSelectbox"] div[role="group"]:hover,
    div[data-testid="stSelectbox"] div:has(> input):hover,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:hover {
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
    div[data-baseweb="input"]:focus-within,
    div[data-testid="stSelectbox"] div.react-aria-Group:focus-within,
    div[data-testid="stSelectbox"] div[class*="e1oobldh0"]:focus-within,
    div[data-testid="stSelectbox"] div[role="group"]:focus-within,
    div[data-testid="stSelectbox"] div:has(> input):focus-within,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
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

    /* Error Border Section 2 */
    div[data-testid="column"]:has(.field-error-sec2) [data-testid="stTextInputRootElement"],
    div[data-testid="column"]:has(.field-error-sec2) div.react-aria-Group,
    div[data-testid="column"]:has(.field-error-sec2) [data-baseweb="input"],
    div[data-testid="column"]:has(.field-error-sec2) [data-baseweb="select"] > div,
    div[class*="st-key-inner_card_sec2"] div:has(> .field-error-sec2) [data-testid="stTextInputRootElement"],
    div[class*="st-key-inner_card_sec2"] div:has(> .field-error-sec2) [data-baseweb="input"],
    div[class*="st-key-inner_card_sec2"] div:has(> .field-error-sec2) [data-baseweb="select"] > div,
    div[class*="st-key-inner_card_sec2"] div:has(> div .field-error-sec2) [data-testid="stTextInputRootElement"],
    div[class*="st-key-inner_card_sec2"] div:has(> div .field-error-sec2) [data-baseweb="input"],
    div[class*="st-key-inner_card_sec2"] div:has(> div .field-error-sec2) [data-baseweb="select"] > div {
        border: 1.5px solid #EF4444 !important;
        border-color: #EF4444 !important;
        box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important;
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

    /* Error Border Section 4 */
    div[data-testid="column"]:has(.field-error-sec4) [data-testid="stTextInputRootElement"],
    div[data-testid="column"]:has(.field-error-sec4) div.react-aria-Group,
    div[data-testid="column"]:has(.field-error-sec4) [data-baseweb="input"],
    div[class*="st-key-inner_card_sec4"] div:has(> .field-error-sec4) [data-testid="stTextInputRootElement"],
    div[class*="st-key-inner_card_sec4"] div:has(> .field-error-sec4) [data-baseweb="input"],
    div[class*="st-key-inner_card_sec4"] div:has(> div .field-error-sec4) [data-testid="stTextInputRootElement"],
    div[class*="st-key-inner_card_sec4"] div:has(> div .field-error-sec4) [data-baseweb="input"] {
        border: 1.5px solid #EF4444 !important;
        border-color: #EF4444 !important;
        box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important;
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
</style>
""", unsafe_allow_html=True)

# Inject Poppins into parent document head
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
        if val.isdigit() and len(val) == 2 and int(val) >= 40 and int(val) <= 90:
            val = f"{int(val)/10:.1f}"
            st.session_state.ielts_raw_input = val
        else:
            try:
                num = float(val)
                if num.is_integer() and 4 <= num <= 9:
                    st.session_state.ielts_raw_input = f"{num:.1f}"
            except ValueError:
                pass
    st.session_state.ielts_input_str = st.session_state.ielts_raw_input

def on_financial_change():
    val = st.session_state.fin_raw_input
    clean_digits = "".join([c for c in str(val) if c.isdigit()])
    if clean_digits:
        num = int(clean_digits)
        st.session_state.fin_input_str = f"{num:,}".replace(",", ".")
    else:
        st.session_state.fin_input_str = ""

# Helper Stepper UI (Design ala Image 1: White Card + Connected Nodes + Checkmarks)
def render_stepper(current_step):
    steps = [
        (1, "1. Data Pengajuan"), 
        (2, "2. Pendidikan & Gap"), 
        (3, "3. Pathway & Kampus"), 
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
# SIDEBAR KIRI (BRANDING & VERTICAL STEPPER SESUAI MOCKUP)
# =============================================================
def render_sidebar(current_step):
    steps_data = [
        (1, "Data Pengajuan", "Informasi dasar pemohon"),
        (2, "Pendidikan & Gap", "Riwayat pendidikan"),
        (3, "Pathway & Kampus", "Pilihan studi"),
        (4, "Profil & Riwayat", "Pengalaman dan latar belakang")
    ]
    step_rows = []
    for idx, (num, title, desc) in enumerate(steps_data):
        if num < current_step:
            state_class = "completed"
            circle_inner = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
        elif num == current_step:
            state_class = "active"
            circle_inner = str(num)
        else:
            state_class = "pending"
            circle_inner = str(num)
        
        connector_html = '<div class="sidebar-step-connector"></div>' if idx < len(steps_data) - 1 else ''
        step_row = (
            f'<div class="sidebar-step-row {state_class}">'
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
        step_rows.append(step_row)
    
    menu_html = "".join(step_rows)
    html = (
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
        f'<div class="sidebar-stepper-menu">{menu_html}</div>'
        '<div class="sidebar-footer-text">&copy; 2026 Visa Track, All rights reserved.</div>'
    )
    return html

with st.sidebar:
    st.markdown(render_sidebar(st.session_state.current_section), unsafe_allow_html=True)

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
                    birth_date = st.date_input(
                        "Tanggal Lahir Student :red[*]",
                        value=None,
                        min_value=date(1960, 1, 1),
                        max_value=date(current_year - 14, 12, 31),
                        format="DD/MM/YYYY",
                        key="input_birth_date",
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
                    apply_date = st.date_input(
                        "Waktu Pengajuan Visa (Apply) :red[*]",
                        value=None,
                        min_value=date(2015, 1, 1),
                        max_value=date(current_year + 2, 12, 31),
                        format="DD/MM/YYYY",
                        key="input_apply_date",
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
                        '<div class="calc-label">Usia Saat Apply</div>'
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
                    has_err = False
                    if birth_date is None:
                        st.session_state["sec1_birth_err"] = True
                        has_err = True
                    else:
                        st.session_state["sec1_birth_err"] = False

                    if apply_date is None:
                        st.session_state["sec1_apply_err"] = True
                        st.session_state["sec1_apply_err_msg"] = "Silahkan masukkan waktu pengajuan visa"
                        has_err = True
                    elif birth_date and apply_date < birth_date:
                        st.session_state["sec1_apply_err"] = True
                        st.session_state["sec1_apply_err_msg"] = "Waktu Pengajuan Visa tidak boleh lebih awal dari Tanggal Lahir Student."
                        has_err = True
                    else:
                        st.session_state["sec1_apply_err"] = False
                        st.session_state["sec1_apply_err_msg"] = None

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

        components.html(f"""
        <script>
        function applyInputGreyBorders() {{
            try {{
                const doc = window.parent.document;
                const hasBirthErr = {birth_err_val};
                const hasApplyErr = {apply_err_val};

                // Ambil kolom di inner_card_sec1
                const cols = doc.querySelectorAll('div[class*="st-key-inner_card_sec1"] div[data-testid="column"]');
                if (cols.length >= 2) {{
                    const styleInput = (col, isErr) => {{
                        const targetEls = col.querySelectorAll('[data-baseweb="input"], [data-testid="stDateInputField"]');
                        targetEls.forEach(el => {{
                            if (isErr) {{
                                el.style.setProperty('border', '1.5px solid #EF4444', 'important');
                                el.style.setProperty('border-color', '#EF4444', 'important');
                                el.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                            }} else {{
                                el.style.setProperty('border', '1.5px solid #CBD5E1', 'important');
                                el.style.setProperty('border-color', '#CBD5E1', 'important');
                                el.style.setProperty('box-shadow', 'none', 'important');
                            }}
                            el.style.setProperty('background-color', '#FFFFFF', 'important');
                            el.style.setProperty('border-radius', '8px', 'important');
                            el.style.setProperty('height', '42px', 'important');
                        }});
                    }};
                    styleInput(cols[0], hasBirthErr);
                    styleInput(cols[1], hasApplyErr);
                }}

                // Input date placeholder
                const textInputs = doc.querySelectorAll('div[data-testid="stDateInput"] input');
                if (textInputs.length >= 1 && !textInputs[0].value) {{
                    textInputs[0].placeholder = "Pilih tanggal lahir student";
                }}
                if (textInputs.length >= 2 && !textInputs[1].value) {{
                    textInputs[1].placeholder = "Pilih tanggal pengajuan visa";
                }}
            }} catch(e) {{}}
        }}
        applyInputGreyBorders();
        setTimeout(applyInputGreyBorders, 30);
        setTimeout(applyInputGreyBorders, 100);
        setTimeout(applyInputGreyBorders, 250);
        setTimeout(applyInputGreyBorders, 500);
        setTimeout(applyInputGreyBorders, 900);
        </script>
        """, height=0, width=0)

    # ---------------------------------------------------------
    # SECTION 2: INFORMASI PENDIDIKAN TERAKHIR & GAP
    # ---------------------------------------------------------
    elif st.session_state.current_section == 2:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 02 / 04</div>'
            '<div class="main-step-title">Informasi Pendidikan Terakhir & Gap</div>'
            '<div class="main-step-desc">Kelompokkan informasi tahun kelulusan terakhir dan durasi jeda studi student.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec2"):
            with st.container(border=True, key="inner_card_sec2"):
                gap_mode = st.radio(
                    "Perhitungan Gap",
                    options=["Mengetahui Bulan dan Tahun", "Hanya Mengetahui Tahun"],
                    key="radio_gap_mode",
                    horizontal=True,
                    label_visibility="visible"
                )

                app_year = st.session_state.get("app_year", current_year)
                apply_date = st.session_state.get("apply_date", today)
                bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

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
                            value=str(st.session_state.get("last_edu_year") or ""),
                            placeholder="Contoh: 2022",
                            key="input_last_edu_year_m",
                            max_chars=4,
                            help=f"Masukkan 4 digit tahun kelulusan terakhir (1990 – {current_year})."
                        )
                        clean_edu_digits = "".join([c for c in raw_edu_year if c.isdigit()])
                        last_edu_year = int(clean_edu_digits) if len(clean_edu_digits) == 4 else None
                        st.session_state["last_edu_year"] = last_edu_year

                        if last_edu_year is not None and 1990 <= last_edu_year <= current_year:
                            st.session_state["sec2_year_err"] = False

                        if st.session_state.get("sec2_year_err"):
                            st.markdown(
                                '<style>'
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child div[data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:first-child div:has(> input) { '
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
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div[data-baseweb="select"] > div, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div.react-aria-Group, '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"]:last-child div:has(> input) { '
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
                            value=str(st.session_state.get("last_edu_year") or ""),
                            placeholder="Contoh: 2021",
                            key="input_last_edu_year_y",
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

                        if st.session_state.get("sec2_year_err"):
                            st.markdown(
                                '<style>'
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] div[data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="column"] div:has(> input), '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stTextInput"] [data-baseweb="input"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"], '
                                'div[class*="st-key-inner_card_sec2"] div[data-testid="stTextInput"] div:has(> input) { '
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
                    '<div class="calc-label">Durasi Gap Studi</div>'
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
                        if bulan_lulus is None:
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

        year_err_val = "true" if st.session_state.get("sec2_year_err") else "false"
        month_err_val = "true" if st.session_state.get("sec2_month_err") else "false"

        components.html(f"""
        <script>
        function bindYearAutoCommitAndBorders() {{
            try {{
                const doc = window.parent.document;
                const curYear = {current_year};
                const hasYearErr = {year_err_val};
                const hasMonthErr = {month_err_val};
                const gapModeIsBoth = "{gap_mode}" === "Mengetahui Bulan dan Tahun";

                const selQuery = [
                    '[data-testid="stTextInputRootElement"]',
                    'div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"]',
                    'div[data-testid="stTextInput"] div.react-aria-Group',
                    'div[data-testid="stTextInput"] div[class*="e1bh1cux2"]',
                    'div[data-testid="stTextInput"] div:has(> input)',
                    'div[data-testid="stTextInput"] div[data-baseweb="input"]',
                    'div[data-testid="stSelectbox"] div.react-aria-Group',
                    'div[data-testid="stSelectbox"] div[class*="e1oobldh0"]',
                    'div[data-testid="stSelectbox"] div[role="group"]',
                    'div[data-testid="stSelectbox"] div:has(> input)',
                    'div[data-testid="stSelectbox"] > div:nth-child(2)',
                    'div[data-testid="stSelectbox"] div[data-baseweb="select"] > div'
                ].join(', ');

                doc.querySelectorAll(selQuery).forEach(wrap => {{
                    wrap.style.setProperty('background-color', '#FFFFFF', 'important');
                    wrap.style.setProperty('background', '#FFFFFF', 'important');
                    wrap.style.setProperty('border', '1.5px solid #CBD5E1', 'important');
                    wrap.style.setProperty('border-color', '#CBD5E1', 'important');
                    wrap.style.setProperty('border-width', '1.5px', 'important');
                    wrap.style.setProperty('border-style', 'solid', 'important');
                    wrap.style.setProperty('border-radius', '8px', 'important');
                    wrap.style.setProperty('height', '42px', 'important');
                    wrap.style.setProperty('min-height', '42px', 'important');
                    wrap.style.setProperty('box-sizing', 'border-box', 'important');
                }});

                if (gapModeIsBoth) {{
                    const cols = doc.querySelectorAll('div[class*="st-key-inner_card_sec2"] div[data-testid="column"]');
                    if (cols.length >= 2) {{
                        const yearInp = cols[0].querySelector('[data-baseweb="input"], [data-testid="stTextInputRootElement"], div:has(> input)');
                        if (yearInp && hasYearErr) {{
                            yearInp.style.setProperty('border', '1.5px solid #EF4444', 'important');
                            yearInp.style.setProperty('border-color', '#EF4444', 'important');
                            yearInp.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                        }}
                        const monthSel = cols[1].querySelector('div[data-baseweb="select"] > div, div.react-aria-Group, div:has(> input)');
                        if (monthSel && hasMonthErr) {{
                            monthSel.style.setProperty('border', '1.5px solid #EF4444', 'important');
                            monthSel.style.setProperty('border-color', '#EF4444', 'important');
                            monthSel.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                        }}
                    }}
                }} else {{
                    const yearInp = doc.querySelector('div[class*="st-key-inner_card_sec2"] [data-baseweb="input"], div[class*="st-key-inner_card_sec2"] [data-testid="stTextInputRootElement"]');
                    if (yearInp && hasYearErr) {{
                        yearInp.style.setProperty('border', '1.5px solid #EF4444', 'important');
                        yearInp.style.setProperty('border-color', '#EF4444', 'important');
                        yearInp.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                    }}
                }}

                doc.querySelectorAll('div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] input').forEach(inp => {{
                    inp.style.setProperty('background-color', 'transparent', 'important');
                    inp.style.setProperty('background', 'transparent', 'important');
                    inp.style.setProperty('color', '#17324D', 'important');
                    inp.style.setProperty('font-size', '13px', 'important');
                }});

                const inputs = doc.querySelectorAll('div[data-testid="stTextInput"] input');
                inputs.forEach(inp => {{
                    const wrap = inp.closest('[data-testid="stTextInputRootElement"]') || inp.closest('div.react-aria-Group') || inp.closest('div[class*="e1bh1cux2"]') || inp.parentElement;
                    if (!inp.dataset.autoCommitBound) {{
                        inp.dataset.autoCommitBound = "true";
                        let timer = null;
                        inp.addEventListener('input', function() {{
                            if (timer) clearTimeout(timer);
                            const digits = (this.value || "").replace(/\\D/g, "");
                            if (digits.length === 4) {{
                                if (wrap) {{
                                    wrap.style.setProperty('border', '1.5px solid #CBD5E1', 'important');
                                    wrap.style.setProperty('border-color', '#CBD5E1', 'important');
                                    wrap.style.setProperty('box-shadow', 'none', 'important');
                                }}
                                timer = setTimeout(() => {{
                                    this.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    this.blur();
                                }}, 150);
                            }}
                        }});
                    }}
                }});
            }} catch(e) {{}}
        }}
        bindYearAutoCommitAndBorders();
        setTimeout(bindYearAutoCommitAndBorders, 30);
        setTimeout(bindYearAutoCommitAndBorders, 100);
        setTimeout(bindYearAutoCommitAndBorders, 250);
        setTimeout(bindYearAutoCommitAndBorders, 500);
        setTimeout(bindYearAutoCommitAndBorders, 900);
        </script>
        """, height=0, width=0)

    # ---------------------------------------------------------
    # SECTION 3: JALUR STUDI (PATHWAY) & PILIHAN KAMPUS
    # ---------------------------------------------------------
    elif st.session_state.current_section == 3:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 03 / 04</div>'
            '<div class="main-step-title">Pathway & Kampus Pilihan</div>'
            '<div class="main-step-desc">Pilih jenjang studi, kampus di Australia, dan durasi rencana studi.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True, key="outer_card_sec3"):
            with st.container(border=True, key="inner_card_sec3"):
                p1, p2 = st.columns(2)
                with p1:
                    campus_level_str = st.selectbox(
                        "Tingkat / Level Institusi",
                        options=["Level 1 — University", 
                                 "Level 2 — College / Private Institute", 
                                 "Level 3 — Vocational / Provider Lain"],
                        index=st.session_state.get("campus_level_idx", 0),
                        help="Kategori level risiko institusi pendidikan di Australia (Level 1: Universitas terakreditasi tinggi, Level 2: Kampus/Kolej swasta, Level 3: Provider vokasi/pelatihan)."
                    )
                    st.session_state["campus_level_idx"] = ["Level 1", "Level 2", "Level 3"].index(campus_level_str[:7]) if "Level" in campus_level_str else 0
                    level_kampus = 1 if "Level 1" in campus_level_str else (2 if "Level 2" in campus_level_str else 3)
                    st.session_state["level_kampus"] = level_kampus

                with p2:
                    has_elicos = st.selectbox(
                        "Mengambil Kursus Bahasa (ELICOS)?",
                        options=["Tidak", "Ya"],
                        index=st.session_state.get("has_elicos_idx", 0),
                        help="Pilih 'Ya' jika student mengambil kursus persiapan bahasa Inggris (ELICOS) sebelum memulai program studi utama."
                    )
                    st.session_state["has_elicos_idx"] = 1 if has_elicos == "Ya" else 0
                    st.session_state["has_elicos"] = has_elicos

                p3, p4 = st.columns(2)
                with p3:
                    has_vocational = st.selectbox(
                        "Mengambil Jalur Kejuruan (Vocational/VET)?",
                        options=["Tidak", "Ya"],
                        index=st.session_state.get("has_vocational_idx", 0),
                        help="Pilih 'Ya' jika student mengambil program kejuruan praktis seperti Certificate atau Diploma vokasi."
                    )
                    st.session_state["has_vocational_idx"] = 1 if has_vocational == "Ya" else 0
                    st.session_state["has_vocational"] = has_vocational

                with p4:
                    has_higher = st.selectbox(
                        "Mengambil Pendidikan Tinggi (Higher Education)?",
                        options=["Tidak", "Ya"],
                        index=st.session_state.get("has_higher_idx", 1),
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

        components.html("""
        <script>
        function applySection3SelectBorders() {
            try {
                const doc = window.parent.document;
                const selQuery = [
                    'div[data-testid="stSelectbox"] div.react-aria-Group',
                    'div[data-testid="stSelectbox"] div[class*="e1oobldh0"]',
                    'div[data-testid="stSelectbox"] div[role="group"]',
                    'div[data-testid="stSelectbox"] div:has(> input)',
                    'div[data-testid="stSelectbox"] > div:nth-child(2)'
                ].join(', ');

                doc.querySelectorAll(selQuery).forEach(wrap => {
                    wrap.style.setProperty('background-color', '#FFFFFF', 'important');
                    wrap.style.setProperty('background', '#FFFFFF', 'important');
                    wrap.style.setProperty('border', '1.5px solid #CBD5E1', 'important');
                    wrap.style.setProperty('border-color', '#CBD5E1', 'important');
                    wrap.style.setProperty('border-width', '1.5px', 'important');
                    wrap.style.setProperty('border-style', 'solid', 'important');
                    wrap.style.setProperty('border-radius', '8px', 'important');
                    wrap.style.setProperty('height', '42px', 'important');
                    wrap.style.setProperty('min-height', '42px', 'important');
                    wrap.style.setProperty('box-sizing', 'border-box', 'important');
                });
            } catch(e) {}
        }
        applySection3SelectBorders();
        setTimeout(applySection3SelectBorders, 50);
        setTimeout(applySection3SelectBorders, 150);
        setTimeout(applySection3SelectBorders, 350);
        setTimeout(applySection3SelectBorders, 700);
        </script>
        """, height=0, width=0)

    # ---------------------------------------------------------
    # SECTION 4: PROFIL LATAR BELAKANG & RIWAYAT VISA
    # ---------------------------------------------------------
    elif st.session_state.current_section == 4:
        st.markdown(
            '<div class="main-page-header">'
            '<div class="main-step-eyebrow">LANGKAH 04 / 04</div>'
            '<div class="main-step-title">Profil Latar Belakang & Riwayat Visa</div>'
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

                    is_ielts_invalid = (raw_ielts_str and (english_prof is None or english_prof < 4.0 or english_prof > 9.0)) or (st.session_state.get("ielts_show_error", False) and (english_prof is None or english_prof < 4.0 or english_prof > 9.0))
                    if is_ielts_invalid:
                        ielts_err_text = "Silahkan masukkan skor IELTS" if not raw_ielts_str else "Skor resmi IELTS harus berada pada rentang 4.0 hingga 9.0"
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:first-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:first-child [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:first-child div:has(> input) { '
                            '    border: 1.5px solid #EF4444 !important; '
                            '    border-color: #EF4444 !important; '
                            '    box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.2) !important; '
                            '} '
                            '</style>'
                            f'<div class="field-error-sec4">{ielts_err_text}</div>',
                            unsafe_allow_html=True
                        )
                    elif english_prof and 4.0 <= english_prof <= 9.0:
                        st.session_state["ielts_show_error"] = False

                with c2:
                    st.text_input(
                        "Kesiapan Finansial / Tabungan (Rupiah)",
                        value=st.session_state.fin_input_str,
                        key="fin_raw_input",
                        placeholder="Contoh: 500.000.000",
                        help="Estimasi dana tabungan atau bukti kesiapan finansial yang dimiliki untuk mendukung biaya studi dan hidup di Australia (dalam Rupiah).",
                        on_change=on_financial_change
                    )
                    digits_only = "".join([c for c in str(st.session_state.fin_input_str) if c.isdigit()])
                    financial_nominal = float(digits_only) if digits_only else None
                    st.session_state["financial_nominal"] = financial_nominal

                    raw_fin = str(st.session_state.get("fin_input_str", "")).strip()
                    is_fin_invalid = (raw_fin and (financial_nominal is None or financial_nominal < 10_000_000)) or (st.session_state.get("fin_show_error", False) and (financial_nominal is None or financial_nominal < 10_000_000))
                    if is_fin_invalid:
                        fin_err_text = "Silahkan masukkan nominal tabungan/finansial" if not raw_fin else "Format belum lengkap, contoh: 500.000.000 (minimal Rp 10.000.000)"
                        st.markdown(
                            '<style>'
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:last-child [data-baseweb="input"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:last-child [data-testid="stTextInputRootElement"], '
                            'div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]:last-child div:has(> input) { '
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
                    related_major = st.selectbox(
                        "Kesesuaian Jurusan",
                        options=["Sesuai / Linier", "Tidak / Lintas Jurusan"],
                        index=st.session_state.get("related_major_idx", 0),
                        help="Kesesuaian program studi yang dituju di Australia dengan latar belakang pendidikan atau riwayat kerja sebelumnya."
                    )
                    st.session_state["related_major_idx"] = 0 if "Sesuai" in related_major else 1
                    st.session_state["related_major"] = related_major

                with r2:
                    emp_continuity = st.selectbox(
                        "Aktivitas Kerja Selama Gap",
                        options=["Iya", "Tidak"],
                        index=st.session_state.get("emp_continuity_idx", 0),
                        help="Apakah student memiliki aktivitas kerja, magang, atau pengalaman profesional yang jelas selama jeda studi (gap)."
                    )
                    st.session_state["emp_continuity_idx"] = 0 if emp_continuity == "Iya" else 1
                    st.session_state["emp_continuity"] = emp_continuity

                with r3:
                    has_refusal = st.selectbox(
                        "Riwayat Penolakan Visa",
                        options=["Tidak", "Pernah"],
                        index=st.session_state.get("has_refusal_idx", 0),
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
                    if eng_val is None or eng_val < 4.0 or eng_val > 9.0:
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

        ielts_err_val = "true" if is_ielts_invalid else "false"
        fin_err_val = "true" if is_fin_invalid else "false"

        components.html(f"""
        <script>
        function applySection4InputBorders() {{
            try {{
                const doc = window.parent.document;
                const hasIeltsErr = {ielts_err_val};
                const hasFinErr = {fin_err_val};
                const selQuery = [
                    '[data-testid="stTextInputRootElement"]',
                    'div[data-testid="stTextInput"] [data-testid="stTextInputRootElement"]',
                    'div[data-testid="stTextInput"] div.react-aria-Group',
                    'div[data-testid="stTextInput"] div[class*="e1bh1cux2"]',
                    'div[data-testid="stTextInput"] div:has(> input)',
                    'div[data-testid="stSelectbox"] div.react-aria-Group',
                    'div[data-testid="stSelectbox"] div[class*="e1oobldh0"]',
                    'div[data-testid="stSelectbox"] div[role="group"]',
                    'div[data-testid="stSelectbox"] div:has(> input)',
                    'div[data-testid="stSelectbox"] > div:nth-child(2)'
                ].join(', ');

                doc.querySelectorAll(selQuery).forEach(wrap => {{
                    wrap.style.setProperty('background-color', '#FFFFFF', 'important');
                    wrap.style.setProperty('background', '#FFFFFF', 'important');
                    wrap.style.setProperty('border', '1.5px solid #CBD5E1', 'important');
                    wrap.style.setProperty('border-color', '#CBD5E1', 'important');
                    wrap.style.setProperty('border-width', '1.5px', 'important');
                    wrap.style.setProperty('border-style', 'solid', 'important');
                    wrap.style.setProperty('border-radius', '8px', 'important');
                    wrap.style.setProperty('height', '42px', 'important');
                    wrap.style.setProperty('min-height', '42px', 'important');
                    wrap.style.setProperty('box-sizing', 'border-box', 'important');
                }});

                doc.querySelectorAll('div[data-testid="stTextInput"] input, div[data-testid="stSelectbox"] input').forEach(inp => {{
                    inp.style.setProperty('background-color', 'transparent', 'important');
                    inp.style.setProperty('background', 'transparent', 'important');
                    inp.style.setProperty('color', '#17324D', 'important');
                    inp.style.setProperty('font-size', '13px', 'important');
                }});

                if (hasIeltsErr) {{
                    const cols = doc.querySelectorAll('div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]');
                    if (cols.length >= 2) {{
                        cols[0].querySelectorAll('[data-testid="stTextInputRootElement"], div.react-aria-Group, [data-baseweb="input"], div:has(> input)').forEach(wrap => {{
                            wrap.style.setProperty('border', '1.5px solid #EF4444', 'important');
                            wrap.style.setProperty('border-color', '#EF4444', 'important');
                            wrap.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                        }});
                    }}
                }}

                if (hasFinErr) {{
                    const cols = doc.querySelectorAll('div[class*="st-key-inner_card_sec4"] div[data-testid="stHorizontalBlock"]:first-child div[data-testid="column"]');
                    if (cols.length >= 2) {{
                        cols[1].querySelectorAll('[data-testid="stTextInputRootElement"], div.react-aria-Group, [data-baseweb="input"], div:has(> input)').forEach(wrap => {{
                            wrap.style.setProperty('border', '1.5px solid #EF4444', 'important');
                            wrap.style.setProperty('border-color', '#EF4444', 'important');
                            wrap.style.setProperty('box-shadow', '0 0 0 1px rgba(239, 68, 68, 0.2)', 'important');
                        }});
                    }}
                }}

                // Sejajarkan tinggi label 3 selectbox di row 2
                const sec4Labels = doc.querySelectorAll('div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] [data-testid="stWidgetLabel"], div[class*="st-key-inner_card_sec4"] div[data-testid="stSelectbox"] label');
                sec4Labels.forEach(lbl => {{
                    lbl.style.setProperty('min-height', '22px', 'important');
                    lbl.style.setProperty('height', 'auto', 'important');
                    lbl.style.setProperty('display', 'flex', 'important');
                    lbl.style.setProperty('align-items', 'center', 'important');
                    lbl.style.setProperty('justify-content', 'space-between', 'important');
                }});
            }} catch(e) {{}}
        }}
        applySection4InputBorders();
        setTimeout(applySection4InputBorders, 50);
        setTimeout(applySection4InputBorders, 150);
        setTimeout(applySection4InputBorders, 350);
        setTimeout(applySection4InputBorders, 700);
        </script>
        """, height=0, width=0)

# =============================================================
# SECTION 5: HASIL PREDIKSI & EVALUASI PROFIL
# =============================================================
elif st.session_state.current_section == 5:
    financial_nominal = st.session_state.get("financial_nominal", 500000000.0)
    age_val = st.session_state.get("age_val", 24.0)
    gap_year = st.session_state.get("gap_year", 1.0)
    last_edu_year = st.session_state.get("last_edu_year", 2022.0)
    app_year = st.session_state.get("app_year", current_year)
    level_kampus = st.session_state.get("level_kampus", 1.0)
    english_prof = st.session_state.get("english_prof", 6.0)
    related_major = st.session_state.get("related_major", "Sesuai / Linier")
    emp_continuity = st.session_state.get("emp_continuity", "Iya")
    has_refusal = st.session_state.get("has_refusal", "Tidak")
    has_elicos = st.session_state.get("has_elicos", "Tidak")
    has_vocational = st.session_state.get("has_vocational", "Tidak")
    has_higher = st.session_state.get("has_higher", "Ya")

    input_payload = {
        'Financial': float(financial_nominal),
        'Age': float(age_val),
        'Gap_Year': float(gap_year),
        'Last_Education_Year': float(last_edu_year),
        'Application_Year': float(app_year),
        'Level_Kampus': float(level_kampus),
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
        'Employment_Continuity': 'Kesinambungan aktivitas selama gap',
        'Age': 'Usia',
        'Related_Major': 'Kesesuaian latar belakang dengan jurusan',
        'Level_Kampus': 'Pilihan level institusi',
        'Has_Refusal': 'Riwayat penolakan visa',
        'Gap_Year': 'Durasi gap pendidikan',
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

    reason_explanations_grant = {
        'Kondisi finansial': f"Kondisi finansial dinilai memadai (Rp {financial_nominal:,.0f}) untuk menopang biaya pendidikan dan kebutuhan hidup selama studi di Australia.",
        'Kesinambungan aktivitas selama gap': "Kesinambungan aktivitas selama masa jeda terisi dengan baik melalui pekerjaan atau kegiatan produktif yang relevan.",
        'Usia': "Usia student berada dalam rentang yang wajar dan didukung profil studi yang konsisten.",
        'Kesesuaian latar belakang dengan jurusan': "Latar belakang pendidikan atau pengalaman kerja sebelumnya selaras dan konsisten dengan program studi yang dituju di Australia.",
        'Pilihan level institusi': "Pilihan level institusi yang dituju memiliki profil risiko yang baik dan mendukung kelancaran aplikasi.",
        'Riwayat penolakan visa': "Student tidak memiliki catatan penolakan visa sebelumnya, yang memberikan nilai positif terhadap profil pengajuan.",
        'Kemahiran bahasa Inggris': f"Kemampuan bahasa Inggris (IELTS {english_prof}) memenuhi standar persyaratan minimum studi yang dituju.",
        'Durasi gap pendidikan': "Durasi gap pendidikan tergolong moderat dan dapat dipertanggungjawabkan dengan baik.",
        'Jalur ELICOS': "Program persiapan bahasa (ELICOS) mendukung kesiapan akademik sebelum menempuh program utama.",
        'Jalur Vocational': "Program kejuruan yang dipilih relevan dengan jalur pengembangan karier terapan.",
        'Jalur Higher Education': "Jalur Higher Education (S1/S2) memberikan nilai akademis yang kuat dan meyakinkan bagi imigrasi.",
        'Waktu pengajuan aplikasi': "Waktu pengajuan visa relatif dekat dengan masa kelulusan, mencerminkan kesinambungan rencana studi yang konsisten.",
        'Tahun kelulusan terakhir': "Tahun kelulusan terakhir tergolong segar dan mendukung kontinuitas rekam jejak akademik student."
    }

    reason_explanations_refusal = {
        'Kondisi finansial': "Kondisi finansial masih perlu diperkuat dengan memastikan dana yang tersedia memadai untuk biaya hidup dan tuition fee (patokan minimum acuan ~Rp450 juta) serta didukung bukti sumber dana yang jelas.",
        'Kesinambungan aktivitas selama gap': "Apabila terdapat masa jeda (gap), pengalaman kerja, usaha, atau aktivitas produktif perlu didokumentasikan dengan bukti tertulis agar tidak menjadi celah kecurigaan imigrasi.",
        'Usia': "Usia student perlu diselaraskan dengan alasan kuat melanjutkan studi, riwayat pendidikan, dan prospek karier saat kembali ke negara asal.",
        'Kesesuaian latar belakang dengan jurusan': "Kesesuaian jurusan perlu diperkuat dengan penjelasan tertulis (Genuine Student Statement) mengenai alasan berpindah bidang studi.",
        'Pilihan level institusi': "Pilihan kampus level 3 atau institusi berisiko memerlukan pemenuhan dokumen finansial dan bukti akademis yang lebih ketat.",
        'Riwayat penolakan visa': "Adanya riwayat penolakan visa sebelumnya merupakan faktor risiko signifikan. Wajib melampirkan penjelasan perbaikan profil yang substansial.",
        'Kemahiran bahasa Inggris': "Kemampuan bahasa Inggris masih perlu ditingkatkan atau dilengkapi dengan paket kursus ELICOS sebelum memulai perkuliahan utama.",
        'Durasi gap pendidikan': "Gap pendidikan yang panjang tanpa dokumentasi aktivitas yang jelas berpotensi menurunkan tingkat keyakinan petugas visa terhadap kriteria Genuine Student.",
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

    with card_col1:
        grant_btn_content = f"{p_grant:.0f}%\nPeluang Disetujui (Grant)"
        if st.button(
            grant_btn_content,
            key="direct_card_grant",
            use_container_width=True
        ):
            st.session_state.active_result_view = "grant"
            st.rerun()

    with card_col2:
        refusal_btn_content = f"{p_refusal:.0f}%\nTingkat Risiko (Refusal)"
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

        shap_positives = df_shap_all[df_shap_all['Raw_SHAP'] > 0.001].sort_values(by='Raw_SHAP', ascending=False)
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

        shap_negatives = df_shap_all[df_shap_all['Raw_SHAP'] < -0.001].sort_values(by='Raw_SHAP', ascending=True)
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

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
    c_rst1, c_rst2 = st.columns(2)
    with c_rst1:
        if st.button("✎  Edit Data Pengajuan", key="btn_edit_submission", use_container_width=True):
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
