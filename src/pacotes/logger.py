import logging
import os
from pathlib import Path
from datetime import date
PASTA_LOGS = Path(os.getcwd(), 'src', 'logs')
now = date.today()
now = date.strftime(now, '%d-%m-%Y')
caminho_log = PASTA_LOGS / f'log {now}.log'
arquivo = Path.exists(caminho_log)
if not arquivo:
    with open(caminho_log, 'w', encoding='utf-8') as log:
        log.close()


logger = logging.getLogger("RPA")

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s")
handler = logging.FileHandler(caminho_log, 'a', encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

