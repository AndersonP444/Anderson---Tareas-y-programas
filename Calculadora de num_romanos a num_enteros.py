def roman_to_int(str):
    result = 0
    for i in range(len(str)-1):
        if dicc[str[i]]<dicc[str[i+1]]:
            result -= dicc[str[i]]
        else:
            result += dicc[str[i]]
    return result + dicc[str[-1]]


dicc = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}
roman = input("Ingrese un número romano: ")
try:
    numero = roman_to_int(roman)
    print(numero)
except KeyError as e:
    print(f"Error: El carácter '{e.args[0]}' no es un número romano válido.")