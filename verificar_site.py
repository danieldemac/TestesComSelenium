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
        print_message("-URL inválida. Certifique-se de que a URL começa com 'http://' ou 'https://'.")
        print_message('x-----------------END-----------------x')
        return

    print_message("-Iniciando testes...")

    # Configurar o navegador Chrome
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)  # Espera implícita de até 10 segundos

    try:
        # Teste 1: Verificar se a página está acessível (status HTTP 200)
        print_message("-Iniciando Teste 1: Verificando acessibilidade da página...")
        response = requests.head(url)
        if response.status_code != 200:
            print_message(f"-Erro no Teste 1: A página não está acessível (HTTP status code {response.status_code}).")
            return
        print_message(f"-Teste 1: A página está acessível. {response.status_code}OK")
       
        

        # Teste 2: Verificar a funcionalidade de links (se a caixa de seleção estiver marcada)
        if test_links.get() == 1:
            print_message("-Iniciando Teste 2: Verificando funcionalidade de links...")
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
                        print_message(f"-Erro no Teste 2: O link '{link_info['text']}' redireciona para '{link_url}' em vez de '{link_info['url']}'.")
                        return
                    print_message(f"-Teste 2: Link '{link_info['text']}' redireciona corretamente.")
                except NoSuchElementException:
                    print_message(f"-Teste 2: Link '{link_info['text']}' não encontrado na página.")

        # Teste 4: Outros testes específicos, como preencher um formulário, clicar em botões, etc.

    except AssertionError as e:
        print_message(e)
    except TimeoutException:
        print_message("-Erro: Tempo limite excedido ao carregar a página.")
    except requests.exceptions.RequestException as e:
        print_message("-Erro: Não foi possível acessar a página. Verifique a URL e sua conexão com a internet.")
    finally:
        driver.quit()

        print_message("-Testes concluídos.")
        print_message('x-----------------END-----------------x')

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

    # Aumentar o tamanho da janela apenas verticalmente
    window.update_idletasks()
    new_height = window.winfo_reqheight() + 50
    new_width = window.winfo_reqwidth()
    window.geometry(f"{new_width}x{new_height}")

# Função para remover um campo de entrada de link
def remove_link_entry():
    if link_entries:
        text_entry = link_entries.pop()
        url_entry = url_entries.pop()
        text_entry.destroy()
        url_entry.destroy()
        # Diminuir o tamanho da janela apenas verticalmente
        window.update_idletasks()
        new_height = window.winfo_reqheight() - 50
        new_width = window.winfo_reqwidth()
        window.geometry(f"{new_width}x{new_height}")


# Configurar a janela
window = tk.Tk()
window.title("Teste de Viabilidade de Site v.Beta - by Daniel Cabral")

# Configuração do estilo da janela
window.geometry("500x600")  

# Adicionar campo de entrada para a URL
url_label = tk.Label(window, text="URL do Site:", font=("Arial", 12))
url_label.pack(pady=10)  # Espaçamento entre elementos

url_entry = tk.Entry(window, width=40)
url_entry.pack(padx=20, pady=5)  # Espaçamento nas laterais e superior

# Adicionar caixa de seleção para testar links
test_links = tk.IntVar()
test_links_check = Checkbutton(window, text="Testar Links", variable=test_links, font=("Arial", 12))
test_links_check.pack(pady=10)

# Adicionar botão para adicionar link (verde)
add_link_button = tk.Button(window, text="Adicionar Link", command=add_link_entry, bg="green", fg="white")
add_link_button.pack(pady=5)

# Adicionar botão para remover link (vermelho)
remove_link_button = tk.Button(window, text="Remover Link", command=remove_link_entry, bg="red", fg="white")
remove_link_button.pack(pady=5)

# Adicionar botão para executar os testes
test_button = tk.Button(window, text="Executar Testes", command=lambda: threading.Thread(target=run_tests).start(), font=("Arial", 14), bg="green", fg="white")
test_button.pack(pady=20)

# Adicionar widget de texto para exibir o resultado
result_text = scrolledtext.ScrolledText(window, state='disabled', wrap=tk.WORD, height=20, width=50, font=("Courier", 12), bg="black", fg="green")
result_text.pack(padx=20, pady=10)  # Espaçamento nas laterais e superior

# Configurar a tag para o estilo desejado
result_text.tag_config("matrix", foreground="green")

# Função para imprimir mensagens na janela com a tag "matrix"
def print_message(message):
    result_text.configure(state='normal')
    result_text.insert(tk.END, message + "\n", "matrix")
    result_text.see(tk.END)
    result_text.configure(state='disabled')

# Lista para armazenar os campos de entrada de links
link_entries = []
url_entries = []

# Iniciar a janela
window.mainloop()