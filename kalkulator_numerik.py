import math

# ==========================================
# KONFIGURASI FUNGSI (Untuk Akar & Integral)
# ==========================================
def f_akar(x):
    # Target: f(x) = 0. Contoh: x^3 - 2x - 5
    return x**3 - 2*x - 5

def df_akar(x):
    # Turunan f_akar. Contoh: 3x^2 - 2
    return 3*x**2 - 2

def f_integral(x):
    # Fungsi yang akan diintegralkan. Contoh: f(x) = e^x
    return math.exp(x) 

# ==========================================
# BAGIAN A: METODE AKAR (ROOT FINDING)
# ==========================================
def bisection(a, b, tol, max_iter):
    print(f"\n{'='*70}")
    print(f"METODE BISECTION (Selang: [{a}, {b}])")
    print(f"{'='*70}")
    if f_akar(a) * f_akar(b) > 0:
        print("Error: f(a) dan f(b) bertanda sama.")
        return
    print(f"{'Iter':<5} | {'a':<12} | {'b':<12} | {'c':<12} | {'f(c)':<12} | {'Error':<12}")
    print(f"{'-'*75}")
    iterasi = 0
    error = tol + 1
    c_old = a
    while error > tol and iterasi < max_iter:
        c = (a + b) / 2
        fc = f_akar(c)
        if iterasi == 0: error_str = "-"
        else:
            error = abs((c - c_old) / c) if c != 0 else 0
            error_str = f"{error:.6f}"
        print(f"{iterasi+1:<5} | {a:<12.6f} | {b:<12.6f} | {c:<12.6f} | {fc:<12.6f} | {error_str:<12}")
        if f_akar(a) * fc < 0: b = c
        else: a = c
        c_old = c
        iterasi += 1
    print(f"{'-'*75}\nAkar Hampiran: {c:.8f}")

def regula_falsi(a, b, tol, max_iter):
    print(f"\n{'='*70}")
    print(f"METODE REGULA FALSI (Selang: [{a}, {b}])")
    print(f"{'='*70}")
    if f_akar(a) * f_akar(b) > 0:
        print("Error: f(a) dan f(b) bertanda sama.")
        return
    print(f"{'Iter':<5} | {'a':<12} | {'b':<12} | {'c':<12} | {'f(c)':<12} | {'Error':<12}")
    print(f"{'-'*75}")
    iterasi = 0
    error = tol + 1
    c_old = a
    while error > tol and iterasi < max_iter:
        fa, fb = f_akar(a), f_akar(b)
        c = (a*fb - b*fa) / (fb - fa)
        fc = f_akar(c)
        if iterasi == 0: error_str = "-"
        else:
            error = abs((c - c_old) / c) if c != 0 else 0
            error_str = f"{error:.6f}"
        print(f"{iterasi+1:<5} | {a:<12.6f} | {b:<12.6f} | {c:<12.6f} | {fc:<12.6f} | {error_str:<12}")
        if fa * fc < 0: b = c
        else: a = c
        c_old = c
        iterasi += 1
    print(f"{'-'*75}\nAkar Hampiran: {c:.8f}")

def newton_raphson(x0, tol, max_iter):
    print(f"\n{'='*70}")
    print(f"METODE NEWTON-RAPHSON (Tebakan: {x0})")
    print(f"{'='*70}")
    print(f"{'Iter':<5} | {'xi':<15} | {'f(xi)':<15} | {'f\'(xi)':<15} | {'Error':<15}")
    print(f"{'-'*75}")
    iterasi = 0
    error = tol + 1
    xi = x0
    while error > tol and iterasi < max_iter:
        f_val = f_akar(xi)
        df_val = df_akar(xi)
        if df_val == 0:
            print("Gagal: Turunan 0.")
            break
        xi_next = xi - (f_val / df_val)
        error = abs(xi_next - xi)
        print(f"{iterasi+1:<5} | {xi:<15.6f} | {f_val:<15.6f} | {df_val:<15.6f} | {error:<15.6f}")
        xi = xi_next
        iterasi += 1
    print(f"{'-'*75}\nAkar Hampiran: {xi:.8f}")

def secant(x0, x1, tol, max_iter):
    print(f"\n{'='*70}")
    print(f"METODE SECANT (x0: {x0}, x1: {x1})")
    print(f"{'='*70}")
    print(f"{'Iter':<5} | {'x_curr':<12} | {'x_new':<12} | {'Error':<12}")
    print(f"{'-'*75}")
    iterasi = 0
    error = tol + 1
    while error > tol and iterasi < max_iter:
        fx0 = f_akar(x0)
        fx1 = f_akar(x1)
        if fx1 - fx0 == 0: break
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x_new - x1)
        print(f"{iterasi+1:<5} | {x1:<12.6f} | {x_new:<12.6f} | {error:<12.6f}")
        x0 = x1
        x1 = x_new
        iterasi += 1
    print(f"{'-'*75}\nAkar Hampiran: {x1:.8f}")

