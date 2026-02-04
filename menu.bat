@echo off
title Corretor Platform - Menu

REM Vai para a pasta raiz do projeto
cd /d "%~dp0"

REM Executa o menu como módulo
python -m src.menu

pause
