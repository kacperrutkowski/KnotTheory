import numpy as np
import pandas as pd
from pathlib import Path
import string

DATA_PATH = Path(__file__).resolve().parent.parent / "data"

df_homfly = pd.read_csv(DATA_PATH / "homfly.csv")
print(df_homfly['HOMFLY (vector)'][101])


def string_to_vector_parser(str_digit : str, sep ="; "):
    def parse(i):
        number = ""
        result = []
        if not (str_digit[0] == "[" and str_digit[-1] == "]"):
            raise ValueError("Invalid format. String does not have square brackets at the end or at the beginning")
        while i < len(str_digit): #przechodzimy przez cały napis
            char = str_digit[i]
            if char == "[":
                sublist, i = parse(i+1)
                result.append(sublist)
            elif char == "]":
                if number:
                    result.append(int(number))  # jeśli number nie jest pusty dodajemy do result
                return result, i
            elif char.isdigit():
                    number += char
            elif str_digit[i: i + len(sep)] == sep:
                if number: #sprawdzamy, czy number nie jest pusty
                    result.append(int(number)) #jeśli nie jest dodajemy do result
                    number = "" #szukamy kolejnego numeru
                i += len(sep) - 1
            elif char == "-":
                if number:
                    raise ValueError("Unexpected '-' in number")
                number += "-"
            else:
                raise ValueError(f"Symbol {char} is not allowed in the input string")
            i += 1
        return result, i

    parsed, i = parse(0)
    if i != len(str_digit):
        raise ValueError("Unbalanced brackets")
    return parsed[0] #usuwamy pierwszy zewnętrzny nawias

some_vector = "[12[3]]"
print(string_to_vector_parser(df_homfly['HOMFLY (vector)'][101]))


