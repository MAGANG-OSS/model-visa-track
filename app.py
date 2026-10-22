import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import os
from datetime import datetime, date

# =============================================================
# 1. KONFIGURASI HALAMAN
# =============================================================
st.set_page_config(
    page_title="Visa Track - Prediksi Student Visa Australia",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================
# TYPOGRAPHY & REFINED STYLING
# =============================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Typography - Hindari menimpa font icon bawaan Streamlit */
    html, body, p, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #1e293b;
    }
    
    .stMarkdown, .stText {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Streamlit Expander Icon & Header Fix */
    div[data-testid="stExpander"] details summary {
        font-family: 'Inter', sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        color: #0b4b60 !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    div[data-testid="stExpander"] details summary svg {
        margin-right: 8px !important;
    }

    .block-container {
        max-width: 1040px !important;
        margin: 0 auto !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* REVISI: Header Kotak Lonjong (Pill/Rounded) Mewah */
    .banner-header {
        background: linear-gradient(135deg, #0b4b60 0%, #0d5c75 45%, #0284c7 100%) !important;
        border-radius: 20px !important;
        padding: 26px 36px;
        margin-top: 15px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(11, 75, 96, 0.18);
        overflow: hidden;
    }
    .banner-accent {
        width: 38px;
        height: 4px;
        background-color: #fbbf24;
        border-radius: 3px;
        margin-bottom: 10px;
    }
    .banner-header h1, .banner-header h1 * {
        font-size: 21px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.01em;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }

    /* Section Headings */
    .section-heading {
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #0d5c75 !important;
        margin-top: 5px;
        margin-bottom: 4px;
        letter-spacing: -0.01em;
    }
    .section-subheading {
        font-size: 13px !important;
        font-weight: 400 !important;
        color: #64748b !important;
        margin-bottom: 18px;
        line-height: 1.45;
    }

    /* REVISI 2: Step Line Indicator (Garis Minimalis, Biru Menyala untuk Aktif) */
    .step-track-wrapper {
        display: flex;
        gap: 10px;
        margin-bottom: 22px;
    }
    .step-track-item {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .step-track-bar {
        height: 4px;
        border-radius: 4px;
        background-color: #e2e8f0;
        transition: all 0.3s ease;
    }
    .step-track-bar.active {
        background-color: #0284c7;
        box-shadow: 0 0 10px rgba(2, 132, 199, 0.6);
    }
    .step-track-title {
        font-size: 11.5px;
        font-weight: 600;
        color: #94a3b8;
    }
    .step-track-title.active {
        color: #0284c7;
        font-weight: 700;
    }

    /* REVISI 2: Input Form Label & Box Diperkecil & Rapi */
    .stNumberInput label, .stSelectbox label, .stRadio label, .stDateInput label, .stTextInput label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #334155 !important;
        margin-bottom: 2px !important;
    }
    .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input, .stTextInput input {
        font-size: 12.5px !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="input"] {
        min-height: 34px !important;
        height: 34px !important;
    }

    /* Tombol Navigasi Standard (Kembali, Selanjutnya, Edit): Biru Tua Khusus Navigasi */
    div.st-key-btn_next_1 button,
    div.st-key-btn_back_2 button,
    div.st-key-btn_next_2 button,
    div.st-key-btn_back_3 button,
    div.st-key-btn_next_3 button,
    div.st-key-btn_back_4 button,
    div.st-key-btn_edit_submission button {
        background-color: #0d5c75 !important;
        color: #ffffff !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 7px !important;
        padding: 9px 24px !important;
        border: none !important;
        box-shadow: 0 3px 10px rgba(13, 92, 117, 0.2) !important;
        transition: all 0.15s ease !important;
    }
    div.st-key-btn_next_1 button p, div.st-key-btn_next_1 button span,
    div.st-key-btn_back_2 button p, div.st-key-btn_back_2 button span,
    div.st-key-btn_next_2 button p, div.st-key-btn_next_2 button span,
    div.st-key-btn_back_3 button p, div.st-key-btn_back_3 button span,
    div.st-key-btn_next_3 button p, div.st-key-btn_next_3 button span,
    div.st-key-btn_back_4 button p, div.st-key-btn_back_4 button span,
    div.st-key-btn_edit_submission button p, div.st-key-btn_edit_submission button span {
        color: #ffffff !important;
    }
    div.st-key-btn_next_1 button:hover,
    div.st-key-btn_back_2 button:hover,
    div.st-key-btn_next_2 button:hover,
    div.st-key-btn_back_3 button:hover,
    div.st-key-btn_next_3 button:hover,
    div.st-key-btn_back_4 button:hover,
    div.st-key-btn_edit_submission button:hover {
        background-color: #084357 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(13, 92, 117, 0.3) !important;
    }

    /* REVISI 2: Hijau Solid untuk Tombol Prediksi (Primary Button) & Tombol Selesai */
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"],
    div.st-key-btn_finish_submission button {
        background-color: #16a34a !important;
        color: #ffffff !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        border-radius: 7px !important;
        padding: 9px 24px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.28) !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span,
    div.stButton > button[data-testid="baseButton-primary"] p,
    div.stButton > button[data-testid="baseButton-primary"] span,
    div.st-key-btn_finish_submission button p,
    div.st-key-btn_finish_submission button span {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover,
    div.st-key-btn_finish_submission button:hover {
        background-color: #15803d !important;
        color: #ffffff !important;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.38) !important;
    }

    /* Warning / Reminder Persis Versi Sebelumnya (Merah Lembut, Bulat Tanda Seru) */
    .reminder-box-prev {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 6px;
        margin-bottom: 20px;
        padding: 10px 14px;
        background-color: #fef2f2;
        border: 1px solid #fee2e2;
        border-radius: 8px;
    }
    .reminder-circle-icon {
        width: 18px;
        height: 18px;
        min-width: 18px;
        border-radius: 50%;
        border: 1.5px solid #dc2626;
        color: #dc2626;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        font-family: inherit;
    }
    .reminder-content-text {
        color: #b91c1c;
        font-size: 12.5px;
        font-weight: 600;
        line-height: 1.35;
    }

    /* Form Error Banner Luas & Jelas */
    .form-error-banner {
        display: flex;
        align-items: center;
        gap: 12px;
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px 18px;
        margin-top: 18px;
        margin-bottom: 8px;
        width: 100%;
    }
    .form-error-icon {
        width: 22px;
        height: 22px;
        min-width: 22px;
        border-radius: 50%;
        background-color: #ef4444;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 800;
    }
    .form-error-text {
        font-size: 13.5px;
        font-weight: 600;
        color: #991b1b;
        line-height: 1.4;
    }

    /* CARD GRANT — HIJAU (MODERN CLEAN MOBILE CARD) */
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
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.08) !important;
        transition: all 0.2s ease !important;
    }
    div.st-key-direct_card_grant button p,
    div.st-key-direct_card_grant button span,
    div.st-key-direct_card_grant button div,
    div[data-testid="stButton"].st-key-direct_card_grant button p,
    div[data-testid="stButton"].st-key-direct_card_grant button span,
    div[data-testid="stButton"].st-key-direct_card_grant button div {
        color: #15803d !important;
        font-size: 21px !important;
        font-weight: 800 !important;
        white-space: pre-line !important;
    }
    div.st-key-direct_card_grant button:hover,
    div[data-testid="stButton"].st-key-direct_card_grant button:hover {
        background-color: #dcfce7 !important;
        background: #dcfce7 !important;
        border-color: #22c55e !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.18) !important;
    }

    /* CARD REFUSAL — MERAH (MODERN CLEAN MOBILE CARD) */
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
        color: #b91c1c !important;
        font-size: 21px !important;
        font-weight: 800 !important;
        white-space: pre-line !important;
    }
    div.st-key-direct_card_refusal button:hover,
    div[data-testid="stButton"].st-key-direct_card_refusal button:hover {
        background-color: #fee2e2 !important;
        background: #fee2e2 !important;
        border-color: #ef4444 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.18) !important;
    }

    /* Rekomendasi Item Lebih Ramping & Bersih */
    .recom-item-clean {
        background-color: #ffffff;
        border: 1px solid #f1f5f9;
        border-left: 3.5px solid #0d5c75;
        border-radius: 6px;
        padding: 11px 14px;
        margin-bottom: 9px;
        font-size: 13px;
        line-height: 1.5;
        color: #334155;
    }
    .recom-item-clean.grant-item {
        border-left-color: #16a34a;
    }
    .recom-item-clean.refusal-item {
        border-left-color: #dc2626;
    }
    .recom-title-clean {
        font-weight: 700;
        color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

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
        # Jika user ketik 2 digit tanpa titik (misal 65, 70, 55, 60), otomatis ubah jadi 6.5, 7.0, 5.5, 6.0
        if val.isdigit() and len(val) == 2 and int(val) >= 40 and int(val) <= 90:
            val = f"{int(val)/10:.1f}"
            st.session_state.ielts_raw_input = val
        else:
            try:
                num = float(val)
                # Jika user ketik angka 4-9 tunggal (misal 6 atau 7), otomatis jadikan 6.0 atau 7.0
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

# =============================================================
# REVISI 1: BANNER HEADER GRADASI BIRU MEWAH
# =============================================================
st.markdown("""
<div class="banner-header">
    <div class="banner-accent"></div>
    <h1>Visa Track: Prediksi Keberhasilan Student Visa Australia</h1>
</div>
""", unsafe_allow_html=True)

# =============================================================
# JIKA SEDANG DI TAHAP FORM INPUT (SECTION 1 s/d 4)
# =============================================================
if st.session_state.current_section in [1, 2, 3, 4]:
    # REVISI 2: Step Line Indicator (Garis bersih & menyala saat aktif)
    step_titles = [
        "1. Data Pengajuan", 
        "2. Pendidikan & Gap", 
        "3. Pathway & Kampus", 
        "4. Profil & Riwayat"
    ]
    
    items_html = []
    for i, title in enumerate(step_titles):
        step_num = i + 1
        is_active = (st.session_state.current_section == step_num)
        bar_class = "step-track-bar active" if is_active else "step-track-bar"
        title_class = "step-track-title active" if is_active else "step-track-title"
        items_html.append(f'<div class="step-track-item"><div class="{bar_class}"></div><div class="{title_class}">{title}</div></div>')
    
    track_html = f'<div class="step-track-wrapper">{"".join(items_html)}</div>'
    st.markdown(track_html, unsafe_allow_html=True)



    # ---------------------------------------------------------
    # SECTION 1: DATA PENGAJUAN STUDENT
    # ---------------------------------------------------------
    if st.session_state.current_section == 1:
        st.markdown('<div class="section-heading">Data Pengajuan Student</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheading">Masukkan informasi student untuk melihat hasil prediksi dan faktor yang berkontribusi terhadap hasil model.</div>', unsafe_allow_html=True)

        d1, d2 = st.columns(2)
        with d1:
            birth_date = st.date_input(
                "Tanggal Lahir Student",
                value=st.session_state.get("birth_date", date(2000, 1, 1)),
                min_value=date(1960, 1, 1),
                max_value=date(current_year - 14, 12, 31),
                help="Pilih tanggal lahir student sesuai identitas paspor."
            )
            st.session_state["birth_date"] = birth_date

        with d2:
            apply_date = st.date_input(
                "Waktu Pengajuan Visa (Apply)",
                value=st.session_state.get("apply_date", today),
                min_value=date(2015, 1, 1),
                max_value=date(current_year + 2, 12, 31),
                help="Tanggal pengajuan aplikasi visa student."
            )
            st.session_state["apply_date"] = apply_date

        calculated_age = apply_date.year - birth_date.year - ((apply_date.month, apply_date.day) < (birth_date.month, birth_date.day))
        age_val = max(15, min(65, calculated_age))
        app_year = apply_date.year
        st.session_state["age_val"] = age_val
        st.session_state["app_year"] = app_year
        
        st.caption(f"Usia saat apply: **{age_val} tahun** (Tahun pengajuan: **{app_year}**)")

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        c_btn1, c_btn2 = st.columns([4.5, 1.2])
        with c_btn2:
            # REVISI 3: Tombol Selanjutnya tanpa tanda panah
            if st.button("Selanjutnya", key="btn_next_1", use_container_width=True):
                st.session_state.current_section = 2
                st.rerun()

    # ---------------------------------------------------------
    # SECTION 2: INFORMASI PENDIDIKAN TERAKHIR & GAP
    # ---------------------------------------------------------
    elif st.session_state.current_section == 2:
        st.markdown('<div class="section-heading">Informasi Pendidikan Terakhir & Gap</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheading">Kelompokkan informasi tahun kelulusan terakhir dan durasi jeda studi student.</div>', unsafe_allow_html=True)

        gap_mode = st.radio(
            "Metode Perhitungan Gap:",
            options=["Mengetahui Bulan dan Tahun", "Hanya Mengetahui Tahun"],
            key="radio_gap_mode"
        )

        app_year = st.session_state.get("app_year", current_year)
        apply_date = st.session_state.get("apply_date", today)
        bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                      "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

        if gap_mode == "Mengetahui Bulan dan Tahun":
            g1, g2 = st.columns(2)
            with g1:
                raw_edu_year = st.text_input(
                    "Tahun Terakhir Pendidikan / Kelulusan", 
                    value=str(st.session_state.get("last_edu_year") or ""),
                    placeholder="Contoh: 2022",
                    key="input_last_edu_year_m",
                    max_chars=4,
                    help="Ketik 4 digit angka tahun kelulusan terakhir (misal: 2022)."
                )
                clean_edu_digits = "".join([c for c in raw_edu_year if c.isdigit()])
                last_edu_year = int(clean_edu_digits) if len(clean_edu_digits) == 4 else None
                st.session_state["last_edu_year"] = last_edu_year
            with g2:
                bulan_lulus = st.selectbox(
                    "Bulan Kelulusan Pendidikan Terakhir", 
                    options=bulan_list, 
                    index=st.session_state.get("bulan_lulus_idx", 4),
                    key="select_bulan_lulus"
                )
                bulan_lulus_idx = bulan_list.index(bulan_lulus) + 1
                st.session_state["bulan_lulus_idx"] = bulan_lulus_idx - 1
                
            bulan_app_idx = apply_date.month
            nama_bulan_app = bulan_list[bulan_app_idx - 1]
            
            if last_edu_year is not None:
                total_months = (app_year - int(last_edu_year)) * 12 + (bulan_app_idx - bulan_lulus_idx)
                gap_year = max(0.0, round(total_months / 12.0, 1))
                st.session_state["gap_year"] = gap_year
                st.caption(f"Gap: **{total_months} bulan** (~{gap_year} tahun) dari {bulan_lulus} {int(last_edu_year)} hingga {nama_bulan_app} {app_year}")
            else:
                st.session_state["gap_year"] = 0.0
                if raw_edu_year and len(clean_edu_digits) != 4:
                    st.caption("⚠️ Masukkan 4 digit angka tahun yang valid (contoh: 2022).")
        else:
            raw_edu_year = st.text_input(
                "Tahun Terakhir Pendidikan / Kelulusan", 
                value=str(st.session_state.get("last_edu_year") or ""),
                placeholder="Contoh: 2021",
                key="input_last_edu_year_y",
                max_chars=4,
                help="Ketik 4 digit angka tahun kelulusan terakhir (misal: 2021)."
            )
            clean_edu_digits = "".join([c for c in raw_edu_year if c.isdigit()])
            last_edu_year = int(clean_edu_digits) if len(clean_edu_digits) == 4 else None
            st.session_state["last_edu_year"] = last_edu_year

            if last_edu_year is not None:
                gap_year = float(max(0, app_year - int(last_edu_year)))
                st.session_state["gap_year"] = gap_year
                st.caption(f"Gap: **{gap_year:.0f} tahun** (dari tahun {int(last_edu_year)} hingga tahun apply {app_year})")
            else:
                st.session_state["gap_year"] = 0.0
                if raw_edu_year and len(clean_edu_digits) != 4:
                    st.caption("⚠️ Masukkan 4 digit angka tahun yang valid (contoh: 2021).")

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        c_btn1, c_btn2, c_btn3 = st.columns([1.2, 3.2, 1.2])
        with c_btn1:
            # REVISI 3: Tombol Kembali tanpa tanda panah
            if st.button("Kembali", key="btn_back_2", use_container_width=True):
                st.session_state["sec2_error"] = None
                st.session_state.current_section = 1
                st.rerun()
        with c_btn3:
            if st.button("Selanjutnya", key="btn_next_2", use_container_width=True):
                edu_yr = st.session_state.get("last_edu_year")
                if edu_yr is None:
                    st.session_state["sec2_error"] = f"Silakan masukkan Tahun Kelulusan dalam 4 digit angka valid (antara 1990 hingga {current_year})."
                    st.rerun()
                elif edu_yr < 1990 or edu_yr > current_year:
                    st.session_state["sec2_error"] = f"Tahun Kelulusan ({edu_yr}) di luar batas valid! Harus antara 1990 hingga {current_year}."
                    st.rerun()
                else:
                    st.session_state["sec2_error"] = None
                    st.session_state.current_section = 3
                    st.rerun()

        # Pesan Error Full-Width Lebar untuk Section 2
        if st.session_state.get("sec2_error"):
            st.markdown(f"""
            <div class="form-error-banner">
                <div class="form-error-icon">!</div>
                <div class="form-error-text">{st.session_state["sec2_error"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # SECTION 3: JALUR STUDI (PATHWAY) & PILIHAN KAMPUS
    # ---------------------------------------------------------
    elif st.session_state.current_section == 3:
        st.markdown('<div class="section-heading">Jalur Studi (Pathway) & Pilihan Kampus</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheading">Tentukan kombinasi jalur program studi yang diambil dan tingkatan institusi tujuan.</div>', unsafe_allow_html=True)

        p1, p2 = st.columns(2)
        with p1:
            campus_level_str = st.selectbox(
                "Tingkat / Level Institusi",
                options=["Level 1 — University", 
                         "Level 2 — College / Private Institute", 
                         "Level 3 — Vocational / Provider Lain"],
                index=st.session_state.get("campus_level_idx", 0),
                help="Kategori level institusi kampus tujuan di Australia."
            )
            st.session_state["campus_level_idx"] = ["Level 1", "Level 2", "Level 3"].index(campus_level_str[:7]) if "Level" in campus_level_str else 0
            level_kampus = 1 if "Level 1" in campus_level_str else (2 if "Level 2" in campus_level_str else 3)
            st.session_state["level_kampus"] = level_kampus

        with p2:
            has_elicos = st.selectbox(
                "Mengambil Kursus Bahasa (ELICOS)?",
                options=["Tidak", "Ya"],
                index=st.session_state.get("has_elicos_idx", 0)
            )
            st.session_state["has_elicos_idx"] = 1 if has_elicos == "Ya" else 0
            st.session_state["has_elicos"] = has_elicos

        p3, p4 = st.columns(2)
        with p3:
            has_vocational = st.selectbox(
                "Mengambil Jalur Kejuruan (Vocational/VET)?",
                options=["Tidak", "Ya"],
                index=st.session_state.get("has_vocational_idx", 0)
            )
            st.session_state["has_vocational_idx"] = 1 if has_vocational == "Ya" else 0
            st.session_state["has_vocational"] = has_vocational

        with p4:
            has_higher = st.selectbox(
                "Mengambil Pendidikan Tinggi (Higher Education)?",
                options=["Tidak", "Ya"],
                index=st.session_state.get("has_higher_idx", 1)
            )
            st.session_state["has_higher_idx"] = 1 if has_higher == "Ya" else 0
            st.session_state["has_higher"] = has_higher

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
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
        st.markdown('<div class="section-heading">Profil Latar Belakang & Riwayat Visa</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subheading">Lengkapi informasi kemampuan bahasa Inggris, kesiapan finansial, dan riwayat pengajuan visa.</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            ielts_val = st.text_input(
                "Kemampuan Bahasa Inggris (Skor IELTS)",
                value=st.session_state.get("ielts_input_str", ""),
                key="ielts_raw_input",
                placeholder="Contoh: 6.0",
                on_change=on_ielts_change,
                help="Ketik skor IELTS (misal: 6 atau 6.5). Jika diketik 65 otomatis menjadi 6.5."
            )
            # Selalu sinkronkan ke ielts_input_str
            st.session_state["ielts_input_str"] = ielts_val
            try:
                clean_ielts = ielts_val.strip().replace(",", ".")
                english_prof = float(clean_ielts) if clean_ielts else None
            except ValueError:
                english_prof = None
            st.session_state["english_prof"] = english_prof

        with c2:
            st.text_input(
                "Kesiapan Finansial / Tabungan (Rupiah)",
                value=st.session_state.fin_input_str,
                key="fin_raw_input",
                placeholder="Contoh: 500.000.000",
                on_change=on_financial_change,
                help="Ketik nominal saldo tabungan. Titik pemisah ribuan otomatis tertata."
            )
            digits_only = "".join([c for c in str(st.session_state.fin_input_str) if c.isdigit()])
            financial_nominal = float(digits_only) if digits_only else None
            st.session_state["financial_nominal"] = financial_nominal

        r1, r2, r3 = st.columns(3)
        with r1:
            related_major = st.selectbox(
                "Kesesuaian Jurusan dengan Background",
                options=["Sesuai / Linier", "Tidak / Lintas Jurusan"],
                index=st.session_state.get("related_major_idx", 0)
            )
            st.session_state["related_major_idx"] = 0 if "Sesuai" in related_major else 1
            st.session_state["related_major"] = related_major

        with r2:
            emp_continuity = st.selectbox(
                "Aktivitas Kerja Selama Gap",
                options=["Iya", "Tidak"],
                index=st.session_state.get("emp_continuity_idx", 0)
            )
            st.session_state["emp_continuity_idx"] = 0 if emp_continuity == "Iya" else 1
            st.session_state["emp_continuity"] = emp_continuity

        with r3:
            has_refusal = st.selectbox(
                "Riwayat Penolakan Visa Sebelumnya",
                options=["Tidak", "Pernah"],
                index=st.session_state.get("has_refusal_idx", 0)
            )
            st.session_state["has_refusal_idx"] = 0 if has_refusal == "Tidak" else 1
            st.session_state["has_refusal"] = has_refusal

        st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
        c_btn1, c_btn2, c_btn3 = st.columns([1.2, 3.2, 1.4])
        with c_btn1:
            if st.button("Kembali", key="btn_back_4", use_container_width=True):
                st.session_state["sec4_error"] = None
                st.session_state.current_section = 3
                st.rerun()
        with c_btn3:
            # REVISI: Tombol Prediksi Hijau Solid
            if st.button("Prediksi", key="btn_submit", type="primary", use_container_width=True):
                eng_val = st.session_state.get("english_prof")
                fin_val = st.session_state.get("financial_nominal")

                if eng_val is None:
                    st.session_state["sec4_error"] = "Silakan masukkan Skor Kemampuan Bahasa Inggris (IELTS) yang valid."
                    st.rerun()
                elif eng_val < 4.0 or eng_val > 9.0:
                    st.session_state["sec4_error"] = f"Skor IELTS ({eng_val}) di luar batas valid! Skor resmi IELTS harus berada pada rentang 4.0 hingga 9.0."
                    st.rerun()
                elif not fin_val or fin_val <= 0:
                    st.session_state["sec4_error"] = "Silakan masukkan Jumlah Kesiapan Finansial / Tabungan yang valid (lebih dari 0)."
                    st.rerun()
                else:
                    st.session_state["sec4_error"] = None
                    st.session_state.current_section = 5
                    st.rerun()

        # Pesan Error Full-Width Lebar, Jelas, Tidak Terjepit di Kanan
        if st.session_state.get("sec4_error"):
            st.markdown(f"""
            <div class="form-error-banner">
                <div class="form-error-icon">!</div>
                <div class="form-error-text">{st.session_state["sec4_error"]}</div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================
# REVISI 7: SECTION 5 HANYA TAMPIL KETIKA USER DI SECTION 5
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

    st.markdown('<div class="section-heading">Hasil Prediksi & Evaluasi Profil</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Klik salah satu card di bawah untuk melihat rincian faktor pendukung secara terpisah.</div>', unsafe_allow_html=True)

    # REVISI 3: Warning / Reminder Persis Versi Sebelumnya (Merah Lembut, Bulat Tanda Seru)
    st.markdown("""
    <div class="reminder-box-prev">
        <div class="reminder-circle-icon">!</div>
        <div class="reminder-content-text">
            <strong>Reminder:</strong> Keputusan akhir visa sepenuhnya merupakan hak prerogatif Department of Home Affairs (Imigrasi Australia).
        </div>
    </div>
    """, unsafe_allow_html=True)

   
    # CARD HASIL PREDIKSI (HIJAU UNTUK GRANT & MERAH UNTUK REFUSAL - MODEL MOBILE CARD ELEGAN)
    st.markdown("""
    <style>
        .st-key-direct_card_grant button,
        div.st-key-direct_card_grant button,
        div[data-testid="stButton"].st-key-direct_card_grant button {
            background-color: #f0fdf4 !important;
            background: #f0fdf4 !important;
            border: 2px solid #86efac !important;
            border-top: 2px solid #86efac !important;
            border-radius: 16px !important;
            min-height: 120px !important;
            padding: 20px 16px !important;
            box-shadow: 0 4px 14px rgba(22, 163, 74, 0.08) !important;
        }
        .st-key-direct_card_grant button p,
        .st-key-direct_card_grant button span,
        div.st-key-direct_card_grant button p,
        div.st-key-direct_card_grant button span {
            color: #15803d !important;
            font-size: 21px !important;
            font-weight: 800 !important;
            white-space: pre-line !important;
        }
        .st-key-direct_card_refusal button,
        div.st-key-direct_card_refusal button,
        div[data-testid="stButton"].st-key-direct_card_refusal button {
            background-color: #fef2f2 !important;
            background: #fef2f2 !important;
            border: 2px solid #fca5a5 !important;
            border-top: 2px solid #fca5a5 !important;
            border-radius: 16px !important;
            min-height: 120px !important;
            padding: 20px 16px !important;
            box-shadow: 0 4px 14px rgba(220, 38, 38, 0.08) !important;
        }
        .st-key-direct_card_refusal button p,
        .st-key-direct_card_refusal button span,
        div.st-key-direct_card_refusal button p,
        div.st-key-direct_card_refusal button span {
            color: #b91c1c !important;
            font-size: 21px !important;
            font-weight: 800 !important;
            white-space: pre-line !important;
        }
    </style>
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
        st.markdown("<div style='text-align: left; color: #64748b; font-size: 12px; margin-top: 4px; margin-bottom: 12px;'>Klik hasil prediksi diatas untuk melihat rincian faktor kontribusi</div>", unsafe_allow_html=True)

    with card_col2:
        refusal_btn_content = f"{p_refusal:.0f}%\nTingkat Risiko (Refusal)"
        if st.button(
            refusal_btn_content,
            key="direct_card_refusal",
            use_container_width=True
        ):
            st.session_state.active_result_view = "refusal"
            st.rerun()

    # Panel Detail Sesuai Card Aktif
    if active_tab == "grant":
        st.markdown('##### 🟢 Faktor Pendukung Prediksi Disetujui (Grant)')
        st.caption("Daftar atribut pelamar yang berkontribusi positif memperkuat profil persetujuan visa:")

        shap_positives = df_shap_all[df_shap_all['Raw_SHAP'] > 0.001].sort_values(by='Raw_SHAP', ascending=False)
        shown_count = 0
        for _, row in shap_positives.iterrows():
            faktor = row['Faktor']
            pct = row['Persen']
            shown_count += 1
            expl = reason_explanations_grant.get(faktor, "Faktor ini memberikan pengaruh positif terhadap profil pengajuan.")
            st.markdown(f"""
            <div class="recom-item-clean grant-item">
                <span class="recom-title-clean">{faktor} (+{pct:.0f}%):</span> {expl}
            </div>
            """, unsafe_allow_html=True)

        if input_payload['Has_Refusal'] == 0 and 'Riwayat penolakan visa' not in shap_positives['Faktor'].values:
            st.markdown(f"""
            <div class="recom-item-clean grant-item">
                <span class="recom-title-clean">Riwayat Bersih:</span> {reason_explanations_grant['Riwayat penolakan visa']}
            </div>
            """, unsafe_allow_html=True)

        if shown_count == 0:
            st.info("Peluang grant didukung oleh kombinasi rata-rata atribut profil yang memenuhi syarat dasar.")

    else:
        st.markdown('##### 🔴 Faktor Risiko Prediksi Ditolak (Refusal)')
        st.caption("Daftar atribut pelamar yang menjadi faktor risiko atau area yang memerlukan perbaikan dokumen:")

        shap_negatives = df_shap_all[df_shap_all['Raw_SHAP'] < -0.001].sort_values(by='Raw_SHAP', ascending=True)
        shown_risk_count = 0
        for _, row in shap_negatives.iterrows():
            faktor = row['Faktor']
            pct = row['Persen']
            shown_risk_count += 1
            expl = reason_explanations_refusal.get(faktor, "Faktor ini berkontribusi terhadap potensi risiko penolakan visa.")
            st.markdown(f"""
            <div class="recom-item-clean refusal-item">
                <span class="recom-title-clean">{faktor} ({pct:.0f}%):</span> {expl}
            </div>
            """, unsafe_allow_html=True)

        if input_payload['Financial'] < 450000000 and 'Kondisi finansial' not in shap_negatives['Faktor'].values:
            st.markdown(f"""
            <div class="recom-item-clean refusal-item">
                <span class="recom-title-clean">Kondisi Finansial (Perhatian Khusus):</span> {reason_explanations_refusal['Kondisi finansial']}
            </div>
            """, unsafe_allow_html=True)

        if input_payload['Has_Refusal'] == 1 and 'Riwayat penolakan visa' not in shap_negatives['Faktor'].values:
            st.markdown(f"""
            <div class="recom-item-clean refusal-item">
                <span class="recom-title-clean">Riwayat Penolakan Visa (Perhatian Khusus):</span> {reason_explanations_refusal['Riwayat penolakan visa']}
            </div>
            """, unsafe_allow_html=True)

        if input_payload['Related_Major'] == 0 and 'Kesesuaian latar belakang dengan jurusan' not in shap_negatives['Faktor'].values:
            st.markdown(f"""
            <div class="recom-item-clean refusal-item">
                <span class="recom-title-clean">Kesesuaian Jurusan (Lintas Bidang):</span> {reason_explanations_refusal['Kesesuaian latar belakang dengan jurusan']}
            </div>
            """, unsafe_allow_html=True)

        if shown_risk_count == 0 and input_payload['Financial'] >= 450000000 and input_payload['Has_Refusal'] == 0:
            st.success("Tidak terdeteksi faktor risiko penolakan yang signifikan pada profil pengajuan ini.")

    # REVISI: Tombol Aksi di Akhir (Edit Pengajuan & Selesai / Pengajuan Baru)
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
