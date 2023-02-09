# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 18:16:11 2023

@author: Mariana Yepes
"""
import statistics
import pandas as pd
import numpy as np
from scipy import stats
import random
import matplotlib.pyplot as plt
import math
from scipy.stats import skew
from scipy.stats import kurtosis
def leer_datos():
    try:
        archivo = input("Ingresa el nombre del archivo: ")
        arch = open(archivo, 'r')
    except FileNotFoundError:
        print("File not found.")
        archivo = input("Enter a file name: ")
        arch = open(archivo, 'r')
    for line in arch:
        try:
            strip = line.strip('\n')
            data = strip.split(', ')
        except:
            data = line.strip('\n')

    try:
        data = [int(num) for num in data]
    except:
        data = [float(num) for num in data]

    return data
def leer_crudos(crudos):
    if isinstance(crudos,pd.core.series.Series):
        return pd.DataFrame(crudos)
    else:
        raw_data = pd.read_csv(crudos,header=None)    
    if len(raw_data.columns) > 1:
        print(f"presiona enter para trabajar solo con la primera columna")
        print(f"Escribe la columna con la que quieres trabajar")
        decision = input()
        if not decision:
            return raw_data.squeeze()
        elif decision=='todo':
            columns = list(raw_data.columns)
            data = raw_data[0].squeeze()
        else:
            decision = list(map(int,decision.split()))
            columns = list(crudos.columns)
            drop = [x for x in columns if x not in decision]
            raw_data = raw_data.drop(axis=1,columns=drop)
            raw_data.columns = range(raw_data.columns.size)
            columns = list(raw_data.columns)
            data = raw_data[0].squeeze()
        if len(columns) > 1:
            for column in columns[1:]:
                data = pd.concat([data,raw_data[column].squeeze()])
    return pd.DataFrame(data) 
def crear_tabla_freq(data, num_clases):
    min_data = data[0].min()
    min_data_ocurr = data[0].value_counts()[min_data]
    max_data = data[0].max()
    range_data = max_data - min_data
    class_width = float(range_data/num_clases)
    bins = np.arange(min_data,max_data+class_width,class_width)
    data['Limites de clase (superior-inferior)'] = pd.cut(data[0],bins=bins)
    data = data.groupby("Limites de clase (superior-inferior)")[0].count().to_frame(name="Frecuencia_absoluta")
    data.iloc[0]["Frecuencia_absoluta"] += min_data_ocurr
    data["anchoclase"]=0
    data["Frecuencia relativa"] = data.Frecuencia_absoluta/data.Frecuencia_absoluta.sum()
    data["Frecuencia absoluta acumulada"] = data.Frecuencia_absoluta.cumsum()
    data["Frecuencia relativa acumulada"] = data["Frecuencia relativa"].cumsum()
    data = data.reset_index()
    data['Marca de clase'] = data['Limites de clase (superior-inferior)'].apply(lambda x: (x.left+x.right)/2)
    cols = data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    for i in range(len(data["Frecuencia relativa"])):
        data["anchoclase"][i]=class_width
    return data
def datos_sinteticos_uniformes(df,requeridos):
    l=[]
    intervalos = df["Limites de clase (superior-inferior)"] 
    for i in range(len(intervalos)):
      hasta=int(requeridos*df["Frecuencia relativa"][i])
      for j in range(hasta):
       #l.append(random.uniform(df["liminf"][i], df["limsup"][i]))
       if i==0:
          l.append(random.uniform(int(intervalos.iloc[i].left), 1+int(intervalos.iloc[i].right)))
       else:
          l.append(random.uniform(int(intervalos.iloc[i].left), 1+int(intervalos.iloc[i].right)))
    #t=np.vstack( l )
    #t.tolist()
    #lista_uniformes_aplanda = [item for sublist in t for item in sublist]
    #return lista_uniformes_aplanda
    return l
def percentil(tabla, n ,percentil):
    p = percentil/100 * n
    intervalos=tabla["Limites de clase (superior-inferior)"]
    for acum in range(len(tabla['Frecuencia absoluta acumulada'])):
        if p >= tabla['Frecuencia absoluta acumulada'][acum] and p< tabla['Frecuencia absoluta acumulada'][acum+1]:
            j = p-tabla['Frecuencia absoluta acumulada'][acum]
           # print(f"j={j}")
            c=acum+1
    # k: ancho de la clase
    k = (tabla['anchoclase'][c])
    #print(f"k={k}")
    #j: para pasar a la siguiente clase
    # nC: frecuencia de esa clase
    nC= tabla['Frecuencia_absoluta'][c]
    ans = (intervalos.iloc[c].left) + k*(j/nC)
    return ans
def estadisticosAgrupados(data, tabla):
    tabla["Marca de clase"]=tabla["Marca de clase"].astype("int")
    media= sum(((tabla['Marca de clase']))*(tabla['Frecuencia_absoluta']))/len(data)
    varianza= sum(((tabla['Marca de clase']) - media)**2 *tabla['Frecuencia_absoluta'])/len(data)
    desviacion= math.sqrt(varianza)
    intervalos=tabla["Limites de clase (superior-inferior)"]
    percentil25= percentil(tabla, len(data), 25)
    percentil50= percentil(tabla, len(data), 50)
    percentil75= percentil(tabla, len(data), 75)
    mini= int(intervalos.iloc[0].left)
    maxi=int(intervalos.iloc[len(tabla)-1].right)
    #kurtosis = (np.sum((tabla["Frecuencia absoluta"] * (tabla["Marca de clase"])) - media)**4) / (varianza**2 * len(data))
    s=tabla['Marca de clase'].repeat(tabla['Frecuencia_absoluta']).reset_index(drop=True)
    asimetria=s.skew()
    kurtosis=s.kurtosis()
    #moda = max(tabla['F Absoluta'])   
    return [len(data), media, desviacion,mini , percentil25, percentil50, percentil75, maxi,asimetria,kurtosis]
def compare_all2(data,lista_uniformes_aplanada,df2):
    uniformes=pd.Series(lista_uniformes_aplanada)
    listaoriginal=pd.Series(data[0])
    ld=listaoriginal.describe()
    lu=uniformes.describe()
    ld.loc["asimetria"]=skew(listaoriginal)
    lu.loc["asimetria"]=skew(lista_uniformes_aplanada)
    ld.loc["kurtosis"]=kurtosis(listaoriginal,bias=True)
    lu.loc["kurtosis"]=kurtosis(lista_uniformes_aplanada,bias=True)

    columns = {"datos crudos": ld,"sinteticos":lu,"agrupados":estadisticosAgrupados(data, df2)}

    comparados_todos=pd.DataFrame(columns)
    
    return comparados_todos
def histogramas(datos1, datos2,bins1,bins2):
    fig = plt.figure(figsize=(15,5))
    
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)

    ax1.hist(datos1,bins=bins1,histtype="bar",ec="black")
    ax1.set_title("Raw data")
    ax2.hist(datos2,bins=bins2,histtype="bar",ec="black")
    ax2.set_title("New data")
    plt.show()
    return fig 
def qqplot(data,uniformes):
    orig=pd.Series(data)
    u=pd.Series(uniformes)
    percentiles=np.arange(0.005,0.995,0.005)
    percentil_datos_crudos=[]
    percentil_datos_uniformes=[]
    for i in percentiles:
        percentil_datos_crudos.append(orig.quantile(q=i))
        percentil_datos_uniformes.append(u.quantile(q=i))
    plt.plot(percentil_datos_uniformes,percentil_datos_crudos)
    plt.xlabel("Datos sintéticos")
    plt.ylabel("Datos crudos ")
def mixtura():
    return pd.DataFrame(pd.concat([pd.Series(np.random.standard_normal(800)),pd.Series(np.random.exponential(1/4,200))]))
"""
a=crear_tabla_freq(data, 12)
uniformes=datos_sinteticos_uniformes(a,5000)
para_tabla_con_uniformes=leer_crudos(pd.Series(uniformes))
b=crear_tabla_freq(para_tabla_con_uniformes, 12)
estadisticosAgrupados(data,a)
comparacion=compare_all2(data, uniformes, a)
histogramas(data[0],uniformes,12,12)
qqplot(data[0],uniformes)
"""
def main():
    data = leer_crudos(pd.Series(leer_datos()))
    num_clases = int(input("Cuántas clases hay? "))
    a=crear_tabla_freq(data, num_clases)
    print(a)
    requeridos = int(input("Cuántos datos requieres? "))*10
    uniformes=datos_sinteticos_uniformes(a,requeridos)
    para_tabla_con_uniformes=leer_crudos(pd.Series(uniformes))
    b=crear_tabla_freq(para_tabla_con_uniformes, num_clases)
    estadisticosAgrupados(data,a) 
    comparacion=compare_all2(data, uniformes, a)
    print(comparacion)
    histogramas(data[0],uniformes,num_clases,num_clases)
    qqplot(data[0],uniformes)

main()

    

    
    

    

    
