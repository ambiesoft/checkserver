setlocal
set TARGETDIR=C:\Linkout\checkserver\
mkdir %TARGETDIR%
C:\LegacyPrograms\FFC\FFC.exe "%~dp0checkserver.py" "%~dp0ok.wav" "%~dp0ng.wav" "%~dp0lsPy\lspy.py" "%~dp0lsPy\logger.py" /to:"%TARGETDIR%"