# ==========================================
# BAGIAN B: METODE INTEGRASI
# ==========================================
def print_header_integrasi(nama_metode, a, b, n):
    print(f"\n{'='*70}")
    print(f"{nama_metode} (Interval: [{a}, {b}], Segmen: {n})")
    print(f"{'='*70}")
    print(f"{'i':<5} | {'xi':<15} | {'f(xi)':<15} | {'Koefisien':<10}")
    print(f"{'-'*70}")

def metode_trapesium(a, b, n):
    h = (b - a) / n
    sum_y = 0
    print_header_integrasi("METODE TRAPESIUM", a, b, n)
    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        if i == 0 or i == n: koef = 1
        else: koef = 2
        sum_y += koef * yi
        print(f"{i:<5} | {xi:<15.6f} | {yi:<15.6f} | {koef:<10}")
    L = (h / 2) * sum_y
    print(f"{'-'*70}\nHasil Integrasi: {L:.8f}")

def metode_simpson_1_3(a, b, n):
    if n % 2 != 0:
        print("\nERROR: Metode Simpson 1/3 wajib n GENAP!")
        return
    h = (b - a) / n
    sum_y = 0
    print_header_integrasi("METODE SIMPSON 1/3", a, b, n)
    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        if i == 0 or i == n: koef = 1
        elif i % 2 != 0: koef = 4
        else: koef = 2
        sum_y += koef * yi
        print(f"{i:<5} | {xi:<15.6f} | {yi:<15.6f} | {koef:<10}")
    L = (h / 3) * sum_y
    print(f"{'-'*70}\nHasil Integrasi: {L:.8f}")

def metode_simpson_3_8(a, b, n):
    if n % 3 != 0:
        print("\nERROR: Metode Simpson 3/8 wajib n KELIPATAN 3!")
        return
    h = (b - a) / n
    sum_y = 0
    print_header_integrasi("METODE SIMPSON 3/8", a, b, n)
    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        if i == 0 or i == n: koef = 1
        elif i % 3 == 0: koef = 2
        else: koef = 3
        sum_y += koef * yi
        print(f"{i:<5} | {xi:<15.6f} | {yi:<15.6f} | {koef:<10}")
    L = (3 * h / 8) * sum_y
    print(f"{'-'*70}\nHasil Integrasi: {L:.8f}")

# ==========================================
# BAGIAN C: METODE SPL (Sistem Persamaan Linear)
# ==========================================
def input_matrix():
    print("\n--- Input Matriks SPL (Ax = b) ---")
    try:
        n = int(input("Masukkan jumlah variabel (n): "))
        print(f"Masukkan elemen matriks A ({n}x{n}) baris per baris:")
        A = []
        for i in range(n):
            row = list(map(float, input(f"Baris {i+1} (pisahkan dengan spasi): ").split()))
            if len(row) != n:
                print("Error: Jumlah elemen tidak sesuai.")
                return None, None, None
            A.append(row)
        
        print(f"Masukkan vektor hasil b (vektor {n} elemen):")
        b = list(map(float, input(f"Vektor b (pisahkan dengan spasi): ").split()))
        if len(b) != n:
            print("Error: Ukuran vektor b tidak sesuai.")
            return None, None, None
        return n, A, b
    except ValueError:
        print("Input salah.")
        return None, None, None

def gauss_elimination(n, A, b):
    print(f"\n{'='*50}")
    print("METODE ELIMINASI GAUSS")
    print(f"{'='*50}")
    
    # Forward Elimination
    for i in range(n):
        if A[i][i] == 0.0:
            print("Error: Pivot nol terdeteksi.")
            return

        for j in range(i+1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] = A[j][k] - ratio * A[i][k]
            b[j] = b[j] - ratio * b[i]

    # Back Substitution
    x = [0] * n
    x[n-1] = b[n-1] / A[n-1][n-1]

    for i in range(n-2, -1, -1):
        sum_ax = 0
        for j in range(i+1, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (b[i] - sum_ax) / A[i][i]

    print("\nHasil Solusi (x):")
    for i in range(n):
        print(f"x{i+1} = {x[i]:.6f}")

def gauss_seidel(n, A, b, tol, max_iter):
    print(f"\n{'='*70}")
    print("METODE GAUSS-SEIDEL")
    print(f"{'='*70}")
    x = [0.0] * n # Initial guess (semua 0)
    print(f"{'Iter':<5} | " + " | ".join([f"x{i+1:<10}" for i in range(n)]) + f" | {'Error Max':<12}")
    print("-" * 80)

    for it in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - sum_ax) / A[i][i]
        
        # Hitung Error relatif maksimum
        error = max(abs((x[i] - x_old[i]) / x[i]) for i in range(n) if x[i] != 0)
        
        # Print baris tabel
        row_vals = " | ".join([f"{val:.6f}" for val in x])
        print(f"{it+1:<5} | {row_vals} | {error:.6f}")

        if error < tol:
            print("-" * 80)
            print("Konvergen!")
            break
            
    print("\nHasil Solusi Akhir:")
    for i in range(n):
        print(f"x{i+1} = {x[i]:.6f}")

