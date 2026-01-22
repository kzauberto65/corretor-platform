@echo off
title Corretor Platform - Menu

REM Ajusta o diretório para a raiz do projeto
cd /d "%~dp0"

REM Executa o menu em Python
python src\menu.py

pause
