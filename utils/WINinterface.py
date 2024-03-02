import fitz  # PyMuPDF
import openai
import tkinter as tk
from tkinter import filedialog, Text, messagebox, scrolledtext
import os


openai.api_key = 'YOUR_API_KEY_HERE' #aqui va tu api de open ai

def extraer_texto_de_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()
    doc.close()
    return texto_completo

def hacer_pregunta_a_gpt(texto_contexto, pregunta):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  # Asegúrate de usar el modelo más reciente disponible
            prompt=f"{texto_contexto}\n\nPregunta: {pregunta}\nRespuesta:",
            temperature=0.5,
            max_tokens=150, #numero maximo de palabras en la respuesta (tokens)
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

def seleccionar_pdf():
    global ruta_pdf, texto_contexto, texto_contexto_limitado
    ruta_pdf = filedialog.askopenfilename(initialdir="/", title="Seleccionar archivo", filetypes=(("archivos pdf", "*.pdf"), ("todos los archivos", "*.*")))
    if ruta_pdf:
        etiqueta_archivo.config(text=f"Archivo Seleccionado: {os.path.basename(ruta_pdf)}")
        texto_contexto = extraer_texto_de_pdf(ruta_pdf)
        texto_contexto_limitado = texto_contexto[:4000]  # Ajusta este valor según el límite de tokens de tu modelo
    else:
        etiqueta_archivo.config(text="Archivo Seleccionado: Ninguno")

def enviar_pregunta():
    pregunta = campo_pregunta.get("1.0", "end-1c")
    if not ruta_pdf or pregunta.strip() == "":
        messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo PDF y escribe una pregunta.")
        return
    respuesta = hacer_pregunta_a_gpt(texto_contexto_limitado, pregunta)
    campo_respuesta.config(state=tk.NORMAL)
    campo_respuesta.delete("1.0", tk.END)
    campo_respuesta.insert(tk.END, respuesta)
    campo_respuesta.config(state=tk.DISABLED)

app = tk.Tk()
app.title("Chatbot PDF")

ruta_pdf = ""
texto_contexto = ""
texto_contexto_limitado = ""

# Configuración de la ventana
app.geometry("600x400")

# Botón para seleccionar el PDF
boton_seleccionar_pdf = tk.Button(app, text="Seleccionar PDF", padx=10, pady=5, fg="white", bg="#263D42", command=seleccionar_pdf)
boton_seleccionar_pdf.pack()

# Etiqueta para mostrar el archivo seleccionado
etiqueta_archivo = tk.Label(app, text="Archivo Seleccionado: Ninguno", bg="gray")
etiqueta_archivo.pack()

# Campo de texto para la pregunta
campo_pregunta = Text(app, height=2, width=50)
campo_pregunta.pack()

# Botón para enviar la pregunta
boton_enviar = tk.Button(app, text="Enviar Pregunta", command=enviar_pregunta)
boton_enviar.pack()

# Campo de texto para la respuesta, usando scrolledtext para facilitar la lectura de respuestas largas
campo_respuesta = scrolledtext.ScrolledText(app, state=tk.DISABLED, height=10, width=50)
campo_respuesta.pack()

app.mainloop()
