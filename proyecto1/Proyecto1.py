"""
PROYECTO 1. Reconocimiento de declaraciones de Java.

Elaborado por:
- 191169 Josué Chicatti
- 181935 Rodrigo Barrera
- 188471 Armando Limón
- 182346 Rogelio Torres
"""

# Importación de la librería para expresiones regulares
import re

# Declaración de variables para almacenar resultados
num_variables = 0  # Contador para el número total de variables
tipos_utilizados = set()  # Conjunto para almacenar los tipos de variables utilizados
variables_por_tipo = {}  # Diccionario para contar el número de variables por tipo
num_variables_inicializadas = 0  # Contador para el número total de variables inicializadas
nombres_variables_por_tipo = {}  # Diccionario para almacenar los nombres de variables por tipo
num_variables_arreglo = 0  # Contador para el número total de variables de tipo arreglo
num_constantes = 0  # Contador para el número total de declaraciones de constantes

# Lista de tipos de datos válidos en Java.
tipos_validos = {"int", "float", "double", "boolean", "String"}

# tipo_regular = r'(val|var)\s+(\S+)\s*:\s*(\S+)\s*=\s*(.*)'

# Expresiones regulares para reconocer declaraciones de variables, incluyendo arreglos en ambos formatos

# Expresión regular para reconocer declaraciones de variables regulares y con inicialización:
# (\S+) captura el tipo de la variable, (\S+) captura el nombre de la variable,
# (?:;\s*|\s*=\s*(".*?"|\S+);) busca un punto y coma opcional seguido de cero o más espacios, o un signo igual seguido de cero o más espacios y una inicialización que puede ser una cadena entre comillas dobles o cualquier otro valor distinto de espacio.
tipo_regular = r'(\S+)\s+(\S+)(?:;\s*|\s*=\s*(".*?"|\S+);)'

# Expresión regular para reconocer declaraciones de variables de tipo arreglo:
# (\S+)\s*\[\s*\]\s*(\S+) captura el tipo y el nombre de la variable en el primer formato, o
# (\S+)\s+\[\s*\]\s*(\S+)\s*=\s*(new\s+\S+\[\d+\]|\{\s*(.*?(\s*,\s*.*?)*?)\s*\})\s*; captura el tipo y el nombre de la variable, así como el contenido del arreglo en el segundo formato.
tipo_arreglo = r'(\S+)\s*\[\s*\]\s*(\S+)|(\S+)\s+\[\s*\]\s*(\S+)\s*=\s*(new\s+\S+\[\d+\]|\{\s*(.*?(\s*,\s*.*?)*?)\s*\})\s*;'

# Expresión regular para reconocer declaraciones de constantes:
# (final\s*\S+)\s+(\S+)\s*=\s*(\S+); captura el modificador 'final', el tipo y el nombre de la constante, y su valor de inicialización.
tipo_constante = r'(final\s*\S+)\s+(\S+)\s*=\s*(\S+);'


# Método para leer el contenido de un archivo y devolverlo como una lista de líneas
def leerArchivo(filename):
    with open(filename, "r") as f:
        lista = f.read().splitlines()
    return lista

