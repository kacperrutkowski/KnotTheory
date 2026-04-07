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

def reverse_vector(knot_vector : list, vector_type : str = "jones"):
    """
    Creates a mirror image of a knot.

    :param knot_vector: A list representing knot's vector
    :param vector_type: A type of vector corresponding to a polynomial. Three values are possible: jones, homfly, kauffman.
    :return: A list representing reversed vector
    """
    if vector_type == "jones":
        return [- knot_vector[1], -knot_vector[0]] + knot_vector[len(knot_vector)-1:1:-1]
    elif vector_type == "homfly" or vector_type == "kauffman":
        return knot_vector[0:2] + [reverse_vector(knot, vector_type= "jones") for knot in knot_vector[2:]]
    else:
        return None

def is_symmetrical(knot_vector : list, vector_type : str = "jones"):
    """
    Checks if the mirror image of the knot is identical with the original knot.
    :param knot_vector: A list representing knot's vector
    :param vector_type: A type of vector corresponding to a polynomial. Three values are possible: jones, homfly, kauffman.
    :return: Boolean value
    """
    return reverse_vector(knot_vector, vector_type) == knot_vector
