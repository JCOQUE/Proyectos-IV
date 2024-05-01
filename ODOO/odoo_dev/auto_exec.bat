@echo off
chcp 65001 > nul


pip install -r requirements.txt
echo. & echo.
kubectl config get-contexts
echo. 
kubectl config use-context docker-desktop
echo {"Amazon": [], "Nike":[]} > dev_addons/agreement_accepted.json
echo. & echo. & echo. & echo. 
echo.  Reseteando kubernetes...
echo. & echo. & echo. & echo. 
kubectl delete all --all
echo. & echo.
kubectl apply -f zookeeper.yaml
l
echo. & echo. & echo. & echo. 
echo --------------------------------------------------------------------
echo. &
python create_kafka.py 
echo. &
echo --------------------------------------------------------------------
echo. & echo. & echo. & echo. 

kubectl apply -f kafka.yaml

timeout /t 5 /nobreak

kubectl get all

echo. & echo. & echo. & echo. 
echo.  Reseteando contenedores...
echo. & echo. & echo. & echo. 
docker compose down
echo. & echo. & echo. & echo. 
echo.  Cargando contenedores...
echo. & echo. & echo. & echo. 
docker compose up -d
echo. & echo. & echo. & echo. 
echo. Proceda a abrir una pestaña de un navegador y escriba en ella [33mlocalhost:8069[0m
echo. & echo.
echo. Ahora, en otra pestaña, de la misma manera, introduzca [33mlocalhost:8070[0m 
echo. & echo. & echo.
echo [36m NOTA:[0m Recuerde actualizar los modulos.
echo. & echo. & echo. & echo. 
