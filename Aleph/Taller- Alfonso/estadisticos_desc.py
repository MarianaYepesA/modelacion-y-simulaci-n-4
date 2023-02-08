"""
Script con funciones para estadísticos descriptivos en Datos Crudos, Datos sintéticos y Estimaciones a partir de la tabla de frecuencias
"""
# Funciodes de estadísticos para Crudos = Sintéticos
import numpy as np
import pandas as pd
import math


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


def asimetria(data: list):
    n = len(data)  # longitud de datos
    s = desv_est(datos=data)  # confused
    m = media(datos=data)
    coeff = n/((n-1)*(n-2))
    estim_asm = 0
    for i in data:
        desv = i - m
        estim_asm += (desv/s)**3
    return coeff*estim_asm


def kurtosis(data: list, len: int):
    n = len
    m = media(datos=data)
    s = desv_est(datos=data)
    denom1 = (n-1)*(n-2)*(n-3)
    coeff = (n*(n+1))/denom1
    sum_par = 0
    for i in data:
        sum_par += (i-m)**4
    sum_par = sum_par/(s**4)
    denom2 = (n-2)*(n-3)
    diff = (3*((n-1)**2))/denom2
    kurt = (coeff*sum_par)-diff
    return kurt


def mediana(datos):
    dat = list(set(orden(datos)))
    while (len(dat) > 1):
        dat = dat[1:]
        dat.reverse()
    return dat[0]


def percentls(datos: list, quantil: float):
    percentil = np.percentile(datos, quantil)
    return percentil


def stats(data: list):
    length = len(data)
    mu = media(data)
    sd = desv_est(datos=data)
    asim = asimetria(data=data)
    kurt = kurtosis(data=data, len=length)
    minim = data[0]
    Q1 = percentls(datos=data, quantil=25)
    Q2 = percentls(datos=data, quantil=50)
    Q3 = percentls(datos=data, quantil=75)
    maxim = data[-1]
    est_dscrp = [mu, sd, asim, kurt, minim, Q1, Q2, Q3, maxim]
    print(est_dscrp)
    return est_dscrp

# Estadísticos Estimados


def est_media(class_marks: list, freq_rel: list):
    est_mean = 0
    for i in range(len(class_marks)):
        est_mean += class_marks[i]*freq_rel[i]
    return est_mean


def est_stdev(class_marks: list, freq_abs: list, mean: float, n: int):
    # lista de desviaciones a la media
    estm_sum = 0
    for i in range(len(class_marks)):
        estm_sum += (class_marks[i]**2)*freq_abs[i]
    estm_variance = (1/(n-1))*(estm_sum-n*(mean**2))
    return math.sqrt(estm_variance)


def est_asm(class_marks: list, freq_abs: list, mean: float, std: float, n: int):
    asm = 0
    for i in range(len(class_marks)):
        desv = freq_abs[i]*(class_marks[i]-mean)**3
        coeff = 1/(n*(std**3))
        asm += coeff*desv
    return asm


def est_kur(class_marks: list, freq_abs: list, mean: float, std: float, n: int):
    sum_est = 0
    for i in range(len(class_marks)):
        desv = freq_abs[i]*(class_marks[i]-mean)**4
        sum_est += desv*(1/n*(std**4))
    kurtosis = sum_est - 3
    return kurtosis


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


def est_stats(tabla_freq, marc_clases: dict):
    liminfs = list(marc_clases.keys())
    limsups = list(marc_clases.values())
    freq_abs = list(tabla_freq['Abs Freq'])
    freq_abs_c = list(tabla_freq['Cumulative A'])
    length = sum(freq_abs)
    freq_rel = list(tabla_freq['Rel Freq'])
    marcas = list(tabla_freq['Mark'])
    mu = est_media(marcas, freq_rel=freq_rel)
    sd = est_stdev(marcas, freq_abs=freq_abs, mean=mu, n=length)
    asim = est_asm(marcas, freq_abs=freq_abs, mean=mu, std=sd, n=length)
    kurt = est_kur(marcas, freq_abs=freq_abs, mean=mu, std=sd, n=length)
    minim = liminfs[0]
    Q1 = percentil(marc_clases, freq_abs_c, 25)
    Q2 = percentil(marc_clases, freq_abs_c, 50)
    Q3 = percentil(marc_clases, freq_abs_c, 75)
    maxim = limsups[-1]
    est_dscrp = [mu, sd, asim, kurt, minim, Q1, Q2, Q3, maxim]
    return est_dscrp

################################################################################


def stat_frame(crudos: list, sint: list, estims: list):
    column_labels = ['Mean', 'SD', 'asim',
                     'kurt', 'MIN', 'Q1', 'Q2', 'Q3', 'MAX']
    row_labels = ['Crudos', 'Sint', 'Estms']
    display = [crudos, sint, estims]
    stat_mat = pd.DataFrame(display, row_labels, column_labels)
    stat_mat = stat_mat.transpose()
    print(stat_mat)
    return stat_mat
