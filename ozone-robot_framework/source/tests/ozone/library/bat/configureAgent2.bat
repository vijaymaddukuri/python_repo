@echo The agent will start approximately 1 minute after you enter the correct master password.
@echo The agent will start as a background service. You need to re-run this bat file and reneter master password if you reboot the machine.

@echo off

REM  DO NOT EDIT FILE
REM ask for user password


REM se the agentPassword value is Password123!
REM for /f "delims=" %%i in ('powershell -file C:\EHC-Software\bootConfig\getpwd.ps1') do set agentPassword=%%i
@echo Checking password validity...
set agentPassword="Password123!"
cd C:\EHC-Software\EHC\autodeploy\buildAutomation\source
python ehcOzoneAgent.py --ozone_password=%agentPassword% --test

REM delete scheduled task if exists
if not exist C:\temp mkdir C:\temp
schtasks /query > C:\temp\agentQuery
findstr /b /i "runAgent" C:\temp\agentQuery > nul
if %errorlevel%==0 ( schTasks /delete /tn runAgent /f )

REM manipulate time
set hour=%time:~0,2%
set min=%time:~3,2%
set /a min=%min%+1
@echo %time%
if %hour% LSS 10 set hour=0%hour:~1,1%
if %min% LSS 10 set min=0%min%
set hourmin=%hour%:%min%
@echo agent will start @ %hourmin%

REM run task
schtasks /create /ru system /tn runAgent  /sc ONCE /st %hourmin% /tr "C:\EHC-Software\bootConfig\runAgent.bat %agentPassword%"

@echo Agent Starting. Please wait.....

ping 127.0.0.1 -n 60 > nul

@echo -----------------------------------------------------------------------
@echo                        !! Agent Started !!
@echo
@echo Press any key to close this window. Agent will continue to run in the background.

