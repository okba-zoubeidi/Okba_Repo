@ECHO OFF
start "Hub1111" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role hub -port 1111
start "Hub2222" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role hub -port 2222
start "Hub8888" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role hub -port 8888