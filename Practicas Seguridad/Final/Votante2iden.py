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


def votante_identidades(texto, certf_v, keyprivate, certf_i):
    #Calculo el hash del voto 
    hash_f(texto,"Hash_voto.dat")
        
    #Abro certificado identidades
    with open(certf_i, "rb") as certf_i_file:
        ctr_i =  certf_i_file.read()
    certf_i_file.close()
        
    #Saco clave pública del identidades
    cert_i = x509.load_pem_x509_certificate(ctr_i)
    keypublic_i = cert_i.public_key()
    
    ei= keypublic_i.public_numbers().e
    ni= keypublic_i.public_numbers().n
    
    #Saco clave privada del votante
    with open(keyprivate, "rb") as key_file:
        private_key_v = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )  
    
    dv= private_key_v.private_numbers().d
    pv= private_key_v.private_numbers().p
    qv= private_key_v.private_numbers().q
    
    #Genero valor de r aleatorio y guardo en fichero
    r = random.randint(2,ni-1)
    r_b = r.to_bytes(sys.getsizeof(r),'big')
    with open("r.dat", "wb") as r_file:
        r_file.write(r_b)
    r_file.close()
    
    #Abro fichero que contiene el hash del voto y paso a int
    with open("Hash_voto.dat", "rb") as hash_v_file:
        hash_v =  hash_v_file.read()
    hash_v_file.close()
    hash_v_int = int.from_bytes(hash_v,'big')
   
    #Obtengo el valor de x
    r_c_int = pow(r,ei,ni)
    x = pow(hash_v_int*r_c_int,1,ni)
    x_b = x.to_bytes(sys.getsizeof(x),'big')
    
    #Guardo en fichero el valor de x
    with open("x.dat", "wb") as x_file:
        x_file.write(x_b)
    x_file.close()
    #print("Parámetro x preparado para enviar a Autoridad de identidades")        
    
    #Hash del parámetro x enviado
    hash_f("x.dat","Hash_x.dat")
    
    #Abro fichero que contiene el hash del x y paso a int
    with open("Hash_x.dat", "rb") as hash_x_file:
        hash_x =  hash_x_file.read()
    hash_x_file.close()
    hash_x_int = int.from_bytes(hash_x,'big')
    
    #Firmo x con la clave privada del votante
    y = pow(hash_x_int,dv,pv*qv)
    y_b = y.to_bytes(sys.getsizeof(y),'big')
    
    #Guardo en fichero el valor de y
    with open("y.dat", "wb") as y_file:
        y_file.write(y_b)
    y_file.close()
    #print("Parámetro y preparado para enviar a Autoridad de identidades")        
    
    return "x.dat", "y.dat"
       
    
