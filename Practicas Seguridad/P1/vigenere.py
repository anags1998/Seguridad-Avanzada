import random
#PRACTICA 1: CIFRADO VIGENERE
abc = 'abcdefghijklmnñopqrstuvwxyz'

def cifrar(plain, key):
    archivo = open(plain,'r')
    cadena = archivo.read()
    archivo2 = open(key,'r')
    clave = archivo2.read()
    cadena_cifrar = ''
    i = 0
    for letra in cadena:
         if letra.isupper() :
            if (letra == ' ') or (letra == '.') or (letra == ',') :
                cadena_cifrar = cadena_cifrar + letra
            else :
                suma = abc.find(letra.lower()) + abc.find(clave[i % len(clave)])
                modulo = int(suma) % len(abc)
                cadena_cifrar = cadena_cifrar + (str(abc[modulo])).upper()
                i+=1
         else :
            if (letra == ' ') or (letra == '.') or (letra == ',') :
                cadena_cifrar = cadena_cifrar + letra
            else :
                suma = abc.find(letra) + abc.find(clave[i % len(clave)])
                modulo = int(suma) % len(abc)
                cadena_cifrar = cadena_cifrar + str(abc[modulo])
                i+=1
    texto_cifrado = "cifrado.txt"
    archivo = open(texto_cifrado,'w+')
    archivo.write(cadena_cifrar)
    return "Se ha encriptado su texto en la siguiente ruta: cifrado.txt"

def descifrar(plain, key):
    archivo = open(plain,'r')
    cadena = archivo.read()
    archivo2 = open(key,'r')
    clave = archivo2.read()
    cadena_cifrar = ''
    i = 0
    for letra in cadena:
         if letra.isupper() :
            if (letra == ' ') or (letra == '.') or (letra == ',') :
                cadena_cifrar = cadena_cifrar + letra
            else :
                suma = abc.find(letra.lower()) - abc.find(clave[i % len(clave)])
                modulo = int(suma) % len(abc)
                cadena_cifrar = cadena_cifrar + (str(abc[modulo])).upper()
                i+=1
         else :
            if (letra == ' ') or (letra == '.') or (letra == ',') :
                cadena_cifrar = cadena_cifrar + letra
            else :
                suma = abc.find(letra) - abc.find(clave[i % len(clave)])
                modulo = int(suma) % len(abc)
                cadena_cifrar = cadena_cifrar + str(abc[modulo])
                i+=1
    texto_descifrado = "descifrado.txt"
    archivo = open(texto_descifrado,'w+')
    archivo.write(cadena_cifrar)
    return "Se ha encriptado su texto en la siguiente ruta: descifrado.txt"

def clave():
    cadena_clave= ''
    for i in range(0, random.randint(0,30)):
        j = random.randint(0,26)
        indice = str(abc[j])
        cadena_clave = cadena_clave + indice
    texto_clave= "clave.txt"
    archivo = open(texto_clave,'w+')
    archivo.write(cadena_clave)
    archivo.close()
    return "Se ha generado la clave en la siguiente ruta: clave.txt"

def main():
    print(clave())
    print(cifrar("plain.txt","clave.txt"))
    print(descifrar("cifrado.txt","clave.txt"))
       
	
if __name__ == '__main__':
	main()