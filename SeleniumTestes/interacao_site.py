from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time

print('------------------------------------------------')
print('-----------Implementação de valores-------------')
print('---------------------------by Daniel Cabral-----')
print('------------------------------------------------')
print('')

# Pergunte ao usuário pelo texto de pesquisa
search_text_nome = input("Digite o nome: ")
search_text_telefone = input("Digite o telefone: ")
search_text_email = input("Digite o Email: ")
search_text_motivo = input("Digite o Motivo -> 1-Dúvida | 2-Elogio | 3- Reclamação :")
search_text_mensagem = input("Digite a mensagem: ")

# Crie uma instância do navegador Chrome
driver = webdriver.Chrome()

# Abra o site
driver.get("http://localhost:8000/")

try:
    # Aguarde até que os campos de entrada sejam visíveis e interagíveis
    nome_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "nome"))
    )
    
    # Insira o texto nos campos de entrada
    nome_input.send_keys(search_text_nome)
    
    telefone_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "telefone"))
    )
    telefone_input.send_keys(search_text_telefone)
    
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "email"))
    )
    email_input.send_keys(search_text_email)

    motivo_select = Select(WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "motivo_contato"))
    ))
    motivo_select.select_by_value(search_text_motivo)

    mensagem_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "mensagem"))
    )
    
    # Selecionar todo o texto no campo de mensagem
    ActionChains(driver).move_to_element(mensagem_input).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    
    # Limpe o campo de mensagem
    mensagem_input.clear()

    # Insira o novo texto da mensagem
    mensagem_input.send_keys(search_text_mensagem)

    # Encontre e pressione o botão ENVIAR
    enviar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='ENVIAR']"))
    )
    enviar_button.click()
    
    # Aguarde 1 minuto
    time.sleep(60)
finally:
    # Feche o navegador
    driver.quit()