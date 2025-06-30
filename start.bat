@echo off

::Nao testado

IF NOT EXIST "venv\" (
    python3 -m venv venv
    call venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
) ELSE (
    call venv\Scripts\activate
)

streamlit run app.py
pause
