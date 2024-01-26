# Importamos todas las librerías que nos permitirán hacer la interfaz, abrir imágenes y reproducir los sonidos.
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import requests
from io import BytesIO

import pygame
import time
import threading


# Esta función se encargará de reproducir el sonido en un hilo separado
def reproducir_audio(archivo_wav):
    def reproducir():
        pygame.mixer.init()
        pygame.mixer.music.load(archivo_wav)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    # Iniciar el hilo para reproducir música
    threading.Thread(target=reproducir).start()

# Esta función  se encargará de abrir las imágenes en cada instancia de la historia, por eso la referimos constantemente.        
def cargar_imagen(url):
    try:
        imagen_respuesta = requests.get(url)
        imagen_respuesta.raise_for_status()

        imagen_pil = Image.open(BytesIO(imagen_respuesta.content))
        imagen_tk = ImageTk.PhotoImage(imagen_pil)
        label_imagen.config(image=imagen_tk)
        label_imagen.image = imagen_tk
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

# Esta función se encargará de borrar el texto mostrado inicialmente para dar espacio al siguiente y, al mismo tiempo, creará las opciones como botones.
def mostrar_historia(texto_historia, opciones):
    texto.delete(1.0, tk.END)
    texto.insert(tk.END, texto_historia)
    crear_botones_opciones(opciones)

# Esta función creará los botones.
def crear_botones_opciones(opciones):
    for boton in botones_opciones:
        boton.destroy()
    botones_opciones.clear()
    for opcion_texto, opcion_accion, *resto_opcion in opciones:
        if resto_opcion:
            url_imagen = resto_opcion[0]
            boton = tk.Button(root, text=opcion_texto, command=lambda url=url_imagen: opcion_accion(url), fg="white", bg="black", font=("Arial", 16))
        else:
            boton = tk.Button(root, text=opcion_texto, command=opcion_accion, fg="white", bg="black", font=("Arial", 16))
        boton.pack(side="top", pady=5)
        botones_opciones.append(boton)

# A partir de aquí, la dinámica es la misma, simplemente cada función hace referencia a otras funciones para que estén conectadas.
# Por ejemplo, en la función "iniciar_historia" se coloca la url de la imagen y luego se refiere a la función "cargar_imagen" para mostrarla.
# Coloco como una variable de tipo string el texto de la historia. Luego se refiere a la función "mostrar_historia" para borrar
# el texto y que me muestre el siguiente. Asimismo, me crea los botones a partir de la lista de opciones que le estoy dando.
# Cada opción conducirá a una función diferente, sea la función "Corona_da" o "Corona_no_da". En cada una de estas, se repite la dinámica.
def iniciar_historia():
    imagen_inicial_url = "https://i.ibb.co/qMDYKxZ/Imagen-Juan-Sanchez-1.jpg"  # Reemplaza esto con la URL de tu imagen inicial
    cargar_imagen(imagen_inicial_url)
    historia_inicial = "Érase una vez, en el año 1512, el explorador Juan Sánchez se encontraba reflexionando sobre los relatos de una fuente mística que otorgaba la eterna juventud. Motivado por la búsqueda de la inmortalidad, decidió emprender una nueva expedición hacia las tierras inexploradas de Florida. Para conseguir financiamiento acude a los reyes de España.\n¿Los reyes le dan el permiso y dinero a Juan Sánchez?\n"

    opciones = [
        ("La corona le da financiamiento", Corona_da),
        ("La corona no le da financiamiento", Corona_no_da)
    ]

    mostrar_historia(historia_inicial, opciones)


def Corona_da(url_imagen=None):
    nueva_historia = "Juan Sánchez inicia su expedición con 4 barcos y 160 hombres. Luego de 5 noches, se cruzan con un inmenso kraken.\nEl capitán Juan Sánchez debe tomar una decisión:"
    imagen1 = "https://media.istockphoto.com/id/1306702763/es/foto/buque-de-guerra-navegando-por-el-mar-durante-una-tormenta.jpg?s=612x612&w=0&k=20&c=mGrFzLP6Hjwgo9HhQWTP3r0JzrCi7RmE3rduHIHnh9A="
    opciones = [
        ("Enfrentarse al kraken", Enfrenta_Kraken),
        ("Desviarse de la ruta original para evitar al kraken", Desvío_Kraken)
    ]
    cargar_imagen(imagen1)
    mostrar_historia(nueva_historia, opciones)
    # Aquí se llama a la función para reproducir música de fondo. Solo colocamos este, pero podríamos introducirlo también en otras instancias refiriendo a la función y con otro archivo de audio.
    reproducir_audio('waves.wav')
    mostrar_historia(nueva_historia, opciones)

def Corona_no_da(url_imagen=None):
    nueva_historia = "Juan decide acudir a la Corona inglesa para buscar el financiamiento que los reyes de España le negaron. La reina Isabel le comunica a Juan que Inglaterra no está en busca de expedicionarios, sino de soldados y le ofrece luchar por el bando inglés a cambio de una gran suma de dinero.\n¿Qué decisión tomará Juan?"
    imagen5 = "https://i.ibb.co/hZYVh95/Imagen-Isabel-I-1.jpg" 
    cargar_imagen(imagen5)
    opciones = [
        ("Juan decide aceptar la oferta", Acepta_fin3),
        ("Juan declina la oferta", Declina_fin4)
    ]
    cargar_imagen(url_imagen) if url_imagen else None
    mostrar_historia(nueva_historia, opciones)

