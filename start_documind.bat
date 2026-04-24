@echo off
title DocuMind - Startup
color 0A

echo ============================================
echo   DocuMind RAG System (Groq Powered)
echo ============================================
echo.

REM Check Docker
echo [1/3] Checking Docker...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running! Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running.
echo.

REM Check if backend image exists to decide fast vs full start
docker image inspect documind_rag-backend >nul 2>&1
if %errorlevel% equ 0 goto fast_start

:full_build
echo [INFO] First run - building images (one-time only, ~5 mins)...
docker-compose up --build -d
goto check_result

:fast_start
echo [INFO] Images found - fast start (no rebuild)...
docker-compose up -d

:check_result
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start. Run: docker-compose logs
    pause
    exit /b 1
)
echo.

REM Wait for backend to be healthy
echo [2/3] Waiting for backend...
set attempts=0

:wait_loop
set /a attempts+=1
if %attempts% gtr 30 (
    echo [ERROR] Backend did not start. Run: docker-compose logs backend
    pause
    exit /b 1
)
timeout /t 2 /nobreak >nul
curl -s http://localhost:8001/health >nul 2>&1
if %errorlevel% neq 0 (
    echo    Attempt %attempts%/30...
    goto wait_loop
)

echo [OK] Ready!
echo.
echo ============================================
echo   DocuMind is RUNNING!
echo   Frontend : http://localhost:3000
echo   Backend  : http://localhost:8001
echo   API Docs : http://localhost:8001/docs
echo   LLM      : Groq (llama-3.3-70b-versatile)
echo ============================================
echo.
echo   To STOP:    docker-compose down
echo   To REBUILD: docker-compose up --build -d
echo ============================================
echo.

timeout /t 2 /nobreak >nul
start http://localhost:3000

pause
