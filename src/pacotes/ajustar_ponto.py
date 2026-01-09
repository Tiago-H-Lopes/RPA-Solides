import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from datetime import date
from time import sleep
from . import logger, validar_e_formatar_cpf

def ajustar_ponto(lista_dias_ajustar: list[str]=None, horarios_ponto: list[str]=None) -> None:
    """
    Função responsável por ajustar o ponto, se nenhum valor for informado, atualizará o ponto do dia \n
    Por padrão irá atualizar o ponto do dia atual, se for um dia entre segunda e sexta. Feriados não estão sendo analisados. \n
    Se quiser atualizar dias especificos basta adicionar na lista no formato dd/mm/yyyy. Ex: [02/12/2026, 03/12/2026, 02/11/2026, 03/11/2026] \n
    Por padrão atualizará com os horários 09:00, 12:00, 13:00 e 18:00 \n
    Se quiser atualizar horarios especificos basta adicionar na lista no formato HH:MM. Ex: ['09:00', '12:00', '13:00', '18:00']
        
    :param lista_dias_ajustar: Lista contendo todos os dias a serem atualizados, no formato dd/mm/yyyy. Por padrão atualizará o dia atual
    :type lista_dias_ajustar: list[str]
    :param horarios_ponto: Lista contendo todos os horarios a serem atualizados, no formato HH:MM. Por padrão atualizará com os horários 09:00, 12:00, 13:00 e 18:00
    :type horarios_ponto: list[str]
    """

    logger.info('Iniciando ajuste de ponto')
    logger.info('Iniciando leitura de credenciais')
    load_dotenv()
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    cpf = os.getenv('CPF')
    url = 'https://app.tangerino.com.br/Tangerino/pages/LoginPage'

    if not user or not password:
        error_msg = 'Credenciais não encontradas no arquivo .env'
        logger.error(error_msg)
        raise ValueError(error_msg)
    if not cpf:
        error_msg = 'CPF não encontrado no arquivo .env'
        raise ValueError(error_msg)
    
    logger.info('Iniciando validação do CPF')
    cpf = validar_e_formatar_cpf(cpf)
    
    if not lista_dias_ajustar:
        today = date.today()
        today = date.strftime(today, '%d/%m/%Y')
        lista_dias_ajustar = [today]
    
    if not horarios_ponto:
        horarios_ponto = ['09:00', '12:00', '13:00', '18:00']

    logger.info(f'Dias a serem ajustados: {lista_dias_ajustar}')
    logger.info(f'Todos os dias serão ajustados com os seguintes horários: {horarios_ponto}')

    #Adiciona ao Chrome opções para rodar no modo headless (em background), na aba icognito para evitar problemas com dados salvos
    #Como boa prática define o tamanho da janela para garantir que todos os elementos estejam visiveis
    #Define um timeout de 15 segundos para detectar os elementos
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    driver = Chrome(options=options)
    driver.implicitly_wait(15)

    logger.info(f'Abrindo google chrome na url: {url}')
    driver.get(url)
    sleep(2)

    #Tela de login
    #Realiza login no site, com código do empregador, pin e cpf
    logger.info('Realizando login no site')
    driver.find_elements(By.CSS_SELECTOR, 'a.login-aba')[1].click()
    driver.find_element(By.NAME, 'codigoEmpregador').send_keys(user)
    driver.find_element(By.NAME, 'pin').send_keys(password)
    driver.find_element(By.NAME, 'btnLogin').click()
    driver.find_element(By.CLASS_NAME, 'cpf').send_keys(cpf)
    driver.find_element(By.CLASS_NAME, 'btnContinuar').click()
    sleep(1)

    #Acessa a tela de Apropriação de horas
    logger.info('Acessando a tela de Apropriação de Horas')
    driver.find_element(By.XPATH, "//a[@rel='Apropriação de horas']").click()
    sleep(2)

    #Seleciona a opção de ajustar ponto, clicando nos 3 pontinhos e depois no icone de atualizar
    #Se o icone for alterado pode quebrar essa parte do código
    logger.info('Abrindo a janela para alteração de ponto')
    driver.find_element(By.CSS_SELECTOR, 'a.icone.icon-menu-triple-line').click()
    driver.find_element(By.CSS_SELECTOR, 'a.icone.icon-clock').click()
    sleep(3)

    #Seleciona a justificativa como esquecimento
    logger.info('Selecionando justificativa como: Esquecimento')
    justificativa = driver.find_element(By.XPATH, "//select[@name='justificativa']")
    select = Select(justificativa)
    select.select_by_value('1') #Esquecimento

    #Loop
    #Para cada dia, na lista de dias a serem ajustados ele ajustará o ponto com os horários informados
    logger.info('Iniciando loop de atualização')
    for dia in lista_dias_ajustar:
        logger.info(f'Atualizando o ponto do dia: {dia}')
        #Altera a data para o dia atual na lista
        data = driver.find_element(By.NAME, 'dataPonto')
        data.clear()
        data.send_keys(dia)

        #Loop
        #Loop responsável por inserir os horários do ponto e salvar as alterações
        for horario in horarios_ponto:
            logger.info(f'Atualizando o ponto do dia: {dia} com o horário {horario}')
            hora = driver.find_element(By.NAME, 'horaPonto')
            salvar = driver.find_element(By.XPATH, "//input[@value='Salvar e Continuar']")

            hora.clear()
            hora.send_keys(horario)

            salvar.click()
            sleep(1)

        logger.info(f'Ponto do dia: {dia} Atualizado com sucesso')
    sleep(1)
    driver.close()
    logger.info(f'Pontos atualizados com sucesso')