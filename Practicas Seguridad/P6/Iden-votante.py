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


def firmado(texto,keyprivate,fichero):
    with open(texto, "rb") as mensaje_file:
        message =  mensaje_file.read()
    mensaje_file.close()
    
    with open(keyprivate, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )  
    
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        
    )
    
    with open(fichero, "wb") as cif_file:
        cif_file.write(signature)
    cif_file.close()
    return "Se ha firmado su texto. "

  

def identidades_votante(x, y, certf_v, keyprivate, certf_i):
    
    #Abro x
    with open(x, "rb") as x_file:
        x_d =  x_file.read()
    x_file.close()
    
    x_int = int.from_bytes(x_d,'big')
    #Hash del parámetro x recibido
    print(hash_f(x,"Hash_x_2.dat"))
    
    #Validación del Hash
    valid = verificacion("Hash_x_2.dat",y,certf_v)
    if valid:
        #Saco clave privada de identidades
        with open(keyprivate, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
        
        pi= private_key.private_numbers().p
        qi= private_key.private_numbers().q
        di= private_key.private_numbers().d
        ni = pi*qi
        b = pow(x_int,di,ni)
        b_b = b.to_bytes(sys.getsizeof(b),'big')
        #Guardo en fichero el valor de b
        with open("B.dat", "wb") as b_file:
            b_file.write(b_b)
        b_file.close()
        #print(firmado(x,keyprivate,"B.dat"))
        return True, "B.dat" 
    else:
        return False, None
    
    
def main():
    validacion, B = identidades_votante("x.dat","y.dat","Alicia.crt", "CA_Servidora_de_identidades.pem", "CA_Servidora_de_identidades.crt")
    print(validacion)
        
if __name__ == '__main__':
	main()       
    
