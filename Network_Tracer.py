import asyncio
import ipaddress
import socket
import time

# Timeout settings (seconds)
LOCAL_TIMEOUT = 1
INTERNET_TIMEOUT = 2

# Limit how many concurrent scans happen at once
MAX_CONCURRENT = 1200

# Store results
open_ports_results = {}
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

# Progress tracking
progress = {
    "total": 0,
    "scanned": 0
}

# Lock for progress updating
progress_lock = asyncio.Lock()


def update_progress():
    percent = (progress["scanned"] / progress["total"]) * 100
    bar_length = 30
    filled = int(percent / 100 * bar_length)
    bar = "█" * filled + "-" * (bar_length - filled)

    print(
        f"\rProgress: |{bar}| {percent:6.2f}% "
        f"({progress['scanned']}/{progress['total']})",
        end="",
        flush=True
    )


async def scan_port(ip, port, timeout):
    try:
        async with semaphore:
            conn = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)

            try:
                service_name = socket.getservbyport(port, "tcp")
            except:
                service_name = "unknown"

            port_info = f"{port} ({service_name.upper()})"

            if ip not in open_ports_results:
                open_ports_results[ip] = []

            open_ports_results[ip].append(port_info)

            writer.close()
            await writer.wait_closed()

    except:
        pass

    # Update progress
    async with progress_lock:
        progress["scanned"] += 1
        update_progress()


async def scan_host(ip, start_port, end_port, timeout):
    queue = asyncio.Queue()

    for port in range(start_port, end_port + 1):
        await queue.put(port)

    async def worker():
        while not queue.empty():
            port = await queue.get()
            await scan_port(ip, port, timeout)
            queue.task_done()

    workers = []
    for _ in range(MAX_CONCURRENT):
        workers.append(asyncio.create_task(worker()))

    await queue.join()

    for w in workers:
        w.cancel()


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


# ------------------ MAIN ------------------

print_banner()
print("Welcome to Network Tracer")

target_input = input(
    "Enter Target IP or IP range (e.g., 192.168.1.1 or 192.168.1.0/24): "
).strip()

while True:
    network_choice = input(
        "Select scan type:\n1) Local network scan\n2) Internet/External scan\nEnter choice: "
    )

    if network_choice == "1":
        scan_timeout = LOCAL_TIMEOUT
        break
    elif network_choice == "2":
        scan_timeout = INTERNET_TIMEOUT
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")

# Validate targets
try:
    if "/" in target_input:
        network = ipaddress.ip_network(target_input, strict=False)
        target_ips = [str(ip) for ip in network.hosts()]
    else:
        ipaddress.ip_address(target_input)
        target_ips = [target_input]
except ValueError:
    print("Invalid IP or network.")
    exit()

# Ports
try:
    start_port = int(input("Enter Start Port: "))
    end_port = int(input("Enter End Port: "))
except ValueError:
    print("Ports must be numbers.")
    exit()

if start_port > end_port or start_port < 1 or end_port > 65535:
    print("Invalid port range.")
    exit()

progress["total"] = len(target_ips) * (end_port - start_port + 1)

print(f"\nScanning {len(target_ips)} host(s), ports {start_port}-{end_port}")
print(f"Max concurrency: {MAX_CONCURRENT}\n")

update_progress()

start_time = time.time()


async def main():
    jobs = []
    for ip in target_ips:
        jobs.append(
            asyncio.create_task(scan_host(ip, start_port, end_port, scan_timeout))
        )
    await asyncio.gather(*jobs)


asyncio.run(main())

# Final Report
total_time = time.time() - start_time
total_open_ports = sum(len(ports) for ports in open_ports_results.values())

print("\n\n" + "=" * 50)
print(f"✅ Scan finished in {total_time:.2f} seconds")
print(f"✅ Found {total_open_ports} open port(s) on {len(open_ports_results)} host(s)")
print("=" * 50)

if open_ports_results:
    for ip, ports in open_ports_results.items():
        print(f"\nHost: {ip}")
        print(f"  Open Ports: {', '.join(sorted(ports))}")
else:
    print("\nNo open ports found.")

print("\n" + "=" * 50)
