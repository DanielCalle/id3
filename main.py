#!/usr/bin/env python3
import pandas as pd


class ID3:
    def run(self):
        keys = pd.read_csv('AtributosJuego.txt', sep=",", header=None)
        data = pd.read_csv('Juego.txt', sep=",", header=None)
        """
        filepath = "AtributosJuego.txt"
        with open(filepath) as fp:
            lines = fp.read().splitlines()
            keys = lines[0].split(",")

        filepath = "Juego.txt"
        with open(filepath) as fp:
            lines = fp.read().splitlines()
            for line in lines:
                data.append(line.split(","))
        """
        
        print(keys)
        print(data)


if __name__ == '__main__':
    ID3().run()
