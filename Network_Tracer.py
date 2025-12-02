import socket
import ipaddress
import threading
import time

# Results are stored here
open_ports_results = {}

# Ensures that only one thread can modify at a time preventing corruption
results_lock = threading.Lock()

# Ensures that output from different threads doesn't overlap
print_lock = threading.Lock()

# Define timeout constants
LOCAL_TIMEOUT = 1 # Shorter timeout for fast local networks
INTERNET_TIMEOUT = 2 # Longer timeout for slower Internet scans


# Scanning Function
def port_scan(ip, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        result = s.connect_ex((ip, port))
        
        if result == 0:
            service_name = "Unknown"
            try:
                service_name = socket.getservbyport(port, 'tcp')
            except OSError:
                pass
            
            port_info = f"{port} ({service_name.upper()})"
            
            with print_lock:
                print(f"[{ip}] Port {port}: Open") 
                
            with results_lock:
                if ip not in open_ports_results:
                    open_ports_results[ip] = []
                open_ports_results[ip].append(port_info)
        
        s.close()
        
    except Exception:
        pass
    
# ASCII Art Banner
def print_banner():
    banner = r"""
 _   _      _                      _      _____                       
| \ | |    | |                    | |    |_   _|                      
|  \| | ___| |___      _____  _ __| | __   | |_ __ __ _  ___ ___ _ __ 
| . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ /   | | '__/ _` |/ __/ _ \ '__|
| |\  |  __/ |_ \ V  V / (_) | |  |   <    | | | | (_| | (_|  __/ |   
\_| \_/\___|\__| \_/\_/ \___/|_|  |_|\_\   \_/_|  \__,_|\___\___|_|  
"""
    print(banner)

# Input Handling
print_banner()
print("Welcome to Network Tracer (TCP Scanner), what ip or ip range do you want me to scan?")
target_input = input("Enter Target IP or IP range (e.g., 192.168.1.1 or 192.168.1.0/24): ")

while True:
    network_choice = input("Select scan type:\n1) Local network scan\n2) Internet/External scan\nEnter choice: ")
    
    if network_choice == '1':
        scan_timeout = LOCAL_TIMEOUT
        print(f"Set scan timeout to {scan_timeout} seconds.")
        break
    elif network_choice == '2':
        scan_timeout = INTERNET_TIMEOUT
        print(f"Set scan timeout to {scan_timeout} seconds.")
        break
    else:
        print("Invalid choice. Please enter '1' for Local or '2' for Internet.")

try:
    if '/' in target_input:
        network = ipaddress.ip_network(target_input, strict=False)
        target_ips = [str(ip) for ip in network.hosts()] 
    else:
        ipaddress.ip_address(target_input)
        target_ips = [target_input]

except ValueError:
    print("Invalid IP address or network range format. Exiting.")
    exit()

try:
    start_port = int(input("Enter Start Port: "))
    end_port = int(input("Enter End Port: "))
except ValueError:
    print("Invalid input. Ports must be numbers. Exiting.")
    exit()

if start_port > end_port or start_port < 1 or end_port > 65535:
    print("Invalid port range. Exiting.")
    exit()

# Scan Execution
print(f"\nStarting TCP scan for target: {target_input} ({len(target_ips)} host(s))")
print(f"Scanning ports {start_port} through {end_port}...")

start_time = time.time()

threads = []

for ip in target_ips:
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=port_scan, args=(ip, port, scan_timeout))
        threads.append(thread)
        thread.start()

try:
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    print("\nScan interrupted by user.")


# Final Report
end_time = time.time()
total_time = end_time - start_time
total_open_ports = sum(len(ports) for ports in open_ports_results.values())

print("\n" + "="*50)
print(f"✅ TCP Scan finished in {total_time:.2f} seconds.")
print(f"Summary: Found {total_open_ports} open port(s) across {len(open_ports_results)} host(s).")
print("="*50)
print("")

if open_ports_results:
    for ip, ports in open_ports_results.items():
        print(f"Host: {ip}")
        print(f"  Open Ports: {', '.join(sorted(ports))}") 
        print() 
else:
    print("No open ports found in the specified range.")

print("="*50)