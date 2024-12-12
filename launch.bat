@echo off
:: Start Vite in a new command prompt
cd /d C:\Users\qwerty\WebstormProjects\3dkanoodle\Views
start cmd /k "npx vite"

:: Activate the virtual environment and run Django in a new command prompt
cd /d C:\Users\qwerty\WebstormProjects\3dkanoodle
start cmd /k "venv\Scripts\activate && python manage.py runserver"