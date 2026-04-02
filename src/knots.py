import numpy as np
import pandas as pd
from pathlib import Path
import string

DATA_PATH = Path(__file__).resolve().parent.parent / "data"

df_homfly = pd.read_csv(DATA_PATH / "homfly.csv")
#print(df_homfly.columns)
print(df_homfly['HOMFLY (vector)'][100])


def vector_parser(str_digit:str):
    def parse(i):
        number = ""
        result = []
        while i < len(str_digit): #przechodzimy przez cały napis
            char = str_digit[i]
            if char == "[":
                sublist, i = parse(i+1)
                result.append(sublist)
            elif char == "]":
                if number:
                    result.append(int(number))  # jeśli nie jest dodajemy do result
                return result, i
            elif char in string.digits:
                if i > 0 and str_digit[i-1] == "-": #przypadek kiedy liczba ujemna
                    number += "-" + char
                else: #przypadek kiedy liczba dodatnia
                    number += char
            else: #napotkano inny znak
                if number: #sprawdzamy, czy number nie jest pusty
                    result.append(int(number)) #jeśli nie jest dodajemy do result
                    number = "" #szukamy kolejnego numeru
            i += 1
        return result, i

    parsed, _ = parse(0)
    return parsed[0]


print(vector_parser(df_homfly['HOMFLY (vector)'][100]))


