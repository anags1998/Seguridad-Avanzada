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
from funciones import hash_f,cifrado_aes

def votante_urna(b, certf_v, keyprivate, certf_i,certf_u):
    #Abro fichero que contiene el valor de b
    with open(b, "rb") as b_file:
        b_b =  b_file.read()
    b_file.close()
    b_int = int.from_bytes(b_b,'big')
    
    #Abro fichero que contiene el valor de r
    with open("r.dat", "rb") as r_file:
        r = r_file.read()
    r_file.close()
    r_int = int.from_bytes(r,'big')
    
    #Abro certificado identidades
    with open(certf_i, "rb") as certf_i_file:
        ctr_i =  certf_i_file.read()
    certf_i_file.close()
        
    #Saco clave pública del identidades
    cert_i = x509.load_pem_x509_certificate(ctr_i)
    keypublic_i = cert_i.public_key()
    
    #Obtengo números públicos del certificado
    ni= keypublic_i.public_numbers().n
    ei= keypublic_i.public_numbers().e
    
    #Abro certificado votante
    with open(certf_v, "rb") as certf_v_file:
        ctr_v =  certf_v_file.read()
    certf_v_file.close()
        
    #Saco clave pública del votante
    cert_v = x509.load_pem_x509_certificate(ctr_v)
    keypublic_v= cert_v.public_key()
    
    #Obtengo números públicos del votante
    nv= keypublic_v.public_numbers().n
    ev= keypublic_v.public_numbers().e
    
    #Abro certificado urna
    with open(certf_u, "rb") as certf_u_file:
        ctr_u =  certf_u_file.read()
    certf_u_file.close()
        
    #Saco clave pública de la urna
    cert_u = x509.load_pem_x509_certificate(ctr_u)
    keypublic_u = cert_u.public_key()
    
    #Obtengo números públicos de la urna
    nu= keypublic_u.public_numbers().n
    eu= keypublic_u.public_numbers().e
    
    #Abro fichero que contiene el hash del voto y paso a int
    with open("Hash_voto.dat", "rb") as hash_v_file:
        hash_v =  hash_v_file.read()
    hash_v_file.close()
    hash_v_int = int.from_bytes(hash_v,'big')
    
    #Calculo B/r y escribo en fichero en bytes
    B_div = b_int*pow(r_int,-1,ni) 
    Br_int = pow(B_div,ei,ni)
    Br_b = B_div.to_bytes(sys.getsizeof(B_div),'big')
    with open("br.dat", "wb") as br_file:
        br_file.write(Br_b)
    br_file.close()
    
    #Validación del Hash
    if hash_v_int == Br_int:
        valid = True
        #print("Comprobación del parámetro B/r realizada, ejecución continúa")
    else:
        valid = False
        #print("Comprobación del parámetro B/r realizada, ejecución parada")
    
    #Cálculo de los parámetros a enviar a la Urna
    if valid: 
        key = get_random_bytes(16)
        key_int = int.from_bytes(key,'big')
        
        iv = get_random_bytes(16)
        iv_int = int.from_bytes(iv,'big')
        
        cifrado_aes("voto.dat",key,iv)
        k_rsa = pow(key_int,eu,nu)
        k_rsa_b = k_rsa.to_bytes(sys.getsizeof(k_rsa),'big')
        
        with open("k_rsa.dat", "wb") as k_rsa_file:
            k_rsa_file.write(k_rsa_b)
        k_rsa_file.close()
        iv_rsa = pow(iv_int,eu,nu)
        iv_rsa_b = iv_rsa.to_bytes(sys.getsizeof(iv_rsa),'big')
        with open("iv_rsa.dat", "wb") as iv_rsa_file:
            iv_rsa_file.write(iv_rsa_b)
        iv_rsa_file.close()
        return True,"cifrado.dat","k_rsa.dat","iv_rsa.dat","br.dat"
    else:
        return False,None,None,None,None
          
    
