#!/bin/bash

# Intra Data Center MultiPath Optimization with
# Emulated Software Defined Networks
#
# Description: this script disable MPTCP in Ubuntu 20.04.
# 
# Author: Lucio A. Rocha
# Last update: 23/11/2020

sysctl -w net.mptcp.mptcp_enabled=0
