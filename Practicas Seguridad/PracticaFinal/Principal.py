#PRACTICA 6. ESCENARIO DE FIRMA CIEGA Y ENSAMBLAJE.
certf_i = "Certificados\CA_Servidora_de_identidades.crt"
keyprivate_i = "Certificados\CA_Servidora_de_identidades.pem"
keyprivate_u = "Certificados/Urna.pem"
certf_u = "Certificados/Urna.crt"

from tkinter import *
from Votante2iden import votante_identidades
from Iden2votante import identidades_votante
from Votante2Urna import votante_urna
from Urnafin import urna_fin  
import os

def main():
    if(os.path.isfile("Alicia.dat") and os.path.isfile("Blanca.dat") and os.path.isfile("Carlos.dat")):
        os.remove("Alicia.dat")
        os.remove("Blanca.dat")
        os.remove("Carlos.dat")
    
    while True:
        #Solo permito votar a los tres votantes, es decir, tres veces
        if(os.path.isfile("Alicia.dat") and os.path.isfile("Blanca.dat") and os.path.isfile("Carlos.dat")):
            #Warning de voto repetido
            window = Tk()
            window.title("Warning")
            miFrame = Frame(window, width = 500, height = 400)
            miFrame.pack()
            nombreLabel = Label(miFrame,text="Se han recogido todos los votos de las personas autorizadas.")
            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
            botonEnvio = Button(window, text = "OK", command = window.quit)
            botonEnvio.pack()
            window.mainloop()
            break
        else:
            #Creación de interfaz para la introducción de los datos necesarios"
            window = Tk()
            window.title("Ventana de parametros")
            miFrame = Frame(window, width = 500, height = 400)
            miFrame.pack()
            
            nombreLabel = Label(miFrame,text="Nombre: ")
            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
            votoLabel = Label(miFrame,text="Voto: ")
            votoLabel.grid(row = 1, column = 0, sticky = "e", padx = 30, pady = 10)
            certfLabel = Label(miFrame,text="Certificado: ")
            certfLabel.grid(row = 2, column = 0, sticky = "e", padx = 30, pady = 10)

            nombreEntry = Entry(miFrame)
            nombreEntry.grid(row = 0, column = 1, padx = 30, pady = 10)
            votoEntry = Entry(miFrame)
            votoEntry.grid(row = 1, column = 1, padx = 30, pady = 10)
            certfEntry = Entry(miFrame)
            certfEntry.grid(row = 2, column = 1, padx = 30, pady = 10)
            
            def codigoBoton():
                nombre = nombreEntry.get()
                with open("nombre.dat", "w") as nombre_file:
                    nombre_file.write(nombre)
                nombre_file.close()
                voto = votoEntry.get()
                with open("voto.dat", "w") as voto_file:
                    voto_file.write(voto)
                voto_file.close()
                certificado = certfEntry.get()
                with open("certf.dat", "w") as cert_file:
                    cert_file.write(certificado)
                cert_file.close()
            
            botonEnvio = Button(window, text = "Salir", command = exit)
            botonEnvio.pack()
            botonEnvio = Button(window, text = "Enviar", command = window.quit)
            botonEnvio.pack()
            botonGuardar = Button(window, text = "Guardar", command = codigoBoton)
            botonGuardar.pack()

            window.mainloop()
            window.destroy()
            
            #Compruebo la existencia de los datos introducidos
            if os.path.isfile("voto.dat") and os.path.isfile("nombre.dat") and os.path.isfile("certf.dat"):
                with open("voto.dat", "r") as voto_file:
                    voto = voto_file.read()
                voto_file.close()
                if (voto.upper() == "NO" or voto.upper() == "SI" or voto.upper() == ""):
                    with open("nombre.dat", "r") as nombre_file:
                        nombre = nombre_file.read()
                    nombre_file.close()
                    
                    with open("certf.dat", "r") as cert_file:
                        certificado = cert_file.read()
                    cert_file.close()
                   
                    keyprivate_v = "Certificados" +  certificado
                    
                    #Comprobación de datos bien introducidos
                    if ((nombre.upper() == "ALICIA") and (certificado == "\Alicia.pem")):
                        if os.path.isfile("Alicia.dat"):
                            #Warning de voto repetido
                            window = Tk()
                            window.title("Warning")
                            miFrame = Frame(window, width = 500, height = 400)
                            miFrame.pack()
                            nombreLabel = Label(miFrame,text="Parando ejecución, ya has votado en otra ocasión.")
                            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                            botonEnvio = Button(window, text = "OK", command = window.quit)
                            botonEnvio.pack()
                            window.mainloop()
                            break
                        else:
                            certf_v = "Certificados\Alicia.crt"
                    elif ((nombre.upper() == "BLANCA") and (certificado == "\Blanca.pem")):
                        if os.path.isfile("Blanca.dat"):
                            #Warning de voto repetido
                            window = Tk()
                            window.title("Warning")
                            miFrame = Frame(window, width = 500, height = 400)
                            miFrame.pack()
                            nombreLabel = Label(miFrame,text="Parando ejecución, ya has votado en otra ocasión.")
                            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                            botonEnvio = Button(window, text = "OK", command = window.quit)
                            botonEnvio.pack()
                            window.mainloop()
                            break
                        else:
                            certf_v = "Certificados\Blanca.crt"
                    elif ((nombre.upper() == "CARLOS") and (certificado == "\Carlos.pem")):
                        if os.path.isfile("Carlos.dat"):
                            #Warning de voto repetido
                            window = Tk()
                            window.title("Warning")
                            miFrame = Frame(window, width = 500, height = 400)
                            miFrame.pack()
                            nombreLabel = Label(miFrame,text="Parando ejecución, ya has votado en otra ocasión.")
                            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                            botonEnvio = Button(window, text = "OK", command = window.quit)
                            botonEnvio.pack()
                            window.mainloop()
                            break
                        else:
                            certf_v = "Certificados\Carlos.crt"
                    else:
                        #Warning de datos mal introducidos
                        window = Tk()
                        window.title("Warning")
                        miFrame = Frame(window, width = 500, height = 400)
                        miFrame.pack()
                        nombreLabel = Label(miFrame,text="Parando ejecución, por datos mal introducidos.")
                        nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                        botonEnvio = Button(window, text = "OK", command = window.quit)
                        botonEnvio.pack()
                        window.mainloop()
                        break
                    
                    #Llamo a la función de Votante-identidad
                    x,y = votante_identidades("voto.dat", certf_v, keyprivate_v, certf_i)
                    #Llamo a la función de identidad-votante
                    validacion, B = identidades_votante(x,y,certf_v, keyprivate_i, certf_i)
                    if validacion:
                        #Llamo a función de votante-urna
                        validacion2,cifrado,RSA,IV_rsa,br = votante_urna(B, certf_v, keyprivate_v, certf_i,certf_u)
                        if validacion2:
                            #Llamo a función de la urna final
                            archivo = nombre + ".dat"
                            validacion3,voto = urna_fin("cifrado.dat","k_rsa.dat","iv_rsa.dat","br.dat",certf_v,certf_i,keyprivate_u,certf_u,archivo)
                            if validacion3:
                                #Todo ha salido bien
                                window = Tk()
                                window.title("Aviso")
                                miFrame = Frame(window, width = 500, height = 400)
                                miFrame.pack()
                                nombreLabel = Label(miFrame,text="Tu voto ha sido procesado.")
                                nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                                botonEnvio = Button(window, text = "OK", command = window.quit)
                                botonEnvio.pack()
                                window.mainloop()
                                window.destroy()
                            else:
                                #Warning de mala validación por urna
                                window = Tk()
                                window.title("Warning")
                                miFrame = Frame(window, width = 500, height = 400)
                                miFrame.pack()
                                nombreLabel = Label(miFrame,text="Parando ejecución, por mala validación final de la Urna.")
                                nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                                botonEnvio = Button(window, text = "OK", command = window.quit)
                                botonEnvio.pack()
                                window.mainloop()
                                break
                        else:
                            #Warning de mala validación por el votante
                            window = Tk()
                            window.title("Warning")
                            miFrame = Frame(window, width = 500, height = 400)
                            miFrame.pack()
                            nombreLabel = Label(miFrame,text="Parando ejecución, por mala validación del Votante.")
                            nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                            botonEnvio = Button(window, text = "OK", command = window.quit)
                            botonEnvio.pack()
                            window.mainloop()
                            break
                    else:
                        #Warning de mala validación por autoridad de identidades
                        window = Tk()
                        window.title("Warning")
                        miFrame = Frame(window, width = 500, height = 400)
                        miFrame.pack()
                        nombreLabel = Label(miFrame,text="Parando ejecución, por mala validación de la Autoridad de Identidades.")
                        nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                        botonEnvio = Button(window, text = "OK", command = window.quit)
                        botonEnvio.pack()
                        window.mainloop()
                        break
                else:
                    #Warning de voto nulo
                    window = Tk()
                    window.title("Warning")
                    miFrame = Frame(window, width = 500, height = 400)
                    miFrame.pack()
                    nombreLabel = Label(miFrame,text="Parando ejecución, su voto es nulo.")
                    nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                    botonEnvio = Button(window, text = "OK", command = window.quit)
                    botonEnvio.pack()
                    window.mainloop()
                    break
            else:
                #Warning falta de datos
                window = Tk()
                window.title("Warning")
                miFrame = Frame(window, width = 500, height = 400)
                miFrame.pack()
                nombreLabel = Label(miFrame,text="Parando ejecución, por falta de datos.")
                nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 30, pady = 10)
                botonEnvio = Button(window, text = "OK", command = window.quit)
                botonEnvio.pack()
                window.mainloop()
                break
        
        
        
if __name__ == '__main__':
	main()  