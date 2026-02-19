@echo off
chcp 65001 >nul
cd /d "%~dp0..\.."
python utilities\extract_apex_domains.py
pause
