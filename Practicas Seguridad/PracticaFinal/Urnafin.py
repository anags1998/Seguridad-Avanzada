#PRACTICA 6. ESCENARIO DE FIRMA CIEGA Y ENSAMBLAJE.

import json
import random
import sys  
import os 
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
from funciones import descifrado_aes,hash_f
  
def urna_fin(cifrado,RSA,IV_rsa,br,certf_v,certf_i,keyprivate,certf_u,archivo):
    #Abro fichero que contiene el valor de cifrado
    with open(cifrado, "rb") as cifrado_file:
        cifrado_b =  cifrado_file.read()
    cifrado_file.close()
    
    #Abro fichero que contiene el valor de RSA
    with open(RSA, "rb") as RSA_file:
        RSA_b = RSA_file.read()
    RSA_file.close()
    RSA_int = int.from_bytes(RSA_b,'big')
    
    #Abro fichero que contiene el valor de IV_rsa
    with open(IV_rsa, "rb") as IV_rsa_file:
        IV_rsa_b = IV_rsa_file.read()
    IV_rsa_file.close()
    IV_rsa_int = int.from_bytes(IV_rsa_b,'big')
    
    #Abro fichero que contiene el valor de br
    with open(br, "rb") as br_file:
        br_b = br_file.read()
    br_file.close()
    br_int = int.from_bytes(br_b,'big')
    
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
    
    #Abro clave privada urna
    with open(keyprivate, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        ) 
    pu= private_key.private_numbers().p
    qu= private_key.private_numbers().q
    du= private_key.private_numbers().d 
    
    #Descifro la clave con RSA
    key_int = pow(RSA_int,du,nu)
    key = key_int.to_bytes(16,'big')
    
    #Descifro IV con RSA
    iv_int = pow(IV_rsa_int,du,pu*qu)
    iv = iv_int.to_bytes(16,'big')
   
    #Obtengo el voto
    descifrado_aes(cifrado,key,iv)
    
    #Calculo el hash del voto 
    hash_f("descifrado.dat","Hash_voto_final.dat")
    
    #Abro fichero que contiene el hash del descifrado y paso a int
    with open("Hash_voto_final.dat", "rb") as hash_v_file:
        hash_v =  hash_v_file.read()
    hash_v_file.close()
    hash_v_int = int.from_bytes(hash_v,'big')
    
    #Obtengo B/R elevado a ei
    br_cif_int = pow(br_int,ei,ni)
    
    #Validación del Hash
    if hash_v_int == br_cif_int:
        valid = True
        #print("Comprobación del hash del descifrado realizada, ejecución continúa")
    else:
        #print("Comprobación del hash del descifrado realizada, ejecución parada")
        valid = False
        
    #Cálculo de la validación final
    if valid: 
        #Abro descifrado 
        with open("descifrado.dat", "rb") as des_file:
            des =  des_file.read()
        des_file.close()
        
        #Escribo en voto_final.dat y borro todos los demas .dat
        with open(archivo, "wb") as voto_file:
            voto_file.write(des)
        voto_file.close()
        os.remove("descifrado.dat")
        os.remove("cifrado.dat")
        os.remove("x.dat")
        os.remove("y.dat")
        os.remove("br.dat")
        os.remove("B.dat")
        os.remove("Hash_voto.dat")
        os.remove("Hash_voto_final.dat")
        os.remove("Hash_x.dat")
        os.remove("Hash_x_2.dat")
        os.remove("iv_rsa.dat")
        os.remove("k_rsa.dat")
        os.remove("r.dat")
        os.remove("voto.dat")
        os.remove("nombre.dat")
        os.remove("certf.dat")
        return True,"voto_final.dat"
    else:
        return False,None
          
    
