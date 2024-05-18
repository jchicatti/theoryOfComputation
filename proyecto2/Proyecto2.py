import re
import sys

'''
Introducción

Las expresiones regulares son secuencias de caracteres que forman un patrón de búsqueda.
Estas se utilizan para encontrar y manipular cadenas de texto de manera eficiente.
En este caso, usamos expresiones regulares para identificar y extraer tokens específicos
(como palabras clave, operadores, y delimitadores) de un archivo fuente predefinido. Esto
nos permite analizar y verificar la estructura sintáctica del código de manera precisa y
eficiente.

Este script analiza bloques de código que contienen estructuras de control 'while'
en un archivo de entrada. El script se encarga de leer el archivo, dividir el contenido
en tokens utilizando expresiones regulares, verificar la sintaxis de los bloques 'while'
y generar estadísticas sobre las variables, operadores y ciclos 'while' presentes en el
código. Se utilizó la librería "re" para simplificar el desarrollo del proyecto.
'''

# Función para leer el archivo de entrada y devolver su contenido como una cadena
def leer_archivo(nombre_archivo):
    '''
    Esta función abre un archivo con el nombre proporcionado y
    lee su contenido completo, devolviéndolo como una cadena de texto.
    Lo usamos para leer archivos cuyo resultado conocemos para hacer pruebas.
    '''
    with open(nombre_archivo, 'r') as archivo:
        return archivo.read()

# Función para dividir la entrada en tokens utilizando expresiones regulares
def dividir_tokens(entrada):
    '''
    Esta función utiliza una expresión regular para reconocer y
    dividir la entrada en tokens. Reconoce palabras clave, operadores,
    números y delimitadores. Luego, elimina los espacios en blanco
    innecesarios y devuelve la lista de tokens.
    '''
    # Expresión regular para reconocer tokens
    patron = re.compile(r'while|[a-z]|[0-9]|[<>=!]=|[<>=]|[{}();]|\s+')

    # Dividir la entrada en tokens
    tokens = patron.findall(entrada)

    # Eliminar espacios en blanco innecesarios
    tokens = [token.strip() for token in tokens if not token.isspace()]

    return tokens

# Función para verificar la sintaxis de los bloques 'while' y extraer variables
def parsear_whiles(tokens, variables):
    '''
    Esta función verifica la sintaxis de los bloques 'while' utilizando una pila.
    Luego, comprueba que cada 'while' tenga los paréntesis y llaves correspondientes.
    Finalmente, extrae y almacena las variables encontradas en el código para
    imprimirlas al final.
    '''
    stack = []
    for token in tokens:
        if token == "while":
            stack.append(token)
        elif token == "{":
            if stack[-1] == 'while':
                stack.append(token)
            else:
                return False
        elif token == "}":
            if stack[-1] == '{':
                stack.pop()  # Pop '{'
                stack.pop()  # Pop 'while'
            else:
                return False
        elif token == "(":
            if stack[-1] == 'while':
                stack.append(token)
            else:
                return False
        elif token == ")":
            if stack[-1] == '(':
                stack.pop()  # Pop '('
            else:
                return False
        elif token.isalpha() and len(token) == 1:
            variables.add(token)
        else:
            pass  # Es número

    return not stack

# Función para generar estadísticas sobre el código fuente
def generar_stats(source_code):
    '''
    Esta función cuenta la cantidad de operadores de comparación y ciclos 'while'
    en el código fuente utilizando expresiones regulares. Devuelve un diccionario
    con el total de operadores y ciclos 'while' encontrados.
    '''
    operators = len(re.findall(r'==|!=|<=|>=|<|>', source_code))
    whiles = len(re.findall(r'\bwhile\b', source_code))
    return {
        'total_operators': operators,
        'total_whiles': whiles
    }

# Función principal del script
def main():
    '''
    Esta es la función principal del script. Define el nombre del archivo de entrada,
    lee el archivo, divide el contenido en tokens y verifica la sintaxis. Si la sintaxis
    es correcta, genera y muestra las estadísticas sobre el código analizado.
    '''
    # nombre_archivo = "entrada.txt"
    # nombre_archivo = "incorrect_while_blocks.txt"
    nombre_archivo = "correct_while_blocks.txt"

    # Leer el archivo de entrada
    entrada = leer_archivo(nombre_archivo)
    print(entrada)

    # Dividir la entrada en tokens
    tokens = dividir_tokens(entrada)
    print(tokens)

    variables = set()

    # Verificar la sintaxis de los bloques 'while' y generar estadísticas si es correcto
    if parsear_whiles(tokens, variables):
        stats = generar_stats(entrada)
        print("Estadísticas de los bloques while analizados:")
        print(f"Total de variables únicas: {len(variables)}")
        print(f"Total de operadores de comparación: {stats['total_operators']}")
        print(f"Total de ciclos 'while': {stats['total_whiles']}")
    else:
        print("El bloque de código es sintácticamente incorrecto.")

# Punto de entrada del script
if __name__ == "__main__":
    main()

# Créditos: Josué Chicatti | Rodrigo Barrera | Armando Limón | Rogelio Torres
