#!/usr/bin/python2

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# How to run (Mininet):
#    mn -c && ./LPDC.py
#
# Note: controller port for OpenDaylight: 6653
#
# Author: Lucio A. Rocha
# Last update: 23/11/2020
#
#Network:
#
#10.10.10.10                                                              .10.70
# (H1)(0)->(1)S2(2)---->(1)S3(2)--->(1)S4(2)<----(1)S5(2)<----(1)S6(2)<--(0)(H7)
# (1).11.10   (3)          (3)         (3)          (3)         (3)      (1).11.70
#  |          |            |           |            |           |        |
#  |          \/           \/          \/           \/          \/       |
#  |          (3)          (3)         (3)          (3)         (3)      |
#  +------>(1)S8(2)---->(1)S9(2)--->(1)S10(2)<---(1)S11(2)<---(1)S12(2)<-+
#             (4)          (4)         (4)          (4)          (4)
#             |            |           |            |            | 
#             |            |           \/           |            |   
#             \/           \/         (2)           \/           \/
#             (2)          (3)       .12.15         (3)          (2)
#             S13(1)--->(1)S14(2)-->(0)H15(1)<---(1)S16(2)<---(1)S17
#             (3)          (4)  .10.15    .11.15    (4)          (3)
#             /\           /\         .13.15        /\           /\
#             |            |          (3)           |            |
#             |            |           /\           |            |
#             (3)          (3)         (3)          (3)          (3) 
#  +------>(1)S19(2)--->(1)S20(2)-->(1)S21(2)<---(1)S22(2)<---(1)S23(2)<-+ 
#  |          (4)          (4)         (4)          (4)          (4)     |
#  |          /\           /\          /\           /\           /\      |
#  |          |            |           |            |            |       |
#  (1).11.18  (3)          (3)         (3)          (3)          (3)     (1).11.24
#(H18)(0)->(1)S25(2)--->(1)S26(2)-->(1)S27(2)<---(1)S28(2)<---(1)S29(2)<-(0)(H24)
#      .10.18                                                             .10.24
#     


import os #For os.system() calls
from mininet.net import Mininet
from mininet.node import Controller,RemoteController,OVSKernelSwitch,UserSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link,TCLink

class StaticTopo(Topo):
    def build(self):
        pass
        
