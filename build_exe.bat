@echo off
title XML Duplicate Cleaner Builder

echo ======================================
echo Building XML Duplicate Cleaner...
echo ======================================

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist XMLDuplicateCleaner.spec del XMLDuplicateCleaner.spec

pyinstaller ^
--onefile ^
--windowed ^
--clean ^
--name XMLDuplicateCleaner ^
--icon=icon.ico ^
main.py

echo.
echo ======================================
echo Build Completed!
echo EXE Location:
echo dist\XMLDuplicateCleaner.exe
echo ======================================
pause