@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo =====================================================
echo   Pushing VocalAutomationProject to GitHub
echo   Repo: dorshimony/VocalSelfCoaching-QA-Automation
echo =====================================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Git is not installed, or not in PATH.
  echo         Download it from https://git-scm.com/download/win
  echo         then run this file again.
  echo.
  pause
  exit /b 1
)

git config user.name >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Git identity is not configured.
  echo         Run these two commands once, then run this file again:
  echo.
  echo         git config --global user.name "Dor Shimony"
  echo         git config --global user.email "your@email.com"
  echo.
  pause
  exit /b 1
)

if not exist ".git" (
  echo [1/6] git init
  git init
  if errorlevel 1 goto failed
) else (
  echo [1/6] repository already initialized - skipping
)

echo [2/6] git add .
git add .
if errorlevel 1 goto failed

echo [3/6] git commit
git commit -m "QA automation project for VocalSelfCoaching"

echo [4/6] git branch -M main
git branch -M main
if errorlevel 1 goto failed

echo [5/6] setting remote origin
git remote remove origin >nul 2>nul
git remote add origin https://github.com/dorshimony/VocalSelfCoaching-QA-Automation.git
if errorlevel 1 goto failed

echo [6/6] git push
echo.
echo     A GitHub sign-in window may open. Approve it - it happens once.
echo.
git push -u origin main
if errorlevel 1 goto failed

echo.
echo =====================================================
echo   DONE
echo   https://github.com/dorshimony/VocalSelfCoaching-QA-Automation
echo =====================================================
echo.
pause
exit /b 0

:failed
echo.
echo =====================================================
echo   Something failed. Copy the message above and send it to Claude.
echo =====================================================
echo.
pause
exit /b 1
