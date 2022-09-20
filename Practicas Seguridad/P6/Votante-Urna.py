#PRACTICA 6. ESCENARIO DE FIRMA CIEGA Y ENSAMBLAJE.
import json
import random
import sys   
from decimal import Decimal
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
    
def verificacion(texto,firma,certf):
    with open(texto, "rb") as mensaje_file:
        message =  mensaje_file.read()
    mensaje_file.close()
    
    with open(firma, "rb") as firma_file:
        signature =  firma_file.read()
    firma_file.close()
    
    with open(certf, "rb") as certf_file:
        ctr =  certf_file.read()
    certf_file.close()
        
    #saco clave pública
    cert = x509.load_pem_x509_certificate(ctr)
    keypublic = cert.public_key()
    
    try:
        keypublic.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        ) 
        return True
    except exceptions.InvalidSignature:
        return False

def votante_urna(b, r, certf_v, keyprivate, certf_i):
    #Abro fichero que contiene el valor de b
    with open(b, "rb") as b_file:
        b_b =  b_file.read()
    b_file.close()
    
    #Abro fichero que contiene el valor de r
    with open(r, "rb") as r_file:
        r_b = r_file.read()
    r_file.close()  
    
    #Abro certificado identidades
    with open(certf_i, "rb") as certf_i_file:
        ctr_i =  certf_i_file.read()
    certf_i_file.close()
        
    #Saco clave pública del identidades
    cert_i = x509.load_pem_x509_certificate(ctr_i)
    keypublic_i = cert_i.public_key()
    
    ei= keypublic_i.public_numbers().e
    ni= keypublic_i.public_numbers().n
           
    #Paso de bytes a int ambos valores
    b_int = int.from_bytes(b_b,'big')
    r_int = int.from_bytes(r_b,'big')
    
    
    print("B:" + str(pow(b_int//r_int,ei,ni)))
    print(b_int//r_int)
    print("Br:" + str(hash_v_int))    
    # b_r = br_firm.to_bytes(sys.getsizeof(br_firm),'big')
    
        
    #Validación del parámetro B/r
    valid = verificacion("Hash_voto.dat","B.dat",certf_i)
    
    if valid: 
        return True
    else:
        return False
    
def main():
    validacion = votante_urna("B.dat","r.dat","Alicia.crt", "CA_Servidora_de_identidades.pem", "CA_Servidora_de_identidades.crt")
    print(validacion)
        
if __name__ == '__main__':
	main()       
    
