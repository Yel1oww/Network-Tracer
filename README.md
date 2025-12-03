Network Tracer: TCP Port Scanner

Network Tracer is a TCP port scanner built in Python.

Key Features

IP Range Support: Supports scanning single IP addresses or entire network ranges specified using CIDR notation (e.g., 192.168.1.0/24).

Service Identification: Attempts to resolve the common service name (e.g., HTTP, SSH, FTP) associated with open ports.

Comprehensive Reporting: Provides a summary report, total scan time, and a detailed, easy-to-read breakdown of all discovered open ports per host.

Prerequisites

To run Network Tracer, you need the following installed on your system:

Python 3.6+

Operating System: Linux, macOS, or Windows.

This script uses standard Python libraries (socket, ipaddress, threading, time) and requires no external dependencies beyond the Python interpreter itself.

Installation

git clone https://github.com/Yel1oww/Network-Tracer

Since all necessary libraries are standard, you can run the script directly:

python3 network_tracer.py


License

This project is licensed under the MIT License - see the LICENSE file for details.
