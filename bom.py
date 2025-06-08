import os
import pyautogui
import openai
import requests
import pyttsx3
from time import sleep
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from funcao_buscar_imagens import clica_na_imagem

# === Carrega variáveis de ambiente ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMAIL_DPE = os.getenv("EMAIL_DPE")
SENHA_EMAIL = os.getenv("SENHA_EMAIL")
USUARIO_SEI = os.getenv("USUARIO_SEI")
SENHA_SEI = os.getenv("SENHA_SEI")
USUARIO_TJAL = os.getenv("USUARIO_TJAL")
SENHA_TJAL = os.getenv("SENHA_TJAL")
USUARIO_SOLAR = os.getenv("USUARIO_SOLAR")
SENHA_SOLAR = os.getenv("SENHA_SOLAR")

IMGS = r"C:\Users\luang\psicologo\setup_descktop\imgs"

# === Automação de acesso ===
clica_na_imagem("1_icone_chrome", pasta=IMGS)
sleep(1)
clica_na_imagem("2_perfil_luan_gama", pasta=IMGS)
sleep(1)

# === Acessar Diario Oficial da DPE/AL ===
pyautogui.hotkey("ctrl", "t")
pyautogui.hotkey("ctrl", "l")
pyautogui.write("https://defensoria.al.def.br/diario-oficial", interval=0.10)
sleep(1)
pyautogui.press("space")
pyautogui.press("enter")
sleep(4)
pyautogui.press("tab", presses=19, interval=0.1)
pyautogui.press("enter")
sleep(7)
clica_na_imagem("baixar_doi", pasta=IMGS)
sleep(1)
pyautogui.press("enter")
sleep(2)
