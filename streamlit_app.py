import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import time

# Set Konfigurasi Halaman
st.set_page_config(
    page_title="Simulasi AAS Shimadzu AA-7000",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Simulasi Interaktif & Analisis AAS Shimadzu AA-7000")
st.markdown("Aplikasi simulasi Spectrophotometer Serapan Atom (AAS) khusus penentuan kadar Tembaga (**Cu**).")

# ==========================================
# TAB NAVIGATION
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🎨 Model 3D Interaktif & Komponen", 
    "🧪 Simulasi Pengukuran Cu", 
    "📊 Kurva Kalibrasi & Perhitungan Kadar"
])

# ==========================================
# TAB 1: MODEL 3D INTERAKTIF AAS SHIMADZU AA-7000
# ==========================================
with tab1:
    st.subheader("Model Visual 3D Alat AAS Shimadzu AA-7000")
    st.info("💡 **Petunjuk:** Anda dapat memutar model 3D di bawah ini 360° menggunakan *click & drag* mouse. Klik tombol di bawah untuk melihat penjelasan komponen!")

    # Menggunakan mesh/shape Plotly untuk merepresentasikan bodi instrumen Shimadzu AA-7000
    fig_3d = go.Figure()

    # Bodi Utama Instrumen (Kotak Putih/Abu)
    fig_3d.add_trace(go.Mesh3d(
        x=[-5, -5, 5, 5, -5, -5, 5, 5],
        y=[-3, 3, 3, -3, -3, 3, 3, -3],
        z=[0, 0, 0, 0, 6, 6, 6, 6],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color='#e0e0e0',
        opacity=0.9,
        name='Main Body AA-7000'
    ))

    # Penutup Atas / Top Cover (Hitam Miring khas Shimadzu AA-7000)
    fig_3d.add_trace(go.Mesh3d(
        x=[-3, -3, 3, 3, -2, -2, 2, 2],
        y=[-2, 2, 2, -2, -2, 2, 2, -2],
        z=[6, 6, 6, 6, 9, 9, 9, 9],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color='#1a1a1a',
        name='Top Hood Cover'
    ))

    # Burner / Atomizer Chamber (Tengah Front Area)
    fig_3d.add_trace(go.Mesh3d(
        x=[-1.5, -1.5, 1.5, 1.5, -1.5, -1.5, 1.5, 1.5],
        y=[-3.2, -2, -2, -3.2, -3.2, -2, -2, -3.2],
        z=[1.5, 1.5, 1.5, 1.5, 3.5, 3.5, 3.5, 3.5],
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        color='#555555',
        name='Burner Head Chamber'
    ))

    # Selang Kapiler Apirasi
    t = np.linspace(0, 1, 50)
    x_cap = -0.2 + 0.1 * np.sin(t * 5)
    y_cap = -3.2 - 0.5 * t
    z_cap = 2.0 - 1.5 * t
    fig_3d.add_trace(go.Scatter3d(
        x=x_cap, y=y_cap, z=z_cap,
        mode='lines',
        line=dict(color='cyan', width=6),
        name='Tubing Aspirasi Kapiler'
    ))

    # Layout Plotly 3D
    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(
                eye=dict(x=1.5, y=-2.0, z=1.2) # Sudut pandang awal 3D
            )
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=450
    )

    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_right:
        st.write("### 🔍 Deskripsi & Fungsi Komponen Utama")
        
        komponen = st.radio(
            "Pilih bagian komponen AAS Shimadzu AA-7000:",
            [
                "Lampu Katoda Rongga (Hollow Cathode Lamp - Cu)",
                "Nebulizer & Kapiler Aspirasi",
                "Atomizer / Kepala Burner (Nyala Api)",
                "Monokromator",
                "Detektor PMT (Photomultiplier Tube)"
            ]
        )

        if komponen == "Lampu Katoda Rongga (Hollow Cathode Lamp - Cu)":
            st.markdown("""
- **Fungsi:** Memancarkan spektrum sinar radiasi spasial dengan panjang gelombang spesifik unsur **Tembaga (Cu 324.7 nm)**.
  - **Prinsip Kerja:** Lampu terisi gas mulia (Argon/Neon). Ketika diberi tegangan tinggi, ion gas menabrak katoda berbahan Cu dan memancarkan foton khas unsur Cu.
            """)
        elif komponen == "Nebulizer & Kapiler Aspirasi":
            st.markdown("""
- **Fungsi:** Menyedot (mengaspirasi) sampel larutan cair melalui tabung kapiler tipis dan mengubahnya menjadi aerosol/kabut halus (*nebulization*).
  - **Prinsip Kerja:** Memanfaatkan efek Venturi udara bertekanan tinggi untuk merubah cairan sampel menjadi tetesan mikro sebelum masuk ke spray chamber.
            """)
        elif komponen == "Atomizer / Kepala Burner (Nyala Api)":
            st.markdown("""
- **Fungsi:** Mengubah kabut halus sampel cair menjadi atom-atom netral bebas (*ground state atoms*) menggunakan energi panas nyala api (Campuran Air-Acetylene).
  - **Prinsip Kerja:** Desolvasi (penguapan pelarut) ➔ Penguapan padatan ➔ Dissosiasi molekul menjadi atom bebas yang siap menyerap sinar HCL.
            """)
        elif komponen == "Monokromator":
            st.markdown("""
- **Fungsi:** Mengisolasi garis resonansi spesifik Tembaga ($324.7\\text{ nm}$) dari panjang gelombang atau spektrum pengganggu lainnya.
  - **Prinsip Kerja:** Menggunakan prisma atau kisi difraksi (*diffraction grating*) untuk meneruskan sinar sesuai λ yang dipilih ke detektor.
            """)
        elif komponen == "Detektor PMT (Photomultiplier Tube)":
            st.markdown("""
- **Fungsi:** Mengukur intensitas sinar radiasi yang lolos melewati nyala api dan mengubah sinyal cahaya menjadi sinyal listrik.
  - **Prinsip Kerja:** Menghitung perbandingan intensitas sinar awal ($I_0$) dan intensitas akhir yang ditransmisikan ($I$), lalu dikonversi menjadi nilai Absorban ($A$).
            """)

