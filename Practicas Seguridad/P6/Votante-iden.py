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

def cifrado_rsa(texto,certf,fichero):
    
    with open(texto, "rb") as mensaje_file:
        clavesesion =  mensaje_file.read()
    mensaje_file.close()
    
    with open(certf, "rb") as certf_file:
        ctr =  certf_file.read()
    certf_file.close()
        
    #saco clave pública
    cert = x509.load_pem_x509_certificate(ctr)
    keypublic = cert.public_key()
    
    e= keypublic.public_numbers().e
    n= keypublic.public_numbers().n
        
    ciphertext = keypublic.encrypt(
        clavesesion,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(fichero, "wb") as cif_file:
        cif_file.write(ciphertext)
    cif_file.close()
    return "Se ha encriptado su texto. "


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

  

def votante_identidades(texto, certf_v, keyprivate, certf_i):
        
    #Calculo el hash del voto 
    print(hash_f(texto,"Hash_voto.dat"))
        
    #Abro certificado identidades
    with open(certf_i, "rb") as certf_i_file:
        ctr_i =  certf_i_file.read()
    certf_i_file.close()
        
    #Saco clave pública del identidades
    cert_i = x509.load_pem_x509_certificate(ctr_i)
    keypublic_i = cert_i.public_key()
    
    #Genero valor de r aleatorio y guardo en fichero
    r = random.randint(2,1000000000000000000000000000)
    print("R:"+str(r))
    r_b = r.to_bytes(sys.getsizeof(r),'big')
    with open("r.dat", "wb") as r_file:
        r_file.write(r_b)
    r_file.close()
    
    #Encripto con clave pública de autoridad de identidades el valor aleatorio r
    print(cifrado_rsa("r.dat",certf_i,"r_cifrado.dat"))
    
    #Abro fichero que contiene el valor encriptado de r
    with open("r_cifrado.dat", "rb") as rc_file:
        r_c = rc_file.read()
    rc_file.close()
    
    #Convierto el valor encriptado de r de bytes a int
    r_c_int = int.from_bytes(r_c,'big')
    
    #Abro fichero que contiene el hash del voto
    with open("Hash_voto.dat", "rb") as hash_v_file:
        hash_v =  hash_v_file.read()
    hash_v_file.close()
    
    #Convierto el valor del hash del voto de bytes a int
    hash_v_int = int.from_bytes(hash_v,'big')
    print("Hash(v):"+str(hash_v_int))
    #Obtengo uno de los parámetros para mandar a autoridad de identidades
    x = (r_c_int*hash_v_int)
    x_b = x.to_bytes(sys.getsizeof(x),'big')
    
    #Guardo en fichero el valor de x
    with open("x.dat", "wb") as x_file:
        x_file.write(x_b)
    x_file.close()
         
    #Hash del parámetro x enviado
    print(hash_f("x.dat","Hash_x.dat"))
    
    #Firmo x con la clave privada del votante
    print(firmado("Hash_x.dat",keyprivate,"y.dat"))
            
    return "x.dat", "y.dat"
    
    
def main():
    x,y = votante_identidades("voto.dat", "Alicia.crt", "Alicia.pem", "CA_Servidora_de_identidades.crt")
    
        
if __name__ == '__main__':
    main()       
    