def topology():
    net = Mininet(topo=StaticTopo(), controller=RemoteController, link=TCLink,switch=OVSKernelSwitch)

    n = 5 #Number of hosts to divide resources
    h1 = net.addHost('h1', cpu=1/n)
    h2 = net.addHost('h2', cpu=1/n) #Na modelagem: h7
    h3 = net.addHost('h3', cpu=1/n) #Na modelagem: h15 Destination    
    h4 = net.addHost('h4', cpu=1/n) #Na modelagem: h18
    h5 = net.addHost('h5', cpu=1/n) #Na modelagem: h24

    bw = 1000
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
 
    s8 = net.addSwitch('s8')
    s9 = net.addSwitch('s9')
    s10 = net.addSwitch('s10')
    s11 = net.addSwitch('s11')
    s12 = net.addSwitch('s12')

    s13 = net.addSwitch('s13')
    s14 = net.addSwitch('s14')
    s16 = net.addSwitch('s16')
    s17 = net.addSwitch('s17')

    s19 = net.addSwitch('s19')
    s20 = net.addSwitch('s20')
    s21 = net.addSwitch('s21')
    s22 = net.addSwitch('s22')
    s23 = net.addSwitch('s23')

    s25 = net.addSwitch('s25')
    s26 = net.addSwitch('s26')
    s27 = net.addSwitch('s27')
    s28 = net.addSwitch('s28')
    s29 = net.addSwitch('s29')
    
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    
    #net.addLink(h1,s2, bw=10) #Mude bw para alterar a bw do link
    net.addLink(h1,s2, bw=bw) #h1-0,s2-1
    net.addLink(h1,s8, bw=bw) #h1-1,s8-1
    #net.addLink(h1,s1, bw=10, delay='100ms') #Delay only in response
    net.addLink(s2,s3, bw=bw) #s2-2,s3-1
    net.addLink(s3,s4, bw=bw) #s3-2,s4-1
    net.addLink(s4,s5, bw=bw) #s4-2,s5-1
    net.addLink(s5,s6, bw=bw) #s5-2,s6-1
    net.addLink(h2,s6, bw=bw) #h2-0,s6-2

    net.addLink(s8,s9, bw=bw) #s8-2,s9-1
    net.addLink(s9,s10, bw=bw) #s9-2,s10-1
    net.addLink(s10,s11, bw=bw) #s10-2,s11-1
    net.addLink(s11,s12, bw=bw) #s11-2,s12-1
    net.addLink(h2,s12, bw=bw) #h2-1,s12-2

    net.addLink(s2,s8, bw=bw) #s2-3,s8-3
    net.addLink(s3,s9, bw=bw) #s3-3,s9-3
    net.addLink(s4,s10, bw=bw) #s4-3,s10-3
    net.addLink(s5,s11, bw=bw) #s5-3,s11-3
    net.addLink(s6,s12, bw=bw) #s6-3,s12-3
    
    net.addLink(s13,s14, bw=bw) #s13-1,s14-1
    net.addLink(s14,h3, bw=bw) #s14-2,h3-1
    net.addLink(h3,s16, bw=bw) #h3-2,s16-1
    net.addLink(s16,s17, bw=bw) #s16-2,s17-1

    net.addLink(s13,s8, bw=bw) #s13-2,s8-4
    net.addLink(s14,s9, bw=bw) #s14-3,s9-4
    net.addLink(h3,s10, bw=bw) #h3-3,s10-4
    net.addLink(s16,s11, bw=bw) #s16-3,s11-4
    net.addLink(s17,s12, bw=bw) #s17-2,s12-4

#--
    net.addLink(h4,s25, bw=bw) #h4-0,s25-1
    net.addLink(h4,s19, bw=bw) #h4-1,s19-1
    net.addLink(s25,s26, bw=bw) #s25-2,s26-1
    net.addLink(s26,s27, bw=bw) #s26-2,s27-1
    net.addLink(s27,s28, bw=bw) #s27-2,s28-1
    net.addLink(s28,s29, bw=bw) #s28-2,s29-1
    net.addLink(h5,s29, bw=bw) #h5-0,s29-2

    net.addLink(s19,s20, bw=bw) #s19-2,s20-1
    net.addLink(s20,s21, bw=bw) #s20-2,s21-1
    net.addLink(s21,s22, bw=bw) #s21-2,s22-1
    net.addLink(s22,s23, bw=bw) #s11-2,s12-1
    net.addLink(h5,s23, bw=bw) #h5-1,s23-2

    net.addLink(s19,s13, bw=bw) #s19-3,s13-3
    net.addLink(s20,s14, bw=bw) #s20-3,s14-4
    net.addLink(s21,h3, bw=bw) #s21-3,h3-3
    net.addLink(s22,s16, bw=bw) #s22-3,s16-4
    net.addLink(s23,s17, bw=bw) #s23-3,s17-3

    net.addLink(s25,s19, bw=bw) #s25-3,s19-4
    net.addLink(s26,s20, bw=bw) #s26-3,s20-4
    net.addLink(s27,s21, bw=bw) #s27-3,s21-4
    net.addLink(s28,s22, bw=bw) #s28-3,s22-4
    net.addLink(s29,s23, bw=bw) #s29-3,s23-4
    
    
    
    net.build()

    c0.start()
    listaSwitches = [2, 3, 4, 5, 6,
                     8, 9, 10, 11, 12,
                     13, 14, 16, 17,
                     19, 20, 21, 22, 23,
                     25, 26, 27, 28, 29
    ]
    for i in listaSwitches:
        s=net.get("s%s"%i)
        s.start([c0])

