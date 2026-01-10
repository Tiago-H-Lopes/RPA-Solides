from pacotes import ajustar_ponto, logger
from datetime import date

def main() -> None:
    # Exemplo de lista de dias e horarios
    # lista_dias_ajustar = ['02/12/2025', '03/12/2025']
    # horarios_ponto = ['09:00', '12:00', '13:00', '18:00']
    # ajustar_ponto(lista_dias_ajustar, horarios_ponto)

    logger.info('Iniciando automação')
    
    ajustar_ponto()    

    logger.info('Automação finalizada com sucesso')

if __name__ == '__main__':
    main()