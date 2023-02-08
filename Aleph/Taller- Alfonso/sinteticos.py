import pandas as pd
import numpy as np
import math
from tabla_freq import *
"""
Construcción de Datos Sintéticos
Alfonso Fierro
"""
# Dada la tabla de freq devolver los puntos sintéticos


def synthetic(classes, frq_relat, puntos):
    # con las frecuencias relativas se tendría que dar la cantidad de datos nuevos para cada clase haciendo freq_rel*puntos.
    targets = [math.ceil(i*puntos) for i in frq_relat]
    # print(targets)
    liminfs = list(classes.keys())
    # print(liminfs)
    limsups = list(classes.values())
    # print(limsups)
    lif = 0
    lup = 0
    synth_data = []
    for i in targets:
        for j in range(i):
            if i != 0:
                synth = np.random.uniform(liminfs[lif], limsups[lup])
                synth_data.append(synth)
            else:
                break
        lif += 1
        lup += 1
    return synth_data


def est_media(class_marks, freq_rel):
    est_mean = 0
    for i in range(len(class_marks)):
        est_mean += class_marks[i]*freq_rel
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
