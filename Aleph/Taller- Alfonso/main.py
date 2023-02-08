import random
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
    num_class = num_marca(marc_clases)
    print('Cuatos datos sintéticos necesita generar?:', end=' ')
    num_sint_dat = int(input())
    print('\n')
    print('---------------------------------------------------------------------------------------------------------------')
    print('Datos Muestrales')
    tabla_muestra = tabla_frecuencia(column, nu_marcs)
    frecu_relat_M = tabla_muestra['Rel Freq']
    print('-----------------------------------------------------------------------------------------------')

    print('DATOS SINTÉTICOS')
    column_sint = synthetic(marc_clases, frecu_relat_M, num_sint_dat)
    tabla_sint = tabla_frecuencia(column_sint, nu_marcs)

    print('-----------------------------------------------------------------------------------------------')
    stat_crudos = stats(column)
    stat_sinth = stats(column_sint)
    stat_stims = est_stats(tabla_muestra, marc_clases=marc_clases)
    tabla_estats = stat_frame(stat_crudos, stat_sinth, stat_stims)
    print(tabla_estats)


    # print(column)
    # print(datos)
main()


def test_kurtosis():
    # Test 1: using a sample data set
    data = [random.randint(1, 100) for i in range(20)]
    len_data = len(data)
    expected_kurtosis = -1.2
    k = kurtosis(data, len_data)
    assert abs(
        k - expected_kurtosis) < 0.6, f"Expected kurtosis of {expected_kurtosis}, but got {k}"

    # Test 2: using a larger sample data set
    data = [random.randint(1, 1000) for i in range(100)]
    len_data = len(data)
    expected_kurtosis = -1.2
    k = kurtosis(data, len_data)
    assert abs(
        k - expected_kurtosis) < 0.6, f"Expected kurtosis of {expected_kurtosis}, but got {k}"

    # Test 3: using a smaller sample data set
    data = [random.randint(1, 10000) for i in range(10)]
    len_data = len(data)
    expected_kurtosis = -1.2
    k = kurtosis(data, len_data)
    assert abs(
        k - expected_kurtosis) < 0.6, f"Expected kurtosis of {expected_kurtosis}, but got {k}"

    print("All tests passed!")


# eenvireen5_test_kurtosis()
