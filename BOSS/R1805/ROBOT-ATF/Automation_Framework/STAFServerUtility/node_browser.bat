@ECHO OFF
start "Node1111" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role node -hub http://localhost:1111/grid/register -browser browserName="chrome" -Dwebdriver.chrome.driver=C:\NodeWebKit\chromedriver_windows.exe -port 8792 -hubPort 1111
start "Node2222" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role node -hub http://localhost:2222/grid/register -browser browserName="chrome" -Dwebdriver.chrome.driver=C:\NodeWebKit\chromedriver_windows.exe -port 8794 -hubPort 2222
start "Node8888" java -jar C:\NodeWebKit\selenium-server-standalone-2.53.0.jar -role node -hub http://localhost:8888/grid/register -browser browserName="chrome" -Dwebdriver.chrome.driver=C:\NodeWebKit\chromedriver_windows.exe -port 8796 -hubPort 8888