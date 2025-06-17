import os
import pyautogui
import pyperclip
from dotenv import load_dotenv
from time import sleep
import webbrowser
import speech_recognition as sr
import subprocess
import threading

# Carrega variáveis do .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def ouvir_comando():
    """Função para ouvir e reconhecer a fala"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando comando de voz...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Comando reconhecido: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio")
            return None
        except sr.RequestError as e:
            print(f"Erro ao fazer requisição ao Google Speech Recognition; {e}")
            return None

def executar_bom_dia():
    """Função para executar o script bom_dia.py"""
    try:
        caminho_bom_dia = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bom_dia.py')
        subprocess.run(['python', caminho_bom_dia])
    except Exception as e:
        print(f"Erro ao executar bom_dia.py: {e}")

def monitorar_comandos():
    """Função para monitorar comandos de voz continuamente"""
    while True:
        comando = ouvir_comando()
        if comando and "bom dia" in comando:
            print("Executando automação do bom dia...")
            executar_bom_dia()
        sleep(1)

# Inicia o monitoramento de comandos em uma thread separada
thread_comandos = threading.Thread(target=monitorar_comandos)
thread_comandos.daemon = True
thread_comandos.start()

# Função para abrir um site e preencher login/senha
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

# Exemplo para sistemas populares
sistemas = [
    ("GMAIL", "https://mail.google.com"),
    ("SPOTIFY", "https://open.spotify.com"),
    ("GOOGLE_AGENDA", "https://calendar.google.com"),
    ("SITES_DE_NOTICIAS", "https://g1.globo.com"),
    # Adicione outros sistemas populares aqui
]

for nome, url in sistemas:
    login = os.getenv(f"LOGIN_{nome}")
    senha = os.getenv(f"SENHA_{nome}")
    if login or senha:
        print(f"Abrindo {nome}...")
        abrir_site(url, login, senha)

# Para sistemas personalizados
idx = 0
while True:
    url = os.getenv(f"URL_CUSTOM_{idx}")
    login = os.getenv(f"LOGIN_CUSTOM_{idx}")
    senha = os.getenv(f"SENHA_CUSTOM_{idx}")
    if not url:
        break
    print(f"Abrindo sistema personalizado: {url}")
    abrir_site(url, login, senha)
    idx += 1

print("Automação concluída!") 
