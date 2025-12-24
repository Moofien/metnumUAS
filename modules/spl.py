import pandas as pd

# Helper: Print Matriks ke String
def matrix_to_str(A):
    n = len(A)
    s = ""
    for i in range(n):
        s += "[ "
        for val in A[i]:
            s += f"{val:8.4f} "
        s += "]\n"
    return s

def vector_to_str(v):
    return "[ " + " ".join([f"{val:8.4f}" for val in v]) + " ]"

# ==========================================
# 1. ELIMINASI GAUSS
# ==========================================
def gauss_elimination(n, A, b):
    A = [row[:] for row in A]
    b = b[:]
    
    steps =  "LANGKAH PERHITUNGAN ELIMINASI GAUSS\n"
    steps += "===================================\n"
    
    try:
        # Forward Elimination
        for i in range(n):
            if A[i][i] == 0.0: return None, "Error: Pivot nol.", ""
            for j in range(i+1, n):
                ratio = A[j][i] / A[i][i]
                steps += f"R{j+1} = R{j+1} - ({ratio:.4f}) * R{i+1}\n"
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
            
        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        return df_res, x, steps
    except Exception as e:
        return None, str(e), ""

# ==========================================
# 2. GAUSS-JORDAN
# ==========================================
def gauss_jordan(n, A, b):
    A = [row[:] for row in A]
    b = b[:]
    
    steps =  "LANGKAH PERHITUNGAN GAUSS-JORDAN\n"
    steps += "================================\n"
    
    try:
        for i in range(n):
            pivot = A[i][i]
            if pivot == 0.0: return None, "Error: Pivot nol.", ""
            
            steps += f"Baris {i+1} dibagi {pivot:.4f} agar pivot jadi 1\n"
            for k in range(n): A[i][k] /= pivot
            b[i] /= pivot
            
            for j in range(n):
                if i != j:
                    ratio = A[j][i]
                    steps += f"R{j+1} - ({ratio:.4f}) * R{i+1} -> Nol-kan kolom {i+1}\n"
                    for k in range(n): A[j][k] -= ratio * A[i][k]
                    b[j] -= ratio * b[i]
        
        x = b
        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        return df_res, x, steps
    except Exception as e:
        return None, str(e), ""

# ==========================================
# 3. LU DECOMPOSITION (DOOLITTLE) - BARU!
# ==========================================
def lu_decomposition(n, A, b):
    # Inisialisasi L dan U
    # L = Identitas (Diagonal 1), U = Kosong
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    steps =  "LANGKAH PERHITUNGAN LU DECOMPOSITION\n"
    steps += "====================================\n"
    steps += "Menggunakan Metode Doolittle (L memiliki diagonal 1)\n\n"

    try:
        # 1. Faktorisasi A menjadi L dan U
        for i in range(n):
            # Matriks U (Segitiga Atas)
            for k in range(i, n):
                sum_val = sum(L[i][j] * U[j][k] for j in range(i))
                U[i][k] = A[i][k] - sum_val
            
            # Matriks L (Segitiga Bawah)
            for k in range(i, n):
                if i == k:
                    L[i][i] = 1.0 # Doolittle: Diagonal L selalu 1
                else:
                    sum_val = sum(L[k][j] * U[j][i] for j in range(i))
                    if U[i][i] == 0: return None, "Error: Pembagian nol di U.", ""
                    L[k][i] = (A[k][i] - sum_val) / U[i][i]

        steps += "1. Hasil Faktorisasi Matriks A = L * U\n"
        steps += "Matriks L (Lower):\n" + matrix_to_str(L) + "\n"
        steps += "Matriks U (Upper):\n" + matrix_to_str(U) + "\n"

        # 2. Forward Substitution (Ly = b) -> Mencari y
        y = [0.0] * n
        for i in range(n):
            sum_val = sum(L[i][j] * y[j] for j in range(i))
            y[i] = b[i] - sum_val
        
        steps += "2. Forward Substitution (Ly = b)\n"
        steps += f"   Vektor y ditemukan: {vector_to_str(y)}\n\n"

        # 3. Back Substitution (Ux = y) -> Mencari x
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            sum_val = sum(U[i][j] * x[j] for j in range(i+1, n))
            if U[i][i] == 0: return None, "Error: Solusi infinit.", ""
            x[i] = (y[i] - sum_val) / U[i][i]

        steps += "3. Backward Substitution (Ux = y)\n"
        steps += f"   Vektor x (Solusi Akhir): {vector_to_str(x)}\n"

        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        return df_res, x, steps

    except Exception as e:
        return None, str(e), ""

# ==========================================
# 4. GAUSS-SEIDEL (Iteratif)
# ==========================================
def gauss_seidel(n, A, b, tol, max_iter):
    x = [0.0] * n
    results = []
    steps = ""
    for it in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - sum_ax) / A[i][i]
        error = max(abs((x[i] - x_old[i]) / x[i]) for i in range(n) if x[i] != 0)
        row = {"Iterasi": it + 1}
        for i in range(n): row[f"x{i+1}"] = x[i]
        row["Error Max"] = error
        results.append(row)
        if error < tol: break
    return pd.DataFrame(results), x, steps

# ==========================================
# 5. JACOBI (Iteratif)
# ==========================================
def jacobi(n, A, b, tol, max_iter):
    x = [0.0] * n
    results = []
    steps = ""
    for it in range(max_iter):
        x_new = [0.0] * n
        for i in range(n):
            sum_ax = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_ax) / A[i][i]
        error = max(abs((x_new[i] - x[i]) / x_new[i]) for i in range(n) if x_new[i] != 0)
        x = x_new
        row = {"Iterasi": it + 1}
        for i in range(n): row[f"x{i+1}"] = x[i]
        row["Error Max"] = error
        results.append(row)
        if error < tol: break
    return pd.DataFrame(results), x, steps