# ==========================================
# TAB 2: SIMULASI PENGUKURAN DAN INTERAKSI CUS
# ==========================================
with tab2:
    st.subheader("🧪 Simulasi Alur Kerja Penyerapan Sinar Radiasi Lampu Cu")

    col_sim_ctrl, col_sim_view = st.columns([1, 2])

    with col_sim_ctrl:
        st.write("#### Parameter Pengujian")
        konsentrasi_sim = st.slider("Konsentrasi Sampel Cu (ppm):", 0.0, 10.0, 3.0, step=0.5)
        
        # Asumsi Hukum Lambert-Beer: A = e * b * c (misal e*b = 0.08)
        absorbansi_sim = 0.082 * konsentrasi_sim + np.random.normal(0, 0.002)
        absorbansi_sim = max(0.0, absorbansi_sim) # Cegah nilai negatif
        
        tombol_aspirasi = st.button("🚀 Aspirasikan Sampel Ke AAS")

    with col_sim_view:
        if tombol_aspirasi:
            with st.spinner("Mengaspirasikan sampel melalui kapiler..."):
                time.sleep(1)
            st.success("Sampel berhasil di-nebulisasi & di-atomisasi pada nyala api!")
            
            # Animasi Visualisasi Sinar Radiasi
            fig_sim = go.Figure()

            # Lampu Katoda Cu (Kiri)
            fig_sim.add_trace(go.Scatter(x=[0], y=[2], mode='markers+text', 
                                         text=['HCL Cu Lamp\n(Pancar Sinar I₀)'], 
                                         textposition='bottom center',
                                         marker=dict(size=30, color='orange', symbol='square')))

            # Nyala Api (Tengah)
            fig_sim.add_trace(go.Scatter(x=[5], y=[2], mode='markers+text', 
                                         text=[f'Nyala Api\n(Atom Cu Neutral)\n[Conc: {konsentrasi_sim} ppm]'], 
                                         textposition='top center',
                                         marker=dict(size=40, color='red', symbol='triangle-up')))

            # Detektor (Kanan)
            fig_sim.add_trace(go.Scatter(x=[10], y=[2], mode='markers+text', 
                                         text=['Detektor PMT\n(Sinar sisa I)'], 
                                         textposition='bottom center',
                                         marker=dict(size=30, color='blue', symbol='square')))

            # Garis Sinar Sisa (Tergantung absorban)
            opacity_sinar = max(0.1, 1.0 - (konsentrasi_sim / 12.0))
            fig_sim.add_shape(type="line", x0=0, y0=2, x1=5, y1=2,
                              line=dict(color="gold", width=8))
            fig_sim.add_shape(type="line", x0=5, y0=2, x1=10, y1=2,
                              line=dict(color="gold", width=8 * opacity_sinar))

            fig_sim.update_layout(
                xaxis=dict(range=[-1, 11], visible=False),
                yaxis=dict(range=[0, 4], visible=False),
                height=250,
                title="Skematik Lintasan Sinar Radiasi Terabsorbsi oleh Atom Cu"
            )
            st.plotly_chart(fig_sim, use_container_width=True)

            # Menampilkan Output Hasil
            st.metric(label="Nilai Absorbansi (A) Terukur", value=f"{absorbansi_sim:.4f} AU")
            st.latex(r"A = -\log_{10}\left(\frac{I}{I_0}\right) = \varepsilon \cdot b \cdot c")

