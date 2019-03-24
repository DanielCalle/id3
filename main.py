#!/usr/bin/env python3
import pandas as pd
import math


class ID3:
    def run(self):
        """
        df_head = pd.read_csv('AtributosJuego.txt', sep=",", header=None)
        df_data = pd.read_csv('Juego.txt', sep=",", header=None)
        df = pd.concat([df_head, df_data])
        df.columns = df.iloc[0]
        df = df.drop(0)
        """
        filepath = "AtributosJuego.txt"
        column_names = ""
        with open(filepath) as fp:
            lines = fp.read().splitlines()
            column_names = lines[0].split(",")

        df = pd.read_csv('Juego.txt', sep=",", header=None, names=column_names)

        for column in df:
            if column != "Jugar":
                valor_merito = 0
                merito = "mérito(" + column + ") = "
                for key, value in df[column].value_counts().items():
                    merito = merito + str(value) + "/" + str(len(df)) + " * "
                    salidas = (df.loc[df[column] == key])
                    p = len(salidas.loc[df["Jugar"] == "si"])
                    n = len(salidas.loc[df["Jugar"] == "no"])
                    merito = merito + "infor(" + str(p) + "/" + str(p+n) + "," + str(n)  + "/" + str(p+n) + ") + "
                    valor_merito = valor_merito + value/len(df) * infor(p/(p+n), n/(p+n))
                merito = merito[:-3] + " = " + str(valor_merito)
                print(merito)


def infor(p, n):
    p1 = 0
    n1 = 0
    if p != 0:
        p1 = -p * math.log2(p)
    if n != 0:
        n1 = -n * math.log2(n)
    
    return p1 + n1


if __name__ == '__main__':
    ID3().run()
