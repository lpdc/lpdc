#!/bin/bash

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: this script enable MPTCP in Ubuntu 20.04.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

modprobe mctcp_desync;modprobe mptcp_balia;modprobe mptcp_binder;modprobe mptcp_blest;modprobe mptcp_coupled;modprobe mptcp_fullmesh;modprobe mptcp_ndiffports;modprobe mptcp_netlink;modprobe mptcp_olia;modprobe mptcp_redundant;modprobe mptcp_rr;modprobe mptcp_wvegas

sysctl -w net.mptcp.mptcp_enabled=1
sysctl -w net.mptcp.mptcp_path_manager=fullmesh
#sysctl -w net.mptcp.mptcp_path_manager=ndiffports
#sysctl -w net.ipv4.tcp_congestion_control=olia
sysctl -w net.ipv4.tcp_congestion_control=cubic
#sysctl -w net.mptcp.mptcp_path_manager=default
echo 8 > /sys/module/mptcp_fullmesh/parameters/num_subflows

dmesg | grep MPTCP
echo "MPTCP_ENABLED: "
cat /proc/sys/net/mptcp/mptcp_enabled
echo "MPTCP congestion control: "
cat /proc/sys/net/ipv4/tcp_congestion_control
echo "MPTCP path manager: "
cat /proc/sys/net/mptcp/mptcp_path_manager
echo "MPTCP scheduler: "
cat /proc/sys/net/mptcp/mptcp_scheduler
echo "NUM SUBFLOWS: "
cat /sys/module/mptcp_fullmesh/parameters/num_subflows 
