import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "AHP TOPSIS SAW.xlsx"
excel_data = pd.ExcelFile(file_path)

# Function to load a specific sheet
def load_sheet(sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Streamlit App
st.title("Visualisasi Data AHP, TOPSIS, SAW, dan AVERAGE")

# Sheet 1: AHP Pembobotan
st.header("1. AHP Pembobotan")
bobot_df = load_sheet("AHP Pembobotan")

if not bobot_df.empty:
    st.write("### Data Bobot")
    st.dataframe(bobot_df)

# Sheet 2: TOPSIS
st.header("2. Perhitungan TOPSIS")
topsis_df = load_sheet("TOPSIS")

if not topsis_df.empty:
    st.write("### Data TOPSIS")
    st.dataframe(topsis_df)

    # Alternatif nilai tertinggi dan terendah
    highest_alternative = topsis_df.iloc[topsis_df.iloc[:, 1].idxmax()]
    lowest_alternative = topsis_df.iloc[topsis_df.iloc[:, 1].idxmin()]

    st.write(f"### Alternatif dengan Nilai Tertinggi:")
    st.write(highest_alternative)

    st.write(f"### Alternatif dengan Nilai Terendah:")
    st.write(lowest_alternative)

# Sheet 3: SAW
st.header("3. Peringkat SAW")
saw_df = load_sheet("SAW")

if not saw_df.empty:
    st.write("### Data Peringkat")
    st.dataframe(saw_df)

    # Visualisasi Diagram Batang
    st.write("### Diagram Batang Peringkat")
    fig, ax = plt.subplots()
    ax.bar(saw_df[saw_df.columns[0]], saw_df[saw_df.columns[1]])
    ax.set_title("Peringkat Alternatif")
    ax.set_xlabel(saw_df.columns[0])
    ax.set_ylabel(saw_df.columns[1])
    st.pyplot(fig)

# Sheet 4: AVERAGE
st.header("4. Peringkat Berdasarkan AVERAGE")
average_df = load_sheet("AVERAGE")

if not average_df.empty:
    st.write("### Data AVERAGE")
    st.dataframe(average_df)

    # Dropdown untuk memilih kriteria
    selected_kriteria = st.selectbox("Pilih Kriteria untuk Penilaian:", average_df.columns[1:])

    if selected_kriteria:
        # Mengambil bobot dari sheet AHP Pembobotan
        if selected_kriteria in bobot_df[bobot_df.columns[0]].values:
            bobot_kriteria = bobot_df.loc[bobot_df[bobot_df.columns[0]] == selected_kriteria, bobot_df.columns[1]].values[0]
        else:
            bobot_kriteria = 1  # Default jika tidak ada bobot yang ditemukan

        # Menghitung nilai akhir dengan pembobotan
        average_df["Nilai Akhir"] = average_df[selected_kriteria] * bobot_kriteria
        sorted_average_df = average_df.sort_values(by="Nilai Akhir", ascending=False)

        st.write(f"### Peringkat Alternatif Berdasarkan: {selected_kriteria}")
        st.dataframe(sorted_average_df[[average_df.columns[0], "Nilai Akhir"]])

        # Visualisasi diagram batang
        st.write("### Diagram Batang Peringkat Berdasarkan Kriteria")
        fig, ax = plt.subplots()
        ax.bar(sorted_average_df[average_df.columns[0]], sorted_average_df["Nilai Akhir"])
        ax.set_title(f"Peringkat Berdasarkan {selected_kriteria}")
        ax.set_xlabel(average_df.columns[0])
        ax.set_ylabel("Nilai Akhir")
        st.pyplot(fig)
