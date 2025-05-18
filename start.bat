@echo off
echo Démarrage du serveur X11 avec VcXsrv...
start "" "C:\Program Files\VcXsrv\vcxsrv.exe" :0 -ac -multiwindow

echo Se déplacer dans le répertoire du projet...
cd C:\Users\toto\document\Kicekifeqoa

echo Construction de l'image Docker avec Docker Compose...
docker-compose build

echo Lancement du conteneur Docker avec Docker Compose...
docker-compose up

pause
