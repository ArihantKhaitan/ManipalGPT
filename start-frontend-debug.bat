@echo off
echo Starting Manipal AI Frontend on port 3004 with debug output...
echo.
echo Checking Node.js version...
node --version
echo.
echo Checking if port 3004 is available...
netstat -ano | findstr :3004
echo.
echo Starting Next.js dev server...
echo If you see errors, they will be displayed below.
echo.
cd frontend
npx next dev -p 3004
pause

