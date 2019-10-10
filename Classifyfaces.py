from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from face_rec_functions import img_filter
from time import sleep
import os
import threading


window = Tk()
window.title("Filtrar fotos")
window.geometry('650x300')

known = ""
unknown = ""
matches = ""
difference = 0.5

# pedir known img path
lbl_known = Label(
    window, text="Carpeta con conocidos: ", font=("Arial", 10))
lbl_known.grid(column=0, row=0)


def known_select():
    dir = filedialog.askdirectory()
    lbl_known.configure(text="Carpeta con conocidos: "+dir)
    global known
    known = dir


btn_known = Button(
    window, text="Seleccionar", command=known_select)
btn_known.grid(column=1, row=0)

# pedir unknown
lbl_unknown = Label(
    window, text="Carpeta a filtar: ", font=("Arial", 10))
lbl_unknown.grid(column=0, row=1)


def unknown_select():
    dir = filedialog.askdirectory()
    lbl_unknown.configure(text="Carpeta a filtrar: "+dir)
    global unknown
    unknown = dir


btn_unknown = Button(
    window, text="Seleccionar", command=unknown_select)
btn_unknown.grid(column=1, row=1)

# pedir matches
lbl_matches = Label(
    window, text="Carpeta destino: ", font=("Arial", 10))
lbl_matches.grid(column=0, row=2)


def matches_select():
    dir = filedialog.askdirectory()
    lbl_matches.configure(text="Carpeta destino: "+dir)
    global matches
    matches = dir


btn_matches = Button(
    window, text="Seleccionar", command=matches_select)
btn_matches.grid(column=1, row=2)


# iniciar
lbl_msg = Label(
    window, text="", font=("Arial", 10))
lbl_msg.grid(column=0, row=5)


def change_label(data):
    print(data)
    lbl_msg.configure(text=data)


# diferencia
lbl_diff = Label(
    window, text="Diferencia aceptable (menor es mas preciso)", font=("Arial", 10))
lbl_diff.grid(column=0, row=4)

valores_diff = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
var = StringVar()
diff_selector = Spinbox(window, textvariable=var, from_=0.2, to=0.9,
                        width=4, values=valores_diff)
diff_selector.grid(column=1, row=4)
var.set(difference)


# thread para correr el proceso en otro hilo mientras la interfaz se mantiene
def init_filter():
    # reviso que se ingresaron los datos necesarios
    if unknown != "" and known != "" and matches != "":
        diferencia = diff_selector.get()
        # me aseguro que diferencia este entre 0.2 y 0.9
        if diferencia == "" or float(diferencia) > 0.9 or float(diferencia) < 0.2:
            diferencia = 0.6
            var.set(diferencia)
        lbl_msg.configure(
            text="Ejecutando... mantén la ventana abierta, el proceso puede tardar unos minutos", fg="blue")
        # abro la carpeta destino
        os.startfile(matches)
        try:
            btn_iniciar.configure(state="disabled")
            img_filter(known, unknown, matches,
                       change_label, diff_selector.get())
            btn_iniciar.configure(state="normal")
        except:
            lbl_msg.configure(
                text="Hubo un error, no se terminó de filtrar", fg="red")
    else:
        lbl_msg.configure(
            text="Selecciona las 3 rutas para continuar", fg="red")


def start_init_filter_thread(event):
    global init_thread
    init_thread = threading.Thread(target=init_filter)
    init_thread.daemon = True
    init_thread.start()


# boton de iniciar
btn_iniciar = Button(window, text="Iniciar filtrado",
                     command=lambda: start_init_filter_thread(None))
btn_iniciar.grid(column=0, row=6)

window.mainloop()
