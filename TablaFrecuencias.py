import pandas as pd
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt

# importar datos de csv
data= pd.read_csv('/Users/valeriacardona/Desktop/medifis.csv', delimiter=";")
data = data['peso']

def clases(classNumber):
    classList=[]
    interval=[]
    amplitud= math.ceil((max(data)- min(data))/classNumber)
    for i in range(min(data),max(data)+amplitud,amplitud):
        classList.append(i)
    #intervalos
    for i in range(len(classList)-1):
        if i==0:
            interval.append('['+str(classList[i])+','+str(classList[i+1])+']')
        else:
            interval.append('('+str(classList[i])+','+str(classList[i+1])+']')
    return (classList,interval)

def marcaClase(classList):
    marca=[]
    for i in range(len(classList)-1):
        marca.append((classList[i]+classList[i+1])/2)
    return marca

def count(classList, data):
    fa=[]
    i=1
    cont=0
    for el in data:
        if el<=classList[i]:
            cont+=1  
        else:
            i+=1
            fa.append(cont)
            cont=1
    fa.append(cont)
    return fa

def frelative(fa):
    fr=[]
    for el in fa:
        fr.append(round(el/len(data),3))    
    return fr
        
def fAcumAbs(fa):
    cont=0
    faa=[]
    for el in fa:
        cont+=el
        faa.append(cont)
    return faa
              
def fAcumRel(faa,l):
    far=[]
    for el in faa:
        far.append(round(el/l,3)  ) 
    return far

def FrequencyTable(data):
    data=sorted(data)
    freqT =  pd.DataFrame()
    classNumber = int(input("Número de clases en la tabla. Introduce 0 para que se haga por defecto: "))
    if classNumber==0:
        classNumber = round(1+ 3.32 * math.log(len(data)))
    classList=clases(classNumber)[0]
    interval=clases(classNumber)[1]
    marca=marcaClase(classList)
    fa=count(classList,data)
    fr=frelative(fa)
    faa=fAcumAbs(fa)
    far=fAcumRel(faa,len(data))
    elementos = {'Clases':interval, 'MarcaClases':marca, 'F Absoluta':fa, 
             'F Abs Relativa':fr,'F Acum Absoluta':faa, 
             'FAcum Relativa':far}
    freqT =  pd.DataFrame(elementos)
    print(freqT)
    return freqT
   
tabla=FrequencyTable(data)

def percentil(tabla, n ,percentil):
    p = percentil/100 * n
    for acum in range(len(tabla['F Acum Absoluta'])):
        if p >= tabla['F Acum Absoluta'][acum] and p< tabla['F Acum Absoluta'][acum+1]:
            j = p-tabla['F Acum Absoluta'][acum] 
            c=acum+1
    # k: longitud de la clase   
    k = int(tabla['Clases'][c][4:6])-int(tabla['Clases'][c][1:3])
    #j: cuanto me quedó faltando en la clase anterior? Por eso pase a la siguiente
    # n: frecuencia de esa clase
    nC= tabla['F Absoluta'][c]
    ans = int(tabla['Clases'][c][1:3]) + k*(j/nC)
    return ans
           
def estadisticosAgrupados(data, tabla):
    media= sum(tabla['MarcaClases'] * tabla['F Absoluta'])/len(data)
    varianza= sum((tabla['MarcaClases'] - media)**2 *tabla['F Absoluta'])/len(data)
    desviacion= math.sqrt(varianza)
    percentil25= percentil(tabla, len(data), 25)
    percentil50= percentil(tabla, len(data), 50)
    percentil75= percentil(tabla, len(data), 75)
    mini= int(tabla['Clases'][0][1:3])
    maxi=int(tabla['Clases'][len(tabla)-1][4:6])
    #moda = max(tabla['F Absoluta'])
    return [len(data), media, desviacion,mini , percentil25, percentil50, percentil75, maxi]
   
def DataSimulationNaive(tabla):
    cantSimu = int(input(' ¿Cuántos datos desea tener? : '))
    sinteticos =[]
    for indice in tabla.index:
        temp= int(round(tabla['F Abs Relativa'][indice] * cantSimu, 0))
        for i in range(temp):
            sinteticos.append(tabla['MarcaClases'][indice])
    return sinteticos

def DataSimulationUniform(tabla):
    cantSimu = int(input(' ¿Cuántos datos desea tener? : '))
    uniform = np.array([])
    for indice in tabla.index:
        temp= int(round(tabla['F Abs Relativa'][indice] * cantSimu,0))
        print('temp', temp)
        #uniform = np.append(uniform, int(tabla['Clases'][indice][1:3]) + (int(tabla['Clases'][indice][4:6])-int(tabla['Clases'][indice][1:3]))* np.random.random_sample(temp))
        uniform = np.append(uniform, np.random.uniform(int(tabla['Clases'][indice][1:3]), int(tabla['Clases'][indice][4:6]), temp))
        print (uniform)
        plt.plot(uniform)
        #b,a= 2,3
        #plt.plot((b - a) * np.random.random_sample(100) + a, np.arange(0,100,1))
        #plt.plot(np.random.uniform(2,3,100), np.arange(0,100,1))
    return uniform
  
def graphs(y1,y2):# FALTA HACER BIEN
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)     
    ax1.hist(y1, bins=5)
    ax1.set_title('Crudos')     
    ax2.hist(y2, bins= 5)
    ax2.set_title('Generados')
    plt.show()
    return fig

def comparationTable(crudos,tabla):
     crudos=data
     sinteticos = pd.Series(DataSimulationNaive(tabla))
     uniformes = pd.Series(DataSimulationUniform(tabla))
     comparacion= pd.DataFrame({'Datos crudos': data.describe() , 
                              'Datos Sinteticos': sinteticos.describe() ,
                              'Datos Sinteticos Uniformes': uniformes.describe(),
                              'Datos Agrupados': estadisticosAgrupados(crudos, tabla)})
     graphs(data,uniformes)
     percentiles = np.arange(0.005, 0.995, 0.005)
     percentil_crudos=[]
     percentil_uniformes=[]
     
     for p in percentiles:
         percentil_crudos.append(data.quantile(q=p))
         percentil_uniformes.append(uniformes.quantile(q=p))
         plt.plot(percentil_crudos, percentil_uniformes)
         plt.xlabel('Datos Crudos')
         plt.ylabel('Datos Sintéticos Uniformes')
     return comparacion
     
comparation = comparationTable(data, tabla)
compCrudosSinteticos = 


    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


