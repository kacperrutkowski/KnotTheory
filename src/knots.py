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

def pd_not_from_dt_code(dt_code) -> list[list[int]]:
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

# knot class, redeimeister moves

class Knot:

    def __init__(self, pd_notation):
        self.__pd_notation = pd_notation
        self.__crossings = [Crossing() for _ in range(len(pd_notation))]
        self.__assign_arcs()

    def __assign_arcs(self):
        assigned = set()
        for i in range(len(self.__pd_notation)): # takes certain crossing
            for i_n in range(len(self.__pd_notation[i])): # takes a number from this crossing
                number1 = self.__pd_notation[i][i_n]
                if number1 not in assigned: # checks if the crossing is already assigned
                    for j in range(i, len(self.__pd_notation)): # visits all the other crossing
                        for j_n in range(len(self.__pd_notation[j])):
                            number2 = self.__pd_notation[j][j_n]
                            if number1 == number2: #checks if the crossing has common arc with the first crossing
                                arc = Arc(number1)
                                # first check what arc is it for the i-th crossing
                                if i_n % 2 == 0: # the arc belongs to lower stride of the i-th crossing
                                    if number1 == min(self.__pd_notation[i][0], self.__pd_notation[i][2]):
                                        # the arc is the back arc of the stride
                                        self.__crossings[i].lower_stride.back_arc = arc
                                    else: # the arc is the front arc of the stride
                                        self.__crossings[i].lower_stride.front_arc = arc
                                else: # the arc belongs to the upper stride of the i-th crossing
                                    if number1 == min(self.__pd_notation[i][1], self.__pd_notation[i][3]):
                                        # the arc is the back arc of the stride
                                        self.__crossings[i].upper_stride.back_arc = arc
                                    else: # the arc is the front arc of the stride
                                        self.__crossings[i].upper_stride.front_arc = arc

                                # now check what arc it is for the j-th crossing
                                if j_n % 2 == 0:  # the arc belongs to lower stride of the j-th crossing
                                    if number1 == min(self.__pd_notation[j][0], self.__pd_notation[j][2]):
                                        # the arc is the back arc of the stride
                                        self.__crossings[j].lower_stride.back_arc = arc
                                    else:  # the arc is the front arc of the stride
                                        self.__crossings[j].lower_stride.front_arc = arc
                                else: # the arc belongs to the upper stride of the j-th crossing
                                    if number1 == min(self.__pd_notation[j][1], self.__pd_notation[j][3]):
                                        # the arc is the back arc of the stride
                                        self.__crossings[j].upper_stride.back_arc = arc
                                    else: # the arc is the front arc of the stride
                                        self.__crossings[j].upper_stride.front_arc = arc
                    assigned.add(number1) # adds the crossing to assigned
                else: #move on if the arc is already assigned
                    continue


class Crossing:
    def __init__(self):
        self.lower_stride = Stride()
        self.upper_stride = Stride()
        self.crossing = None

class Stride:
    def __init__(self):
        self.front_arc = None
        self.back_arc = None
        self.crossing = None

class Arc:
    def __init__(self, number):
        self.number =  number


knot = Knot([[1,5,2,4],[3,1,4,6],[5,3,6,2]])
print(knot.crossings[0].lower_stride.front_arc.number)

