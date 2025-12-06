import streamlit as st
import pandas as pd

# Import modul buatan sendiri dari folder 'modules'
from modules import akar, integrasi, spl

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Kalkulator Numerik",
    page_icon="🧮",
    layout="wide"
)

# Judul Utama
st.title("🧮 Project Kalkulator Metode Numerik")
st.markdown("---")

# Sidebar Menu
with st.sidebar:
    st.header("Menu Navigasi")
    menu = st.radio("Pilih Topik:", 
        ["Beranda", "Akar Persamaan", "Integrasi Numerik", "Sistem Persamaan Linear"])
    
    st.info("Dibuat oleh Kelompok XX")

# ==========================================
# 1. HALAMAN BERANDA
# ==========================================
if menu == "Beranda":
    st.subheader("Selamat Datang!")
    st.write("""
    Aplikasi ini dibuat untuk memenuhi Tugas Akhir Mata Kuliah Metode Numerik.
    
    **Fitur yang tersedia:**
    1. **Akar Persamaan**: Bisection, Regula Falsi, Newton-Raphson, Secant.
    2. **Integrasi Numerik**: Trapesium, Simpson 1/3, Simpson 3/8.
    3. **SPL**: Eliminasi Gauss, Gauss-Seidel, Jacobi.
    
    Silakan pilih menu di sebelah kiri untuk memulai perhitungan.
    """)

# ==========================================
# 2. HALAMAN AKAR PERSAMAAN
# ==========================================
elif menu == "Akar Persamaan":
    st.header("🔍 Pencarian Akar Persamaan")
    
    # Pilihan Metode
    metode = st.selectbox("Pilih Metode", 
        ["Bisection", "Regula Falsi", "Newton-Raphson", "Secant"])
    
    # Info Fungsi
    st.info("Fungsi yang digunakan (Hardcoded):")
    st.latex(r"f(x) = x^3 - 2x - 5")

    # Layout Input
    col1, col2 = st.columns(2)
    
    with col1:
        # Input khusus per metode
        if metode in ["Bisection", "Regula Falsi"]:
            a = st.number_input("Batas Bawah (a)", value=2.0)
            b = st.number_input("Batas Atas (b)", value=3.0)
        elif metode == "Newton-Raphson":
            x0 = st.number_input("Tebakan Awal (x0)", value=2.0)
        elif metode == "Secant":
            x0 = st.number_input("Tebakan Pertama (x0)", value=2.0)
            x1 = st.number_input("Tebakan Kedua (x1)", value=3.0)

    with col2:
        # Input Parameter Umum
        tol = st.number_input("Toleransi Error", value=0.0001, format="%.6f")
        max_iter = st.number_input("Maksimum Iterasi", value=20, step=1)

    # Tombol Hitung
    if st.button("Hitung Akar"):
        df_res = None
        hasil = None
        
        # Panggil Fungsi dari Module 'akar'
        if metode == "Bisection":
            df_res, hasil = akar.bisection(a, b, tol, max_iter)
        elif metode == "Regula Falsi":
            df_res, hasil = akar.regula_falsi(a, b, tol, max_iter)
        elif metode == "Newton-Raphson":
            df_res, hasil = akar.newton_raphson(x0, tol, max_iter)
        elif metode == "Secant":
            df_res, hasil = akar.secant(x0, x1, tol, max_iter)

        # Tampilkan Hasil
        if df_res is not None:
            st.success(f"✅ Akar Hampiran ditemukan: **{hasil:.8f}**")
            
            with st.expander("Lihat Tabel Iterasi", expanded=True):
                st.dataframe(df_res, use_container_width=True)
                
                # Plot Grafik Error (Opsional - Bonus Visual)
                if "Error" in df_res.columns:
                    # Bersihkan data error yang "-" agar bisa di-plot
                    chart_data = df_res[df_res["Error"] != "-"]
                    chart_data["Error"] = pd.to_numeric(chart_data["Error"])
                    st.line_chart(chart_data, x="Iterasi", y="Error")
        else:
            st.error(hasil) # Tampilkan pesan error jika ada

