@echo off
cd C:\Users\Miguel Castillo\Desktop\Recibo_compraenUSAec
call venv\Scripts\activate
waitress-serve --port=8080 Recibo_compraenUSAec.wsgi:application