import numpy as np
import pandas as pd
from pathlib import Path
import string

DATA_PATH = Path(__file__).resolve().parent.parent / "data"

df_homfly = pd.read_csv(DATA_PATH / "homfly.csv")

print(df_homfly['HOMFLY (vector)'])

def string_to_vector(string_vector : str):
    result = []
    i = 0
    while i < len(string_vector):
        if string_vector[i] == "[":
            result.append(string_vector[i + 1:])
            i += 1
        if string_vector[i] in string.digits:
            result.append(int(string_vector[i]))
            i += 1
        if string_vector[i] == "-":
            result.append(string_vector[i:i+2])
            i += 2
        if string_vector[i] in [";"," "]:
            i += 1
        if string_vector[i] == "]":
            return result
        else:
            print(f"{string_vector[i]} is an invalid symbol")


vector = string_to_vector("[1; 2; 3; [3; -4]; 5]")