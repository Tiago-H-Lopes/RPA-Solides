import logging
import os
from pathlib import Path
from datetime import date
PASTA_LOGS = Path(os.getcwd(), 'logs')
now = date.today()
now = date.strftime(now, '%d-%m-%Y')
caminho_log = PASTA_LOGS / f'log {now}.log'
logger = logging.getLogger("RPA")

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s")
handler = logging.FileHandler(caminho_log, 'a', encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

