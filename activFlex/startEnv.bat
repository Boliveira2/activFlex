@echo off
REM Ativar o ambiente virtual
call venv\Scripts\activate.bat

REM Apagar builds anteriores (opcional mas recomendado)
rmdir /s /q dist
rmdir /s /q build
del main.spec 2>nul

REM Gerar o executável com PyInstaller
pyinstaller --name "GestaoPagamentos" ^
 --onefile ^
 --windowed ^
 --add-data "data;data" ^
 --add-data "scripts;scripts" ^
 main.py

REM Mensagem final
echo.
echo ========================================
echo      Executável criado em dist\
echo ========================================
pause
