#!/usr/bin/env python3
class ID3:
    def run(self):
        filepath = "AtributosJuego.txt"
        with open(filepath) as fp:
            lines = fp.read().splitlines()
            keys = lines[0].split(",")
            print(keys)
        
        


if __name__ == '__main__':
    ID3().run()