#    h1 = net.get('h1')
#    h2 = net.get('h2')

    h1.cmd('ifconfig h1-eth0 10.10.10.10/24')
    h1.cmd('ifconfig h1-eth1 10.10.11.10/24')
    
    #--
    h2.cmd('ifconfig h2-eth0 10.10.10.70/24')
    h2.cmd('ifconfig h2-eth1 10.10.11.70/24')

    #--
    h3.cmd('ifconfig h3-eth0 10.10.10.15/24')
    h3.cmd('ifconfig h3-eth1 10.10.11.15/24')
    h3.cmd('ifconfig h3-eth2 10.10.12.15/24')
    h3.cmd('ifconfig h3-eth3 10.10.13.15/24')

    #--
    h4.cmd('ifconfig h4-eth0 10.10.10.18/24')
    h4.cmd('ifconfig h4-eth1 10.10.11.18/24')

    #--
    h5.cmd('ifconfig h5-eth0 10.10.10.24/24')
    h5.cmd('ifconfig h5-eth1 10.10.11.24/24')

    
    #---
    improved = 2   #0-default,1-sysctl + interfaces,2-only sysctl
    if improved==1: #sysctl + interfaces

        IFACES=[
            "s2-eth1","s2-eth2","s2-eth3",
            "s3-eth1","s3-eth2","s3-eth3",
            "s4-eth1","s4-eth2","s4-eth3",
            "s5-eth1","s5-eth2","s5-eth3",
            "s6-eth1","s6-eth2","s6-eth3",
            
            "s8-eth1","s8-eth2","s8-eth3", "s8-eth4",
            "s9-eth1","s9-eth2","s9-eth3", "s9-eth4",
            "s10-eth1","s10-eth2","s10-eth3", "s10-eth4",
            "s11-eth1","s11-eth2","s11-eth3", "s11-eth4",
            "s12-eth1","s12-eth2","s12-eth3", "s12-eth4"

            "s13-eth1","s13-eth2","s13-eth3",
            "s14-eth1","s14-eth2","s14-eth3", "s14-eth4",
            "s16-eth1","s16-eth2","s16-eth3", "s16-eth4",
            "s17-eth1","s17-eth2","s17-eth3",

            "s19-eth1","s19-eth2","s19-eth3", "s19-eth4",
            "s20-eth1","s20-eth2","s20-eth3", "s20-eth4",
            "s21-eth1","s21-eth2","s21-eth3", "s21-eth4",
            "s22-eth1","s22-eth2","s22-eth3", "s22-eth4",
            "s23-eth1","s23-eth2","s23-eth3", "s23-eth4",

            "s25-eth1","s25-eth2","s25-eth3", 
            "s26-eth1","s26-eth2","s26-eth3", 
            "s27-eth1","s27-eth2","s27-eth3", 
            "s28-eth1","s28-eth2","s28-eth3",
            "s29-eth1","s29-eth2","s29-eth3"
        ]
        MTU=9000
        TXQ=500
        RXU=300
        MBUF=204217728
        
        os.system('sysctl -w net.mptcp.mptcp_checksum=0')

        os.system('sysctl -w net.ipv4.tcp_rmem="4096 524288 '+str(MBUF)+'"')
        os.system('sysctl -w net.ipv4.tcp_wmem="4096 524288 '+str(MBUF)+'"')
        os.system('sysctl -w net.ipv4.tcp_mem="768174 10242330 15363480"')
        
        os.system('sysctl -w net.ipv4.tcp_low_latency=1')
        os.system('sysctl -w net.ipv4.tcp_no_metrics_save=1')
        os.system('sysctl -w net.ipv4.tcp_timestamps=1')
        os.system('sysctl -w net.ipv4.tcp_sack=1')

        os.system('sysctl -w net.core.rmem_max=524287')
        os.system('sysctl -w net.core.wmem_max=524287')
        os.system('sysctl -w net.core.optmem_max=524287')

        os.system('sysctl -w net.core.netdev_max_backlog=10000')

        os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic')
        
        # Setup RFS
        for CPU in range(1):
            for iface in IFACES:
                os.system('echo 9 > /sys/class/net/'+iface+'/queues/rx-'+str(CPU)+'/rps_cpus')
                #os.system('echo 9 > /sys/class/net/'+iface+'/queues/tx-'+str(CPU)+'/xps_cpus')
                os.system('echo 1024 > /sys/class/net/'+iface+'/queues/rx-'+str(CPU)+'/rps_flow_cnt')
                
                os.system('echo 1024 > /proc/sys/net/core/rps_sock_flow_entries')
                
                os.system('service irqbalance stop')
                
                # Let's use jumbo frames
                for iface in IFACES:
                    os.system('ifconfig '+iface+' mtu '+str(MTU)+' txqueuelen '+str(TXQ))
                    
                    #Not works: operation not supported
                    # Interrupt coalescing
                    #for iface in IFACES:
                    #	os.system('ethtool -C '+iface+' rx-usecs '+str(RXU))
                    
                    # IRQ CPU Affinity. (I'm not sure if this is necessary)
                    #for i in {104..157}; do
                    #echo "04" > /proc/irq/$i/smp_affinity
                    #done
    elif improved==2: #only sysctl
        MTU=9000
        TXQ=500
        RXU=300
        MBUF=204217728
        
        os.system('sysctl -w net.mptcp.mptcp_checksum=0')

        os.system('sysctl -w net.ipv4.tcp_rmem="4096 524288 '+str(MBUF)+'"')
        os.system('sysctl -w net.ipv4.tcp_wmem="4096 524288 '+str(MBUF)+'"')
        os.system('sysctl -w net.ipv4.tcp_mem="768174 10242330 15363480"')
        
        os.system('sysctl -w net.ipv4.tcp_low_latency=1')
        os.system('sysctl -w net.ipv4.tcp_no_metrics_save=1')
        os.system('sysctl -w net.ipv4.tcp_timestamps=1')
        os.system('sysctl -w net.ipv4.tcp_sack=1')

        os.system('sysctl -w net.core.rmem_max=524287')
        os.system('sysctl -w net.core.wmem_max=524287')
        os.system('sysctl -w net.core.optmem_max=524287')

        os.system('sysctl -w net.core.netdev_max_backlog=10000')

        os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic')

        os.system('echo 1024 > /proc/sys/net/core/rps_sock_flow_entries')
        os.system('service irqbalance stop')
    else:
        #Default values
        os.system('sysctl -w net.mptcp.mptcp_checksum=1')
        
        os.system('sysctl -w net.ipv4.tcp_rmem="4096 131072 6291456"')
        os.system('sysctl -w net.ipv4.tcp_wmem="4096 16384 4194304"')
        os.system('sysctl -w net.ipv4.tcp_mem="122772 163698 245544"')
        os.system('sysctl -w net.ipv4.tcp_low_latency=0')
        os.system('sysctl -w net.ipv4.tcp_no_metrics_save=0')
        os.system('sysctl -w net.ipv4.tcp_timestamps=1')
        os.system('sysctl -w net.ipv4.tcp_sack=1')

        os.system('sysctl -w net.core.rmem_max=229376')
        os.system('sysctl -w net.core.wmem_max=229376')
        os.system('sysctl -w net.core.optmem_max=20480')

        os.system('sysctl -w net.core.netdev_max_backlog=1000')

        os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic')
        
        os.system('echo 0 > /proc/sys/net/core/rps_sock_flow_entries')
        os.system('service irqbalance start')
    CLI(net)

    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')

    topology()
    
