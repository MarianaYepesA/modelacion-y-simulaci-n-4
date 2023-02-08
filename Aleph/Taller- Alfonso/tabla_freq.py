"""
Visualización de Datos Crudos (Raw-Data) a través de su tabla de frecuencia
"""
import pandas as pd
import math
from sinteticos import *
# Pandas como módulo de lectura para archivos csv


def orden(datos):
    return sorted(datos)


def media(datos):
    return sum(datos)/len(datos)


def desv_est(datos):
    suma_desvs = 0
    coeff = 1/(len(datos)-1)
    x_bar = media(datos)
    for i in datos:
        suma_desvs += (i-x_bar)**2
    return math.sqrt(coeff*suma_desvs)


def asimetria(datos):
    n = len(datos)  # longitud de datos
    s = desv_est(datos=datos)  # confused
    m = media(datos=datos)
    coeff = n/((n-1)*(n-2))
    estim_asm = 0
    for i in datos:
        desv = i - m
        estim_asm += (desv/s)**3
    return coeff*estim_asm


def kurtosis(datos):
    n = len(datos)
    m = media(datos=datos)
    s = desv_est(datos=datos)
    coeff = (n*(n+1))/((n-1)*(n-1)*(n-3))
    sum_par = 0
    for i in datos:
        sum_par += ((i-m)/s)**4
    diff = (3*((n-1)**2))/((n-2)(n-3))
    kurt = (coeff*sum_par)-diff
    return kurt


def mediana(datos):
    dat = list(set(orden(datos)))
    while (len(dat) > 1):
        dat = dat[1:]
        dat.reverse()
    return dat[0]


def marcas_de_clase(datos, cortes):
    banda_datos = (datos[-1]-datos[0])/cortes
    bounds = {}
    cut = datos[0]
    count = 1
    while (count <= cortes):
        bounds[cut] = cut + banda_datos
        cut = cut + banda_datos
        count += 1
    return bounds


def num_marca(intervalos):
    liminf = list(intervalos.keys())
    limsup = list(intervalos.values())
    strt = ((limsup[0]+liminf[0])/2)
    step = limsup[0] - liminf[0]
    num_marca = []
    for i in range(len(liminf)):
        mid = strt + step*i
        num_marca.append(mid)
    return num_marca


def freqAbs(datos, marcas):
    llaves = list(marcas.keys())
    values = list(marcas.values())
    recuento = []
    for i in range(len(llaves)-1):
        count = 0  # cuenta de la freq absoluta
        for j in datos:  # traverse datos
            if j <= values[i]:  # ignora el tope del intervalo [...]
                count += 1
            else:
                datos = datos[count:]
                # como los datos están ordenados se puede cortar la lista para evitar redundancias
                break
        recuento.append(count)
    recuento.append(len(datos))
    return recuento


def freqAbsAcum(freqAbs):
    freq_acums = []
    sum = 0
    for i in freqAbs:
        sum += i
        freq_acums.append(sum)

    return freq_acums


def freqRelAcum(freqAbs):
    total = sum(freqAbs)
    rel_accum = []
    partSum = 0

    for i in freqAbs:
        partSum += i
        rel_accum.append(partSum/total)

    return rel_accum


def freqRel(freqAbs):
    total = sum(freqAbs)
    frqRels = []

    for i in freqAbs:
        frqRels.append(i/total)

    return frqRels


def marcas_to_str(marcas_de_clase):
    int_str = ''
    liminf = list(marcas_de_clase.keys())
    limsup = list(marcas_de_clase.values())
    list_marks = []
    for i in range(len(limsup)):
        if i != (0):
            int_str = '('+str(liminf[i])+','+str(limsup[i])+']'
            list_marks.append(int_str)
            int_str = ''
        else:
            int_str = '['+str(liminf[i])+','+str(limsup[i])+']'
            list_marks.append(int_str)
            int_str = ''
    return (list_marks)


def percentil(marcas_clase: dict, abs_freq_c: list, percentil: float):
    data_len = abs_freq_c[-1]
    nth_value = (percentil/100)*data_len
    limsups = list(marcas_clase.values())
    liminfs = list(marcas_clase.keys())
    ind_loc = 0
    for cumul in abs_freq_c:
        if cumul < nth_value:
            ind_loc += 1
        else:
            break
    if ind_loc != 0:
        step = limsups[ind_loc]-liminfs[ind_loc]
        dif_c = abs_freq_c[ind_loc]-abs_freq_c[ind_loc-1]
        coef = nth_value-abs_freq_c[ind_loc-1]
        estimate = liminfs[ind_loc]+(step/dif_c)*coef
        return estimate
    else:
        step = limsups[ind_loc]-liminfs[ind_loc]
        estimate = liminfs[ind_loc]+(step/abs_freq_c[ind_loc])*nth_value
        return estimate


def tabla_frecuencia(datos_in, cortes_in):
    datos_in = orden(datos=datos_in)
    marcas = marcas_de_clase(datos_in, cortes_in)
    marcas_str = marcas_to_str(marcas)
    nums_marcas = num_marca(marcas)
    frec_abs = freqAbs(datos_in, marcas=marcas)
    frec_relt = freqRel(frec_abs)
    frec_abs_acu = freqAbsAcum(frec_abs)
    frec_rel_acu = freqRelAcum(frec_abs)
    display = [marcas_str, nums_marcas, frec_abs,
               frec_abs_acu, frec_relt, frec_rel_acu]
    headers = ['Class', 'Mark', 'Abs Freq',
               'CumulativeA', 'Rel Freq', 'CumulativeR']
    frame = pd.DataFrame(display, headers)
    frame = frame.transpose()
    print(frame)
    return frame
