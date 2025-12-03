Network Tracer: TCP Port Scanner

Network Tracer is a Python-based TCP port scanner that helps you discover open ports and identify common services on single IPs or entire network ranges.

---

Key Features

IP Range Support: Scan single IP addresses or entire network ranges using CIDR notation (e.g., 192.168.1.0/24).
Service Identification: Attempts to identify common services (HTTP, SSH, FTP, etc.) running on open ports.
Comprehensive Reporting: Generates an easy-to-read report with open ports per host and total scan time.

---

Prerequisites
Python: Version 3.6 or higher
Operating Systems: Linux, macOS, or Windows
Libraries: Uses standard Python libraries (socket, ipaddress, time, etc...) — no external dependencies required

---

Installation

Clone the repository:
git clone https://github.com/Yel1oww/Network-Tracer
cd Network-Tracer

Run the scanner:
python3 network_tracer.py

---

Usage

Simply run the script and follow the prompts to scan a single IP or a network range. The script will output:
Open ports for each host
Common service names for identified ports
Total scan duration

---

License

This project is licensed under the MIT License. See the LICENSE file for details.

---
