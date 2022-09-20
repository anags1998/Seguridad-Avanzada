#PRACTICA 6. ESCENARIO DE FIRMA CIEGA Y ENSAMBLAJE.
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
from funciones import hash_f

def identidades_votante(x, y, certf_v, keyprivate, certf_i):
    #Abro x
    with open(x, "rb") as x_file:
        x_d =  x_file.read()
    x_file.close()
    
    x_int = int.from_bytes(x_d,'big')
    
    #Abro y
    with open(y, "rb") as y_file:
        y_d =  y_file.read()
    y_file.close()
    
    y_int = int.from_bytes(y_d,'big')
    
    #Hash del parámetro x recibido
    hash_f(x,"Hash_x_2.dat")
    with open("Hash_x_2.dat", "rb") as hash_x_file:
        hash_x =  hash_x_file.read()
    hash_x_file.close()
    
    hash_x_int = int.from_bytes(hash_x,'big')
    
    #Abro certificado identidades
    with open(certf_v, "rb") as certf_v_file:
        ctr_v =  certf_v_file.read()
    certf_v_file.close()
        
    #Saco clave pública del identidades
    cert_v = x509.load_pem_x509_certificate(ctr_v)
    keypublic_v = cert_v.public_key()
    
    ev= keypublic_v.public_numbers().e
    nv= keypublic_v.public_numbers().n
    
    #Validación del Hash
    if hash_x_int == pow(y_int,ev,nv):
        valid = True
        #print("Comprobación del hash de x realizada, ejecución continúa")
    else:
        valid = False
        #print("Comprobación del hash de x realizada, ejecución parada")
        
    #Obtención del parámetro B
    if valid:
        with open(keyprivate, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        ) 
        pi= private_key.private_numbers().p
        qi= private_key.private_numbers().q
        di= private_key.private_numbers().d  
        b = pow(x_int,di,pi*qi)
        
        b_b = b.to_bytes(sys.getsizeof(b),'big')
        with open("B.dat", "wb") as b_file:
            b_file.write(b_b)
        b_file.close()
        return True, "B.dat" 
    else:
        return False, None
           
    
