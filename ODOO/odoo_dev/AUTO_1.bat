@echo off

set ANSICON=TRUE

pip install -r requirements.txt
echo. & echo.
kubectl delete all --all
kubectl apply -f zookeeper.yaml
echo. & echo. & echo. & echo.   
echo. Observe la [33mINTERNAL-IP[0m que se muestra a continuacion:
echo. & echo. & echo. & echo. 
kubectl get nodes -o wide
echo. & echo. & echo. & echo.  
set /p input="Introduzca la INTERNAL-IP: "
echo. & echo.
echo --------------------------------------------------------------------
echo. &
python create_kafka.py %input%
echo. &
echo --------------------------------------------------------------------
echo. & echo. & echo. & echo. 
echo.  Antes de seguir, asegurese de que la ip introducida coincida con [33mINTERNAL-IP[0m.
echo.  En ese caso, ejecute [92mAUTO_2.bat[0m
echo. &
echo. [36m NOTA:[0m En caso de haber introducido mal la ip debera volver a ejecutar [92mAUTO_1.bat[0m de nuevo.
echo. & echo. & echo. & echo. 
