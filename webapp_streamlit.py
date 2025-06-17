import streamlit as st
import os
from dotenv import set_key
import subprocess
import zipfile
import re
from pathlib import Path
import shutil
import json

# Configurações da página
st.set_page_config(
    page_title="Configuração de Automação Genérica",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Constantes
SISTEMAS_POPULARES = [
    "GMail",
    "Spotify",
    "Google Agenda",
    "Sites de Notícias",
    "YouTube",
    "Webmail",
    "SEI",
    "TJ-AL (e-SAJ)",
    "SOLAR",
    "ChatGPT",
    "Diário Oficial"
]

ARQUIVOS_PACOTE = [
    "consulta.py",
    "bom_dia.py",
    "funcao_buscar_imagens.py",
    "voz_listener_consulta.py",
    "voz_listener.py",
    "requirements.txt",
    ".env"
]

# Funções auxiliares
def validar_url(url):
    """Valida se a URL está em um formato válido"""
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domínio
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))

def sanitizar_nome_arquivo(nome):
    """Remove caracteres inválidos do nome do arquivo"""
    return re.sub(r'[<>:"/\\|?*]', '', nome)

def criar_backup_env():
    """Cria um backup do arquivo .env antes de modificá-lo"""
    if os.path.exists(".env"):
        backup_path = ".env.backup"
        shutil.copy2(".env", backup_path)
        return backup_path
    return None

def restaurar_backup_env(backup_path):
    """Restaura o backup do arquivo .env em caso de erro"""
    if backup_path and os.path.exists(backup_path):
        shutil.copy2(backup_path, ".env")
        os.remove(backup_path)

def salvar_configuracoes(sistemas_selecionados, sistemas_custom, configs):
    """Salva as configurações no arquivo .env"""
    env_path = ".env"
    backup_path = criar_backup_env()
    
    try:
        # Salva sistemas populares
        for sistema in sistemas_selecionados:
            set_key(env_path, f"LOGIN_{sistema.upper().replace(' ', '_')}", configs.get(f"login_{sistema}", ""))
            set_key(env_path, f"SENHA_{sistema.upper().replace(' ', '_')}", configs.get(f"senha_{sistema}", ""))
        
        # Salva sistemas personalizados
        for idx, s in enumerate(sistemas_custom):
            set_key(env_path, f"URL_CUSTOM_{idx}", s['url'])
            set_key(env_path, f"LOGIN_CUSTOM_{idx}", configs.get(f"login_custom_{idx}", ""))
            set_key(env_path, f"SENHA_CUSTOM_{idx}", configs.get(f"senha_custom_{idx}", ""))
        
        # Remove backup se tudo deu certo
        if backup_path and os.path.exists(backup_path):
            os.remove(backup_path)
        return True
    except Exception as e:
        # Restaura backup em caso de erro
        restaurar_backup_env(backup_path)
        st.error(f"Erro ao salvar configurações: {e}")
        return False

def gerar_pacote_instalacao():
    """Gera o pacote de instalação em formato ZIP"""
    try:
        # Cria diretório temporário para o pacote
        temp_dir = Path("temp_package")
        temp_dir.mkdir(exist_ok=True)
        
        # Copia arquivos necessários
        for fname in ARQUIVOS_PACOTE:
            if os.path.exists(fname):
                shutil.copy2(fname, temp_dir / fname)
        
        # Copia imagens
        if os.path.exists("imagens"):
            shutil.copytree("imagens", temp_dir / "imagens", dirs_exist_ok=True)
        
        # Cria o ZIP
        with zipfile.ZipFile("automacao_personalizada.zip", "w") as z:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    z.write(file_path, arcname)
        
        # Limpa diretório temporário
        shutil.rmtree(temp_dir)
        return True
    except Exception as e:
        st.error(f"Erro ao gerar pacote: {e}")
        # Limpa em caso de erro
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        return False