def Acepta_fin3(url_imagen=None):
    nueva_historia = "Juan se enlista en el ejército inglés. Participa en algunas batallas hasta llegar a ser contraalmirante en una fragata. En 1588, su participación es clave en la victoria inglesa sobre la Armada Invencible, con lo cual se hace merecedor de grandes mercedes por parte de la reina Isabel, quien lo nombra capitán de un navío llamado el Perla Negra. Juan acabará sus días como capitán del Perla Negra.\n\nFIN DE LA HISTORIA DE JUAN SÁNCHEZ"
    # En algunas funciones, la lista de "opciones" está vacía porque ya no se necesitan opciones ni botones, puesto que esa historia específica ya acabó.
    opciones = []
    cargar_imagen(url_imagen) if url_imagen else None
    mostrar_historia(nueva_historia, opciones)


def Declina_fin4(url_imagen=None):
    nueva_historia = "A pesar de haber sido denegado, Juan no sería capaz de luchar por otro bando que no sea el de su patria, por lo que se retira del palacio inglés y vuelve a España con la esperanza de enrolarse en la expedición de otro navegante a quien el financiamiento le sea otorgado.\n\nFIN DE LA HISTORIA DE JUAN SÁNCHEZ"
    imagen5 = " https://i.ibb.co/gdxWmbT/Imagen-Vuelve-Arrepentido.png" 
    cargar_imagen(imagen5)
    opciones = []
    mostrar_historia(nueva_historia, opciones)


    nueva_historia = "A pesar de haber sido denegado, Juan no sería capaz de luchar por otro bando que no sea el de su patria, por lo que se retira del palacio inglés y vuelve a España con la esperanza de enrolarse en la expedición de otro navegante a quien el financiamiento le sea otorgado.\n\nFIN DE LA HISTORIA DE JUAN SÁNCHEZ"
    opciones = []
    cargar_imagen(url_imagen) if url_imagen else None
    mostrar_historia(nueva_historia, opciones)

def Enfrenta_Kraken(url_imagen=None):
    nueva_historia = "Juan Sánchez logra vencer al kraken y continúa su camino. A los dos días, ve tierra firme y su brújula le indica que va por el buen camino. Desembarcan y se adentran a la selva. Juan y sus hombres se encuentran con un pueblo indígena.\nJuan no está seguro de cómo reaccionar."
    imagen2 = "https://i.ibb.co/Z29BhZh/Imagen-Kraken-1-1.jpg"
    cargar_imagen(imagen2)
    # Añade un ejercicio matemático
    respuesta_correcta = 4
    respuesta_usuario = simpledialog.askinteger("Ejercicio Matemático", "Resuelve: 2 + 2")

    # Verifica la respuesta
    if respuesta_usuario == respuesta_correcta:
        opciones = [
            ("Decide atacar porque piensa que los indígenas son violentos", Ataca_fin1),
            ("Intenta conversar con la tribu indígena", Conversa_fin2)
        ]
        cargar_imagen(url_imagen) if url_imagen else None
        mostrar_historia(nueva_historia, opciones)
    else:
        # Si la respuesta es incorrecta, puedes mostrar un mensaje y volver a solicitar la respuesta o manejarlo según tus necesidades.
        print("Respuesta incorrecta. Inténtalo de nuevo.")

def Desvío_Kraken(url_imagen=None):
    nueva_historia = "Juan Sánchez decide tomar otro camino y llega a una isla donde son recibidos por indígenas. Estos indígenas\nreciben a la tripulación de Juan como dioses y, siendo Juan el capitán, se vuelve el gobernador de la isla.\nFIN DE LA HISTORIA DE JUAN SÁNCHEZ."
    imagen4 = "https://i.ibb.co/SK4p0xk/Imagen-Espa-oles-Dioses.jpg"
    cargar_imagen(imagen4)
    opciones = []
    cargar_imagen(url_imagen) if url_imagen else None
    mostrar_historia(nueva_historia, opciones)

def Ataca_fin1(url_imagen=None):
    nueva_historia = "El bando de Juan logra vencer, pero él se encuentra malherido y gran parte de sus hombres han muerto en el conflicto. No tiene más opción que buscar ayuda en las islas vecinas. Sin embargo, las tribus indígenas, conociendo que los españoles atacaron a la comunidad anterior, los matan. Juan Sánchez es asesinado en una isla.\n\nFIN DE LA HISTORIA DE JUAN SÁNCHEZ"
    imagen3 = "https://i.ibb.co/0hTshTC/Imagen-Lo-Matan.jpg"
    cargar_imagen(imagen3)
    opciones = []
    cargar_imagen(url_imagen) if url_imagen else None
    mostrar_historia(nueva_historia, opciones)

def Conversa_fin2(url_imagen=None):
    nueva_historia = "Juan no logra entenderse con los indígenas, pero, por fortuna, uno de sus hombres ha participado de\notras expediciones y conoce la lengua de los indios, con quienes logra entablar conversación. Para su buena suerte,\nlos indígenas conocen la ruta hacia la Fuente de la Juventud y los guían hasta ella.\n\n¡JUAN SÁNCHEZ LOGRA ENCONTRAR LA FUENTE DE LA JUVENTUD Y RECUPERARÁ SU JUVENTUD PERDIDA!"
    imagen4 = "https://i.ibb.co/bBvLmMQ/Imagen-Encuentra-Fuente.jpg"
    cargar_imagen(imagen4)   
    opciones = []
    mostrar_historia(nueva_historia, opciones)
    

# Crear la ventana principal
root = tk.Tk()
root.title("Historia Interactiva")
root.geometry("800x600")

# Crear widgets
label_imagen = tk.Label(root)
label_imagen.pack()

texto = tk.Text(root, wrap="word", width=80, height=10, font=("Arial", 14), padx=10, pady=10)
texto.pack()

botones_opciones = []

# Iniciar la historia
iniciar_historia()

# Bucle principal de la interfaz gráfica
root.mainloop()

