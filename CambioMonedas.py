#importar la libreria para operaciones estadisticas
import pandas as pd
#importar libreria para interfaz grafica de usuario
from tkinter import *
from tkinter.ttk import Notebook
from tkinter import messagebox

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
    if cmbMoneda.current() >=0:
        df.sort_values(by="Fecha", ascending=False).head()
        cambios = df[df["Moneda"]==monedas[cmbMoneda.current()]]
        y = cambios["Cambio"]

        fechas=cambios["Fecha"]

        print(fechas)
        
    else:
        messagebox.showerror("Error graficando", "No ha seleccionado la moneda")

def estadisticas():
    pass

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



