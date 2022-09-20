import sys

import sys
import pathlib

from Crypto.Random import *
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import *
def cifradoRSA(clave):
    #Abro clave 
    with open(clave, "rb") as des_file:
        clave_b =  des_file.read()
    des_file.close()
    print(clave_b)
    #Abro certificado urna
    with open("Urna.crt", "rb") as certf_u_file:
        ctr_u =  certf_u_file.read()
    certf_u_file.close()
        
    #Saco clave pública de la urna
    cert_u = x509.load_pem_x509_certificate(ctr_u)
    keypublic_u = cert_u.public_key()
    
    #Obtengo números públicos de la urna
    nu= keypublic_u.public_numbers().n
    eu= keypublic_u.public_numbers().e 
    
    k_int = int.from_bytes(clave_b,'big')
    print(k_int)
    k_rsa = pow(k_int,eu,nu)
    k_rsa_b = k_rsa.to_bytes(sys.getsizeof(k_rsa),'big')
        
    with open("k_cif.dat", "wb") as k_rsa_file:
        k_rsa_file.write(k_rsa_b)
    k_rsa_file.close()



def descifradoRSA(clave_cifrada):
    #Abro clave 
    with open(clave_cifrada, "rb") as des_file:
        clave_b =  des_file.read()
    des_file.close()
    
    k_int = int.from_bytes(clave_b,'big')
    with open("Urna.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        ) 
        
    pu= private_key.private_numbers().p
    qu= private_key.private_numbers().q
    du= private_key.private_numbers().d 
    
    #Descifro la clave con RSA
    key_int = pow(k_int,du,pu*qu)
    key = key_int.to_bytes(16,'big')
    print(key_int)
    print(key)
    with open("k_descif.dat", "wb") as k_rsa_file:
        k_rsa_file.write(key)
    k_rsa_file.close()


if __name__ == '__main__':
	
    f=open(sys.argv[1],"wb")
    f.write(get_random_bytes(16))
    f.close()
    cifradoRSA(sys.argv[1])
    descifradoRSA("k_cif.dat")
#descifradoRSA(r"Clave_cifrada.DAT")