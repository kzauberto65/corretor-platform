@echo off
setlocal

echo ============================================
echo   CORRETOR PLATFORM - IMPORTADOR DE ARQUIVOS
echo ============================================
echo.

if "%~1"=="" (
    echo Arraste um arquivo .xlsx em cima deste .bat
    pause
    exit /b
)

set "ARQUIVO=%~1"

echo Arquivo recebido:
echo %ARQUIVO%
echo.

REM Vai para a pasta src
cd /d "%~dp0src"

REM Executa o ingestor como módulo (ESSENCIAL)
python -m ingestao.ingest "%ARQUIVO%"

echo.
echo Processo finalizado.
pause