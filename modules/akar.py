import pandas as pd
import sympy as sp

# Helper untuk mengubah string menjadi fungsi matematika
def parse_function(func_str):
    x = sp.symbols('x')
    try:
        # Ubah string jadi expression sympy
        expr = sp.sympify(func_str)
        # Ubah jadi fungsi python biasa f(x)
        f = sp.lambdify(x, expr, "numpy")
        return x, expr, f
    except:
        return None, None, None

# ==========================================
# 1. METODE BISECTION
# ==========================================
def bisection(func_str, a, b, tol, max_iter):
    # Parsing fungsi dari string user
    x_sym, expr, f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah."

    results = [] 
    
    try:
        if f(a) * f(b) > 0:
            return None, "Error: f(a) dan f(b) bertanda sama (tidak mengapit akar)."
    except Exception as e:
        return None, f"Error Evaluasi Fungsi: {e}"
        
    iterasi = 0
    error = tol + 1
    c_old = a
    c = a 
    
    while error > tol and iterasi < max_iter:
        c = (a + b) / 2
        fc = f(c)
        
        if iterasi == 0: 
            error_str = "-"
        else:
            error = abs((c - c_old) / c) if c != 0 else 0
            error_str = f"{error:.6f}"
            
        results.append({
            "Iterasi": iterasi + 1,
            "a": a, "b": b, "c": c,
            "f(c)": fc, "Error": error_str
        })
        
        if f(a) * fc < 0: b = c
        else: a = c
        
        c_old = c
        iterasi += 1
        
    return pd.DataFrame(results), c

# ==========================================
# 2. METODE REGULA FALSI
# ==========================================
def regula_falsi(func_str, a, b, tol, max_iter):
    x_sym, expr, f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah."

    results = []
    try:
        if f(a) * f(b) > 0:
            return None, "Error: f(a) dan f(b) bertanda sama."
    except:
        return None, "Error saat menghitung nilai fungsi."

    iterasi = 0
    error = tol + 1
    c_old = a
    c = a

    while error > tol and iterasi < max_iter:
        fa, fb = f(a), f(b)
        
        # Cegah pembagian nol
        if (fb - fa) == 0: return None, "Error: Pembagian dengan nol (fb - fa = 0)"
        
        c = (a*fb - b*fa) / (fb - fa)
        fc = f(c)
        
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

# ==========================================
# 3. METODE NEWTON RAPHSON
# ==========================================
def newton_raphson(func_str, x0, tol, max_iter):
    x_sym, expr, f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah."

    # OTOMATIS MENGHITUNG TURUNAN! (Hebatnya Sympy)
    expr_diff = sp.diff(expr, x_sym)
    df = sp.lambdify(x_sym, expr_diff, "numpy")

    results = []
    iterasi = 0
    error = tol + 1
    xi = x0
    
    while error > tol and iterasi < max_iter:
        f_val = f(xi)
        df_val = df(xi)
        
        if df_val == 0: return None, "Gagal: Turunan bernilai 0."
        
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

# ==========================================
# 4. METODE SECANT
# ==========================================
def secant(func_str, x0, x1, tol, max_iter):
    x_sym, expr, f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah."

    results = []
    iterasi = 0
    error = tol + 1
    
    while error > tol and iterasi < max_iter:
        fx0 = f(x0)
        fx1 = f(x1)
        
        if fx1 - fx0 == 0: return None, "Gagal: Pembagian nol (fx1 - fx0 = 0)"
        
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