# ==========================================
# 3. HALAMAN INTEGRASI NUMERIK
# ==========================================
elif menu == "Integrasi Numerik":
    st.header("∫ Integrasi Numerik")
    
    metode = st.selectbox("Pilih Metode", 
        ["Trapesium", "Simpson 1/3", "Simpson 3/8"])
    
    st.info("Fungsi yang diintegralkan:")
    st.latex(r"f(x) = e^x")
    
    c1, c2, c3 = st.columns(3)
    with c1: a = st.number_input("Batas Bawah (a)", value=0.0)
    with c2: b = st.number_input("Batas Atas (b)", value=1.0)
    with c3: n = st.number_input("Jumlah Segmen (n)", value=4, step=1)
    
    if st.button("Hitung Integral"):
        df_res = None
        hasil = None
        
        if metode == "Trapesium":
            df_res, hasil = integrasi.metode_trapesium(a, b, n)
        elif metode == "Simpson 1/3":
            df_res, hasil = integrasi.metode_simpson_1_3(a, b, n)
        elif metode == "Simpson 3/8":
            df_res, hasil = integrasi.metode_simpson_3_8(a, b, n)
            
        if df_res is not None:
            st.success(f"✅ Hasil Integrasi: **{hasil:.8f}**")
            st.dataframe(df_res, use_container_width=True)
        else:
            st.error(hasil) # Error message (misal n ganjil di simpson 1/3)

# ==========================================
# 4. HALAMAN SISTEM PERSAMAAN LINEAR
# ==========================================
elif menu == "Sistem Persamaan Linear":
    st.header("🧮 Penyelesaian SPL (Matriks)")
    
    metode = st.selectbox("Pilih Metode", 
        ["Eliminasi Gauss (Direct)", "Gauss-Seidel (Iteratif)", "Jacobi (Iteratif)"])
    
    # Input Ukuran Matriks
    n_var = st.number_input("Jumlah Variabel (n)", min_value=2, max_value=10, value=3)
    
    st.write("### Masukkan Koefisien Matriks A dan Vektor b")
    st.caption("Format: A11 A12 ... | b1")
    
    # Input Grid Dinamis untuk Matriks
    matrix_A = []
    vector_b = []
    
    # Membuat Grid Input
    for i in range(n_var):
        cols = st.columns(n_var + 1) # +1 untuk vektor b
        row_vals = []
        for j in range(n_var):
            with cols[j]:
                val = st.number_input(f"A[{i+1},{j+1}]", key=f"A_{i}_{j}", value=0.0)
                row_vals.append(val)
        matrix_A.append(row_vals)
        
        with cols[n_var]: # Kolom terakhir untuk b
            val_b = st.number_input(f"b[{i+1}]", key=f"b_{i}", value=0.0)
            vector_b.append(val_b)
            
    # Input Tambahan untuk Metode Iteratif
    tol, max_iter = 0.0001, 20
    if "Iteratif" in metode:
        c1, c2 = st.columns(2)
        with c1: tol = st.number_input("Toleransi Error", value=0.0001, format="%.6f")
        with c2: max_iter = st.number_input("Maksimum Iterasi", value=20)

    if st.button("Selesaikan SPL"):
        df_res = None
        hasil = None
        
        if "Eliminasi Gauss" in metode:
            df_res, hasil = spl.gauss_elimination(n_var, matrix_A, vector_b)
        elif "Gauss-Seidel" in metode:
            df_res, hasil = spl.gauss_seidel(n_var, matrix_A, vector_b, tol, max_iter)
        elif "Jacobi" in metode:
            df_res, hasil = spl.jacobi(n_var, matrix_A, vector_b, tol, max_iter)
            
        if df_res is not None:
            st.success("✅ Solusi Ditemukan!")
            
            # Tampilkan Hasil Akhir (Vector x)
            st.write("Nilai Variabel:")
            result_dict = {f"x{i+1}": [val] for i, val in enumerate(hasil)}
            st.dataframe(pd.DataFrame(result_dict), hide_index=True)
            
            # Tampilkan Tabel Iterasi (Jika ada)
            if "Iteratif" in metode:
                st.write("Riwayat Iterasi:")
                st.dataframe(df_res, use_container_width=True)
                
                # Grafik Konvergensi Error
                if "Error Max" in df_res.columns:
                     st.line_chart(df_res, x="Iterasi", y="Error Max")
        else:
            st.error(hasil)