def executar_automacao():
    """Executa o script de automação"""
    try:
        result = subprocess.run(
            ["python", "automacao_voz.py"],
            capture_output=True,
            text=True,
            timeout=600
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return None, "Tempo limite excedido ao executar automação"
    except Exception as e:
        return None, f"Erro ao executar automação: {e}"

def criar_estrutura_usuario(nome_usuario, email):
    """Cria a estrutura de pastas e arquivos para o usuário"""
    try:
        # Cria pasta do usuário
        pasta_usuario = Path(nome_usuario)
        pasta_usuario.mkdir(exist_ok=True)
        
        # Cria pasta imagens
        (pasta_usuario / "imagens").mkdir(exist_ok=True)
        
        # Cria arquivo de configuração do usuário
        config = {
            "nome": nome_usuario,
            "email": email,
            "data_criacao": str(Path.cwd())
        }
        with open(pasta_usuario / "config.json", "w") as f:
            json.dump(config, f, indent=4)
        
        return pasta_usuario
    except Exception as e:
        st.error(f"Erro ao criar estrutura: {e}")
        return None

def criar_arquivo_bom_dia(pasta_usuario, sistemas_selecionados, sistemas_custom):
    """Cria o arquivo bom_dia.py personalizado"""
    try:
        template = """import os
import pyautogui
import pyperclip
from dotenv import load_dotenv
from time import sleep
import webbrowser

# Carrega variáveis do .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def abrir_site(url, login=None, senha=None, delay=5):
    webbrowser.open(url)
    sleep(delay)  # Aguarda o site abrir
    if login:
        pyperclip.copy(login)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab')
        sleep(1)
    if senha:
        pyperclip.copy(senha)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        sleep(2)

# Sistemas configurados
sistemas = [
{0}
]

# Sistemas personalizados
sistemas_custom = [
{1}
]

def main():
    print("Iniciando automação...")
    
    # Abre sistemas populares
    for nome, url in sistemas:
        login = os.getenv(f"LOGIN_{{nome}}")
        senha = os.getenv(f"SENHA_{{nome}}")
        if login or senha:
            print(f"Abrindo {{nome}}...")
            abrir_site(url, login, senha)
    
    # Abre sistemas personalizados
    for nome, url in sistemas_custom:
        login = os.getenv(f"LOGIN_CUSTOM_{{nome}}")
        senha = os.getenv(f"SENHA_CUSTOM_{{nome}}")
        if login or senha:
            print(f"Abrindo {{nome}}...")
            abrir_site(url, login, senha)
    
    print("Automação concluída!")

if __name__ == "__main__":
    main()
"""
        
        # Prepara os sistemas selecionados
        sistemas_str = ",\n".join([f'    ("{s}", "{url}")' for s, url in [
            ("GMAIL", "https://mail.google.com"),
            ("SPOTIFY", "https://open.spotify.com"),
            ("GOOGLE_AGENDA", "https://calendar.google.com"),
            ("SITES_DE_NOTICIAS", "https://g1.globo.com"),
            ("YOUTUBE", "https://www.youtube.com"),
            ("WEBMAIL", "https://webmail.itec.al.gov.br"),
            ("SEI", "https://sei.al.gov.br/sip/login.php"),
            ("TJ_AL", "https://www2.tjal.jus.br/sajcas/login"),
            ("SOLAR", "https://solar.defensoria.al.def.br/atendimento/"),
            ("CHATGPT", "https://chat.openai.com"),
            ("DIARIO_OFICIAL", "https://defensoria.al.def.br/diario-oficial")
        ] if s.replace("_", " ").title() in sistemas_selecionados])
        
        # Prepara os sistemas personalizados
        custom_str = ",\n".join([f'    ("{s["nome"]}", "{s["url"]}")' for s in sistemas_custom])
        
        # Cria o arquivo
        with open(pasta_usuario / "bom_dia.py", "w") as f:
            f.write(template.format(sistemas_str, custom_str))
        
        return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo bom_dia.py: {e}")
        return False

def criar_arquivo_listener(pasta_usuario):
    """Cria o arquivo voz_listener.py"""
    try:
        template = """import speech_recognition as sr
import sys, subprocess, os
from time import sleep

TRIGGER = "bom dia"  # frase-chave

r = sr.Recognizer()
with sr.Microphone() as mic:
    r.adjust_for_ambient_noise(mic, duration=1)   # calibra ruído
    print("Listener iniciado — fone de ouvido ligado.")
    while True:
        print(f"Diga: {TRIGGER}")
        audio = r.listen(mic, phrase_time_limit=5)
        try:
            comando = r.recognize_google(audio, language='pt-BR').lower()
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print("Erro na API de voz:", e)
            continue

        if TRIGGER in comando:
            print("Comando reconhecido! Iniciando automação...")
            subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(__file__), 'bom_dia.py')],
                check=True
            )
            sleep(1)
"""
        
        with open(pasta_usuario / "voz_listener.py", "w") as f:
            f.write(template)
        
        return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo voz_listener.py: {e}")
        return False

def criar_arquivo_requirements(pasta_usuario):
    """Cria o arquivo requirements.txt"""
    try:
        requirements = """PyAutoGUI==0.9.54
python-dotenv==1.0.1
opencv-python==4.8.1.78
Pillow==10.1.0
openai>=1.14.3
requests>=2.31.0
pyttsx3>=2.90
beautifulsoup4>=4.12.3
PyPDF2>=3.0.1
SpeechRecognition>=3.10.1
numpy==1.26.4
screeninfo
mss
streamlit>=1.32.0

#⚠️ pyaudio deve ser instalado assim:
# pip install pipwin
# pipwin install pyaudio
"""
        with open(pasta_usuario / "requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        
        return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo requirements.txt: {e}")
        return False

def criar_arquivo_instrucoes(pasta_usuario):
    """Cria o arquivo de instruções"""
    try:
        instrucoes = """# Instruções de Instalação e Uso

1. Crie o ambiente virtual:
   ```
   py -3.11 -m venv .venv
   ```

2. Ative o ambiente virtual:
   ```
   .\.venv\Scripts\Activate.ps1
   ```

3. Atualize o pip:
   ```
   python.exe -m pip install --upgrade pip
   ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Instale o PyAudio:
   ```
   pip install pipwin
   pipwin install pyaudio
   ```

# Captura de Imagens

Para capturar as imagens necessárias para a automação:

1. Abra cada sistema que deseja automatizar
2. Use a ferramenta de captura de tela do Windows (Win + Shift + S)
3. Capture os elementos importantes como:
   - Campo de login
   - Campo de senha
   - Botão de login
   - Menus importantes
4. Salve as imagens na pasta 'imagens' com nomes descritivos como:
   - login_gmail.png
   - senha_gmail.png
   - botao_login_gmail.png
   - menu_principal_gmail.png

# Uso

1. Execute o listener de voz:
   ```
   python voz_listener.py
   ```

2. Diga "bom dia" para iniciar a automação

3. O sistema irá:
   - Abrir os sites configurados
   - Preencher login e senha
   - Navegar pelos menus
   - Executar as ações programadas

# Observações

- Mantenha o microfone ligado
- Fale claramente o comando "bom dia"
- As imagens devem ser capturadas na mesma resolução de tela
- Não mova as janelas durante a automação
"""
        with open(pasta_usuario / "INSTRUCOES.txt", "w", encoding="utf-8") as f:
            f.write(instrucoes)
        
        return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo de instruções: {e}")
        return False

def criar_arquivo_bat(pasta_usuario):
    """Cria o arquivo install.bat para instalação automática"""
    try:
        conteudo = r"""@echo off
cd %~dp0
py -3.11 -m venv .venv
call .\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pipwin
pipwin install pyaudio
echo Instalação concluída! Leia o arquivo INSTRUCOES.txt para o próximo passo.
pause
"""
        with open(pasta_usuario / "install.bat", "w", encoding="utf-8") as f:
            f.write(conteudo)
        return True
    except Exception as e:
        st.error(f"Erro ao criar arquivo install.bat: {e}")
        return False

# Interface principal
st.title("🤖 Seu Assistente de Automação")

# Inicializa o dicionário de configurações
configs = {}

# Seção 1: Informações do usuário
st.header("1. Informações do Usuário")

col1, col2 = st.columns(2)
with col1:
    nome_usuario = st.text_input(
        "Nome do usuário",
        help="Seu nome ou identificador",
        max_chars=50
    )
with col2:
    email_usuario = st.text_input(
        "E-mail",
        help="Seu e-mail para contato",
        max_chars=100
    )

if not nome_usuario or not email_usuario:
    st.warning("Por favor, preencha seu nome e e-mail para continuar.")
    st.stop()

# Cria estrutura do usuário
pasta_usuario = criar_estrutura_usuario(nome_usuario, email_usuario)
if not pasta_usuario:
    st.error("Erro ao criar estrutura do usuário. Tente novamente.")
    st.stop()

# Seção 2: Seleção de sistemas
st.header("2. Escolha as automações que deseja executar")

sistemas_selecionados = st.multiselect(
    "Selecione os sistemas/programas a automatizar:",
    SISTEMAS_POPULARES,
    help="Escolha um ou mais sistemas para automatizar"
)

# Seção 3: Sistemas personalizados
st.subheader("Adicionar outro sistema personalizado")
with st.expander("➕ Adicionar novo sistema/site personalizado"):
    col1, col2 = st.columns(2)
    with col1:
        nome_custom = st.text_input(
            "Nome do sistema/site",
            help="Ex: Sistema Interno",
            max_chars=50
        )
        url_custom = st.text_input(
            "URL do sistema/site",
            help="Ex: https://sistema.exemplo.com"
        )
    with col2:
        login_custom = st.text_input(
            "Login (opcional)",
            help="Se o sistema requer login",
            max_chars=100
        )
        senha_custom = st.text_input(
            "Senha (opcional)",
            type="password",
            help="Se o sistema requer senha",
            max_chars=100
        )
    
    add_custom = st.button("Adicionar sistema personalizado")
    if add_custom:
        if not nome_custom or not url_custom:
            st.error("Nome e URL são obrigatórios!")
        elif not validar_url(url_custom):
            st.error("URL inválida! Use um formato como https://exemplo.com")
        else:
            nome_sanitizado = sanitizar_nome_arquivo(nome_custom)
            if nome_sanitizado != nome_custom:
                st.warning(f"Nome sanitizado para: {nome_sanitizado}")
                nome_custom = nome_sanitizado
            
            if "sistemas_custom" not in st.session_state:
                st.session_state["sistemas_custom"] = []
            st.session_state["sistemas_custom"].append({
                "nome": nome_custom,
                "url": url_custom,
                "login": login_custom,
                "senha": senha_custom
            })
            st.success(f"Sistema '{nome_custom}' adicionado!")

# Exibe sistemas personalizados
sistemas_custom = st.session_state.get("sistemas_custom", [])
if sistemas_custom:
    st.markdown("**Sistemas personalizados adicionados:**")
    for idx, s in enumerate(sistemas_custom):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"- {s['nome']} ({s['url']})")
        with col2:
            if st.button("🗑️", key=f"del_{idx}"):
                sistemas_custom.pop(idx)
                st.session_state["sistemas_custom"] = sistemas_custom
                st.rerun()

st.markdown("---")

# Seção 4: Configurações de Automação para cada sistema
st.header("3. Configuração detalhada de cada automação")

if not sistemas_selecionados and not sistemas_custom:
    st.warning("Selecione pelo menos um sistema para configurar as automações.")
    st.stop()

# Para sistemas populares
for sistema in sistemas_selecionados:
    with st.expander(f"⚙️ {sistema}"):
        tipo_automacao = st.radio(
            f"Como deseja automatizar o {sistema}?",
            ["URL, login e senha", "Clique em imagem(s)"],
            key=f"tipo_{sistema}"
        )
        if tipo_automacao == "URL, login e senha":
            col1, col2 = st.columns(2)
            with col1:
                configs[f"login_{sistema}"] = st.text_input(
                    f"Login",
                    key=f"login_{sistema}",
                    help=f"Login para acessar {sistema}"
                )
            with col2:
                configs[f"senha_{sistema}"] = st.text_input(
                    f"Senha",
                    type="password",
                    key=f"senha_{sistema}",
                    help=f"Senha para acessar {sistema}"
                )
            configs[f"tipo_{sistema}"] = "url"
        else:
            imagens = st.file_uploader(
                f"Faça upload das imagens para o {sistema}",
                type=["png"],
                accept_multiple_files=True,
                key=f"img_{sistema}"
            )
            acoes = []
            if imagens:
                for idx, img in enumerate(imagens):
                    nome_img = sanitizar_nome_arquivo(img.name)
                    st.image(img, caption=nome_img, width=150)
                    acao = st.text_area(
                        f"O que o assistente deve fazer após clicar em '{nome_img}'?",
                        key=f"acao_{sistema}_{idx}"
                    )
                    # Salva imagem na pasta do usuário
                    img_path = pasta_usuario / "imagens" / nome_img
                    with open(img_path, "wb") as f:
                        f.write(img.getbuffer())
                    acoes.append({"imagem": nome_img, "acao": acao})
            configs[f"imagens_{sistema}"] = acoes
            configs[f"tipo_{sistema}"] = "imagem"

# Para sistemas personalizados
for idx, s in enumerate(sistemas_custom):
    with st.expander(f"⚙️ {s['nome']} (Personalizado)"):
        tipo_automacao = st.radio(
            f"Como deseja automatizar o {s['nome']}?",
            ["URL, login e senha", "Clique em imagem(s)"],
            key=f"tipo_custom_{idx}"
        )
        if tipo_automacao == "URL, login e senha":
            col1, col2 = st.columns(2)
            with col1:
                configs[f"login_custom_{idx}"] = st.text_input(
                    f"Login",
                    value=s['login'],
                    key=f"login_custom_{idx}",
                    help=f"Login para acessar {s['nome']}"
                )
            with col2:
                configs[f"senha_custom_{idx}"] = st.text_input(
                    f"Senha",
                    value=s['senha'],
                    type="password",
                    key=f"senha_custom_{idx}",
                    help=f"Senha para acessar {s['nome']}"
                )
            configs[f"tipo_custom_{idx}"] = "url"
        else:
            imagens = st.file_uploader(
                f"Faça upload das imagens para o {s['nome']}",
                type=["png"],
                accept_multiple_files=True,
                key=f"img_custom_{idx}"
            )
            acoes = []
            if imagens:
                for jdx, img in enumerate(imagens):
                    nome_img = sanitizar_nome_arquivo(img.name)
                    st.image(img, caption=nome_img, width=150)
                    acao = st.text_area(
                        f"O que o assistente deve fazer após clicar em '{nome_img}'?",
                        key=f"acao_custom_{idx}_{jdx}"
                    )
                    # Salva imagem na pasta do usuário
                    img_path = pasta_usuario / "imagens" / nome_img
                    with open(img_path, "wb") as f:
                        f.write(img.getbuffer())
                    acoes.append({"imagem": nome_img, "acao": acao})
            configs[f"imagens_custom_{idx}"] = acoes
            configs[f"tipo_custom_{idx}"] = "imagem"

st.markdown("---")

# Seção 5: Upload de imagens
st.header("4. Upload de imagens de referência (opcional)")
st.info("Faça upload de imagens .png que serão usadas como referência para a automação.")

uploaded_files = st.file_uploader(
    "Arraste ou selecione imagens .png",
    type=["png"],
    accept_multiple_files=True,
    help="Selecione imagens capturadas no próprio computador para melhor compatibilidade"
)

if uploaded_files:
    os.makedirs("imagens", exist_ok=True)
    for file in uploaded_files:
        nome_sanitizado = sanitizar_nome_arquivo(file.name)
        if nome_sanitizado != file.name:
            st.warning(f"Nome do arquivo sanitizado: {nome_sanitizado}")
        
        with open(os.path.join("imagens", nome_sanitizado), "wb") as f:
            f.write(file.getbuffer())
    st.success(f"{len(uploaded_files)} imagem(ns) salva(s) na pasta 'imagens'.")

st.markdown("---")

# Seção 6: Gerar pacote de instalação
st.header("5. Gerar pacote de instalação")
st.info("Gere um pacote .zip com todas as configurações para instalar em outro computador.")

if st.button("📦 Gerar pacote de instalação (.zip)", use_container_width=True):
    with st.spinner("Gerando pacote..."):
        # Cria arquivos necessários
        if not criar_arquivo_bom_dia(pasta_usuario, sistemas_selecionados, sistemas_custom):
            st.error("Erro ao criar arquivo bom_dia.py")
            st.stop()
        
        if not criar_arquivo_listener(pasta_usuario):
            st.error("Erro ao criar arquivo voz_listener.py")
            st.stop()
        
        if not criar_arquivo_requirements(pasta_usuario):
            st.error("Erro ao criar arquivo requirements.txt")
            st.stop()
        
        if not criar_arquivo_instrucoes(pasta_usuario):
            st.error("Erro ao criar arquivo de instruções")
            st.stop()
        
        if not criar_arquivo_bat(pasta_usuario):
            st.error("Erro ao criar arquivo install.bat")
            st.stop()
        
        # Cria o ZIP
        try:
            with zipfile.ZipFile(f"{nome_usuario}_automacao.zip", "w") as z:
                for root, _, files in os.walk(pasta_usuario):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, pasta_usuario)
                        z.write(file_path, arcname)
            
            with open(f"{nome_usuario}_automacao.zip", "rb") as f:
                st.download_button(
                    "⬇️ Baixar pacote de instalação",
                    f,
                    file_name=f"{nome_usuario}_automacao.zip",
                    use_container_width=True
                )
            
            st.success("Pacote gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar pacote: {e}") 
