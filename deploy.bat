@echo off
setlocal enabledelayedexpansion

:: Ejecuta la generación del paquete fuente
python setup.py sdist

:: Obtiene el último archivo generado en el directorio dist
for /f "delims=" %%i in ('dir /b /o-d dist\*.tar.gz') do (
    set "latest_file=%%i"
    goto :break
)
:break

:: Verifica si se encontró el archivo más reciente
if "%latest_file%"=="" (
    echo No se encontró ningún archivo para subir.
    endlocal
    exit /b 1
)

:: Sube el archivo más reciente a PyPI usando la configuración del archivo .pypirc
python -m twine upload "dist\!latest_file!"

:: Finaliza el script
endlocal