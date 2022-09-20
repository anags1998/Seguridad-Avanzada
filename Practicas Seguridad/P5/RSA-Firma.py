#PRACTICA 5 FIRMA Y VERIFICACIÓN RSA. 
#Comprobación de voto de Alicia
import sys   
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography import exceptions

def firmado(texto,keyprivate):
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
    
    with open("firma.dat", "wb") as cif_file:
        cif_file.write(signature)
    cif_file.close()
    return "Se ha firmado su texto en la siguiente ruta: firma.dat"


   
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
        

  
def main():
    key = b"HOLA"
    with open("resumen.dat", "wb") as key_file:
        key_file.write(key) 
    key_file.close()
    
    print(firmado("resumen.dat","Alicia.pem"))
    print(verificacion("resumen.dat","firma.dat","Alicia.crt"))
   
    
        
if __name__ == '__main__':
	main()