def jacobi(n, A, b, tol, max_iter):
    print(f"\n{'='*70}")
    print("METODE JACOBI")
    print(f"{'='*70}")
    x = [0.0] * n # Initial guess
    print(f"{'Iter':<5} | " + " | ".join([f"x{i+1:<10}" for i in range(n)]) + f" | {'Error Max':<12}")
    print("-" * 80)

    for it in range(max_iter):
        x_new = [0.0] * n
        
        for i in range(n):
            sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_ax) / A[i][i]
            
        error = max(abs((x_new[i] - x[i]) / x_new[i]) for i in range(n) if x_new[i] != 0)
        x = x_new
        
        row_vals = " | ".join([f"{val:.6f}" for val in x])
        print(f"{it+1:<5} | {row_vals} | {error:.6f}")

        if error < tol:
            print("-" * 80)
            print("Konvergen!")
            break
            
    print("\nHasil Solusi Akhir:")
    for i in range(n):
        print(f"x{i+1} = {x[i]:.6f}")

# ==========================================
# MAIN MENU (UTAMA)
# ==========================================
def main_menu():
    while True:
        print("\n" + "="*40)
        print("   KALKULATOR METODE NUMERIK LENGKAP")
        print("="*40)
        print("1. Akar Persamaan (Root Finding)")
        print("2. Integrasi Numerik")
        print("3. Penyelesaian SPL (Matriks)")
        print("4. Keluar")
        
        pilihan = input("Pilih kategori (1-4): ")
        
        if pilihan == '1':
            print("\n--- Metode Akar ---")
            print("1. Bisection")
            print("2. Regula Falsi")
            print("3. Newton-Raphson")
            print("4. Secant")
            m = input("Pilihan (1-4): ")
            try:
                tol = float(input("Toleransi: "))
                max_iter = int(input("Maks iterasi: "))
            except: continue

            if m == '1':
                a, b = float(input("a: ")), float(input("b: "))
                bisection(a, b, tol, max_iter)
            elif m == '2':
                a, b = float(input("a: ")), float(input("b: "))
                regula_falsi(a, b, tol, max_iter)
            elif m == '3':
                x0 = float(input("x0: "))
                newton_raphson(x0, tol, max_iter)
            elif m == '4':
                x0, x1 = float(input("x0: ")), float(input("x1: "))
                secant(x0, x1, tol, max_iter)

        elif pilihan == '2':
            print("\n--- Metode Integrasi ---")
            print("1. Trapesium")
            print("2. Simpson 1/3")
            print("3. Simpson 3/8")
            m = input("Pilihan (1-3): ")
            try:
                a, b = float(input("a: ")), float(input("b: "))
                n = int(input("n (segmen): "))
            except: continue

            if m == '1': metode_trapesium(a, b, n)
            elif m == '2': metode_simpson_1_3(a, b, n)
            elif m == '3': metode_simpson_3_8(a, b, n)
            
        elif pilihan == '3':
            print("\n--- Metode SPL ---")
            print("1. Eliminasi Gauss (Direct)")
            print("2. Gauss-Seidel (Iteratif)")
            print("3. Jacobi (Iteratif)")
            m = input("Pilihan (1-3): ")
            
            n, A, b = input_matrix()
            if n is None: continue
            
            if m == '1':
                gauss_elimination(n, A, b)
            elif m in ['2', '3']:
                try:
                    tol = float(input("Toleransi error (cth 0.0001): "))
                    max_iter = int(input("Maks iterasi: "))
                    if m == '2': gauss_seidel(n, A, b, tol, max_iter)
                    elif m == '3': jacobi(n, A, b, tol, max_iter)
                except ValueError: print("Input error.")
        
        elif pilihan == '4':
            print("Program Selesai.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main_menu()