## Linear Programming for Data Center

How to cite this work:

**Rocha, L. A. "Intra Data Center MultiPath Optimization with Emulated Software Defined Networks". The 35th International Conference on Advanced Information Netowrking and Applications (AINA-2021), Ryerson University, Toronto, Canada, 2021.** 

Contact at: [outrosdiasvirao at gmail.com](mailto:outrosdiasvirao@gmail.com)

Table 2 in AINA 2021 article presents duplicate results.
Please, consider the values obtained in this spreeadsheet bellow:

The results are publicaly available at: https://osf.io/qkvj3/
```
MD5SUM b7305a652872bcf0021a1359b3f221bc  results_with_fixes_for_AINA_2021_article.ods
```

The code for GLPK is available here: https://github.com/lpdc/lpdc/blob/master/LPDC.mod

```
MD5SUM: 72a337ee5d5af41e1ebcfba2fb24f5fc LPDC.mod
```

The code for MPTCP in Mininet is available here: https://github.com/lpdc/lpdc/blob/master/LPDC.py

```
MD5SUM: 731c61a1c1d0dc27c59987f179b7f37a LPDC.py
```

## How to run this project:

0) Recompile the MPTCP kernel: (https://multipath-tcp.org)

```
# make menuconfig

# make -j4

# make -j4 modules_install

# make install

# update-grub
```

0.1) Reboot the operating system. Verify the MPTCP enabled in the kernel:

```
# dmesg | grep MPTCP
```

1) Ubuntu: Setup GRUB to start with the MPTCP kernel by default ('-A100' to show until 100 matches)

```
# grep -A150 submenu /boot/grub/grub.cfg | grep menuentry

...
...
(Default kernel)
submenu 'Advanced options for Ubuntu' $menuentry_id_option 'gnulinux-advanced-b5b06d70-ea98-45ab-be8a-55b2fcec9baf' {
...
(MPTCP kernel)
menuentry 'Ubuntu, with Linux 4.19.105+' --class ubuntu --class gnu-linux --class gnu --class os $menuentry_id_option 'gnulinux-4.19.105+-advanced-b5b06d70-ea98-45ab-be8a-55b2fcec9baf'
...
```

1.1) From the previous output, insert in '/etc/default/grub':

```
GRUB_DEFAULT="DEFAULT_KERNEL>NEW_MPTCP_KERNEL"

For example (Don't forget double quotes "...", and symbol '>'):
GRUB_DEFAULT="gnulinux-advanced-b5b06d70-ea98-45ab-be8a-55b2fcec9baf>gnulinux-4.19.105+-advanced-b5b06d70-ea98-45ab-be8a-55b2fcec9baf"
```

1.2) In terminal:

```
# update-grub

# reboot
```
   
2.1) Load the MPTCP modules and inital setup (Note: see _mptcp_enable.sh / _mptcp_disable.sh):

```
#ls /lib/modules/4.19.105+/kernel/net/mptcp

#lsmod

modprobe mctcp_desync

#modprobe mptcp_balia

#modprobe mptcp_binder

modprobe mptcp_blest

#modprobe mptcp_coupled

modprobe mptcp_fullmesh

#modprobe mptcp_ndiffports

modprobe mptcp_netlink

#modprobe mptcp_olia

modprobe mptcp_redundant

modprobe mptcp_rr

modprobe mptcp_wvegas

#cat /proc/sys/net/ipv4/tcp_congestion_control

sysctl -w net.mptcp.enabled=1

sysctl -w net.ipv4.tcp_congestion_control=olia  

sysctl -w net.mptcp.mptcp_path_manager=fullmesh

echo 5 > /sys/module/mptcp_fullmesh/parameters/num_subflows

sysctl -p  (Nota: carrega tambem o que estah em /etc/sysctl.conf) 
```


2.2) (Optional) Visualize MPTCP setup (See: _mptcp_visualizer.sh)

```
#List the operating system settings

#cat /etc/os-release
   
#List all system variables

sysctl -a

#Verify the available TCP congestion control

#cat /proc/sys/net/ipv4/tcp_congestion_control
```

2.3) (Optional) Load a new TCP congestion control (See: _mptcp_enable.sh  / _mptcp_disable.sh)

