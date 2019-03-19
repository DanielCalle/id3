#!/usr/bin/env python3
import pandas as pd


class ID3:
    def run(self):
        df_head = pd.read_csv('AtributosJuego.txt', sep=",", header=None)
        df_data = pd.read_csv('Juego.txt', sep=",", header=None)
        df = pd.concat([df_head, df_data])
        df.columns = df.iloc[0]
        df = df.drop(0)
        print(df["Jugar"].value_counts())



if __name__ == '__main__':
    ID3().run()
