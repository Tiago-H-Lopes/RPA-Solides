from pacotes import ajustar_ponto, logger
from datetime import date

def main() -> None:
    logger.info('Iniciando automação')
    
    today = date.today()
    today = date.strftime(today, '%d/%m/%Y')
    lista_dias_ajustar = [today]
    horarios_ponto = ['09:00', '12:00', '13:00', '18:00']
    
    ajustar_ponto(lista_dias_ajustar, horarios_ponto)

    logger.info('Automação finalizada com sucesso')

if __name__ == '__main__':
    main()