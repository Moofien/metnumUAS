import pandas as pd
import sympy as sp

# Helper: Parsing fungsi
def parse_function(func_str):
    x = sp.symbols('x')
    try:
        expr = sp.sympify(func_str)
        f = sp.lambdify(x, expr, "numpy")
        return f
    except:
        return None

# ==========================================
# 1. METODE TRAPESIUM
# ==========================================
def metode_trapesium(func_str, a, b, n):
    f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah.", ""

    h = (b - a) / n
    sum_y = 0
    results = []
    
    steps =  "LANGKAH PERHITUNGAN METODE TRAPESIUM\n"
    steps += "====================================\n"
    steps += f"1. Diketahui:\n"
    steps += f"   - f(x) : {func_str}\n"
    steps += f"   - h    : ({b} - {a}) / {n} = {h}\n\n"
    steps += f"2. Tabel Evaluasi:\n"
    steps += f"   ----------------------------------------------------------\n"
    steps += f"   |  i  |     xi     |     f(xi)    | Koef |    Hasil     |\n"
    steps += f"   ----------------------------------------------------------\n"

    try:
        sum_middle = 0
        f_start = 0
        f_end = 0

        for i in range(n + 1):
            xi = a + i * h
            yi = f(xi)
            
            if i == 0: 
                koef = 1
                f_start = yi
            elif i == n: 
                koef = 1
                f_end = yi
            else: 
                koef = 2
                sum_middle += yi
                
            term = koef * yi
            sum_y += term
            
            # Format Tabel Manual Rapi
            steps += f"   | {i:3d} | {xi:10.4f} | {yi:12.6f} | {koef:4d} | {term:12.6f} |\n"
            results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef, "Term": term})

        L = (h / 2) * sum_y
        
        steps += f"   ----------------------------------------------------------\n"
        steps += f"   Total Jumlah (Sigma)                    = {sum_y:12.6f}\n\n"

        steps += f"3. Rumus Akhir:\n"
        steps += "   L = (h/2) * [ f(awal) + 2*(Total Tengah) + f(akhir) ]\n"
        steps += f"   L = ({h}/2) * {sum_y:.6f}\n"
        steps += f"   L = {L:.8f}"

        return pd.DataFrame(results), L, steps
    except Exception as e:
        return None, f"Error: {str(e)}", ""

# ==========================================
# 2. METODE SIMPSON 1/3
# ==========================================
def metode_simpson_1_3(func_str, a, b, n):
    if n % 2 != 0: return None, "Error: n harus GENAP", ""
    
    f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah.", ""

    h = (b - a) / n
    sum_y = 0
    results = []

    steps =  "LANGKAH PERHITUNGAN METODE SIMPSON 1/3\n"
    steps += "======================================\n"
    steps += f"1. Diketahui:\n"
    steps += f"   - f(x) : {func_str}\n"
    steps += f"   - h    : {h}\n\n"
    steps += f"2. Tabel Evaluasi:\n"
    steps += f"   ----------------------------------------------------------\n"
    steps += f"   |  i  |     xi     |     f(xi)    | Koef |    Hasil     |\n"
    steps += f"   ----------------------------------------------------------\n"

    try:
        sum_odd = 0   # Jumlah Ganjil
        sum_even = 0  # Jumlah Genap
        f_start = 0
        f_end = 0

        for i in range(n + 1):
            xi = a + i * h
            yi = f(xi)
            
            if i == 0: 
                koef = 1
                f_start = yi
            elif i == n: 
                koef = 1
                f_end = yi
            elif i % 2 != 0: 
                koef = 4
                sum_odd += yi
            else: 
                koef = 2
                sum_even += yi
                
            term = koef * yi
            sum_y += term
            
            steps += f"   | {i:3d} | {xi:10.4f} | {yi:12.6f} | {koef:4d} | {term:12.6f} |\n"
            results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef, "Term": term})

        L = (h / 3) * sum_y
        
        steps += f"   ----------------------------------------------------------\n"
        steps += f"   Total Jumlah (Sigma)                    = {sum_y:12.6f}\n\n"

        steps += f"3. Rumus Akhir:\n"
        steps += "   L = (h/3) * [ f(awal) + 4(Total Ganjil) + 2(Total Genap) + f(akhir) ]\n"
        steps += f"   L = ({h:.4f}/3) * [ {f_start:.4f} + 4({sum_odd:.4f}) + 2({sum_even:.4f}) + {f_end:.4f} ]\n"
        steps += f"   L = ({h:.4f}/3) * {sum_y:.6f}\n"
        steps += f"   L = {L:.8f}"

        return pd.DataFrame(results), L, steps
    except Exception as e:
        return None, f"Error: {str(e)}", ""

# ==========================================
# 3. METODE SIMPSON 3/8
# ==========================================
def metode_simpson_3_8(func_str, a, b, n):
    if n % 3 != 0: return None, "Error: n harus Kelipatan 3", ""
    
    f = parse_function(func_str)
    if f is None: return None, "Error: Format fungsi salah.", ""
    
    h = (b - a) / n
    sum_y = 0
    results = []

    steps =  "LANGKAH PERHITUNGAN METODE SIMPSON 3/8\n"
    steps += "======================================\n"
    steps += f"1. Diketahui:\n"
    steps += f"   - f(x) : {func_str}\n"
    steps += f"   - h    : {h}\n\n"
    steps += f"2. Tabel Evaluasi:\n"
    steps += f"   ----------------------------------------------------------\n"
    steps += f"   |  i  |     xi     |     f(xi)    | Koef |    Hasil     |\n"
    steps += f"   ----------------------------------------------------------\n"

    try:
        sum_non_multiples = 0
        sum_multiples = 0
        f_start = 0
        f_end = 0

        for i in range(n + 1):
            xi = a + i * h
            yi = f(xi)
            
            if i == 0: 
                koef = 1
                f_start = yi
            elif i == n: 
                koef = 1
                f_end = yi
            elif i % 3 == 0: 
                koef = 2
                sum_multiples += yi
            else: 
                koef = 3
                sum_non_multiples += yi
                
            term = koef * yi
            sum_y += term
            
            steps += f"   | {i:3d} | {xi:10.4f} | {yi:12.6f} | {koef:4d} | {term:12.6f} |\n"
            results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef, "Term": term})

        L = (3 * h / 8) * sum_y
        
        steps += f"   ----------------------------------------------------------\n"
        steps += f"   Total Jumlah (Sigma)                    = {sum_y:12.6f}\n\n"

        steps += f"3. Rumus Akhir:\n"
        steps += "   L = (3h/8) * [ f(awal) + 3(Total Bukan 3k) + 2(Total Kelipatan 3k) + f(akhir) ]\n"
        steps += f"   L = (3*{h:.4f}/8) * {sum_y:.6f}\n"
        steps += f"   L = {L:.8f}"

        return pd.DataFrame(results), L, steps
    except Exception as e:
        return None, f"Error: {str(e)}", ""