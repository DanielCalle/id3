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


def best_merit(attributes, examples):
    N = len(examples)
    M = len(attributes) - 1
    merit = [{} for i in range(M)]
    tp = 0
    tn = 0
    for example in examples:
        p = 0
        n = 0

        if example[M] == "si":
            p = 1
            tp = tp + 1
        else:
            n = 1
            tn = tn + 1

        for i in range(M):
            if example[i] not in merit[i].keys():
                merit[i][example[i]] = [0, 0]

            merit[i][example[i]][0] = merit[i][example[i]][0] + p
            merit[i][example[i]][1] = merit[i][example[i]][1] + n

    merit_result = [[attribute, 0, []] for attribute in attributes[:-1]]
    lower_merit = ["", 2, []]
    for i in range(M):
        for key, value in merit[i].items():
            a = (value[0]+value[1])
            p = value[0]/a
            n = value[1]/a
            merit_result[i][1] = merit_result[i][1] + a/N * infor(p, n)
            merit_result[i][2].append(key)

        if lower_merit[1] > merit_result[i][1]:
            lower_merit[0] = merit_result[i][0]
            lower_merit[1] = merit_result[i][1]
            lower_merit[2] = merit_result[i][2]

    lower_merit.append([tp, tn])
    return lower_merit


def infor(p, n):
    p1 = 0
    n1 = 0

    if p != 0:
        p1 = -p * math.log2(p)
    if n != 0:
        n1 = -n * math.log2(n)

    return p1 + n1


def split_data(attributes, examples, merito):
    column = -1
    for i in range(len(attributes)-1):
        if attributes[i] == merito[0]:
            column = i

    rows = {respuesta: [] for respuesta in merito[2]}
    for example in examples:
        rows[example[column]].append([x for i, x in enumerate(example) if i != column])

    return [[x for i, x in enumerate(attributes) if i != column], rows]


def id3(attributes, examples, node=Node()):
    """
        si atributos.vacio o % > umbral entonces
            cerrar arbol
        si no
            atributo = mejor_merito(atributos, ejemplos)
            por cada valor en atributo.valores hacer
                atributos2 = atributos.quitar(atributo)
                ejemplos2 = ejemplos.quitar(atributo, !valor)
                node.hijo = id3(atributos2, ejemplos2)
    """
    attribute = best_merit(attributes, examples)
    node.set_name(attribute[0])
    # print(attribute)
    if len(attributes) == 1:
        return None
    elif attribute[1] == 0:
        if attribute[3][0] == 0:
            node.set_name("no")
        elif attribute[3][1] == 0:
            node.set_name("si")
        else:
            new_data = split_data(attributes, examples, attribute)
            for edge, examples2 in split_data(attributes, examples, attribute)[1].items():
                child_node = Node()
                child_node.set_name(examples2[0][len(examples2[0])-1])
                node.add_child(child_node, edge)
        return node
    else:
        new_data = split_data(attributes, examples, attribute)
        attributes2 = new_data[0]
        for edge, examples2 in split_data(attributes, examples, attribute)[1].items():
            child_node = id3(attributes2, examples2, Node())
            node.add_child(child_node, edge)
        
        return node


def print_node(node, text=""):
    if len(node.get_childs()) > 0:
        for child in node.get_childs():
            print_node(child[1], text + "(" + node.get_name() + " = " + child[0] + ") -> ")
    else:
        print("%s%s" % (text, node.get_name()))


def check(node, attributes, example):
    if len(node.get_childs()) == 0:
        return node.get_name()
    else:
        for i in range(len(attributes)):
            if node.get_name() == attributes[i]:
                for child in node.get_childs():
                    if child[0] == example[i]:
                        return check(child[1], attributes, example)

        return "No hay reglas para este example"


if __name__ == '__main__':
    filepath = "AtributosJuego.txt"
    attributes = ""
    with open(filepath) as fp:
        lines = fp.read().splitlines()
        attributes = lines[0].split(",")

    filepath = "Juego.txt"
    examples = []
    with open(filepath) as fp:
        lines = fp.read().splitlines()
        for line in lines:
            example = line.split(",")
            if len(example) > 1:
                examples.append(example)

    node = id3(attributes, examples)
    if node is None:
        print("Incorrect format")
    else:
        print_node(node)
        cond = True
        while cond:
            example = input("Enter a new example to evaluate: ").split(",")
            if len(example) == (len(attributes)-1) and type(example) == list:
                print(check(node, attributes, example))
            else:
                cond = False
