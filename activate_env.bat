@echo off
echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated!
echo.
echo You can now run:
echo - cd data ^&^& python preprocess_alarm_data.py
echo - cd data ^&^& python train_models.py
echo - cd backend ^&^& uvicorn main:app --reload
echo - cd frontend ^&^& npm run dev
echo.
cmd /k 