@echo off
echo Starting Der Dümmste Fliegt...
uvicorn app.main:app --reload --host 0.0.0.0 --port 80
pause