#!/usr/bin/env python3

import argparse
from mininet.net import Mininet
from mininet.node import Node, Host, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

# inyecta el comando que hace que el Kernel deje de descartar paquetes ajenos y
# los reenvíe usando su tabla de ruteo
class LinuxRouter(Node):
    """Un nodo que actúa como router activando IP forwarding en el kernel."""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1') # comando mencionado arriba

    # apaga la funcion de red volviendo al contenedor a su estado inicial de host
    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0') 
        super(LinuxRouter, self).terminate()



def construir_red_wan(num_sucursales):
    net = Mininet(topo=None, build=False)

    info(f'\n*** Construyendo topología para {num_sucursales} sucursal(es)...\n')
    
    r_matriz = net.addHost('R_Matriz', cls=LinuxRouter)

    # Armado dinámico de nodos y enlaces segun argumento
    for i in range(1, num_sucursales + 1):
        # Cálculos de IPs WAN (/29) 
        base_wan = (i - 1) * 8   # cada 8 nodos hay salto de red en /29
        ip_suc_wan = f'192.168.100.{base_wan + 1}/29' 
        
        # Cálculos de IPs LAN (/24)
        gateway_lan = f'10.0.{i}.1'
        ip_host1 = f'10.0.{i}.252/24'
        ip_host2 = f'10.0.{i}.253/24'
        ip_host3 = f'10.0.{i}.254/24'
        
        # Instanciamos los HOSTS primero:
        h1_suc = net.addHost(f'H1_Suc{i}', cls=Host, ip=ip_host1, defaultRoute=f'via {gateway_lan}')
        h2_suc = net.addHost(f'H2_Suc{i}', cls=Host, ip=ip_host2, defaultRoute=f'via {gateway_lan}')
        h3_suc = net.addHost(f'H3_Suc{i}', cls=Host, ip=ip_host3, defaultRoute=f'via {gateway_lan}')

        # SWITCHES
        s_suc = net.addSwitch(f's{i}', cls=OVSKernelSwitch, failMode='standalone') 
        # el standalone logra que el switch se comporte como un layer2 tradicional, solucionando un bug por falta
        # de controladores en el kernel del ubuntu de la VM 
        
        # ROUTERS (Se agregan como host pasándole nuestra clase LinuxRouter)
        r_suc = net.addHost(f'R_Suc{i}', cls=LinuxRouter, ip=ip_suc_wan)

        # 4° ENLACES (WAN y LAN)
        net.addLink(r_suc, r_matriz, intfName1=f'R_Suc{i}-wan', intfName2=f'R_Matriz-wan{i}')
        net.addLink(r_suc, s_suc, intfName1=f'R_Suc{i}-lan')
        
        net.addLink(s_suc, h1_suc)
        net.addLink(s_suc, h2_suc)
        net.addLink(s_suc, h3_suc)

    info('*** Iniciando la red base\n')
    net.build()
    net.start()

    info('*** Inyectando rutas estáticas y configurando interfaces...\n')
    for i in range(1, num_sucursales + 1):
        base_wan = (i - 1) * 8
        ip_matriz_wan = f'192.168.100.{base_wan + 6}/29'
        ip_suc_wan_limpia = f'192.168.100.{base_wan + 1}' 
        ip_suc_lan = f'10.0.{i}.1/24'

        r_suc = net.get(f'R_Suc{i}')
        
        # Interfaces
        r_suc.cmd(f'ip addr add {ip_suc_lan} dev R_Suc{i}-lan')
        r_matriz.cmd(f'ip addr add {ip_matriz_wan} dev R_Matriz-wan{i}')

        # Ruteo Sucursal -> Todo a la Matriz
        r_suc.cmd(f'ip route add default via 192.168.100.{base_wan + 6}')

        # Ruteo Matriz -> Hacia la LAN específica de cada sucursal
        r_matriz.cmd(f'ip route add 10.0.{i}.0/24 via {ip_suc_wan_limpia}')

    info('*** Red WAN nacional operativa. Entrando a la consola interactiva...\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    parser = argparse.ArgumentParser(description="Simulador de Red WAN Nacional con N sucursales - Teleinformática")
    
    parser.add_argument('-n', '--sucursales', type=int, default=2, 
                        help="Cantidad de sucursales a simular (por defecto: 2)")
    parser.add_argument('--demo', action='store_true', 
                        help="Modo TP: Despliega exactamente 6 sucursales para la entrega")
    
    args = parser.parse_args()

    # Si flag --demo, ignoramos el -n y hacemos la ejecucion con 6 sucursales
    cantidad = 6 if args.demo else args.sucursales

    construir_red_wan(cantidad) # inicia la red