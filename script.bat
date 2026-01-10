@echo off
color 0b

echo ==========================================
echo    INICIANDO ROBO DE AJUSTE DE PONTO
echo ==========================================

echo [1/3] Ativando ambiente virtual...
call .\venv\Scripts\activate

echo [2/3] Executando codigo python
python src/main.py

echo [3/3] Processo finalizado com sucesso!
echo ==========================================