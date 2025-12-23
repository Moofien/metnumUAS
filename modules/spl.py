import pandas as pd

# Helper: Print Matriks ke String
def matrix_to_str(A, b):
    n = len(A)
    s = ""
    for i in range(n):
        s += "[ "
        for val in A[i]:
            s += f"{val:8.4f} "
        s += f"| {b[i]:8.4f} ]\n"
    return s

# ==========================================
# 1. ELIMINASI GAUSS (Forward Elim + Back Subst)
# ==========================================
def gauss_elimination(n, A, b):
    # Copy data
    A = [row[:] for row in A]
    b = b[:]
    
    steps =  "LANGKAH PERHITUNGAN ELIMINASI GAUSS\n"
    steps += "===================================\n"
    steps += "Matriks Augmented Awal:\n"
    steps += matrix_to_str(A, b) + "\n"
    
    try:
        # A. FORWARD ELIMINATION
        steps += "A. ELIMINASI MAJU (Forward Elimination)\n"
        for i in range(n):
            # Pivot checking
            if A[i][i] == 0.0: return None, "Error: Pivot nol.", ""
            
            for j in range(i+1, n):
                ratio = A[j][i] / A[i][i]
                
                steps += f"   R{j+1} = R{j+1} - ({ratio:.4f}) * R{i+1}\n"
                
                for k in range(n):
                    A[j][k] = A[j][k] - ratio * A[i][k]
                b[j] = b[j] - ratio * b[i]
            
            if i < n-1:
                steps += f"   -> Matriks setelah eliminasi kolom {i+1}:\n"
                steps += matrix_to_str(A, b) + "\n"

        # B. BACK SUBSTITUTION
        steps += "B. SUBSTITUSI BALIK (Back Substitution)\n"
        x = [0] * n
        
        # Hitung x terakhir
        x[n-1] = b[n-1] / A[n-1][n-1]
        steps += f"   x{n} = {b[n-1]:.4f} / {A[n-1][n-1]:.4f} = {x[n-1]:.6f}\n"

        # Hitung x mundur
        for i in range(n-2, -1, -1):
            sum_ax = 0
            expr_str = ""
            for j in range(i+1, n):
                sum_ax += A[i][j] * x[j]
                expr_str += f"({A[i][j]:.4f} * {x[j]:.4f}) + "
            
            expr_str = expr_str.rstrip(" + ")
            val = (b[i] - sum_ax) / A[i][i]
            x[i] = val
            
            steps += f"   x{i+1} = ({b[i]:.4f} - [{expr_str}]) / {A[i][i]:.4f} = {x[i]:.6f}\n"

        # Hasil Akhir untuk Tabel
        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        return df_res, x, steps

    except Exception as e:
        return None, str(e), ""

# ==========================================
# 2. GAUSS-JORDAN (Diagonalisasi)
# ==========================================
def gauss_jordan(n, A, b):
    A = [row[:] for row in A]
    b = b[:]
    
    steps =  "LANGKAH PERHITUNGAN GAUSS-JORDAN\n"
    steps += "================================\n"
    steps += "Matriks Augmented Awal:\n"
    steps += matrix_to_str(A, b) + "\n"
    
    try:
        for i in range(n):
            steps += f"--- Proses Baris {i+1} (Pivot di A[{i+1},{i+1}]) ---\n"
            
            # 1. Normalisasi Pivot (Jadikan 1)
            pivot = A[i][i]
            if pivot == 0.0: return None, "Error: Pivot nol.", ""
            
            steps += f"   R{i+1} = R{i+1} / {pivot:.4f}\n"
            
            for k in range(n):
                A[i][k] /= pivot
            b[i] /= pivot
            
            # 2. Nol-kan kolom lainnya
            for j in range(n):
                if i != j:
                    ratio = A[j][i]
                    steps += f"   R{j+1} = R{j+1} - ({ratio:.4f}) * R{i+1}\n"
                    for k in range(n):
                        A[j][k] -= ratio * A[i][k]
                    b[j] -= ratio * b[i]
            
            steps += f"   -> Matriks saat ini:\n"
            steps += matrix_to_str(A, b) + "\n"
        
        x = b
        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        
        steps += "Matriks sudah menjadi Identitas. Solusi x ada di kolom paling kanan.\n"
        return df_res, x, steps

    except Exception as e:
        return None, str(e), ""

# ==========================================
# 3. GAUSS-SEIDEL (Iteratif)
# ==========================================
def gauss_seidel(n, A, b, tol, max_iter):
    x = [0.0] * n
    results = []
    
    # Tidak menghasilkan langkah teks panjang, tapi tabel iterasi
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
# 4. JACOBI (Iteratif)
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