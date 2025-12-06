import math
import pandas as pd

def f_integral(x):
    return math.exp(x) 

def metode_trapesium(a, b, n):
    h = (b - a) / n
    sum_y = 0
    results = []
    
    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        
        if i == 0 or i == n: koef = 1
        else: koef = 2
            
        term = koef * yi
        sum_y += term
        
        results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef})

    L = (h / 2) * sum_y
    return pd.DataFrame(results), L

def metode_simpson_1_3(a, b, n):
    if n % 2 != 0: return None, "Error: n harus Genap"
    
    h = (b - a) / n
    sum_y = 0
    results = []

    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        
        if i == 0 or i == n: koef = 1
        elif i % 2 != 0: koef = 4
        else: koef = 2
            
        term = koef * yi
        sum_y += term
        results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef})

    L = (h / 3) * sum_y
    return pd.DataFrame(results), L

def metode_simpson_3_8(a, b, n):
    if n % 3 != 0: return None, "Error: n harus kelipatan 3"
    
    h = (b - a) / n
    sum_y = 0
    results = []

    for i in range(n + 1):
        xi = a + i * h
        yi = f_integral(xi)
        
        if i == 0 or i == n: koef = 1
        elif i % 3 == 0: koef = 2
        else: koef = 3
            
        term = koef * yi
        sum_y += term
        results.append({"i": i, "xi": xi, "f(xi)": yi, "Koefisien": koef})

    L = (3 * h / 8) * sum_y
    return pd.DataFrame(results), L