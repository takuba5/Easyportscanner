import socket
import ipaddress
import time
import argparse
import sys

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\nERROR IN USING THE PROGRAM: {message}")
        print(
            "Usage: python scanner.py --host <IP_address/domain> --ports <ports>no spaces --delay <delay> --timeout <timeout> --output <filename> ")
        print("For detailed help and description of the program, use: python scanner.py --help")
        sys.exit(2)


parser = CustomArgumentParser(description='This program scans the given IP address or domain for open ports in the specified range..')
parser.add_argument('--host',required=True,help='IP address or domain')
parser.add_argument('--delay', type=float, default=0.5, help='Delay between ports (in seconds)(default 0.5).')
parser.add_argument('--timeout', type=float, default=0.5, help='Port connection timeout in seconds (default 0.5)')
parser.add_argument('--output',type=str,help='Save the results to a txt file')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--ports', type=str, help='Ports (e.g. 22,80,443,1000-2000)')
group.add_argument('--popular', action='store_true', help='Scan 50 most common ports')


args = parser.parse_args()

print("<<Easy network scanner>>")
print("--------------------------------------------------")
print("This program scans the specified IP address or domain for")
print("open ports in the specified range. Use arguments")
print("command line to configure scanning.")
print("--------------------------------------------------")

try:
   host = args.host
   ip = socket.gethostbyname(host)
   ipaddress.ip_address(ip)
except socket.gaierror:
    print(f"ERROR: The hostname '{host}' could not be resolved. Please make sure it is correct.")
    sys.exit(1)
except ValueError:
    print(f"ERROR: {ip} is not a valid IP address.")
    sys.exit(1)
except socket.error as e:
   print(f"ERROR: Can't connect to port: {e}")
   sys.exit(1)
open_ports =[]
close_ports = 0


def save_to_file(filename, host, ip, open_ports, closed_ports, duration_min, duration_sec):
    with open(filename, "w", encoding='utf-8') as file:
        file.write("<< Scan Results >>\n")
        file.write("--------------------------------------------------\n")
        file.write(f"Target Host: {host} ({ip})\n\n")

        file.write(f"Open Ports ({len(open_ports)}):\n")
        if open_ports:

            for i in range(0, len(open_ports), 10):
                file.write("  " + " ".join(map(str, open_ports[i:i + 10])) + "\n")
        else:
            file.write("None\n")

        file.write(f"\nClosed/Filtered Ports: {closed_ports}\n")
        file.write(f"Scanning Time: {duration_min} min {duration_sec} sec\n")
        file.write("--------------------------------------------------\n")
    print(f"\n Results saved to {filename}")



def ports_function():
    if args.popular:
        return sorted([
            20, 21, 22, 23, 25, 53, 67, 68, 69, 80,
            110, 111, 123, 135, 137, 138, 139, 143, 161, 162,
            179, 389, 443, 445, 465, 514, 515, 993, 995, 1080,
            1194, 1433, 1434, 1521, 1723, 2049, 3306, 3389, 5060, 5432,
            5900, 6000, 6379, 6667, 8000, 8080, 8443, 8888, 9000, 10000
        ])
    elif args.ports:
        ports_list = []
        b = args.ports
        items = b.split(',')
        for item in items:
            item = item.strip()
            if '-' in item:
                a = item.split('-')
                if len(a) != 2:
                    print(f"ERROR: Invalid port range format '{item}'.")
                    sys.exit(1)
                try:
                    start = int(a[0])
                    end = int(a[1])
                except ValueError:
                    print(f"ERROR: Invalid port range format '{item}'.")
                    sys.exit(1)
                if start < 0 or start > 65535 or end < 0 or end > 65535:
                    print(f"ERROR: Port range '{item}' is not valid (valid range 0-65535).")
                    sys.exit(1)
                if start > end:
                    print(f"ERROR: Start port is greater than end port in range '{item}'.")
                    sys.exit(1)
                ports_list.extend(range(start, end + 1))
            else:
                try:
                    port = int(item)
                    if port < 0 or port > 65535:
                        print(f"ERROR: {port} is not a valid port number.")
                        sys.exit(1)
                    ports_list.append(port)
                except ValueError:
                    print(f"ERROR: Invalid port '{item}'.")
                    sys.exit(1)
        return sorted(ports_list)


wait_time = args.delay
ports_list = ports_function()
ports_list.sort()
start_time = time.time()
print(f"Scanning host {host} ({ip}) for port {ports_list}")

for port in ports_list:

  a= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  a.settimeout(args.timeout)

  try:
      result = a.connect_ex((ip, port))
      if result == 0:
          print(f"Port {port}: OPEN!")
          open_ports.append(port)
          try:
              banner_bytes = a.recv(1024)
              banner = banner_bytes.decode('utf-8', errors='ignore').strip()
              if banner:
                  print(f"Banner: {banner}")
              else:
                  print(f"No immediate banner received for port {port}.")
          except socket.timeout:

              print(f"No immediate banner received for port {port} (timeout).")
          except socket.error as e:

              print(f"Error receiving banner from port {port}: {e}")
          except UnicodeDecodeError:

              print(f"Received non-UTF-8 banner for port {port}.")
          except Exception as e:
              print(f"An unexpected error occurred while grabbing banner from port {port}: {e}")

      else:
          close_ports += 1
          pass
  except socket.error as e:
      print(f"ERROR: Connection to port {port} failed: {e}")
  finally:
      time.sleep(wait_time)
      a.close()

open_ports.sort()
end_time = time.time()
time = int(end_time - start_time)
minutes = time // 60
seconds = time % 60

if args.output:
    save_to_file(args.output,args.host,ip,open_ports,close_ports,minutes,seconds)





print("\n--------------------------------------------------")
print("<< Scan Completed >>")
print(f"Number of open ports: {open_ports}, closed/filtered: {close_ports}!")
print(f"Scanning time: {minutes} min {seconds} sec")
print("--------------------------------------------------")


