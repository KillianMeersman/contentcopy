@REM GOTO FULLINSTALL
GOTO QUICKINSTALL
:FULLINSTALL
python.exe -m pip install --upgrade pip
pip install Gooey
pip install pyinstaller-versionfile
pip install hashlib
pip install logging
pip install os

REM # Exe installer:
pip install -U pyinstaller

:QUICKINSTALL
python createVersionFile.py
REM Get the version number from the const.py file
setlocal
for /f "tokens=2 delims== " %%G in ('findstr "VERSION=" const.py') do set VERSION=%%~G
@REM echo %VERSION%
pyinstaller --exclude=config.ini --version-file=versionfile.txt  --icon=contentcopy.ico --windowed --onefile contentcopy\contentcopy.py

set OUTPUT_FILE=dist\ContentCopy_v%VERSION%.zip
python -c "import zipfile, os; files_to_zip=['dist\contentcopy.exe', 'README.md', 'LICENSE']; zip_file=zipfile.ZipFile('%OUTPUT_FILE%', 'w'); [zip_file.write(file_to_zip, os.path.basename(file_to_zip)) for file_to_zip in files_to_zip]; zip_file.close()"
