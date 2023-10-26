import tkinter as tk
from tkinter import scrolledtext, Checkbutton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import threading

# Função para verificar a validade da URL
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

# Função para imprimir mensagens na janela
def print_message(message):
    result_text.configure(state='normal')
    result_text.insert(tk.END, message + "\n")
    result_text.see(tk.END)
    result_text.configure(state='disabled')

# Função para executar os testes em uma thread separada
def run_tests():
   # Obter a URL do campo de entrada
    url = url_entry.get()
    

    # Verificar se a URL é válida
    if not is_valid_url(url):
        print_message("URL inválida. Certifique-se de que a URL começa com 'http://' ou 'https://'.")
        return

    print_message("Iniciando testes...")

    # Configurar o navegador Chrome
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)  # Espera implícita de até 10 segundos

    try:
        # Teste 1: Verificar se a página está acessível (status HTTP 200)
        print_message("Iniciando Teste 1: Verificando acessibilidade da página...")
        response = requests.head(url)
        if response.status_code != 200:
            print_message(f"Erro no Teste 1: A página não está acessível (HTTP status code {response.status_code}).")
            return
        print_message("Teste 1: A página está acessível.")
       
        

        # Teste 2: Verificar a funcionalidade de links (se a caixa de seleção estiver marcada)
        if test_links.get() == 1:
            print_message("Iniciando Teste 2: Verificando funcionalidade de links...")
            links_to_check = []

            # Lê os links adicionados pelo usuário
            for i in range(len(link_entries)):
                text = link_entries[i].get()
                url = url_entries[i].get()
                links_to_check.append({"text": text, "url": url})

            for link_info in links_to_check:
                try:
                    link = driver.find_element(By.PARTIAL_LINK_TEXT, link_info["text"])
                    link_url = link.get_attribute("href")

                    if link_url != link_info["url"]:
                        print_message(f"Erro no Teste 2: O link '{link_info['text']}' redireciona para '{link_url}' em vez de '{link_info['url']}'.")
                        return
                    print_message(f"Teste 2: Link '{link_info['text']}' redireciona corretamente.")
                except NoSuchElementException:
                    print_message(f"Teste 2: Link '{link_info['text']}' não encontrado na página.")

        # Teste 4: Outros testes específicos, como preencher um formulário, clicar em botões, etc.

    except AssertionError as e:
        print_message(e)
    except TimeoutException:
        print_message("Erro: Tempo limite excedido ao carregar a página.")
    except requests.exceptions.RequestException as e:
        print_message("Erro: Não foi possível acessar a página. Verifique a URL e sua conexão com a internet.")
    finally:
        driver.quit()

        print_message("Testes concluídos.")

# Função para adicionar um campo de entrada de link
def add_link_entry():
    text_entry = tk.Entry(window, width=15)
    url_entry = tk.Entry(window, width=30)
    text_entry.insert(0, "Nome do Link")
    url_entry.insert(0, "URL do Link")
    text_entry.pack()
    url_entry.pack()
    link_entries.append(text_entry)
    url_entries.append(url_entry)


# Configurar a janela
window = tk.Tk()
window.title("Teste de Viabilidade de Site v.Beta - by Daniel Cabral ")

# Adicionar campo de entrada para a URL
url_label = tk.Label(window, text="URL do Site:")
url_label.pack()
url_entry = tk.Entry(window)
url_entry.pack()

# Adicionar caixa de seleção para testar links
test_links = tk.IntVar()
test_links_check = Checkbutton(window, text="Testar Links", variable=test_links)
test_links_check.pack()

# Adicionar botão para adicionar links
add_link_button = tk.Button(window, text="Adicionar Link", command=add_link_entry)
add_link_button.pack()

# Adicionar botão para executar os testes
test_button = tk.Button(window, text="Executar Testes", command=lambda: threading.Thread(target=run_tests).start())
test_button.pack()

# Adicionar widget de texto para exibir o resultado
result_text = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD, height=10, width=40)
result_text.pack()

# Lista para armazenar os campos de entrada de links
link_entries = []
url_entries = []

# Lista para armazenar as verificações de elementos
element_checks = []

# Lista para armazenar os campos de entrada de seletores
by_entries = []
value_entries = []

# Iniciar a janela
window.mainloop()