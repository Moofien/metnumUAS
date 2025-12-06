import pandas as pd

# Definisi Fungsi
def f_akar(x):
    return x**3 - 2*x - 5

def df_akar(x):
    return 3*x**2 - 2

# Metode Bisection
def bisection(a, b, tol, max_iter):
    results = [] # Tempat menyimpan data tabel
    
    if f_akar(a) * f_akar(b) > 0:
        return None, "Error: f(a) dan f(b) bertanda sama."
        
    iterasi = 0
    error = tol + 1
    c_old = a
    c = a # Inisialisasi awal
    
    while error > tol and iterasi < max_iter:
        c = (a + b) / 2
        fc = f_akar(c)
        
        if iterasi == 0: 
            error_str = "-"
            error_val = None
        else:
            error = abs((c - c_old) / c) if c != 0 else 0
            error_str = f"{error:.6f}"
            error_val = error
            
        # Simpan baris ke list
        results.append({
            "Iterasi": iterasi + 1,
            "a": a, "b": b, "c": c,
            "f(c)": fc, "Error": error_str
        })
        
        if f_akar(a) * fc < 0: b = c
        else: a = c
        
        c_old = c
        iterasi += 1
        
    return pd.DataFrame(results), c

# Metode Regula Falsi
def regula_falsi(a, b, tol, max_iter):
    results = []
    if f_akar(a) * f_akar(b) > 0:
        return None, "Error: f(a) dan f(b) bertanda sama."

    iterasi = 0
    error = tol + 1
    c_old = a
    c = a

    while error > tol and iterasi < max_iter:
        fa, fb = f_akar(a), f_akar(b)
        c = (a*fb - b*fa) / (fb - fa)
        fc = f_akar(c)
        
        if iterasi == 0: error_str = "-"
        else:
            error = abs((c - c_old) / c) if c != 0 else 0
            error_str = f"{error:.6f}"
            
        results.append({
            "Iterasi": iterasi + 1,
            "a": a, "b": b, "c": c,
            "f(c)": fc, "Error": error_str
        })

        if fa * fc < 0: b = c
        else: a = c
        c_old = c
        iterasi += 1
        
    return pd.DataFrame(results), c

# Metode Newton Raphson
def newton_raphson(x0, tol, max_iter):
    results = []
    iterasi = 0
    error = tol + 1
    xi = x0
    
    while error > tol and iterasi < max_iter:
        f_val = f_akar(xi)
        df_val = df_akar(xi)
        
        if df_val == 0: return None, "Gagal: Turunan 0."
        
        xi_next = xi - (f_val / df_val)
        error = abs(xi_next - xi)
        
        results.append({
            "Iterasi": iterasi + 1,
            "xi": xi, "f(xi)": f_val,
            "f'(xi)": df_val, "Error": error
        })
        
        xi = xi_next
        iterasi += 1
        
    return pd.DataFrame(results), xi

# Metode Secant
def secant(x0, x1, tol, max_iter):
    results = []
    iterasi = 0
    error = tol + 1
    
    while error > tol and iterasi < max_iter:
        fx0 = f_akar(x0)
        fx1 = f_akar(x1)
        
        if fx1 - fx0 == 0: return None, "Gagal: Pembagian nol"
        
        x_new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x_new - x1)
        
        results.append({
            "Iterasi": iterasi + 1,
            "x_curr": x1, "x_new": x_new, "Error": error
        })
        
        x0 = x1
        x1 = x_new
        iterasi += 1
        
    return pd.DataFrame(results), x1