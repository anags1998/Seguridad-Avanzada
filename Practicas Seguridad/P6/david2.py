import sys
import pathlib

from Crypto.Random import *
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import *


def firmaRSA(mensaje):
    # Abro clave
    with open(mensaje, "rb") as des_file:
        doc = des_file.read()
    des_file.close()

    doc_int = int.from_bytes(doc, 'big')

    # Obtengo clave privada de Carlos
    with open("Carlos.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    pu = private_key.private_numbers().p
    qu = private_key.private_numbers().q
    du = private_key.private_numbers().d


    doc_firma = pow(doc_int, du, pu * qu)
    doc_firma_b = doc_firma.to_bytes(sys.getsizeof(doc_firma), 'big')

    with open("firma.DAT", "wb") as firma_file:
        firma_file.write(doc_firma_b)
    firma_file.close()


def verificarRSA(mensaje_firmado, mensaje):
    # Abro clave
    with open(mensaje_firmado, "rb") as firma_file:
        doc_firmado = firma_file.read()
    firma_file.close()
    with open(mensaje, "rb") as des_file:
        mensaje_b = des_file.read()
    des_file.close()
    
    # Abro certificado urna
    with open("Carlos.crt", "rb") as certf_u_file:
        ctr_u = certf_u_file.read()
    certf_u_file.close()

    # Saco clave pública de la urna
    cert_u = x509.load_pem_x509_certificate(ctr_u)
    keypublic_u = cert_u.public_key()

    # Obtengo números públicos de la urna
    nu = keypublic_u.public_numbers().n
    eu = keypublic_u.public_numbers().e

    doc_firmado_int = int.from_bytes(doc_firmado, 'big')
    mensaje_int = int.from_bytes(mensaje_b, 'big')
    
    
    doc_desfirmado = pow(doc_firmado_int, eu, nu)
    
    
    if mensaje_int == doc_desfirmado:
        valid = True
        return valid
    else:
        valid = False
        return valid
   

name = 'main'
if name == 'main':
    firmaRSA("voto.dat")
    valid = verificarRSA("firma.DAT", "voto.dat")
    print(valid)