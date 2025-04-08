import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from threading import RLock

_lock = RLock()


st.title("Extrator de métricas")
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

    st.write("### Preview", df.head())
    st.write(f"**Número de linhas:** {len(df)}")
    st.write(f"**Número de colunas:** {len(df.columns)}")
    
    st.write("## Análise geral")
    scan1 = pd.to_numeric(df.where(df['Scan'] == 1).fillna(0)['WE(1).Current (A)'], errors='coerce')
    scan2 = pd.to_numeric(df.where(df['Scan'] == 2).fillna(0)['WE(1).Current (A)'], errors='coerce')
    scan3 = pd.to_numeric(df.where(df['Scan'] == 3).fillna(0)['WE(1).Current (A)'], errors='coerce')
    avg = (scan1 + scan2 + scan3)/3
    st.write('### Média das correntes')
    st.write(avg)

    with _lock:
        fig, ax = plt.subplots()
        ax.plot(df.where(df['Scan'] == 1)['Potential applied (V)'], avg)
        ax.set_xlabel('Potential applied (V)')
        ax.set_ylabel('WE(1).Current (A)')
        ax.set_title('Corrente média em função do potencial')
        ax.legend()
        st.pyplot(fig)

    st.write('### Descrição da média')
    st.write(avg.describe())

    for i in range(1, df['Scan'].max() + 1):
        df_scan = df.where(df['Scan'] == i).dropna(how='all')
        st.write(f"### Scan {i}")
        st.write(df_scan.head())

        st.write(f"**Número de pontos:** {len(df_scan)}")
        st.write(f"**Descrição da corrente gerada:**")
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

        st.write(f"**Mediana da corrente:** {current_mean:.2e}")
        st.write(f"**Desvio padrão da corrente:** {current_std:.2e}")
        st.write(f"**Pico da corrente (Forward):** {peak_current_forward:.2e} at {peak_potential_forward:.2f} V")
        st.write(f"**Vale da corrente (Reverse):** {min_current_reverse:.2e} at {min_potential_reverse:.2f} V")

        # Find the potential at half the peak current (forward)
        half_peak_current_forward = peak_current_forward / 2
        # Find the potential value closest to the half peak current
        potential_at_half_peak_forward = df['Potential applied (V)'].iloc[(df['WE(1).Current (A)'] - half_peak_current_forward).abs().argsort()[0]]
        st.write(f"**Potencial a metade do pico (Forward):** {potential_at_half_peak_forward:.2f} V")

        # Find the potential at half the minimum current (reverse)
        half_min_current_reverse = min_current_reverse / 2
        # Find the potential value closest to the half minimum current
        potential_at_half_min_reverse = df['Potential applied (V)'].iloc[(df['WE(1).Current (A)'] - half_min_current_reverse).abs().argsort()[0]]
        st.write(f"**Potencial a metade do vale (Reverse):** {potential_at_half_min_reverse:.2f} V")

    # Scan by scan, take the average of currents 
     