```
#modprobe balia

#Setup the new MPTCP congestion control

sysctl -w net.ipv4.tcp_congestion_control=balia

#Setup the topology manager

sysctl -w net.mptcp.mptcp_path_manager=fullmesh

#Reload the changes

sysctl -p
```

2.4 (Optional) Update the number of MPTCP subflows: (See: _mptcp_enable.sh / _mptcp_disable.sh)

```
echo $subflows > /sys/module/mptcp_fullmesh/parameters/num_subflows
```

2.5) (Optional) Setup the MPTCP scheduler (e.g. default, roundrobin or redundant): (See: _mptcp_enable.sh / _mptcp_disable.sh)

```
sysctl -w net.mptcp.mptcp_scheduler=default

sysctl -p
```

2.6) Disable MPTCP flows (See: _mptcp_disable.sh):
```
sysctl -w net.mptcp.mptcp_enabled=0
```

3) OpenDaylight Karaf (ODL) 0.8.4 (Note: the next steps were not tested in more recent versions of ODL):

3.1) (Optional) Restart setup (if Karaf crashes):

```
karaf clean
```

3.2) Run ODL:
```
karaf
```

3.3) Install ODL plugins (See: _karaf_plugins_para_instalar.txt)

```
feature:install odl-dluxapps-applications odl-dlux-core odl-dluxapps-nodes odl-dluxapps-yangui odl-mdsal-apidocs odl-mdsal-all odl-l2switch-all odl-l2switch-switch odl-l2switch-switch-ui odl-l2switch-switch-rest odl-neutron-service odl-neutron-northbound-api odl-neutron-hostconfig-ovs
```

4) Mininet

4.1) Run https://github.com/lpdc/lpdc/blob/master/LPDC.py

4.2) (Optional) For MPTCP tests in Mininet by command line:

```
mn --topo tree,2 --controller remote,ip=10.0.0.10,port=6653 --switch=ovsk,protocols=OpenFlow13

mn --custom scenario.py --topo scenario --controller remote,ip=127.0.0.1,port=6653 --switch=ovsk,protocols=OpenFlow13
```

4.3) (Optional) MPTCP example in Mininet:

```
#!/usr/bin/python2
#
# To run: ./scenario.py
#
# Note: controller port for OpenDaylight: 6633
#
#                 H1
#            (0)     (1)
#             /        \ 
#          (1)         (1)
#           S1(3)---(3)S2
#          (2)         (2)
#            |          |
#          (2)         (2)
#           S3(3)---(3)S4
#          (1)         (1)
#             \        /
#            (0)     (1)
#                 H2
#                 
from mininet.net import Mininet
from mininet.node import Controller,RemoteController,OVSKernelSwitch,UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link,TCLink

def topology():
    net = Mininet(controller=RemoteController, link=TCLink,switch=OVSKernelSwitch)
    print('Creating nodes')
    h1 = net.addHost('h1',ip='10.10.10.10/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2',ip='10.10.10.30/24', mac='00:00:00:00:00:02')
    s1 = net.addSwitch('s1', listenPort=6671, mac='00:00:00:00:00:03')
    s2 = net.addSwitch('s2', listenPort=6672, mac='00:00:00:00:00:04')
    s3 = net.addSwitch('s3', listenPort=6673, mac='00:00:00:00:00:03')
    s4 = net.addSwitch('s4', listenPort=6674, mac='00:00:00:00:00:04')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    print('Creating links')

    #Note: zero port is for controller in the switches
    
    #net.addLink(h1,s1,0,1) #h1 port 0---s1 in port 1
    Link(h1,s1, intfName1='h1-eth0')
    net.addLink(s1,s3,2,2)
    net.addLink(h2,s3,0,1)
    
    Link(h1,s2, intfName2='h1-eth1')
    net.addLink(s2,s4,2,2)
    net.addLink(h2,s4,1,1)

    net.addLink(s1,s2,3,3)
    net.addLink(s3,s4,3,3)

    
    h1.cmd('ifconfig h1-eth0 10.10.10.10/24')
    h1.cmd('ifconfig h1-eth1 10.10.20.10/24')
    h2.cmd('ifconfig h2-eth0 10.10.10.30/24')
    h2.cmd('ifconfig h2-eth1 10.10.20.30/24')
    
    h1.cmd('ip route add 10.10.10.0/24 dev h1-eth0 scope link table 1')
    h1.cmd('ip route add default via 10.10.10.30 dev h1-eth0 table 1')
    h1.cmd('ip route add 10.10.20.0/24 dev h1-eth1 scope link table 2')
    h1.cmd('ip route add default via 10.10.20.30 dev h1-eth1 table 2')
    h1.cmd('ip route add default scope global nexthop via 10.10.10.30 dev h1-eth0')
    h1.cmd('ip rule add from 10.10.10.10 table 1')
    h1.cmd('ip rule add from 10.10.20.10 table 2')

    h2.cmd('ip route add 10.10.10.0/24 dev h2-eth0 scope link table 1')
    h2.cmd('ip route add default via 10.10.10.10 dev h2-eth0 table 1')
    h2.cmd('ip route add 10.10.20.0/24 dev h2-eth1 scope link table 2')
    h2.cmd('ip route add default via 10.10.20.10 dev h2-eth1 table 2')
    h2.cmd('ip route add default scope global nexthop via 10.10.10.10 dev h2-eth0')
    h2.cmd('ip rule add from 10.10.10.30 table 1')
    h2.cmd('ip rule add from 10.10.20.30 table 2')
    
    print('Starting network')
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])

    print('Running CLI')
    CLI(net)

    print('Stopping network')
    net.stop()
    
if __name__ == '__main__':
    setLogLevel('info')
    topology()

```

