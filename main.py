#!/usr/bin/env python3
import pandas as pd


class ID3:
    def run(self):
        df_head = pd.read_csv('AtributosJuego.txt', sep=",", header=None)
        df_data = pd.read_csv('Juego.txt', sep=",", header=None)
        df = pd.concat([df_head, df_data])
        df.columns = df.iloc[0]
        df = df.drop(0)

        for column in df:
            merito = "mérito(" + column + ") = "
            for key, value in df[column].value_counts().items():
                merito = merito + str(value) + "/" + str(len(df)) + " + "
                merito = merito + "infor("
                salidas = (df.loc[df[column] == key])["Jugar"]
                for c in salidas.value_counts():
                    merito = merito + str(c) + "/" + str(len(salidas)) + ","
                merito = merito[:-1]
                merito = merito + ")" + " + "

            merito = merito[:-3]
            print(merito)



if __name__ == '__main__':
    ID3().run()
