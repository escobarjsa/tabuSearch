import numpy as np
import matplotlib.pyplot as plt
import time

matriz = [
    [1, 3, 3, 2, 2, 1],
    [2, 3, 4, 6, 4, 3],
    [2, 1, 3, 3, 2, 2],
    [2, 4, 3, 5, 4, 2],
    [1, 3, 2, 1, 3, 2],
    [2, 2, 1, 2, 1, 2],
    [3, 1, 1, 3, 1, 2]
]

np.random.seed(114514)  # valores aleateoreos con valores semillas
iterations = 5000
tablaTabu = []
bestValues = []


def rutaInicial(_ruta_len):
    _ruta = list(range(_ruta_len))
    np.random.shuffle(_ruta)
    return _ruta


def calcularCosto(_ruta, _d):
    i = _ruta.copy()
    _dis = _d[i[0]][i[len(_ruta) - 1]]
    for j in range(len(_ruta) - 1):
        _dis += _d[i[j]][i[j + 1]]
    return _dis


def costoMatrizInicial():
    _d = np.zeros([len(matriz), len(matriz)])
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            _d[i][j] = np.sqrt(pow(matriz[i][0] - matriz[j][0], 2) + pow(matriz[i][1] - matriz[j][1], 2))
    return _d


# generar vecino, y de acuerdo a ese vecino obtenemos mejor valor
# El vecino alimenta la tabla
def obtenerVecino(_tabla_tabu, _tabu_len, _ruta):
    _vecino = []
    _len = len(_ruta)

    for i in range(_tabu_len):
        temp = _ruta.copy()
        m1 = np.random.randint(0, _len - 2)
        m2 = np.random.randint(m1 + 1, _len - 1)
        temp[m1:m2 + 1] = reversed(temp[m1:m2 + 1])
        if temp not in _tabla_tabu:
            _vecino.append(temp)
    while not _vecino:
        temp = _ruta.copy()
        m1 = np.random.randint(0, _len - 2)
        m2 = np.random.randint(m1 + 1, _len - 1)
        temp[m1:m2 + 1] = reversed(temp[m1:m2 + 1])
        if temp not in _tabla_tabu:
            _vecino.append(temp)
    return _vecino


# Calcular costos, para obtener el mejor resultado
def buscarMejorValor(_vecino, _d):
    d_min = calcularCosto(_vecino[0], _d)
    _bestValue = _vecino[0]
    for i in _vecino:
        if calcularCosto(i, _d) < d_min:
            d_min = calcularCosto(i, _d)
            _bestValue = i
    return d_min, _bestValue


def actualizarTabu(_tabla_tabu, _tabu_len, _ruta):
    _tabla_tabu.append(_ruta)
    if len(_tabla_tabu) > _tabu_len:
        del _tabla_tabu[0]


# Grafica
def plotValues(_best_values):
    X = []
    Y = []
    for i in range(len(_best_values)):
        X.append(i)
        t = _best_values[i][0]
        Y.append(t)
    plt.plot(X, Y)
    plt.show()


def busquedaTabu():
    ruta = rutaInicial(len(matriz))
    _d = costoMatrizInicial()
    t = time.time()
    tabu_len = len(matriz)
    for i in range(iterations):
        vecino = obtenerVecino(tablaTabu, tabu_len, ruta)
        bestValue = buscarMejorValor(vecino, _d)
        bestValues.append(bestValue)
        ruta = bestValue[1]
        # print("Iteración", i, "Mejor valor", bestValue[0])
        actualizarTabu(tablaTabu, tabu_len, ruta)

    t = time.time() - t
    plotValues(bestValues)
    mejorValor = max(bestValues)  #maximizar el valor de la función
    #mejorValor = min(bestValues)
    print("Mejor valor", mejorValor[0], "Tiempo", t, "Iteraciones", iterations)
    # return bestValues, min(bestValues), t


busquedaTabu()


