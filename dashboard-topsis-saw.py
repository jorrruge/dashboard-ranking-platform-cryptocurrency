import streamlit as st
import pandas as pd

# Streamlit App
st.title("Visualisasi Data AHP, TOPSIS, SAW, dan AVERAGE")

# File Excel
file_path = "AHP TOPSIS SAW.xlsx"

# Load Excel file without external engine
@st.cache_data
def load_data(sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Sheet 1: AHP Pembobotan
st.header("1. AHP Pembobotan")
try:
    bobot_df = load_data("AHP Pembobotan")
    st.dataframe(bobot_df)
except Exception as e:
    st.error(f"Sheet 'AHP Pembobotan' tidak ditemukan: {e}")

# Sheet 2: TOPSIS
st.header("2. Perhitungan TOPSIS")
try:
    topsis_df = load_data("TOPSIS")
    st.dataframe(topsis_df)

    if not topsis_df.empty:
        # Menampilkan alternatif nilai tertinggi dan terendah
        st.write("### Alternatif Nilai Tertinggi dan Terendah")
        highest = topsis_df.iloc[topsis_df.iloc[:, 1].idxmax()]
        lowest = topsis_df.iloc[topsis_df.iloc[:, 1].idxmin()]
        st.write("Alternatif Tertinggi:", highest)
        st.write("Alternatif Terendah:", lowest)
except Exception as e:
    st.error(f"Sheet 'TOPSIS' tidak ditemukan: {e}")

# Sheet 3: SAW
st.header("3. Peringkat SAW")
try:
    saw_df = load_data("SAW")
    st.dataframe(saw_df)
except Exception as e:
    st.error(f"Sheet 'SAW' tidak ditemukan: {e}")

# Sheet 4: AVERAGE
st.header("4. Peringkat Berdasarkan AVERAGE")
try:
    average_df = load_data("AVERAGE")
    st.dataframe(average_df)

    # Pilihan kriteria untuk penilaian
    st.write("### Pilih Kriteria untuk Penilaian")
    selected_kriteria = st.selectbox("Kriteria:", average_df.columns[1:], key="criteria")

    if selected_kriteria:
        # Menghitung nilai akhir
        st.write(f"### Peringkat Berdasarkan: {selected_kriteria}")
        sorted_df = average_df.sort_values(by=selected_kriteria, ascending=False)
        st.dataframe(sorted_df[[average_df.columns[0], selected_kriteria]])
except Exception as e:
    st.error(f"Sheet 'AVERAGE' tidak ditemukan: {e}")
