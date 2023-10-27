import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import Button, filedialog, Text

def selecionar_arquivo():
    global caminho_arquivo_excel, arquivo_selecionado
    caminho_arquivo_excel = filedialog.askopenfilename()
    arquivo_selecionado.set(caminho_arquivo_excel)
    selecionar_arquivo_button.config(bg="green")

def buscar_ceps():
    if not caminho_arquivo_excel:
        print("Selecione um arquivo Excel primeiro.")
        return

    driver = webdriver.Chrome()
    driver.get("https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm")

    df = pd.read_excel(caminho_arquivo_excel)

    for index, row in df.iterrows():
        uf = row["UF"]
        localidade = row["Localidade"]

        driver.execute_script("document.getElementsByName('UF')[0].value = arguments[0];", uf)
        driver.execute_script("document.getElementsByName('Localidade')[0].value = arguments[0];", localidade)

        buscar_button = driver.find_element(By.XPATH, "//input[@value='Buscar']")
        buscar_button.click()
        time.sleep(2)

        # Agora, você deve pegar o elemento correto que contém o intervalo de CEPs
        cep_element = driver.find_element(By.XPATH, "//table[@class='tmptabela']//tr[3]/td[2]")
        cep = cep_element.text
        resultado_text.insert('end', f"UF: {uf}, Localidade: {localidade}, CEP: {cep}\n")

        # Voltar para a página de busca
        driver.get("https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm")

    driver.quit()

root = tk.Tk()
root.title("Buscar CEPs v.Beta - By Daniel Cabral")

selecionar_arquivo_button = Button(root, text="Selecionar Arquivo Excel", command=selecionar_arquivo, bg="red")
selecionar_arquivo_button.pack()

arquivo_selecionado = tk.StringVar()
arquivo_selecionado_label = tk.Label(root, textvariable=arquivo_selecionado, fg="green")
arquivo_selecionado_label.pack()

buscar_ceps_button = Button(root, text="Buscar CEPs", command=buscar_ceps, bg="green")
buscar_ceps_button.pack()

resultado_text = Text(root)
resultado_text.pack()

caminho_arquivo_excel = ""

root.mainloop()