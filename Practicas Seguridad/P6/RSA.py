#PRACTICA 4 CIFRADO Y DESCIFRADO RSA. 
#Alicia envía su voto a la urna
import sys   
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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
    return "Se ha encriptado su texto en la siguiente ruta: Clave_cifrada.dat"


   
def descifrado_rsa(texto,keyprivate):
   
    with open(texto, "rb") as mensaje_file:
        clavecif =  mensaje_file.read()
    mensaje_file.close()
    
    
    with open(keyprivate, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )
    
    p= private_key.private_numbers().p
    q= private_key.private_numbers().q
    d= private_key.private_numbers().d
    
    
    plaintext = private_key.decrypt(
        clavecif,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )   
    with open("Clave_descifrada.dat", "wb") as dcif_file:
        dcif_file.write(plaintext)
    dcif_file.close()
   
    return "Se ha desencriptado su texto en la siguiente ruta: Clave_descifrada.dat"


  
def main():
    key = b"HOLA"
    with open("Clave_AES.dat", "wb") as key_file:
        key_file.write(key) 
    key_file.close()
    
    print(cifrado_rsa("Clave_AES.dat","Urna.crt","Clave_cifrada.dat"))
    print(descifrado_rsa("Clave_cifrada.dat","Urna.pem"))
   
    
        
if __name__ == '__main__':
	main()