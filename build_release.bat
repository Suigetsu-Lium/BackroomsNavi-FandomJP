@echo off
chcp 65001 > nul
setlocal

cd /d "%~dp0"

echo ================================================
echo   Backrooms Navigation System - Build
echo ================================================
echo.

set DIST_DIR=dist\BackroomsNavigationSystem_FandomJP
set INTERNAL_DIR=%DIST_DIR%\_internal

echo [1/3] PyInstallerでビルドしています...
pyinstaller --clean --noconfirm --onedir --console ^
    --name BackroomsNavigationSystem_FandomJP ^
    --paths modules ^
    --collect-submodules modules ^
    BackroomsNavigationSystem_FandomJP.py

if errorlevel 1 (
    echo.
    echo ❌ ビルドに失敗しました。
    pause
    exit /b 1
)

echo.
echo [2/3] _internal 内に必要なデータフォルダを配置しています...

:: すべて _internal の中にコピー・作成する
if exist "parsed_index" (
    echo   - parsed_index を _internal にコピー中...
    xcopy /E /I /Y "parsed_index" "%INTERNAL_DIR%\parsed_index\" > nul
) else (
    mkdir "%INTERNAL_DIR%\parsed_index" 2>nul
)

if exist "level_lists" (
    echo   - level_lists を _internal にコピー中...
    xcopy /E /I /Y "level_lists" "%INTERNAL_DIR%\level_lists\" > nul
) else (
    mkdir "%INTERNAL_DIR%\level_lists" 2>nul
)

if exist "index_html" (
    echo   - index_html を _internal にコピー中...
    xcopy /E /I /Y "index_html" "%INTERNAL_DIR%\index_html\" > nul
) else (
    mkdir "%INTERNAL_DIR%\index_html" 2>nul
)

:: その他モジュールが使用する空フォルダを _internal 内に準備
if not exist "%INTERNAL_DIR%\data" mkdir "%INTERNAL_DIR%\data" 2>nul
if not exist "%INTERNAL_DIR%\extracted_fandom_levels" mkdir "%INTERNAL_DIR%\extracted_fandom_levels" 2>nul

echo.
echo [3/3] ビルドが正常に完了しました！
echo.
echo 出力先:
echo %DIST_DIR%\
echo.
pause
