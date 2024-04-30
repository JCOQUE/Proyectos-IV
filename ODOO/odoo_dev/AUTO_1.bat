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
echo.  Ejectue [92mpython create_kafka.py ^<INTERNAL-IP^>[0m
echo.
echo.  Una vez hecho esto, ejecute [92mAUTO_2.bat[0m
echo. & echo. & echo. & echo. 
