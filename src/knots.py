import regina
import snappy
# polynomial functions

def string_to_vector_parser(str_digit : str, sep ="; "): #do dopracowania, nie uwzględnia niektórych edge caseów
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

#loading knots with regina or snappy, pd notation, counting bigons

def load_knot_from_regina(sig) -> regina.Link:
    """
    Laads knot using native Regina knot signature.
    :param sig: a string which is a native Regina knot signature
    :return: regina.Link
    """
    L = regina.Link.fromKnotSig(sig)

    return L

def load_knot_from_dt_code(dt_code) -> snappy.Link:
    letters = "abcdefghijklmnopqrs"
    n_cross = len(dt_code)
    snappy_code = "DT:" + letters[n_cross - 1] + "a" + letters[n_cross - 1] + dt_code
    L = snappy.Link(snappy_code)
    return L

def pd_not_from_dt_code(dt_code):
    L = load_knot_from_dt_code(dt_code)
    pd_not = L.PD_code()
    return pd_not

def count_bigons_from_pd(pd_not : list[tuple[int]]) -> int:
    pd_sets = []
    for crossing in pd_not:
        pd_sets.append(set(crossing))

    num_bigon = 0

    for i in range(len(pd_sets)):
        for j in range(i + 1, len(pd_sets)):
            inters = pd_sets[i].intersection(pd_sets[j])
            if len(inters) == 2:
                num_bigon += 1

    return num_bigon

def check_if_bigons(pd_not : list[tuple[int]]) -> int:
    pd_sets = []
    for crossing in pd_not:
        pd_sets.append(set(crossing))

    for i in range(len(pd_sets)):
        for j in range(i + 1, len(pd_sets)):
            inters = pd_sets[i].intersection(pd_sets[j])
            if len(inters) == 2:
                return True

    return False