# Método principal para detectar y analizar las declaraciones en el código Java.
def detectar(declaraciones):
    # Variables globales para llevar la cuenta de diferentes tipos de declaraciones y estados.
    global num_variables, variables_por_tipo, tipos_utilizados
    global num_variables_inicializadas, num_variables_arreglo, num_constantes
    
    # Itera sobre cada declaración en la lista de declaraciones.
    for declaracion in declaraciones:
        # Intenta encontrar coincidencias con las expresiones regulares definidas para tipos de declaración.
        match_regular = re.match(tipo_regular, declaracion)
        match_arreglo = re.match(tipo_arreglo, declaracion)
        match_constante = re.match(tipo_constante, declaracion)
        
        # Determina si la declaración incluye inicialización (presencia de '=').
        esInicializada = '=' in declaracion

        # Procesa declaraciones regulares.
        if match_regular:
            # Extrae el tipo y el nombre de la variable de la coincidencia encontrada por la expresión regular.
            # match_regular.groups()[0] contiene el tipo de la variable.
            # match_regular.groups()[1] contiene el nombre de la variable.
            tipo, nombre_variable = match_regular.groups()[0], match_regular.groups()[1]
            # Llama a la función procesarDeclaracion con los detalles de la variable.
            # esInicializada indica si la declaración incluye una inicialización.
            procesarDeclaracion(tipo, nombre_variable, esInicializada)
            
        # Procesa declaraciones de arreglos.
        elif match_arreglo:
            # Verifica si el tipo del arreglo (antes de los corchetes) está en la lista de tipos válidos.
            if match_arreglo.groups()[0] in tipos_validos:
                # Extrae el tipo y el nombre del arreglo de la coincidencia encontrada.
                tipo, nombre_variable = match_arreglo.groups()[0], match_arreglo.groups()[1]
                # Procesa la declaración del arreglo, indicando que es un arreglo (esArreglo=True).
                procesarDeclaracion(tipo, nombre_variable, esInicializada, esArreglo=True)
            # Si la primera coincidencia no es válida, intenta con el segundo formato de declaración de arreglo.
            elif len(match_arreglo.groups()) > 3 and match_arreglo.groups()[3] in tipos_validos:
                # Este bloque maneja el caso donde los corchetes están separados del tipo por un espacio.
                tipo, nombre_variable = match_arreglo.groups()[3], match_arreglo.groups()[4]
                # Procesa la declaración como un arreglo.
                procesarDeclaracion(tipo, nombre_variable, esInicializada, esArreglo=True)
                
        # Procesa declaraciones de constantes.
        elif match_constante:
            # La expresión regular captura 'final tipo' como un solo grupo.
            # Se divide este grupo para separar la palabra clave 'final' del tipo real de la constante.
            partes = match_constante.group(1).split()
            # Verifica si el tipo de la constante está en la lista de tipos válidos.
            if len(partes) > 1 and partes[1] in tipos_validos:
                # Extrae el tipo y el nombre de la constante.
                tipo, nombre_variable = partes[1], match_constante.group(2)
                # Procesa la declaración como una constante (esConstante=True).
                procesarDeclaracion(tipo, nombre_variable, esInicializada, esConstante=True)


# Función para procesar y contabilizar cada declaración identificada según su tipo.
def procesarDeclaracion(tipo, nombre_variable, esInicializada, esArreglo=False, esConstante=False):
    # Actualiza las variables globales basadas en el tipo y estado de la declaración.
    global num_variables, variables_por_tipo, tipos_utilizados
    global num_variables_inicializadas, num_variables_arreglo, num_constantes
    
    # Verifica si el tipo está en la lista de tipos válidos antes de procesar.
    if tipo in tipos_validos:
        num_variables += 1  # Contador total de variables.
        tipos_utilizados.add(tipo)  # Conjunto de tipos únicos utilizados.
        variables_por_tipo[tipo] = variables_por_tipo.get(tipo, 0) + 1  # Contador de variables por tipo.
        nombres_variables_por_tipo.setdefault(tipo, []).append(nombre_variable)  # Nombres de variables por tipo.
        
        if esInicializada:
            num_variables_inicializadas += 1  # Contador de variables inicializadas.
        if esArreglo:
            num_variables_arreglo += 1  # Contador de arreglos.
        if esConstante:
            num_constantes += 1  # Contador de constantes.

#Script principal y prints
if __name__ == '__main__':
    #
    # ARCHIVO DE ENTRADA
    #
    fileName = "datos.txt"  # Nombre del archivo de entrada
    declaraciones = leerArchivo(fileName)  # Lectura de las declaraciones desde el archivo
    detectar(declaraciones)  # Llamada al método de detección y análisis de declaraciones
    # Impresión de resultados finales
    print(f"Numero total de variables declaradas: {num_variables}")
    print(f"Numero total de tipos utilizados en las declaraciones encontradas: {len(tipos_utilizados)}")
    print(f"Numero total de variables declaradas de cada tipo: {variables_por_tipo}")
    print(f"Numero total de variables inicializadas: {num_variables_inicializadas}")
    print(f"Numero total de variables de tipo arreglo: {num_variables_arreglo}")
    print(f"Numero total de declaraciones constantes: {num_constantes}")
    print("Clasificación de todos los nombres de variables por tipo declarado:")
    for tipo, nombres in nombres_variables_por_tipo.items():
        print(f"- {tipo}: {', '.join(nombres)}")