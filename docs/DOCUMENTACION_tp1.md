# Enunciado
Una organización con alcance nacional ha contratado enlaces para sus **6 sucursales** con la idea de armar una *red Wan* Nacional. En el armado de esta red Wan se ha dispuesto utilizar para el direccionamiento IP la red **192.168.100.0/24** *dividida en subredes con máscara* **/29**.

*Cada sucursal* utilizará para su *direccionamiento IP interno* una red **/24** completa, del tipo **10.0.n.0/24** 

De este modo *cada sucursal poseerá* un enlace Wan (**red 192.168.100.{SUB_RED}/29**) *y* una red interna (**10.0.n.0/24**).

La *Dirección IP* del enlace wan *del router de la sucursal* **será la primera dirección utilizable** de la red **/29**, su *contraparte* en la *casa matríz* **será la última dirección utilizable** de la red **/29**.

La dirección IP privada del router de la sucursal será la primer dirección utilizable de la red 10.0.n.0/24.

  
  
La correspondencia de direcciones de enlaces y redes estará dada por la siguiente regla:

**Sucursal 1**-> Enlace Wan: Primer red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.1.0/24

**Sucursal 2**-> Enlace Wan: Segunda red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.2.0/24

**Sucursal 3**-> Enlace Wan: Tercer red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.3.0/24

**Sucursal 4**-> Enlace Wan: Cuarta red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.4.0/24

**Sucursal 5**-> Enlace Wan: Quinta red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.5.0/24

**Sucursal 6**-> Enlace Wan: Sexta red 192.168.100.{SUB_RED}/29 -> Direccionamiento privado: 10.0.6.0/24



**Resolución**:
Deberá **desarrollar todo el direccionamiento IP de las redes conjuntamente con un esquema** de la misma.

Implementar con mininet el router de casa matriz, dos sucursales con: el router *primer IP* y un puesto de trabajo de la sucursal *última IP*.
# Calculo del Subneteo
Red Base: 192.168.100.0/24 . Esta red debe ser subneteada a /29

Pedimos prestado 5 bits, de host para la red, osea 2⁵=32 direcciones IP, lo que significa que es posible *armar 32 subredes*
Quedandonos 3 bits para host, osea 2³=*8 direcciones para host por subred* . 

Ahora hay que identificar la *primera dir utilizable* (para la sucursal) y la *ultima direccion utilizable* (para la Casa Matriz).

*Rangos /29* (Casa Matriz):
         1° dir = dir de *red*          2° dir = dir de *broadcast*
**Sucursal 1**= 192.168.100.0/29 -> 192.168.100.7/29 

**Sucursal 2**= 192.168.100.8/29 -> 192.168.100.15/29

**Sucursal 3**= 192.168.100.16/29 -> 192.168.100.23/29

**Sucursal 4**= 192.168.100.24/29 -> 192.168.100.31/29

**Sucursal 5**= 192.168.100.32/29 -> 192.168.100.39/29

**Sucursal 6**= 192.168.100.40/29 -> 192.168.100.47/29


De forma que el esquema de la red WAN queda:

| Enlace WAN | Red /29             | IP Router Sucursal (Primera Utilizable) | IP Router Casa Matriz (Última Utilizable) |
| ---------- | ------------------- | --------------------------------------- | ----------------------------------------- |
| Sucursal 1 | `192.168.100.0/29`  | `192.168.100.1`                         | `192.168.100.6`                           |
| Sucursal 2 | `192.168.100.8/29`  | `192.168.100.9`                         | `192.168.100.14`                          |
| Sucursal 3 | `192.168.100.16/29` | `192.168.100.17`                        | `192.168.100.22`                          |
| Sucursal4  | `192.168.100.24/29` | `192.168.100.25`                        | `192.168.100.30`                          |
| Sucursal 5 | `192.168.100.32/29` | `192.168.100.33`                        | `192.168.100.38`                          |
| Sucursal 6 | `192.168.100.40/29` | `192.168.100.41`                        | `192.168.100.46`                          |


*Rangos /24* (Sucursal, direccionamiento privado):
     1° dir = dir de *red*          2° dir = dir de *broadcast*
**Sucursal 1**= 10.0.1.0/24 -> 10.0.1.255/24

**Sucursal 2**= 10.0.2.0/24 -> 10.0.2.255/24

**Sucursal 3**= 10.0.3.0/24 -> 10.0.3.255/24

**Sucursal 4**= 10.0.4.0/24 -> 10.0.4.255/24

**Sucursal 5**= 10.0.5.0/24 -> 10.0.5.255/24

**Sucursal 6**= 10.0.6.0/24 -> 10.0.6.255/24

De forma que el esquema de la red privada queda:

| Sucursal  | Red Privada (/24) | IP Router LAN (Primera utilizable) | IP Puesto de Trabajo (Última utilizable |
| --------- | ----------------- | ---------------------------------- | --------------------------------------- |
| Sucursal1 | `10.0.1.0/24`     | `10.0.1.1`                         | `10.0.1.254`                            |
| Sucursal2 | `10.0.2.0/24`     | `10.0.2.1`                         | `10.0.2.254`                            |
| Sucursal3 | `10.0.3.0/24`     | `10.0.3.1`                         | `10.0.3.254`                            |
| Sucursal4 | `10.0.4.0/24`     | `10.0.4.1`                         | `10.0.4.254`                            |
| Sucursal5 | `10.0.5.0/24`     | `10.0.5.1`                         | `10.0.5.254`                            |
| Sucursal6 | `10.0.6.0/24`     | `10.0.6.1`                         | `10.0.6.254`                            |
# Diagrama de la red
![[diagrama_red.png]]
De todas maneras adjunto tmb el pdf correspondiente
