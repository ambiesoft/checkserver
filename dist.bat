set TARGETDIR=\\Inpsrv\Share\Linkout\checkserver\
mkdir %TARGETDIR%
C:\LegacyPrograms\FFC\FFC.exe "%~dp0checkserver.py" "%~dp0ok.wav" "%~dp0ng.wav" /to:"%TARGETDIR%"
