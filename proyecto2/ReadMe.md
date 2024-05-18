# Análisis de Bloques 'while' en Código Fuente de Java

## Descripción

Este repositorio contiene un programa que analiza bloques de código que contienen estructuras de control 'while' del lenguaje de programación Java en un archivo de entrada. Utiliza expresiones regulares para dividir el contenido en tokens, verifica la sintaxis de los bloques 'while' y genera estadísticas sobre variables, operadores y ciclos 'while'.

## Requisitos

- CMD/PowerShell
- Python 3.X

## Ejecución

1. Descargar los archivos necesarios.
    1.1 Asegúrese de tener 'Proyecto2.py' y un ejemplo de texto de entrada. Para propósitos de documentación y pruebas, proporcionamos los archivos 'incorrect_while_blocks.txt' y 'correct_while_blocks.txt'. No obstante, puede diseñar su propio archivo para realizar las pruebas.
2. Preparar los archivos de entrada.
    2.1 Asegúrese de tener el archivo de entrada dentro del mismo directorio que el script 'Proyecto2.py'.
3. Ejecutar el script desde la terminal:

```cmd
python Proyecto2.py
```

## Resultados

El programa imprimirá los resultados en la terminal de la siguiente manera:

* Total de variables únicas
* Total de operadores de comparación
* Total de ciclos while

## Ejemplo de bloques correctos.

```java
while (x < y) {
    while (4 == 2) {
        while (z > a) {
        }
        while (b == d) {
        }
    }
}
while (x <= z) {
}
while (a > b) {
 while (f != 5) {
 }
}
```

El resultado que se imprimirá en la terminal será:

```cmd
while (x < y) {
    while (4 == 2) {
        while (z > a) {
        }
        while (b == d) {
        }
    }
}
while (x <= z) {
}
while (a > b) {
 while (f != 5) {
 }
}

['while', '(', 'x', '<', 'y', ')', '{', 'while', '(', '4', '==', '2', ')', '{', 'while', '(', 'z', '>', 'a', ')', '{', '}', 'while', '(', 'b', '==', 'd', ')', '{', '}', '}', '}', 'while', '(', 'x', '<=', 'z', ')', '{', '}', 'while', '(', 'a', '>', 'b', ')', '{', 'while', '(', 'f', '!=', '5', ')', '{', '}', '}']
Estadísticas de los bloques while analizados:
Total de variables únicas: 7
Total de operadores de comparación: 7
Total de ciclos 'while': 7
```

## Ejemplo de bloques incorrectos.

```java
while (x < 1)
    while (4 = 2) {
        while (z > a)
            while (1 > 1) { }
}
```

El resultado que se imprimirá en la terminal será:

```cmd
while (x < 1)
    while (4 = 2) {
        while (z > a)
            while (1 > 1) { }
}

['while', '(', 'x', '<', '1', ')', 'while', '(', '4', '=', '2', ')', '{', 'while', '(', 'z', '>', 'a', ')', 'while', '(', '1', '>', '1', ')', '{', '}', '}']
El bloque de código es sintácticamente incorrecto.
```