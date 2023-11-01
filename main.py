from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print('------------------------------------------------')
print('-----------Teste inicial com Selenium-----------')
print('---------------------------by Daniel Cabral-----')
print('------------------------------------------------')
print('')
# Pergunte ao usuário pelo texto de pesquisa
search_text = input("Digite o texto de pesquisa: ")

# Crie uma instância do navegador Chrome
driver = webdriver.Chrome()

# Abra o Google
driver.get("https://www.google.com")

try:
    # Aguarde até que o campo de pesquisa seja visível e interagível
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )
    
    # Insira o texto no campo de pesquisa
    search_box.send_keys(search_text)
    
    # Envie a pesquisa pressionando Enter
    search_box.send_keys(Keys.RETURN)
    
    # Espere por um tempo (você pode ajustar esse valor)
    driver.implicitly_wait(10)
finally:
    # Feche o navegador
    driver.quit()