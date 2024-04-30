@echo off

kubectl apply -f kafka.yaml
kubectl apply -f hpa.yaml

timeout /t 5 /nobreak

kubectl get all
docker compose down
docker compose up -d
echo. & echo. & echo. & echo. 
echo. Proceda a abrir una pestania de un navegador y escriba en ella [33mlocalhost:8069[0m
echo. [31mMUY IMPORTANTE[0m: En esta pestaniaa asigne, a poder ser, [92mproducer[0m como nombre de la base de datos.
echo. En caso de querer utilizar otro, se recomienda cambiar en [31mdocker-compose.yaml[0m, la linea [36mcommand: odoo -u pedidos -d ^<tu_nombre_base_datos^>[0m en el servicio de [31mproducer[0m.
echo. & echo.
echo. Ahora, en otra pestani, de la misma manera, introduzca [33mlocalhost:8070[0m teniendo en cuenta la misma indicaciones anteriormente mencionadas. Unicamente que ahora en la seccion [31mconsumer[0m del [31mdocker-compose.yaml[0m