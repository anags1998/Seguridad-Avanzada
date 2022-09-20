#PRACTICA 2: CIFRADO AES Y HASH

import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from base64 import b64decode
from Crypto.Hash import SHA256


def cifrado(texto,key,iv):
    mensaje_fich = open(texto,'r')
    data = mensaje_fich.read()
    mensaje_fich.close()
    
    
    cipher = AES.new(key, AES.MODE_CBC,iv)
    mensaje = bytes(data,'utf-8')
    ct_bytes = cipher.encrypt(pad(mensaje, AES.block_size))
    ct = b64encode(ct_bytes).decode('utf-8')
    
    
    cifrado = open("cifrado.dat",'w+')
    cifrado.write(ct)
    cifrado.close()
    return "Se ha encriptado su texto en la siguiente ruta: cifrado.dat"


def descifrado(cifrado,key,iv):
    
    cifrado_f = open(cifrado,'r')
    data = cifrado_f.read()
    cifrado_f.close()
        
    cipher = AES.new(key, AES.MODE_CBC,iv)
    mensaje = b64decode(data)
    pt = unpad(cipher.decrypt(mensaje), AES.block_size)
    
    
    descifrado = open("descifrado.dat",'w+')
    descifrado.write(pt.decode('utf-8'))
    descifrado.close()
    return "Se ha desencriptado su texto en la siguiente ruta: descifrado.dat"

def hash_f(texto):
    mensaje_fich = open(texto,'r')
    data = mensaje_fich.read()
    mensaje_fich.close()
    
    mensaje = bytes(data,'utf-8')
    hash_o = SHA256.new(mensaje)
    hash_t = hash_o.digest()
    
    resumen = open("resumen.dat",'w+')
    hash_e = b64encode(hash_t).decode('utf-8')
    resumen.write(hash_e)
    resumen.close()
    return "Hash de su texto en la siguiente ruta: resumen.dat"

    
    
    
    
    
def main():

    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    print(cifrado("voto.dat",key,iv))
    print(descifrado("cifrado.dat",key,iv))
    print(hash_f("voto.dat"))
    
        
if __name__ == '__main__':
	main()