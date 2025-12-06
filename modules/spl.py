import pandas as pd

def gauss_elimination(n, A, b):
    # Metode Gauss biasanya langsung hasil akhir, tidak ada tabel iterasi
    # Forward Elimination
    try:
        for i in range(n):
            if A[i][i] == 0.0: return None, "Pivot nol terdeteksi."
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
            
        # Ubah ke dataframe agar seragam (meski cuma 1 baris)
        df_res = pd.DataFrame([{"x"+str(i+1): val for i, val in enumerate(x)}])
        return df_res, x
    except Exception as e:
        return None, str(e)

def gauss_seidel(n, A, b, tol, max_iter):
    x = [0.0] * n
    results = []
    
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
            
    return pd.DataFrame(results), x

def jacobi(n, A, b, tol, max_iter):
    x = [0.0] * n
    results = []
    
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
            
    return pd.DataFrame(results), x