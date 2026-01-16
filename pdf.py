
# ================= IMPORTACIONES =================
from reportlab.lib.pagesizes import A4, landscape   # Tamaño de página y orientación horizontal
from reportlab.pdfgen import canvas                 # Motor para crear PDFs
from reportlab.lib.units import cm                  # Medidas en centímetros
from reportlab.lib.colors import HexColor, black, white  # Colores
import calendar                                     # Manejo de calendarios
import os                                           # Manejo de rutas y archivos
from tkinter import messagebox                      # Mensajes emergentes
from datetime import datetime                       # Fecha actual


# =================================================
# FUNCIÓN PRINCIPAL PARA GENERAR EL PDF
# =================================================
def generar_pdf(cliente, anio, mes_nombre, mes):

    # ================= RUTA DE DESCARGAS =================
    # Obtiene la ruta del usuario actual y la carpeta Downloads
    ruta = os.path.join(os.path.expanduser("~"), "Downloads")

    # Nombre base del archivo
    base = f"Calendario_{cliente}_{mes_nombre}_{anio}"
    archivo = os.path.join(ruta, f"{base}.pdf")

    # Evitar sobrescribir: si existe, crea uno con número consecutivo
    contador = 1
    while os.path.exists(archivo):
        archivo = os.path.join(ruta, f"{base}_{contador}.pdf")
        contador += 1

    # ================= CREACIÓN DEL PDF =================
    # Página tamaño A4 en horizontal
    c = canvas.Canvas(archivo, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Fecha actual (para resaltar el día de hoy)
    hoy = datetime.today()

    # ================= COLORES =================
    color_encabezado = HexColor("#4B7421")   # Verde oscuro encabezados
    color_fin = HexColor("#C5E0B4")           # Verde claro fines de semana
    color_hoy = HexColor("#F4B6B6")           # Rosado día actual
    color_fuera = HexColor("#888888")         # Gris días fuera del mes

    # ================= TÍTULO =================
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        width / 2,
        height - 2.0 * cm,
        "Registro de Alimentación"
    )

    # ================= DATOS DEL CLIENTE =================
    y_datos = height - 3.5 * cm

    # Etiqueta Cliente
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y_datos, "Cliente:")

    # Nombre del cliente
    c.setFont("Helvetica", 18)
    c.drawString(4.5 * cm, y_datos, cliente)

    # Espacio vertical
    y_datos -= 1.0 * cm

    # ================= MES + DÍA ACTUAL =================
    c.setFont("Helvetica-Bold", 15)
    c.drawString(2 * cm, y_datos, "Mes:")

    c.setFont("Helvetica", 15)
    c.drawString(
        3.6 * cm,
        y_datos,
        f"{mes_nombre} {hoy.day}"
    )

    # ================= AÑO =================
    c.setFont("Helvetica-Bold", 15)
    c.drawString(6.5 * cm, y_datos, "Año:")

    c.setFont("Helvetica", 15)
    c.drawString(8.2 * cm, y_datos, str(anio))

    # ================= CALENDARIO =================
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    cal = calendar.monthcalendar(anio, mes)

    # ---------- Datos del mes anterior ----------
    if mes == 1:
        mes_anterior = 12
        anio_anterior = anio - 1
    else:
        mes_anterior = mes - 1
        anio_anterior = anio

    dias_mes_anterior = calendar.monthrange(anio_anterior, mes_anterior)[1]
    contador_mes_siguiente = 1  # Para días del mes siguiente

    # Posición y tamaño del calendario
    x0 = 1.5 * cm
    y0 = height - 5.9 * cm
    ancho = (width - 2.5 * cm) / 7
    alto = 3.0 * cm

    # ================= ENCABEZADOS DE DÍAS =================
    c.setFont("Helvetica-Bold", 11)
    for i, d in enumerate(dias):
        c.setFillColor(color_encabezado)
        c.rect(x0 + i * ancho, y0, ancho, 1 * cm, fill=1, stroke=1)
        c.setFillColor(white)
        c.drawCentredString(
            x0 + i * ancho + ancho / 2,
            y0 + 0.35 * cm,
            d
        )

    c.setFillColor(black)

    # ================= CELDAS DEL CALENDARIO =================
    y = y0 - alto

    for fila, semana in enumerate(cal):
        for col, dia in enumerate(semana):

            # Fondo por defecto
            fondo = None

            # Fines de semana
            if col in (5, 6):
                fondo = color_fin

            # Día actual
            if dia == hoy.day and mes == hoy.month and anio == hoy.year:
                fondo = color_hoy

            # Dibujar celda
            if fondo:
                c.setFillColor(fondo)
                c.rect(x0 + col * ancho, y, ancho, alto, fill=1, stroke=1)
                c.setFillColor(black)
            else:
                c.rect(x0 + col * ancho, y, ancho, alto)

            # ---------- DÍAS DEL MES ACTUAL ----------
            if dia != 0:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(
                    x0 + col * ancho + 0.2 * cm,
                    y + alto - 0.6 * cm,
                    str(dia)
                )

                # Checks
                c.setFont("Helvetica", 9)
                for j, txt in enumerate(["Desayuno", "Almuerzo", "Comida"]):
                    yy = y + alto - (1.4 + j * 0.7) * cm
                    c.rect(
                        x0 + col * ancho + 0.2 * cm,
                        yy,
                        0.4 * cm,
                        0.4 * cm
                    )
                    c.drawString(
                        x0 + col * ancho + 0.8 * cm,
                        yy + 0.05 * cm,
                        txt
                    )

            # ---------- DÍAS FUERA DEL MES ----------
            else:
                c.setFont("Helvetica", 10)
                c.setFillColor(color_fuera)

                if fila == 0:
                    ceros = semana.count(0)
                    dia_fuera = dias_mes_anterior - ceros + col + 1
                else:
                    dia_fuera = contador_mes_siguiente
                    contador_mes_siguiente += 1

                c.drawString(
                    x0 + col * ancho + 0.2 * cm,
                    y + alto - 0.6 * cm,
                    str(dia_fuera)
                )

                c.setFillColor(black)

        y -= alto

    # ================= GUARDAR PDF =================
    c.save()

    # Confirmación visual
    messagebox.showinfo(
        "PDF generado",
        f"PDF generado correctamente en Descargas:\n{archivo}"
    )
