from functools import reduce
from math import gcd

def frecuencia(texto, long_palabra):
    lista_palabras = []

    for i in range(len(texto)):
        if len(texto[i:i+long_palabra]) == long_palabra:
            palabra = texto[i:i+long_palabra]
            dic = buscar(palabra, i, texto, long_palabra)
            if not dic.get('repeticion') == 0:
                if len(lista_palabras) == 0:
                    lista_palabras.append(dic)
                else:
                    dic_repetido = 0
                    for dic_temp in lista_palabras:
                        if dic_temp.get('palabra') == palabra:
                            dic_repetido += 1
                    if dic_repetido == 0:
                        lista_palabras.append(dic)

    return lista_palabras


def calcular_llave_criptografica(lista_palabras):
    distancias = []
    for i in lista_palabras:
        for j in i.get('distancias'):
            distancias.append(j)
    llave = reduce(gcd, tuple(distancias))

    return llave


def buscar(palabra, distancia, texto, longitud_palabra):
    dic = {'palabra': palabra, 'repeticion': 0, 'distancias': []}
    for i in range(len(texto)):
        #if palabra == texto[i:i+longitud_palabra] and not i - distancia == 0 and i > distancia:
        if palabra == texto[i:i+longitud_palabra] and not i - distancia == 0:
            dic['repeticion'] += 1
            dic['distancias'].append(i - distancia)
            distancia = i
    return dic


def subcriptogramas(texto, long_clave):
    # Almacenamiento de los subcriptogramas con la longitud de la clave
    dic = {}
    for i in range(long_clave):
        dic[i] = ''

    i = 0
    for letra in texto:
        dic[i] += letra
        i += 1
        if i == long_clave:
            i = 0
    return dic


def num_letras_repetidas(subcriptograma):
    dic = {}
    for letra in subcriptograma:
        dic[letra] = subcriptograma.count(letra)
    return dic


def letra_mas_repetida(dic_letras):
    mayores = {}
    for i in range(len(dic_letras)):
        letra = max(dic_letras, key=dic_letras.get)
        # Numero de veces que se repite una letra en el criptograma
        if dic_letras.get(letra) > 5:
            mayores[letra] = dic_letras.pop(letra)
    return mayores


alfabeto = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8,
    'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'Ñ': 14, 'O': 15, 'P': 16,
    'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
    'Y': 25, 'Z': 26
}

# alfabeto = {
#     'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8,
#     'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
#     'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
#     'Y': 24, 'Z': 25
# }


def descifrar_clave(letra_1, letra_2):
    # print('letras ------', letra_1,':', letra_2)
    letra_mas_repetida_1 = 'A'
    letra_mas_repetida_2 = 'E'
    for posicion in range(2):
        valor_clave_1 = (alfabeto.get(letra_1) - alfabeto.get(letra_mas_repetida_1)) % len(alfabeto)
        valor_clave_2 = (alfabeto.get(letra_2) - alfabeto.get(letra_mas_repetida_2)) % len(alfabeto)
        if valor_clave_1 == valor_clave_2:
            for letra_alfabeto, valor_alfabeto in alfabeto.items():
                if valor_alfabeto == valor_clave_1:
                    # print('valor -----------', valor_alfabeto, ':', letra_alfabeto)
                    return letra_alfabeto
        else:
            letra_mas_repetida_1 = 'E'
            letra_mas_repetida_2 = 'A'


def descifrar_letra(letra, clave):
    # Aplica la formula para obtener el texto en claro
    valor_descifrado = (alfabeto.get(letra) - alfabeto.get(clave)) % len(alfabeto)
    for letra_alfabeto, valor_alfabeto in alfabeto.items():
        if valor_alfabeto == valor_descifrado:
            return letra_alfabeto


def metodo_kasiski(ruta_archivo):
    texto_completo = leer_archivo(ruta_archivo)
    texto = texto_completo[:215]

    longitud_palabra = 3
    lista_palabras = frecuencia(texto, longitud_palabra)
    # print('lista', lista_palabras)
    longitud_clave = calcular_llave_criptografica(lista_palabras)
    print('longitud clave', longitud_clave)
    print()

    criptograma = subcriptogramas(texto, longitud_clave)

    lista_subcriptogramas = []
    for subcriptograma in criptograma.values():
        lista_subcriptogramas.append(num_letras_repetidas(subcriptograma))
        print('subs:', subcriptograma)

    letras_mas_repetidas = []
    for letras in lista_subcriptogramas:
        # print('lista sub:', letras)
        letras_mas_repetidas.append(letra_mas_repetida(letras))
    print()
    print('letra mas repetida', letras_mas_repetidas)
    print()

    clave_criptografica = []
    for letras in letras_mas_repetidas:
        l = letras.keys()
        for letra_1 in l:
            for letra_2 in l:
                clave_criptografica.append(descifrar_clave(letra_1, letra_2))
            else:
                break

    clave_cadena = ''
    for letra in clave_criptografica:
        if letra:
            clave_cadena += letra
    print('Clave criptografica:', clave_cadena)


    texto_clave = clave_cadena * len(texto_completo)

    texto_clave = texto_clave[:len(texto_completo)]

    for letra in clave_criptografica:
        texto_descifrado = []
        for i in range(len(texto_completo)):
            texto_descifrado.append(descifrar_letra(texto_completo[i], texto_clave[i]))
        # print()
        # print(texto_descifrado)
        # print()

        mensaje_claro = ''
        for letra in texto_descifrado:
            mensaje_claro += letra

    print("Archivo generado")
    texto_descifrado = "texto_claro.txt.dec"
    archivo = open(texto_descifrado,'w+')
    archivo.write(mensaje_claro)


if __name__ == '__main__':
    plain = "includes/cifrado.txt"
    archivo = open(plain,'r')
    texto_completo = archivo.read()
    texto = texto_completo[:215]

    longitud_palabra = 3
    lista_palabras = frecuencia(texto, longitud_palabra)
    # print('lista', lista_palabras)
    longitud_clave = calcular_llave_criptografica(lista_palabras)
    print('longitud clave', longitud_clave)
    print()

    criptograma = subcriptogramas(texto, longitud_clave)

    lista_subcriptogramas = []
    for subcriptograma in criptograma.values():
        lista_subcriptogramas.append(num_letras_repetidas(subcriptograma))
        print('subs:', subcriptograma)

    letras_mas_repetidas = []
    for letras in lista_subcriptogramas:
        # print('lista sub:', letras)
        letras_mas_repetidas.append(letra_mas_repetida(letras))
    print()
    print('letra mas repetida', letras_mas_repetidas)
    print()

    clave_criptografica = []
    for letras in letras_mas_repetidas:
        l = letras.keys()
        for letra_1 in l:
            for letra_2 in l:
                clave_criptografica.append(descifrar_clave(letra_1, letra_2))
            else:
                break

    clave_cadena = ''
    for letra in clave_criptografica:
        if letra:
            clave_cadena += letra
    print('Clave criptografica:', clave_cadena)


    texto_clave = clave_cadena * len(texto_completo)

    texto_clave = texto_clave[:len(texto_completo)]

    for letra in clave_criptografica:
        texto_descifrado = []
        for i in range(len(texto_completo)):
            texto_descifrado.append(descifrar_letra(texto_completo[i], texto_clave[i]))
        # print()
        # print(texto_descifrado)
        # print()

        mensaje_claro = ''
        for letra in texto_descifrado:
            mensaje_claro += letra

    print("Archivo generado")
    texto_descifrado = "includes/texto_claro.txt.dec"
    archivo = open(texto_descifrado,'w+')
    archivo.write(mensaje_claro)
