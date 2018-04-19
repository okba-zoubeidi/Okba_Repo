@ECHO OFF                                                                              
FOR /F %%T IN ('Wmic process where^(Name^="python.exe"^)get ProcessId^|more +1') DO (
SET /A ProcessId=%%T) &GOTO SkipLine                                                   
:SkipLine                                                                              
echo ProcessId = %ProcessId% 
TASKKILL /pid %ProcessId% /F


