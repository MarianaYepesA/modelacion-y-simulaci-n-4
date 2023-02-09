import math
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt 
from scipy.stats import skew, kurtosis

def num_classes(data): 
    num = int(input("Ingrese la cantidad de clases (o 0 para la cantidad por defecto): "))
    op1 = 1 + 3.32*math.log(len(data))
    if num <= 0 or num >= 15: 
        if op1 < 10: num = round(op1) 
        else: num = 10  
    return num
        
    
def classes(data, number):
    lower_limit, upper_limit = int(min(data))-1, int(max(data)+1)
    rang = upper_limit - lower_limit
    width = math.trunc(rang/number) 
    actual = lower_limit + width
    classes = [(lower_limit, actual)]

    while actual < upper_limit:
        sig = actual + width 
        new = (actual, sig)
        classes.append(new)
        actual = sig
    return classes


def midpoints(classes):
    midpoint = []
    for i in range(len(classes)):
        if i == len(classes): 
            curr = (classes[i][1] + classes[i][0])/2
        else: curr = (classes[i][1] + classes[i][0])/2
        midpoint.append(curr)
    return midpoint


def frecuencies(classes, data):
    absolute, relative = [], []
    n = len(data)
    for i in range(len(classes)):
        current = 0
        for j in data:
            if i == 0:
                if j >= classes[i][0] and j <= classes[i][1]:
                    current = current + 1 
            else: 
                if j > classes[i][0] and j <= classes[i][1]:
                    current = current + 1 
        absolute.append(current)
        relative.append(current/n)
    
    absolute_cumm, relative_cumm = [], [] 
    for i in range(len(absolute)):
        if i == 0: 
            actual1, actual2 = absolute[i], relative[i]
        else:
            actual1, actual2 = absolute[i] + absolute_cumm[i-1], relative[i] + relative_cumm[i-1]
        absolute_cumm.append(actual1)
        relative_cumm.append(actual2)
        
    return absolute, absolute_cumm, relative, relative_cumm
    

def build_table(data, num):
    clases = classes(data, num)
    marca_clase = midpoints(clases)
    absolute, absolute_cumm, relative, relative_cumm = frecuencies(clases, data)
    texto_clases = []
    for i in range(len(clases)):
        if i == 0: new = "[{}, {}]".format(clases[i][0], clases[i][1])
        else: new = "({}, {}]".format(clases[i][0], clases[i][1])
        texto_clases.append(new)
    
    table = {"Clases": texto_clases, "Marca de Clase": marca_clase, "Frecuencia Absoluta": absolute, "Frecuencia Relativa": relative, "Frec. Acum. Absoluta": absolute_cumm, "Frec. Acum. Relativa": relative_cumm}
    df = pd.DataFrame(table)
    return df 


def sinteticos(table, n, num_c, datos1):
    marca = table['Marca de Clase']
    relative = table['Frecuencia Relativa']
    clases = classes(datos1, num_c)
    naive, uniforme = [], []
    for i in range(len(marca)):
        num = round(n*relative[i])
        value = marca[i]
        naive += num * [value]
    
        low, high = clases[i][0], clases[i][1]
        for i in range(num+1):
            if i == 0: 
                value2 = random.uniform(low, high)
            else: value2 = random.uniform(low, high)
            uniforme.append(value2)
    
    return naive, uniforme


def mean_table(table):
    marca, absoluta = table['Marca de Clase'], table['Frecuencia Absoluta']
    suma = 0
    for i in range(len(marca)):
        suma += marca[i]*absoluta[i]
    media = suma/(table['Frec. Acum. Absoluta'].iloc[-1])
    return media


def varianza_table(table, mean):
    marca, absoluta = table['Marca de Clase'], table['Frecuencia Absoluta']
    suma = 0
    n = table['Frec. Acum. Absoluta'].iloc[-1]
    for i in range(len(marca)):
        val = absoluta[i]*((marca[i] - mean)**2)
        suma += val
    varianza = suma/n
    return varianza


def asimetria_table(table, mean, sd):
    marca, absoluta = table['Marca de Clase'], table['Frecuencia Absoluta']
    suma = 0
    n = table['Frec. Acum. Absoluta'].iloc[-1]
    for i in range(len(marca)):
        val = absoluta[i]*((marca[i] - mean)**3)
        suma += val
    asimetria = suma/(n*(sd**3))
    return asimetria


def curtosis_table(table, mean, sd):
    marca, absoluta = table['Marca de Clase'], table['Frecuencia Absoluta']
    suma = 0
    n = table['Frec. Acum. Absoluta'].iloc[-1]
    for i in range(len(marca)):
        val = absoluta[i]*((marca[i] - mean)**4)
        suma += val
    curtosis = suma/(n*(sd**4))
    return curtosis


def percentile_table(table, p, clases):
    absolute_cumm = table['Frec. Acum. Absoluta']
    total = (absolute_cumm.iloc[-1])
    val = p*0.01*total
    for i in range(len(clases)):
        if i == 0:
            if val <= absolute_cumm[i]:
                clase, index = clases[i], i
        else:
            if val <= absolute_cumm[i] and val >= absolute_cumm[i-1]:
                clase, index = clases[i], i
    L = clase[0]
    k = clase[1] - clase[0]
    n = table['Frecuencia Absoluta'].iloc[index]
    if index == 0: 
        j = val
    else: j = val - absolute_cumm[index-1]
    percentil = L + k*(j/n)        
    return percentil
    

