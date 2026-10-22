import unittest
from datetime import date
import numpy as np
import pandas as pd
import joblib

class TestVisaPredictionLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 1. Load Model dan Fitur yang tersimpan
        cls.model = joblib.load('model_random_forest.pkl')
        cls.features = joblib.load('model_features.pkl')

    # TC-01 & TC-02: Pengujian Normalisasi IELTS
    def test_ielts_normalization(self):
        # Kasus 1: User salah ketik 65 padahal maksudnya 6.5
        val_typo = "65"
        if val_typo.isdigit() and len(val_typo) == 2:
            clean_val = f"{int(val_typo) / 10:.1f}"
        self.assertEqual(clean_val, "6.5")

        # Kasus 2: User ketik 6 ingin jadi 6.0
        val_single = "6"
        if val_single.isdigit() and len(val_single) == 1:
            clean_val2 = f"{float(val_single):.1f}"
        self.assertEqual(clean_val2, "6.0")

    # TC-03: Pengujian Pembersihan Nominal Tabungan (Rupiah)
    def test_financial_nominal_cleaning(self):
        raw_input = "500.000.000"
        digits_only = "".join([c for c in raw_input if c.isdigit()])
        nominal = float(digits_only)
        self.assertEqual(nominal, 500000000.0)

    # TC-04: Pengujian Kalkulasi Usia saat Apply
    def test_age_calculation(self):
        birth_date = date(2000, 1, 1)
        apply_date = date(2026, 1, 1)
        age = apply_date.year - birth_date.year - ((apply_date.month, apply_date.day) < (birth_date.month, birth_date.day))
        self.assertEqual(age, 26)

    # TC-05: Pengujian Kalkulasi Gap Year
    def test_gap_year_calculation(self):
        last_edu_year = 2022
        app_year = 2026
        gap = max(0, app_year - last_edu_year)
        self.assertEqual(gap, 4)

    # TC-06 & TC-07: Pengujian Model ML & Konsistensi Probabilitas
    def test_model_inference_pipeline(self):
        sample_input = {
            'Financial': 500000000.0,
            'Age': 24.0,
            'Gap_Year': 1.0,
            'Last_Education_Year': 2022.0,
            'Application_Year': 2024.0,
            'Level_Kampus': 1.0,
            'English_Proficiency_Cleaned': 6.5,
            'Related_Major': 1,
            'Has_Refusal': 0,
            'Employment_Continuity': 1,
            'Has_ELICOS': 0,
            'Has_Vocational': 0,
            'Has_Higher': 1
        }
        # Susun DataFrame sesuai urutan model_features
        df = pd.DataFrame([sample_input])[self.features]
        self.assertEqual(list(df.columns), self.features)

        # Cek prediksi probabilitas
        proba = self.model.predict_proba(df)[0]
        p_refusal = proba[0] * 100
        p_grant = proba[1] * 100

        # Probabilitas total wajib 100% (dengan toleransi pembulatan float)
        self.assertAlmostEqual(p_refusal + p_grant, 100.0, places=4)
        self.assertTrue(0.0 <= p_grant <= 100.0)
        self.assertTrue(0.0 <= p_refusal <= 100.0)

if __name__ == '__main__':
    unittest.main()
