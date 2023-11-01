from fpdf import FPDF
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
    imprimir_resultados_button.config(bg="red")

resultados = []  # Variável global para armazenar os resultados

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
        resultados.append(f"UF: {uf}, Localidade: {localidade}, CEP: {cep}")
        resultados.append("--------------------------")

        resultado_text.insert('end', f"UF: {uf}, Localidade: {localidade}, CEP: {cep}\n")
        resultado_text.insert('end', "--------------------------\n")

        # Voltar para a página de busca
        driver.get("https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCEP.cfm")

    driver.quit()
    imprimir_resultados_button.config(bg="blue")

def imprimir_resultados():
    if resultados:
        nome_arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if nome_arquivo:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            for resultado in resultados:
                pdf.multi_cell(0, 10, resultado)
                pdf.ln(10)

            pdf.output(nome_arquivo)

root = tk.Tk()
root.title("Buscar CEPs v.Beta - By Daniel Cabral")

selecionar_arquivo_button = Button(root, text="Selecionar Arquivo Excel", command=selecionar_arquivo, bg="red")
selecionar_arquivo_button.grid(row=0, column=0)

arquivo_selecionado = tk.StringVar()
arquivo_selecionado_label = tk.Label(root, textvariable=arquivo_selecionado, fg="green")
arquivo_selecionado_label.grid(row=0, column=1)

buscar_ceps_button = Button(root, text="Buscar CEPs", command=buscar_ceps, bg="green")
buscar_ceps_button.grid(row=0, column=2)

imprimir_resultados_button = Button(root, text="Imprimir Resultados", command=imprimir_resultados, bg="red")
imprimir_resultados_button.grid(row=0, column=3)

resultado_text = Text(root)
resultado_text.grid(row=1, columnspan=4)

caminho_arquivo_excel = ""

root.mainloop()