def estadisticos(data, table, naive, uniforme, num_c):
    clases = classes(data, num_c)
    media = [mean_table(table), np.mean(data), np.mean(naive), np.mean(uniforme)]
    desv = [math.sqrt(varianza_table(table, mean_table(table))), np.std(data), np.std(naive), np.std(uniforme)]
    Q1 = [percentile_table(table, 25, clases), np.percentile(data,25), np.percentile(naive,25), np.percentile(uniforme,25)]
    Q2 = [percentile_table(table, 50, clases), np.percentile(data,50), np.percentile(naive,50), np.percentile(uniforme,50)]
    Q3 = [percentile_table(table, 75, clases), np.percentile(data,75), np.percentile(naive,75), np.percentile(uniforme,75)]
    asimetria = [asimetria_table(table, media[0], desv[0]), skew(data), skew(naive), skew(uniforme)]
    curtosis = [curtosis_table(table, media[0], desv[0]), kurtosis(data), kurtosis(naive), kurtosis(uniforme)]
    estad = {'Media': media, 'Desv Estándar': desv, 'Q1': Q1, 'Q2 (Mediana)': Q2, 'Q3': Q3, 'Asimetría': asimetria, 'Curtosis': curtosis}
    nombres = ["Datos Agrupados", "Datos Crudos", "Sinteticos Naive", "Sinteticos Uniforme"]
    df = pd.DataFrame(estad, nombres)
    return df


def percentiles(sinteticos, data, table, num_c): 
    clases = classes(data, num_c)
    percentiles_crudos, percentiles_sinteticos, percentiles_agrupados = [], [], []
    for i in range(1,99,1):
        x1 = np.percentile(data, i)
        x2 = percentile_table(table, i, clases)
        y = np.percentile(sinteticos, i)
        percentiles_crudos.append(x1)
        percentiles_agrupados.append(x2)
        percentiles_sinteticos.append(y)
    return percentiles_crudos, percentiles_sinteticos, percentiles_agrupados


def fix_bins(clases):
    bins = []
    for i in range(len(clases)):
        if i == 0:
            new1 = clases[i][0]
            new2 = clases[i][1] + 0.00001
            bins.append(new1)
            bins.append(new2)
        else: 
            new1 = clases[i][1] + 0.00001
            bins.append(new1)
    return bins


def datos1():
    datos_ns = list(np.random.normal(0,1,800))
    datos_exp = list(np.random.exponential(4,200))
    datos1 = datos_ns + datos_exp
    n = len(datos1)
    num_c = num_classes(datos1)
    table = build_table(datos1, num_c)
    naive, uniforme = sinteticos(table, 10*n, num_c, datos1)
    estad = estadisticos(datos1, table, naive, uniforme, num_c)
    percentiles_crudos, percentiles_sinteticos, percentiles_agrupados = percentiles(uniforme, datos1, table, num_c)
 
    bins_hist = fix_bins(classes(datos1, num_c)) 
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)     
    ax1.hist(datos1, bins = bins_hist, edgecolor = "black")
    ax1.set_title('Crudos Mixtura')     
    ax2.hist(uniforme, bins = bins_hist, edgecolor = "black")
    ax2.set_title('Generados Mixtura')
    plt.show()
    
    fig2, ax3 = plt.subplots()
    ax3.scatter(percentiles_sinteticos,percentiles_crudos, color = 'red')
    ax3.set_title("Percentiles Mixtura")
    ax3.set_xlabel("Percentiles Datos Simulados")
    ax3.set_ylabel("Percentiles Datos Crudos")
    low, high = min(percentiles_sinteticos), max(percentiles_sinteticos) + 1
    ax3.plot([low,high], [low,high], color = 'black')
    plt.show()
    
    return table, estad


def datos2():
    archivo = pd.read_csv('portfolio5.csv')
    datos2 = list(archivo['Other'])
    n = len(datos2)
    num_c = num_classes(datos2)
    table = build_table(datos2, num_c)
    naive, uniforme = sinteticos(table, 10*n, num_c, datos2)
    estad = estadisticos(datos2, table, naive, uniforme, num_c)
    percentiles_crudos, percentiles_sinteticos, percentiles_agrupados = percentiles(uniforme, datos2, table, num_c)
    
    bins_hist = fix_bins(classes(datos2, num_c)) 
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)     
    ax1.hist(datos2, bins = bins_hist, edgecolor = "black", color = 'seagreen')
    ax1.set_title('Crudos Portfolio5')     
    ax2.hist(uniforme, bins = bins_hist, edgecolor = "black", color = 'seagreen')
    ax2.set_title('Generados Portfolio5')
    plt.show()
    
    fig2, ax3 = plt.subplots()
    ax3.scatter(percentiles_sinteticos,percentiles_crudos, color = 'm')
    ax3.set_title("Percentiles Portfolio5")
    ax3.set_xlabel("Percentiles Datos Simulados")
    ax3.set_ylabel("Percentiles Datos Crudos")
    low, high = min(percentiles_sinteticos), max(percentiles_sinteticos) + 1
    ax3.plot([low,high], [low,high], color = 'black')
    plt.show()
    
    return table, estad


print("--- Datos de la mixtura --- ")
table1, estad1 = datos1()
print("\n--- Datos de la última columna de Portolfio5 --- ")
table2, estad2 = datos2()

