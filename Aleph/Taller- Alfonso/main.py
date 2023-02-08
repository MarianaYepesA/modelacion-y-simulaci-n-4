from orden_y_sinth import *
from estadisticos_desc import *
import pandas as pd


def main():
    print('Indique el nombre del archivo:', end=" ")
    archivo = str(input())
    print('Indique el nombre de la variable a analizar:', end=" ")
    var = str(input())
    data = pd.read_csv(archivo)
    column = data[var]
    column = orden(column)
    # print(column)
    print('Cuantas marcas de clase se necesesitan?:', end=" ")
    nu_marcs = int(input())
    marc_clases = marcas_de_clase(column, nu_marcs)
    print('Cuatos datos sintéticos necesita generar?:', end=' ')
    num_sint_dat = int(input())
    print('\n')
    print('---------------------------------------------------------------------------------------------------------------')
    print('Datos Muestrales')
    tabla_muestra = tabla_frecuencia(column, nu_marcs)
    frecu_relat_M = tabla_muestra['Rel Freq']
    cum_frecu_a = list(tabla_muestra['CumulativeA'])
    print('-----------------------------------------------------------------------------------------------')
    print('Estadísticos Muestrales')

    print('Media: '+str(media(column)))
    print('Desv Est: '+str(desv_est(column)))
    print('Media: '+str(media(column)))
    print('Mediana: ' + str(mediana(column)))
    print('Q1 '+str(percentil(marc_clases, cum_frecu_a, 25)))
    print('-----------------------------------------------------------------------------------------------')

    print('DATOS SINTÉTICOS')
    column_sint = synthetic(marc_clases, frecu_relat_M, num_sint_dat)
    tabla_sint = tabla_frecuencia(column_sint, nu_marcs)

    print('-----------------------------------------------------------------------------------------------')
    print('Estadísticos de Datos Sintéticos')

    print('Media: '+str(media(column_sint)))
    print('Desv Est: '+str(desv_est(column_sint)))
    print('Media: '+str(media(column_sint)))
    print('Mediana: ' + str(mediana(column_sint)))

    # print(column)
    # print(datos)
main()
