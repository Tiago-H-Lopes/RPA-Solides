import re
from .logger import logger

def validar_e_formatar_cpf(cpf_input):
    """
    Valida se o CPF está no formato correto (xxx.xxx.xxx-xx).
    Se estiver, retorna o valor.
    Se não estiver, limpa, formata e retorna.
    """
    # Regex para o formato exato: 3 dígitos, ponto, 3 dígitos, ponto, 3 dígitos, traço, 2 dígitos
    regex_formato_correto = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    
    #Verifica se já está no formato correto
    if re.match(regex_formato_correto, str(cpf_input)):
        logger.info("CPF Já estava no formato correto.")
        return cpf_input
    
    #Se não estiver, remove tudo o que não for número
    apenas_numeros = re.sub(r'\D', '', str(cpf_input))
    
    #Verifica se sobraram exatamente 11 dígitos
    if len(apenas_numeros) == 11:
        #Aplica a formatação
        cpf_formatado = f"{apenas_numeros[:3]}.{apenas_numeros[3:6]}.{apenas_numeros[6:9]}-{apenas_numeros[9:]}"
        logger.info(f"CPF Formatado de '{cpf_input}' para '{cpf_formatado}'")
        return cpf_formatado
    else:
        #Se não tiver 11 dígitos, o dado é inválido
        error_msg = "Erro: CPF Inválido (quantidade de dígitos incorreta)"
        logger.error(error_msg)
        raise ValueError(error_msg)