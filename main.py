import math


def id3(atributos, ejemplos):
    """
        si atributos.vacio o % > umbral entonces
            cerrar arbol
        si no
            atributo = mejor_merito(atributos, ejemplos)
            por cada valor en atributo.valores hacer
                atributos2 = atributos.quitar(atributo)
                ejemplos2 = ejemplos.quitar(atributo, !valor)
                nodo.hijo = id3(atributos2, ejemplos2)
    """
    print(mejor_merito(atributos, ejemplos))


def mejor_merito(atributos, ejemplos):
    N = len(ejemplos)
    M = len(atributos) - 1
    meritos = [{} for i in range(M)]
    for ejemplo in ejemplos:
        p = 0
        n = 0

        if ejemplo[M] == "si":
            p = 1
        else:
            n = 1

        for i in range(M):
            if ejemplo[i] not in meritos[i].keys():
                meritos[i][ejemplo[i]] = [0, 0]

            meritos[i][ejemplo[i]][0] = meritos[i][ejemplo[i]][0] + p
            meritos[i][ejemplo[i]][1] = meritos[i][ejemplo[i]][1] + n

    resultado_meritos = [[atributo, 0] for atributo in atributos[:-1]]
    mejor_merito = ["", 0]
    for i in range(M):
        for key, value in meritos[i].items():
            a = (value[0]+value[1])
            p = value[0]/a
            n = value[1]/a
            resultado_meritos[i][1] = resultado_meritos[i][1] + a/N * infor(p, n)

        if mejor_merito[1] < resultado_meritos[i][1]:
            mejor_merito[0] = resultado_meritos[i][0]
            mejor_merito[1] = resultado_meritos[i][1]

    return mejor_merito


def infor(p, n):
    p1 = 0
    n1 = 0

    if p != 0:
        p1 = -p * math.log2(p)
    if n != 0:
        n1 = -n * math.log2(n)

    return p1 + n1


if __name__ == '__main__':
    filepath = "AtributosJuego.txt"
    atributos = ""
    with open(filepath) as fp:
        lines = fp.read().splitlines()
        atributos = lines[0].split(",")

    filepath = "Juego.txt"
    ejemplos = []
    with open(filepath) as fp:
        lines = fp.read().splitlines()
        for line in lines:
            ejemplo = line.split(",")
            if(len(ejemplo) > 1):
                ejemplos.append(ejemplo)

    id3(atributos, ejemplos)
