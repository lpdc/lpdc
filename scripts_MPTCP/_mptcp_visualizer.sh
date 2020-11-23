#!/bin/bash

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: this script show the MPTCP setup in Ubuntu 20.04.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

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
 
