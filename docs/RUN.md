# Instrucciones de ejecución

Primero, otorgar permisos de ejecución al script (asegúrate de estar en el directorio correcto):
```bash
chmod +x caso1.py
```

Ejecutar el script. Para el entorno completo del Trabajo Práctico (Matriz + 6 Sucursales), utilizamos el flag `--demo`:
```bash
sudo ./wan_nacional.py --demo
```
*(Nota: Se puede usar `sudo ./wan_nacional.py -n 2` para probar escenarios libres).*

Una vez que el entorno cargue, ya estarás en la consola interactiva. Para la prueba de fuego (validar que el ruteo estático funciona en toda la red), ejecuta un ping entre todos los nodos:
```bash
mininet> pingall
```

### Comandos para explorar y defender la topología

Para ver todos los nodos instanciados en la red:
```bash
mininet> nodes
```

Para ver la topología física (cómo están conectados los cables virtuales entre Routers, Switches y Hosts):
```bash
mininet> net
```

Para ver un volcado de información con todas las IPs asignadas rápidamente:
```bash
mininet> dump
```

**Verificación de Interfaces por Nodo:**
Para ver las interfaces de red de cada equipo usamos `ip addr` o `ifconfig`:
```bash
mininet> R_Matriz ip addr
mininet> R_Suc1 ip addr
mininet> H1_Suc1 ifconfig
```

**Pruebas de Ruteo Avanzadas:**
Para ver por qué routers pasa el paquete viajando desde un host de la Sucursal 1 hasta la Sucursal 6 (ideal para demostrar que pasa por la Casa Matriz):
```bash
mininet> H1_Suc1 traceroute 10.0.6.254
``