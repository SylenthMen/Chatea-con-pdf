import streamlit as st
import fitz  # PyMuPDF
import openai
import os

# Configura tu clave API de OpenAI aquí
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

# Título de la aplicación
st.title('Chatea con tu PDF')
st.subheader('Haz preguntas sobre el contenido de tu archivo PDF.')

# Carga de archivos PDF
uploaded_file = st.file_uploader("Carga tu archivo PDF aquí", type=['pdf'])
if uploaded_file is not None:
    # Asegura que el directorio 'temp' exista
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Guarda el archivo PDF temporalmente
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extrae el texto del PDF
    texto_contexto = extraer_texto_de_pdf(temp_file_path)
    # Asegura que el texto no exceda el límite de tokens
    texto_contexto_limitado = texto_contexto[:4000]  # Ajusta según necesidad

    # Campo para ingresar la pregunta
    pregunta = st.text_input('Ingresa tu pregunta sobre el contenido del PDF:')
    
    if st.button('Enviar Pregunta'):
        if pregunta:
            # Genera y muestra la respuesta
            respuesta = hacer_pregunta_a_gpt(texto_contexto_limitado, pregunta)
            st.text_area("Respuesta:", value=respuesta, height=150)
        else:
            st.warning('Por favor, ingresa una pregunta.')

# Instrucciones al no cargar un archivo
else:
    st.write("Por favor, carga un archivo PDF para continuar.")
