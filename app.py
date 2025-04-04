import streamlit as st
import pandas as pd
import numpy as np


st.title("Metrohm data extractor")
uploaded_file = st.file_uploader("Selecione arquivo XLSX exportado pelo Metrohm", type=["xlsx"])

if uploaded_file:
    # Check if columns exist
    df = pd.read_excel(uploaded_file)
    try:
        required_columns = ['Scan', 'Potential applied (V)', 'WE(1).Current (A)']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error: Column '{col}' not found in the uploaded file.")
                st.stop()  # Stop execution if a required column is missing
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        st.stop()

    st.write("### Data Preview", df.head())
    st.write(f"**Total Rows:** {len(df)}")
    st.write(f"**Total Columns:** {len(df.columns)}")
    
    for i in range(1, df['Scan'].max() + 1):
        df_scan = df.where(df['Scan'] == i).dropna(how='all')
        st.write(f"### Scan {i} Data")
        st.write(df_scan.head())

        st.write(f"**Scan {i} - Number of points:** {len(df_scan)}")
        st.write(f"**Scan {i} - Description of Current.**")
        st.write(df_scan['WE(1).Current (A)'].describe())

        # Plot
        #st.line_chart(df_scan, x='Potential applied (V)', y='WE(1).Current (A)')

        # Statistics
        current_mean = df_scan['WE(1).Current (A)'].mean()
        current_std = df_scan['WE(1).Current (A)'].std()
        peak_current_forward = df['WE(1).Current (A)'].max()
        peak_potential_forward = df.loc[df['WE(1).Current (A)'].idxmax(), 'Potential applied (V)']
        min_current_reverse = df['WE(1).Current (A)'].min()
        min_potential_reverse = df.loc[df['WE(1).Current (A)'].idxmin(), 'Potential applied (V)']

        st.write(f"**Scan {i} - Current Mean:** {current_mean:.2e}")
        st.write(f"**Scan {i} - Current Standard Deviation:** {current_std:.2e}")
        st.write(f"**Scan {i} - Current Peak (Forward):** {peak_current_forward:.2e} at {peak_potential_forward:.2f} V")
        st.write(f"**Scan {i} - Current Minimum (Reverse):** {min_current_reverse:.2e} at {min_potential_reverse:.2f} V")

