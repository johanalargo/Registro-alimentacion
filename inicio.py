# ================= IMPORTACIONES =================
import tkinter as tk                          # Interfaz gráfica
from tkinter import ttk, messagebox           # Widgets avanzados y mensajes
import calendar                               # Calendario mensual
from PIL import Image, ImageTk                # Manejo de imágenes (logo)
from pdf import generar_pdf                   # Función que genera el PDF
import os                                     # Manejo de rutas
from datetime import datetime                 # Fecha actual
import time                                   # Manejo de tiempos (loading)


# ==================================================
# VENTANA PRINCIPAL
# ==================================================
root = tk.Tk()

# Se oculta al inicio para mostrar primero el loading
root.withdraw()

root.title("Registro de Alimentación")
root.geometry("1200x750")

# Ícono de la aplicación  logo    
root.iconbitmap('image/logo.ico')


# ==================================================
# VENTANA "ACERCA DE"
# ==================================================
def mostrar_acerca_de():
    ventana = tk.Toplevel(root)
    ventana.title("Acerca de")
    ventana.geometry("420x320")
    ventana.iconbitmap("image/logo.ico")
    ventana.resizable(False, False)

    # Centrar ventana
    x = (ventana.winfo_screenwidth() // 2) - (420 // 2)
    y = (ventana.winfo_screenheight() // 2) - (320 // 2)
    ventana.geometry(f"420x320+{x}+{y}")

    frame = tk.Frame(ventana, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    # Título
    tk.Label(frame, text="Registro de Alimentación",
             font=("Arial", 15, "bold")).pack(pady=10)

    # Versión
    tk.Label(frame, text="Versión 1.0.0",
             font=("Arial", 12)).pack(pady=5)

    ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=10)

    # Autor
    tk.Label(frame, text="Desarrollado por:",
             font=("Arial", 11, "bold")).pack()

    tk.Label(frame, text="Johana Andrea Largo",
             font=("Arial", 11)).pack(pady=5)

    # Descripción
    tk.Label(
        frame,
        text=(
            "Aplicación para el control mensual\n"
            "de alimentación por cliente.\n\n"
            "Incluye calendario interactivo\n"
            "y generación de reportes en PDF."
        ),
        font=("Arial", 10),
        justify="center"
    ).pack(pady=10)

    tk.Label(frame, text="© 2026",
             font=("Arial", 9), fg="gray").pack(pady=5)

    tk.Button(frame, text="Cerrar",
              width=12, command=ventana.destroy).pack(pady=10)


# ==================================================
# MENÚ SUPERIOR
# ==================================================
def crear_menu():
    menu_bar = tk.Menu(root)

    menu_ayuda = tk.Menu(menu_bar, tearoff=0)
    menu_ayuda.add_command(label="Acerca de", command=mostrar_acerca_de)

    menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)
    root.config(menu=menu_bar)


# ==================================================
#   LOADING
# ==================================================
def mostrar_loading():
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg="white")

    # Tamaño y centrado
    ancho, alto = 450, 300
    x = (splash.winfo_screenwidth() // 2) - (ancho // 2)
    y = (splash.winfo_screenheight() // 2) - (alto // 2)
    splash.geometry(f"{ancho}x{alto}+{x}+{y}")

    splash.lift()
    splash.attributes("-topmost", True)

    # ---------- LOGO ----------
    try:
        ruta_logo = os.path.join(os.path.dirname(__file__), "image", "logo.png")
        img = Image.open(ruta_logo)
        img = img.resize((120, 120), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)

        lbl_logo = tk.Label(splash, image=logo_img, bg="white")
        lbl_logo.image = logo_img   # 🔑 evita que el logo se borre
        lbl_logo.pack(pady=10)
    except Exception as e:
        print("Error cargando logo:", e)

    # ---------- TEXTO ----------
    tk.Label(splash, text="Registro de Alimentación",
             font=("Arial", 16, "bold"), bg="white").pack(pady=5)

    tk.Label(splash, text="Cargando aplicación...",
             font=("Arial", 11), bg="white").pack(pady=5)

    # ---------- BARRA ----------
    barra = ttk.Progressbar(
        splash,
        orient="horizontal",
        length=300,
        mode="determinate",
        maximum=100
    )
    barra.pack(pady=10)

    lbl_porcentaje = tk.Label(splash, text="0%",
                              font=("Arial", 11, "bold"), bg="white")
    lbl_porcentaje.pack()

    progreso = 0

    def cerrar_final():
        splash.destroy()
        root.deiconify()   # Mostrar app principal
        crear_menu()       # Crear menú superior

    def avanzar():
        nonlocal progreso
        progreso += 2
        barra["value"] = progreso
        lbl_porcentaje.config(text=f"{progreso}%")

        if progreso < 100:
            splash.after(50, avanzar)
        else:
            splash.after(2000, cerrar_final)

    avanzar()


# ==================================================
# TÍTULO PRINCIPAL
# ==================================================
tk.Label(
    root,
    text="Registro de Alimentación",
    font=("Arial", 18, "bold")
).pack(pady=10)


# ==================================================
# CLIENTE
# ==================================================
frame_cliente = tk.Frame(root)
frame_cliente.pack(pady=5)

tk.Label(frame_cliente, text="Cliente:",
         font=("Arial", 20, "bold")).grid(row=0, column=0, padx=8)

entry_cliente = tk.Entry(frame_cliente, width=25, font=("Arial", 12))
entry_cliente.grid(row=0, column=1, padx=5)


# ==================================================
# AÑO / MES
# ==================================================
frame_control = tk.Frame(root)
frame_control.pack(pady=5)

tk.Label(frame_control, text="Año:",
         font=("Arial", 15, "bold")).grid(row=0, column=0, padx=6)

tk.Label(frame_control, text="Mes:",
         font=("Arial", 15, "bold")).grid(row=0, column=2, padx=8)

spin_anio = tk.Spinbox(frame_control, from_=2020, to=2100,
                       width=13, font=("Arial", 12))
spin_anio.grid(row=0, column=1, padx=5)
spin_anio.delete(0, "end")
spin_anio.insert(0, 2026)

meses = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

combo_mes = ttk.Combobox(frame_control, values=meses,
                          state="readonly", width=15)
combo_mes.grid(row=0, column=3, padx=5)
combo_mes.current(0)


# ==================================================
# BOTÓN PDF
# ==================================================
def llamar_pdf():
    cliente = entry_cliente.get().strip()
    anio = int(spin_anio.get())
    mes_nombre = combo_mes.get()
    mes = combo_mes.current() + 1

    if not cliente:
        messagebox.showwarning("Falta dato", "Ingrese el nombre del cliente")
        return

    generar_pdf(cliente, anio, mes_nombre, mes)


btn_pdf = tk.Button(
    frame_control,
    text="Generar PDF",
    bg="#1976D2",
    fg="white",
    font=("Arial", 11, "bold"),
    command=llamar_pdf
)
btn_pdf.grid(row=0, column=5, padx=10)


# ==================================================
# CALENDARIO INTERACTIVO
# ==================================================
frame_cal = tk.Frame(root, borderwidth=2, relief="solid")
frame_cal.pack(padx=10, pady=10, fill="both", expand=True)

dias_semana = [
    "Lunes", "Martes", "Miércoles",
    "Jueves", "Viernes", "Sábado", "Domingo"
]


def generar_calendario():
    for widget in frame_cal.winfo_children():
        widget.destroy()

    anio = int(spin_anio.get())
    mes = combo_mes.current() + 1
    cal = calendar.monthcalendar(anio, mes)
    hoy = datetime.today()

    # Encabezados
    for col, dia in enumerate(dias_semana):
        tk.Label(frame_cal, text=dia, bg="#4B7421",
                 fg="white", font=("Arial", 10, "bold"),
                 height=2).grid(row=0, column=col, sticky="nsew")

    for fila, semana in enumerate(cal, start=1):
        for col, dia in enumerate(semana):
            color = "white"
            if col in (5, 6):
                color = "#D3E4CD"
            if dia == hoy.day and mes == hoy.month and anio == hoy.year:
                color = "#FFCDD2"

            celda = tk.Frame(frame_cal, bg=color,
                             borderwidth=1, relief="solid")
            celda.grid(row=fila, column=col, sticky="nsew")

            if dia != 0:
                tk.Label(celda, text=str(dia),
                         font=("Arial", 10, "bold"),
                         bg=color).pack(anchor="ne", padx=4, pady=2)

                for txt in ("Desayuno", "Almuerzo", "Comida"):
                    tk.Checkbutton(celda, text=txt,
                                   bg=color).pack(anchor="w")

    for i in range(7):
        frame_cal.columnconfigure(i, weight=1)
    for i in range(len(cal) + 1):
        frame_cal.rowconfigure(i, weight=1)


# ==================================================
# ARRANQUE
# ==================================================
generar_calendario()
root.after(100, mostrar_loading)
root.mainloop()