# ==========================================
# TAB 3: KALIBRASI & PERHITUNGAN KADAR
# ==========================================
with tab3:
    st.subheader("📊 Kurva Kalibrasi Deret Standar & Regresi Linier Cu")

    st.write("Masukkan data eksperimen absorbansi deret standar Tembaga (Cu):")

    # Table Input Deret Standar Default
    default_data = pd.DataFrame({
        'Konsentrasi Standar (ppm)': [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
        'Absorbansi (AU)': [0.000, 0.162, 0.325, 0.488, 0.651, 0.810]
    })

    edited_df = st.data_editor(default_data, num_rows="dynamic")

    x_std = edited_df['Konsentrasi Standar (ppm)'].values
    y_std = edited_df['Absorbansi (AU)'].values

    # Hitung Regresi Linier
    if len(x_std) >= 2:
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_std, y_std)
        r_squared = r_value**2

        col_reg, col_graph = st.columns([1, 2])

        with col_reg:
            st.write("#### Hasil Statistik Regresi:")
            st.write(f"**Slope ($m$):** `{slope:.5f}`")
            st.write(f"**Intercept ($c$):** `{intercept:.5f}`")
            st.write(f"**R-Squared ($R^2$):** `{r_squared:.5f}`")
            st.latex(rf"y = {slope:.4f}x + ({intercept:.4f})")

            st.markdown("---")
            st.write("#### Hitung Sampel Tak Diketahui")
            abs_sampel = st.number_input("Masukkan Absorbansi Sampel ($y$):", value=0.410, format="%.4f")
            
            # Rumus x = (y - c) / m
            if slope != 0:
                kadar_cu = (abs_sampel - intercept) / slope
                st.success(f"**Kadar Tembaga (Cu) Sampel:** {kadar_cu:.4f} ppm")
            else:
                st.error("Slope tidak boleh nol!")

        with col_graph:
            # Buat Garis Regresi Plot
            x_line = np.linspace(min(x_std), max(x_std), 100)
            y_line = slope * x_line + intercept

            fig_calib = go.Figure()
            # Titik Standar
            fig_calib.add_trace(go.Scatter(x=x_std, y=y_std, mode='markers', name='Data Standar',
                                           marker=dict(size=10, color='blue')))
            # Garis Linier
            fig_calib.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Garis Regresi',
                                           line=dict(color='red', dash='dash')))
            
            # Titik Sampel
            if 'kadar_cu' in locals():
                fig_calib.add_trace(go.Scatter(x=[kadar_cu], y=[abs_sampel], mode='markers', name='Sampel Test',
                                               marker=dict(size=14, color='green', symbol='star')))

            fig_calib.update_layout(
                title="Kurva Kalibrasi Standar Cu",
                xaxis_title="Konsentrasi Cu (ppm)",
                yaxis_title="Absorbansi (AU)",
                height=400
            )
            st.plotly_chart(fig_calib, use_container_width=True)

st.markdown("---")
st.caption("Aplikasi Dibuat untuk Simulasi Laboratorium Analisis Spektroskopi AAS Shimadzu AA-7000.")
