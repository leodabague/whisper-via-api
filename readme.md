# 🎥 Transcritor de Áudio/Vídeo com OpenAI Whisper

Transcreva arquivos de áudio e vídeo (MP4, WAV, OGG) de forma simples e rápida usando a API da OpenAI (Whisper) em uma interface intuitiva feita com Streamlit.

---

## ✨ Funcionalidades

- Upload de arquivos MP4, WAV ou OGG (até 25MB)
- Transcrição automática via OpenAI Whisper
- Download da transcrição em TXT ou VTT (legendas)
- Preview do texto transcrito
- Interface web simples e responsiva

---
## ⚙️ Como Usar Usando Streamlit Cloud
1. **Entrar no site**
https://transcricao-api.streamlit.app/

2. **Colocar a OpenAI API KEY**

3. **Subir o arquivo**

4. **Baixar a transcrição**

## ⚙️ Como Usar Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/leodabague/whisper-via-api.git
   cd whisper-via-api
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Obtenha sua API Key da OpenAI:**
   - Acesse [OpenAI Platform](https://platform.openai.com/)
   - Crie uma conta e gere uma chave em "API Keys"

4. **Execute o app:**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador:**  
   O Streamlit abrirá automaticamente, ou acesse [http://localhost:8501](http://localhost:8501)

---

## 📋 Formatos Suportados

- **Entrada:** MP4, WAV, OGG
- **Saída:** TXT, VTT

---

## 🔒 Segurança

Sua chave da API é usada apenas localmente e não é armazenada.

---

## 🤖 Powered by OpenAI Whisper  
📝 Desenvolvido por [Leo Dabague](https://github.com/leodabague)

---

> Dúvidas ou sugestões? Abra uma issue ou contribua!
