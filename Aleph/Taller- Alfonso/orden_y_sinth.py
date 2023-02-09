"""
Visualización de Datos Crudos (Raw-Data) a través de su tabla de frecuencia
"""
import pandas as pd
import math
from estadisticos_desc import *
# Pandas como módulo de lectura para archivos csv


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
               'Cumulative A', 'Rel Freq', 'Cumulative R']
    frame = pd.DataFrame(display, headers)
    frame = frame.transpose()
    return frame
