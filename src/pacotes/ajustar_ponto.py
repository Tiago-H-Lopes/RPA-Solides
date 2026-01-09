import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from datetime import date
from time import sleep

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')
cpf = os.getenv('CPF')
url = 'https://app.tangerino.com.br/Tangerino/?wicket:interface=:1:body:loginForm:baterPonto::ILinkListener::'

today = date.today()
today = date.strftime(today, '%d/%m/%Y')

#Por padrão irá atualizar o ponto do dia atual, se for um dia útil. Feriados não estão sendo analisados.
#Se quiser atualizar dias especificos basta adicionar na lista no formato dd/mm/yyyy. Ex: [02/12/2026, 03/12/2026, 02/11/2026, 03/11/2026]
lista_dias_ajustar = [today]
horarios_ponto = ['09:00', '12:00', '13:00', '18:00']

if not user or not password:
    raise ValueError('Credenciais não encontradas no arquivo .env')
if not cpf:
    raise ValueError('CPF não encontrado no arquivo .env')

#Adiciona ao Chrome opções para rodar no modo headless (em background), na aba icognito para evitar problemas com dados salvos
#E como boa prática define o tamanho da janela para garantir que todos os elementos estejam visiveis
options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_argument('--window-size=1920,1080')
driver = Chrome(options=options)
actions = ActionChains(driver)

driver.implicitly_wait(15)
driver.get(url)
sleep(2)

driver.find_elements(By.CSS_SELECTOR, 'a.login-aba')[1].click()
driver.find_element(By.NAME, 'codigoEmpregador').send_keys(user)
driver.find_element(By.NAME, 'pin').send_keys(password)
driver.find_element(By.NAME, 'btnLogin').click()
driver.find_element(By.CLASS_NAME, 'cpf').send_keys(cpf)
driver.find_element(By.CLASS_NAME, 'btnContinuar').click()
sleep(1)

driver.find_element(By.XPATH, "//a[@rel='Apropriação de horas']").click()
sleep(2)

driver.find_element(By.CSS_SELECTOR, 'a.icone.icon-menu-triple-line').click()
driver.find_element(By.CSS_SELECTOR, 'a.icone.icon-clock').click()
sleep(3)

justificativa = driver.find_element(By.XPATH, "//select[@name='justificativa']")
select = Select(justificativa)
select.select_by_value('1') #Esquecimento

for dia in lista_dias_ajustar:
    data = driver.find_element(By.NAME, 'dataPonto')
    data.clear()
    data.send_keys(dia)

    for horario in horarios_ponto:
        hora = driver.find_element(By.NAME, 'horaPonto')
        salvar = driver.find_element(By.XPATH, "//input[@value='Salvar e Continuar']")

        hora.clear()
        hora.send_keys(horario)

        salvar.click()
        sleep(1)

sleep(1)
driver.close()