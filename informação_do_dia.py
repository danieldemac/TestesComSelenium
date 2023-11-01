from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import Text, Scrollbar
import re

# Função para remover espaços em branco extras e linhas em branco
def clean_text(text):
    words = text.split()
    cleaned_words = [word for word in words if word != '']
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text

# Lista de URLs de jornais
urls = [
    "https://www.diariodepernambuco.com.br/"
]

noticias = {}

try:
    # Configurar o navegador Chrome
    with webdriver.Chrome() as driver:
        for url in urls:
            driver.get(url)

            # Verificar se há elementos h1 na página
            h1_elements = driver.find_elements(By.TAG_NAME, "h1")
            h1_texts = [element.text for element in h1_elements] if h1_elements else []

            # Verificar se há elementos h3 na página
            h3_elements = driver.find_elements(By.TAG_NAME, "h3")
            h3_texts = [element.text for element in h3_elements] if h3_elements else []

            # Armazenar os textos em um dicionário usando a URL como chave
            noticias[url] = {
                "h1": h1_texts,
                "h3": h3_texts
            }
except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")

# Criar uma janela para exibir a mensagem
root = tk.Tk()
root.title("Notícias de Jornais")

# Criar uma caixa de texto rolável para exibir a mensagem
message_text = Text(root, wrap=tk.WORD, height=20, width=80)
message_text.pack()

# Adicionar uma barra lateral para rolar a caixa de texto
scrollbar = Scrollbar(root, command=message_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
message_text.config(yscrollcommand=scrollbar.set)

# Montar a mensagem
message = "Notícias de Vários Jornais:\n\n"
for url, elements in noticias.items():
    message += f"URL: {url}\n"
    if elements["h1"]:
        message += "Elementos h1:\n"
        for h1_text in elements["h1"]:
            message += f"{clean_text(h1_text)}\n"
    if elements["h3"]:
        message += "Elementos h3:\n"
        for h3_text in elements["h3"]:
            message += f"{clean_text(h3_text)}\n"
    
    # Adicione uma linha em branco somente se houver texto na seção atual
    if elements["h1"] or elements["h3"]:
        message += "\n"

# Exibir a mensagem na caixa de texto
message_text.insert(tk.END, message)

root.mainloop()