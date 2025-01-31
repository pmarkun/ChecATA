import streamlit as st
import fitz  # PyMuPDF
import openai
from openai import OpenAI


# Cliente OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def extrair_texto_pdf(file_buffer):
    with fitz.open(stream=file_buffer, filetype="pdf") as doc:
        texto = ""
        for page in doc:
            texto += page.get_text()
    return texto

def carregar_checklist():
    with open("checklist.md", "r", encoding='utf-8') as file:
        checklist = file.read()
    return checklist

def analisar_texto_com_gpt4(texto, prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": texto,
            }
        ],
        model="gpt-4o",
    )
    
    return chat_completion.choices[0].message.content

st.title('Verificador de Ata de Conferência')

checklist = carregar_checklist()
st.sidebar.markdown("## Checklist")
st.sidebar.markdown(checklist)

suploaded_file = st.file_uploader("Escolha um arquivo PDF", type='pdf')
if uploaded_file:
    texto_pdf = extrair_texto_pdf(uploaded_file.getvalue())
    st.text_area("Texto extraído do PDF", texto_pdf, height=300)

    
    
    if st.button("Verificar Documento"):
        with st.spinner('Analisando documento...'):
            resposta = analisar_texto_com_gpt4(texto_pdf, checklist)
            st.text_area("Resposta da OpenAI", resposta, height=300)
        st.success("Análise concluída!")