4.4) (Optional) Manual network setup for hosts in Mininet:
```
h1 ifconfig h1-eth0 10.10.10.10/24
h1 ifconfig h1-eth1 10.10.20.10/24
h1 ip route add 10.10.10.0/24 dev h1-eth0 scope link table 1
h1 ip route add default via 10.10.10.30 dev h1-eth0 table 1
h1 ip route add 10.10.20.0/24 dev h1-eth1 scope link table 2
h1 ip route add default via 10.10.20.30 dev h1-eth1 table 2
h1 ip route add default scope global nexthop via 10.10.10.30 dev h1-eth0
h1 ip rule show
h1 ip rule add from 10.10.10.10 table 1
h1 ip rule add from 10.10.20.10 table 2
h1 ip rule show
h1 ip route
h1 ip route show table 1
%-----------------------
h2 ifconfig h2-eth0 10.10.10.30/24
h2 ifconfig h2-eth1 10.10.20.30/24
h2 ip route add 10.10.10.0/24 dev h2-eth0 scope link table 1
h2 ip route add default via 10.10.10.10 dev h2-eth0 table 1
h2 ip route add 10.10.20.0/24 dev h2-eth1 scope link table 2
h2 ip route add default via 10.10.20.10 dev h2-eth1 table 2
h2 ip route add default scope global nexthop via 10.10.10.10 dev h2-eth0
h2 ip rule show
h2 ip rule add from 10.10.10.30 table 1
h2 ip rule add from 10.10.20.30 table 2
h2 ip rule show
h2 ip route
h2 ip route show table 1
```

4.5) (Optional) Open terminals in Mininet environment:
```
   h1 xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T h1
   h2 xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T h2
```

4.6) (Optional) Run iperf in Mininet hosts:

```
h2: iperf -s
h1: iperf -c 10.10.10.20 -t 100
```

5) (Optional) Use Wireshark to verify MPTCP subflows.

6) (Optional) Iperf3multi (See the folder _mininet_scripts_).

Iperf3multi is a function written in Python that simultaneously runs iperf3 between
each host instantiated in Mininet. (Based on: http://www.muzixing.com/pages/2015/02/22/fattree-topo-and-iperfmulti-function-in-mininet.html)

You can edit iperf3multi as follow:

```
Edit the file: mininet/mininet/net.py (Look for iperf3multi)

Edit the file: mininet/mininet/cli.py (Look for iperf3multi)

Edit this file to include the new command in Mininet: mininet/bin/mn (Look for iperf3multi)

Run in terminal to update the changes in Mininet:

mininet/util/install -n
```

7) (Optional) Graphics with Gnuplot (See the folder _scripts_MPTCP_)

## For internal development (only):

git init

git add *

git commit -m "Release"

git rm --cached .gitignore~

git remote add origin https://github.com/lpdc/lpdc.git

git push origin master


