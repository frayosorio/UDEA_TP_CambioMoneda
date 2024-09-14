#importar la libreria para operaciones estadisticas
import pandas as pd
#importar libreria para interfaz grafica de usuario
from tkinter import *
from tkinter.ttk import Notebook
from tkinter import messagebox
#importar libreria para manejo de fechas y tiempo
from datetime import *
#importar libreria para crear gráficas
from matplotlib import pyplot as plt
#importar libreria util
import Util

iconos = ["./iconos/grafica.png", \
          "./iconos/datos.png"]

textosBotones = ["Gráfica Cambio vs Fecha", "Datos Estadísticos"]

df = None

def obtenerMonedas():
    global df
    df = pd.read_csv("Cambios Monedas.csv")
    monedas = df["Moneda"].tolist()
    return list(set(monedas))
    #return list(dict.fromkeys(monedas))

def graficar():
    #global df, monedas
    if cmbMoneda.current() >= 0:
        nb.select(0)
        df.sort_values(by="Fecha", ascending=False).head()
        cambios = df[df["Moneda"]==monedas[cmbMoneda.current()]]
        y = cambios["Cambio"]

        fechas=cambios["Fecha"]
        x = [datetime.strptime(f, "%d/%m/%Y").date() for f in fechas]
        
        #crear grafica
        plt.clf()
        plt.title("Cambios de la moneda "+monedas[cmbMoneda.current()])
        plt.ylabel("Cambios")
        plt.xlabel("Fechas")
        plt.plot(x, y)
        nombreArchivo = "Grafica Cambios Moneda.png"
        plt.savefig(nombreArchivo)

        #mostrar la grafica
        Util.agregarImagen(paneles[0], nombreArchivo, 0, 0)
    else:
        messagebox.showerror("Error graficando", "No ha seleccionado la moneda")

def estadisticas():
    if cmbMoneda.current() >= 0:
        nb.select(1)
        cambios = df[df["Moneda"]==monedas[cmbMoneda.current()]]

        #mostrar el promedio
        Util.agregarEtiqueta(paneles[1], "Promedio:", 0, 0)
        #Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].mean()), 0, 1)
        Util.agregarEtiqueta(paneles[1], f"{cambios['Cambio'].mean():.2f}", 0, 1)

        #mostrar la desviación estandar
        Util.agregarEtiqueta(paneles[1], "Desviación:", 1, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].std()), 1, 1)

        #mostrar el maximo
        Util.agregarEtiqueta(paneles[1], "Máximo:", 2, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].max()), 2, 1)

        #mostrar el mínimo
        Util.agregarEtiqueta(paneles[1], "Mínimo:", 3, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].min()), 3, 1)

        #mostrar la moda
        Util.agregarEtiqueta(paneles[1], "Moda:", 4, 0)
        f = 4
        for moda in cambios["Cambio"].mode():
            Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(moda), f, 1)
            f+=1
    else:
        messagebox.showerror("Error en estadísticas", "No ha seleccionado la moneda")

#crear una ventana
v = Util.crearVentana("Cambios de Monedas", "400x300")

#agregar una barra de herramientas basada en una lista de archivos con imagenes
botones = Util.agregarBarra(v, iconos, textosBotones)
botones[0].configure(command = graficar)
botones[1].configure(command = estadisticas)

#agregar contenedor para la lista que permite escoger la moneda a procesar
frm = Frame(v)
frm.pack(side=TOP, fill=X)
Util.agregarEtiqueta(frm, "Moneda:", 0, 0)

monedas = obtenerMonedas()
cmbMoneda = Util.agregarLista(frm, monedas, 0, 1)

#agregar panel de pestañas para mostrar resultados
nb = Notebook(v)
nb.pack(fill=BOTH, expand=YES)
encabezados = ["Gráfica", "Datos"]
paneles = []
for e in encabezados:
    frm = Frame(v)
    paneles.append(frm)
    nb.add(frm, text=e)



