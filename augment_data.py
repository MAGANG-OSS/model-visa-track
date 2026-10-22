"""
augment_data.py - Generate 40 synthetic rows untuk melengkapi dataset ke 300 baris
Situasi:
  - 260 baris sudah ada (data asli, sudah/belum berlabel)
  - Butuh 40 sintetis agar total = 300
  - Target distribusi: 205 GRANT : 95 REFUSAL

CATATAN PENELITIAN:
  - 123 baris referensi labelnya dipertahankan.
  - Label baris lain (dari 260) diisi stratified agar mencapai 205:95.
  - 40 baris sintetis dibuat dari Gaussian Noise berdasarkan data asli.
  - File ini untuk latihan pipeline teknis RF, bukan evaluasi final skripsi.
"""

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# --- KONFIGURASI -----------------------------------------------
INPUT_FILE     = "data_cleaned.xlsx"   # file 260 baris (ganti jika nama berbeda)
SHEET_NAME     = 0
LABEL_COLUMN   = "Outcome"
TARGET_TOTAL   = 300
TARGET_GRANT   = 205
TARGET_REFUSAL = 95
GRANT_VALUE    = "GRANT"
REFUSAL_VALUE  = "REFUSAL"
OUTPUT_EXCEL   = "data_augmented_300.xlsx"
OUTPUT_CSV     = "data_augmented_300.csv"
RANDOM_SEED    = 42
# --------------------------------------------------------------

np.random.seed(RANDOM_SEED)
print("=" * 55)
print("  AUGMENTASI DATASET ? 300 BARIS")
print("  Target: 205 GRANT : 95 REFUSAL")
print("=" * 55)

# STEP 1: Load data 260 baris
print(f"\n[1] Load: {INPUT_FILE}")
df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
print(f"    Baris: {len(df)} | Kolom: {len(df.columns)}")

# Distribusi awal
g0 = (df[LABEL_COLUMN] == GRANT_VALUE).sum()
r0 = (df[LABEL_COLUMN] == REFUSAL_VALUE).sum()
empty0 = df[LABEL_COLUMN].isna().sum()
print(f"    GRANT: {g0} | REFUSAL: {r0} | Kosong: {empty0}")

# STEP 2: Impute missing values (numerik=median, kategorik=modus)
print(f"\n[2] Impute missing values...")
feature_cols = [c for c in df.columns if c != LABEL_COLUMN]
num_cols = df[feature_cols].select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df[feature_cols].select_dtypes(exclude=[np.number]).columns.tolist()

if num_cols:
    df[num_cols] = SimpleImputer(strategy="median").fit_transform(df[num_cols])
if cat_cols:
    df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])
print(f"    Numerik ({len(num_cols)} kol): median | Kategorik ({len(cat_cols)} kol): modus")

# STEP 3: Isi label yang kosong agar mendekati target distribusi
print(f"\n[3] Assign label ke baris yang kosong...")
need_g = TARGET_GRANT - g0
need_r = TARGET_REFUSAL - r0
empty_idx = df[df[LABEL_COLUMN].isna()].index.tolist()

if len(empty_idx) > 0:
    n_assign = min(len(empty_idx), need_g + need_r)
    labels = ([GRANT_VALUE] * min(need_g, n_assign) +
              [REFUSAL_VALUE] * max(0, n_assign - min(need_g, n_assign)))
    np.random.shuffle(labels)
    for i, idx in enumerate(empty_idx[:n_assign]):
        df.at[idx, LABEL_COLUMN] = labels[i]
    print(f"    Assigned {n_assign} label ke baris kosong")
else:
    print(f"    Tidak ada baris kosong label, skip.")

g1 = (df[LABEL_COLUMN] == GRANT_VALUE).sum()
r1 = (df[LABEL_COLUMN] == REFUSAL_VALUE).sum()
print(f"    Sekarang: {len(df)} baris | {g1} GRANT | {r1} REFUSAL")

# STEP 4: Generate 40 baris sintetis (Gaussian Noise)
n_synthetic = TARGET_TOTAL - len(df)
need_g2 = TARGET_GRANT - g1
need_r2 = TARGET_REFUSAL - r1
print(f"\n[4] Generate {n_synthetic} baris sintetis...")
print(f"    Perlu: {need_g2} GRANT | {need_r2} REFUSAL sintetis")

def gen_rows(source_df, n, label_val):
    rows = []
    for _ in range(n):
        base = source_df.sample(1).iloc[0].copy()
        for col in num_cols:
            std = source_df[col].std()
            if std > 0:
                base[col] = round(base[col] + np.random.normal(0, std * 0.05), 4)
        base[LABEL_COLUMN] = label_val
        rows.append(base)
    return pd.DataFrame(rows)

synth_parts = []
if need_g2 > 0:
    src = df[df[LABEL_COLUMN] == GRANT_VALUE]
    synth_parts.append(gen_rows(src, need_g2, GRANT_VALUE))
    print(f"    ? {need_g2} synthetic GRANT")
if need_r2 > 0:
    src = df[df[LABEL_COLUMN] == REFUSAL_VALUE]
    synth_parts.append(gen_rows(src, need_r2, REFUSAL_VALUE))
    print(f"    ? {need_r2} synthetic REFUSAL")

df_final = pd.concat([df] + synth_parts, ignore_index=True)

# STEP 5: Verifikasi & Export
gf = (df_final[LABEL_COLUMN] == GRANT_VALUE).sum()
rf = (df_final[LABEL_COLUMN] == REFUSAL_VALUE).sum()
print(f"\n[5] HASIL FINAL:")
print(f"    Total  : {len(df_final)} baris (target {TARGET_TOTAL})")
print(f"    GRANT  : {gf} ({gf/len(df_final)*100:.1f}%) — target {TARGET_GRANT}")
print(f"    REFUSAL: {rf} ({rf/len(df_final)*100:.1f}%) — target {TARGET_REFUSAL}")

df_final.to_excel(OUTPUT_EXCEL, index=False)
df_final.to_csv(OUTPUT_CSV, index=False)
print(f"\n    ? {OUTPUT_EXCEL}")
print(f"    ? {OUTPUT_CSV}")
print("\n" + "=" * 55)
print("  SELESAI!")
print("=" * 55)
