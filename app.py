import streamlit as st
import tempfile
import os
from openai import OpenAI
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Transcritor",
    page_icon="🎥"
)

st.title("🎥 Transcritor via API (openAI)")
st.markdown("---")

# Função para converter transcrição em formato VTT
def create_vtt_content(transcription_text):
    """Cria conteúdo VTT básico a partir do texto da transcrição"""
    vtt_content = "WEBVTT\n\n"
    vtt_content += "00:00:00.000 --> 99:59:59.999\n"
    vtt_content += transcription_text
    return vtt_content

# Função para fazer a transcrição
def transcribe_audio(api_key, audio_file):
    """Realiza a transcrição usando a API da OpenAI"""
    try:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("Transcrevendo áudio... Isso pode levar alguns minutos."):
            transcription = client.audio.transcriptions.create(
                model="whisper-1",  # Modelo correto para transcrição
                file=audio_file,
                response_format="text"
            )
        
        return transcription, None
    except Exception as e:
        return None, str(e)


st.subheader("⚙️ Configurações")

# Input para chave da API
api_key = st.text_input(
    "Chave da API OpenAI:",
    type="password",
    help="Digite sua chave da API da OpenAI"
)

# Upload do arquivo
uploaded_file = st.file_uploader(
    "Selecione um arquivo p/ transcrição:",
    type=['mp4', 'wav', 'ogg', 'm4a', 'webm'],
    help="Extensões suportadas: (.mp4, .wav, .ogg, .m4a, .webm). Tamanho máximo 25MB por arquivo."
)

st.divider()

st.subheader("📋 Como usar:")
st.info("""
1. Insira sua chave da API da OpenAI
2. Faça upload de um arquivo .mp4 .wav .ogg .m4a .webm
3. Clique em "Transcrever"
4. Baixe os arquivos de transcrição (TXT, VTT)
""")

# Área principal de processamento
if uploaded_file is not None and api_key:
    st.markdown("---")
    st.subheader("🎬 Arquivo Carregado")
    
    # Mostrar informações do arquivo
    file_details = {
        "Nome": uploaded_file.name,
        "Tamanho": f"{uploaded_file.size / (1024*1024):.2f} MB",
        "Tipo": uploaded_file.type
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nome do Arquivo", file_details["Nome"])
    with col2:
        st.metric("Tamanho", file_details["Tamanho"])
    with col3:
        st.metric("Tipo", file_details["Tipo"])
    
    # Botão para iniciar transcrição
    if st.button("🚀 Iniciar Transcrição", type="primary"):
        # Salvar arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            # Abrir arquivo para transcrição
            with open(tmp_file_path, "rb") as audio_file:
                transcription_text, error = transcribe_audio(api_key, audio_file)
            
            if error:
                st.error(f"Erro na transcrição: {error}")
            else:
                st.success("✅ Transcrição concluída com sucesso!")
                
                # Armazenar transcrição na sessão
                st.session_state.transcription = transcription_text
                st.session_state.filename = uploaded_file.name
                
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {str(e)}")
        finally:
            # Limpar arquivo temporário
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

# Mostrar resultados se existirem
if hasattr(st.session_state, 'transcription') and st.session_state.transcription:
    st.markdown("---")
    st.subheader("📝 Resultado da Transcrição")
    
    # Mostrar amostra do texto
    transcription_text = st.session_state.transcription
    filename = st.session_state.filename
    
    # Exibir preview do texto
    st.text_area(
        "Preview da Transcrição:",
        value=transcription_text[:500] + "..." if len(transcription_text) > 500 else transcription_text,
        height=150,
        disabled=True
    )
    
    st.info(f"📊 Total de caracteres: {len(transcription_text)}")
    
    # Botões de download
    st.markdown("### 💾 Downloads")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Botão para download do arquivo TXT
        txt_filename = f"{os.path.splitext(filename)[0]}_transcricao.txt"
        st.download_button(
            label="📄 Baixar como TXT",
            data=transcription_text,
            file_name=txt_filename,
            mime="text/plain",
            type="secondary"
        )
    
    with col2:
        # Botão para download do arquivo VTT
        vtt_content = create_vtt_content(transcription_text)
        vtt_filename = f"{os.path.splitext(filename)[0]}_legendas.vtt"
        st.download_button(
            label="🎬 Baixar como VTT",
            data=vtt_content,
            file_name=vtt_filename,
            mime="text/vtt",
            type="secondary"
        )

# Rodapé com informações
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🔒 Sua chave da API é mantida segura e não é armazenada.</p>
    <p>🤖 Powered by OpenAI Whisper | 📝 Leo Dabague</p>
</div>
""", unsafe_allow_html=True)

# Sidebar com informações adicionais
with st.sidebar:
    st.header("ℹ️ Informações")
    
    st.markdown("""
    ### 🎯 Sobre a Ferramenta
    
    Esta ferramenta utiliza a API da OpenAI (Whisper) para transcrever arquivos de vídeo em formato MP4.
    
    ### 🔧 Recursos
    - ✅ Transcrição automática
    - ✅ Download em formato TXT
    - ✅ Download em formato VTT (legendas)
    - ✅ Preview da transcrição
    - ✅ Interface intuitiva
    
    ### 🚀 Como Obter sua API Key
    1. Acesse [OpenAI Platform](https://platform.openai.com/)
    2. Faça login ou crie uma conta
    3. Vá em "API Keys"
    4. Crie uma nova chave
    5. Copie e cole aqui
    
    ### 📋 Formatos Suportados
    - **Entrada**: MP4, WAV, OGG, M4A, WEBM
    - **Saída**: TXT, VTT
    """)
    
    st.markdown("---")
    st.markdown("**Construído por: Leo Dabague**")