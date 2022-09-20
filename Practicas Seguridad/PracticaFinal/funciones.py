#Funciones realizadas en prácticas anteriores y utilizadas en el ensamblaje
import json
import random
import sys   
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from base64 import b64decode
from Crypto.Hash import SHA256
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography import exceptions

def hash_f(texto,fichero):
    #Abro fichero que contiene el texto
    with open(texto, "rb") as mensaje_file:
        mensaje =  mensaje_file.read()
    mensaje_file.close()
    
    #Realizo el hash de dicho texto
    hash_o = SHA256.new(mensaje)
    hash_t = hash_o.digest()
    
    #Guardo el hash del texto en un fichero
    with open(fichero, "wb") as hash_file:
        hash_file.write(hash_t)
    hash_file.close()
    return "Hash de su texto realizado. "
    

def cifrado_aes(texto,key,iv):
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
    return "Se ha encriptado su voto en la siguiente ruta: cifrado.dat"

def descifrado_aes(cifrado,key,iv):
    cifrado_f = open(cifrado,'r')
    data = cifrado_f.read()
    cifrado_f.close()
    
    cipher = AES.new(key, AES.MODE_CBC,iv)
    mensaje = b64decode(data)
    pt = unpad(cipher.decrypt(mensaje), AES.block_size)
       
    descifrado = open("descifrado.dat",'w+')
    descifrado.write(pt.decode('utf-8'))
    descifrado.close()
    return "Se ha desencriptado su voto en la siguiente ruta: descifrado.dat"
  