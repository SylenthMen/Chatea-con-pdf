import fitz  # PyMuPDF
import openai
import re
import os

# Configura tu clave API de OpenAI aquí
openai.api_key = 'TU API KEY AQUI'

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
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"]
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

def chat_con_usuario(texto_contexto):
    print("🤖 Hola, soy tu asistente. Puedes preguntarme sobre el contenido del PDF.")
    while True:
        entrada_usuario = input("¿Qué te gustaría saber? (escribe 'salir' para terminar): ")
        if entrada_usuario.lower() == 'salir':
            break
        respuesta = hacer_pregunta_a_gpt(texto_contexto, entrada_usuario)
        print(f"Respuesta: {respuesta}")

directorio_actual = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta al archivo PDF usando la estructura de directorios
ruta_pdf = os.path.join(directorio_actual, "pdfs", "pdfprueba.pdf")

# Extraer el texto del PDF
texto_contexto = extraer_texto_de_pdf(ruta_pdf)

# Limitar el texto a un tamaño manejable por GPT (puedes ajustar esto según sea necesario)
texto_contexto_limitado = texto_contexto[:4000]  # Ajusta este valor según el límite de tokens de tu modelo

# Iniciar el chat
chat_con_usuario(texto_contexto_limitado)