import math
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt 

def num_classes(data): 
    num = int(input("Ingrese la cantidad de clases (o 0 para la cantidad por defecto): "))
    op1 = 1 + 3.32*math.log(len(data))
    if num <= 0 or num >= 15: 
        if op1 < 10: num = round(op1) 
        else: num = 10  
    return num
        
    
def classes(data, number):
    lower_limit, upper_limit = min(data), max(data)
    rang = upper_limit - lower_limit
    width = round(rang/number)  
    classes = [(lower_limit, lower_limit + width)]
    actual = lower_limit + width
    while actual < upper_limit:
        sig = actual + width + 1
        new = (actual, sig)
        classes.append(new)
        actual = sig
    return classes


def midpoints(classes):
    midpoint = []
    for i in classes:
        curr = (i[1] + i[0])/2
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
    clas = classes(data, num)
    marca_clase = midpoints(clas)
    absolute, absolute_cumm, relative, relative_cumm = frecuencies(clas, data)
    table = {"Clases": clas, "Marca de Clase": marca_clase, "Frecuencia Absoluta": absolute, "Frecuencia Relativa": relative, "Frec. Acum. Absoluta": absolute_cumm, "Frec. Acum. Relativa": relative_cumm}
    df = pd.DataFrame(table)
    return df 


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
    varianza = suma/(n-1)
    return varianza


def percentile_table(table, p):
    clases = table["Clases"]
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
    

def sinteticos(table, n):
    marca = table['Marca de Clase']
    relative = table['Frecuencia Relativa']
    clases = table["Clases"]
    naive, uniforme = [], []
    for i in range(len(marca)):
        num = round(n*relative[i])
        value = marca[i]
        naive += num * [value]
    
        low, high = clases[i][0], clases[i][1]
        for i in range(num):
            if i == 0: 
                value2 = random.randint(low, high)
            else: value2 = random.randint(low+1, high)
            uniforme.append(value2)
    
    return naive, uniforme


def estadisticos(data, table, naive, uniforme):
    media = [mean_table(table), np.mean(data), np.mean(naive), np.mean(uniforme)]
    varianza = [varianza_table(table, mean_table(table)), np.var(data), np.var(naive), np.var(uniforme)]
    Q1 = [percentile_table(table, 25), np.percentile(data,25), np.percentile(naive,25), np.percentile(uniforme,25)]
    Q2 = [percentile_table(table, 50), np.percentile(data,50), np.percentile(naive,50), np.percentile(uniforme,50)]
    Q3 = [percentile_table(table, 75), np.percentile(data,75), np.percentile(naive,75), np.percentile(uniforme,75)]
    estad = {'Media': media, 'Varianza': varianza, 'Q1': Q1, 'Q2 (Mediana)': Q2, 'Q3': Q3}
    nombres = ["Datos Agrupados", "Datos Crudos", "Sinteticos Naive", "Sinteticos Uniforme"]
    df = pd.DataFrame(estad, nombres)
    return df


def percentiles(sinteticos, data, table): 
    percentiles_crudos, percentiles_sinteticos, percentiles_agrupados = [], [], []
    for i in range(1,99,1):
        x1 = np.percentile(data, i)
        x2 = percentile_table(table, i)
        y = np.percentile(uniforme, i)
        percentiles_crudos.append(x1)
        percentiles_agrupados.append(x2)
        percentiles_sinteticos.append(y)
    return percentiles_crudos, percentiles_sinteticos, percentiles_agrupados



medifis = pd.read_csv('medifis.csv', sep = ';')
#data = list(medifis["estatura"])
data = [18, 20, 21, 27, 29, 20, 19, 30,32, 19, 34, 19, 24, 29, 18, 37, 38, 22, 30, 39, 32, 44, 33, 46, 54, 49, 18, 51, 21, 21]
num_c = num_classes(data)

table = build_table(data, num_c)
naive, uniforme = sinteticos(table, 1000)
estad = estadisticos(data, table, naive, uniforme)
#plt.hist(data, bins = num_c)
#plt.hist(naive, bins = num_c)

percentiles_crudos, percentiles_sinteticos, percentiles_agrupados = percentiles(uniforme, data, table)

plt.scatter(percentiles_agrupados,percentiles_sinteticos)

#asimetria y curtosis 


    

