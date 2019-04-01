import math


class Node:
    def __init__(self):
        self.childs = []

    def add_child(self, node, edge):
        self.childs.append([edge, node])

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_childs(self):
        return self.childs


def mejor_merito(atributos, ejemplos):
    N = len(ejemplos)
    M = len(atributos) - 1
    meritos = [{} for i in range(M)]
    tp = 0
    tn = 0
    for ejemplo in ejemplos:
        p = 0
        n = 0

        if ejemplo[M] == "si":
            p = 1
            tp = tp + 1
        else:
            n = 1
            tn = tn + 1

        for i in range(M):
            if ejemplo[i] not in meritos[i].keys():
                meritos[i][ejemplo[i]] = [0, 0]

            meritos[i][ejemplo[i]][0] = meritos[i][ejemplo[i]][0] + p
            meritos[i][ejemplo[i]][1] = meritos[i][ejemplo[i]][1] + n

    resultado_meritos = [[atributo, 0, []] for atributo in atributos[:-1]]
    menor_merito = ["", 2, []]
    for i in range(M):
        for key, value in meritos[i].items():
            a = (value[0]+value[1])
            p = value[0]/a
            n = value[1]/a
            resultado_meritos[i][1] = resultado_meritos[i][1] + a/N * infor(p, n)
            resultado_meritos[i][2].append(key)

        if menor_merito[1] > resultado_meritos[i][1]:
            menor_merito[0] = resultado_meritos[i][0]
            menor_merito[1] = resultado_meritos[i][1]
            menor_merito[2] = resultado_meritos[i][2]

    menor_merito.append([tp, tn])
    return menor_merito


def infor(p, n):
    p1 = 0
    n1 = 0

    if p != 0:
        p1 = -p * math.log2(p)
    if n != 0:
        n1 = -n * math.log2(n)

    return p1 + n1


def split_data(atributos, ejemplos, merito):
    column = -1
    for i in range(len(atributos)-1):
        if atributos[i] == merito[0]:
            column = i

    rows = {respuesta: [] for respuesta in merito[2]}
    for ejemplo in ejemplos:
        rows[ejemplo[column]].append([x for i, x in enumerate(ejemplo) if i != column])

    return [[x for i, x in enumerate(atributos) if i != column], rows]


def id3(atributos, ejemplos, nodo=Node()):
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
    atributo = mejor_merito(atributos, ejemplos)
    nodo.set_name(atributo[0])
    # print(atributo)
    if len(atributos) == 1:
        return nodo
    elif atributo[1] == 0:
        if atributo[3][0] == 0:
            nodo.set_name("no")
        elif atributo[3][1] == 0:
            nodo.set_name("si")
        else:
            new_data = split_data(atributos, ejemplos, atributo)
            for edge, ejemplos2 in split_data(atributos, ejemplos, atributo)[1].items():
                child_node = Node()
                child_node.set_name(ejemplos2[0][len(ejemplos2[0])-1])
                nodo.add_child(child_node, edge)
        return nodo
    else:
        new_data = split_data(atributos, ejemplos, atributo)
        # print(new_data)
        atributos2 = new_data[0]
        for edge, ejemplos2 in split_data(atributos, ejemplos, atributo)[1].items():
            # print(ejemplos2)
            child_node = id3(atributos2, ejemplos2, Node())
            nodo.add_child(child_node, edge)
        
        return nodo


def print_node(nodo, text=""):
    if len(nodo.get_childs()) > 0:
        for child in nodo.get_childs():
            print_node(child[1], text + "(" + nodo.get_name() + " = " + child[0] + ") -> ")
    else:
        print("%s%s" % (text, nodo.get_name()))


def check(nodo, atributos, ejemplo):
    if len(nodo.get_childs()) == 0:
        return nodo.get_name() == ejemplo[len(ejemplo)-1]
    else:
        for i in range(len(atributos)):
            if nodo.get_name() == atributos[i]:
                for child in nodo.get_childs():
                    if child[0] == ejemplo[i]:
                        return check(child[1], atributos, ejemplo)

        return False


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
            if len(ejemplo) > 1:
                ejemplos.append(ejemplo)

    nodo = id3(atributos, ejemplos)
    print_node(nodo)
    cond = True
    while cond:
        ejemplo = input("Enter a new example to evaluate: ").split(",")
        if len(ejemplo) == len(atributos) and type(ejemplo) == list:
            print(check(nodo, atributos, ejemplo))
        else:
            cond = False
