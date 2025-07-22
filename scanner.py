import socket
import ipaddress
import time
import argparse
import sys

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\nERROR IN USING THE PROGRAM: {message}")
        print(
            "Usage: python scanner.py --host <IP_address/domain> --ports <ports>no spaces --delay <delay> --timeout <timeout>")
        print("For detailed help and description of the program, use: python scanner.py --help")
        sys.exit(2)


parser = CustomArgumentParser(description='This program scans the given IP address or domain for open ports in the specified range..')
parser.add_argument('--host',required=True,help='IP address or domain')
parser.add_argument('--ports',required=True,type=str, help='Ports')
parser.add_argument('--delay', type=float, default=0.5, help='Delay between ports (in seconds)(default 0.5).')
parser.add_argument('--timeout', type=float, default=0.5, help='Port connection timeout in seconds (default 0.5)')

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
open_ports = 0
close_ports = 0

def ports_function():
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
    return ports_list

wait_time = args.delay
ports_list = ports_function()
start_time = time.time()
print(f"Scanning host {host} ({ip}) for port {ports_list}")

for port in ports_list:

  a= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  a.settimeout(args.timeout)

  try:
      wynik = a.connect_ex((ip, port))
      if wynik == 0:
          print(f"Port {port}: OPEN!")
          open_ports += 1
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
      a.close()
time.sleep(wait_time)

end_time = time.time()
czas = int(end_time - start_time)
minutes = czas // 60
seconds = czas % 60




print("\n--------------------------------------------------")
print("<< Scan Completed >>")
print(f"Number of open ports: {open_ports}, closed/filtered: {close_ports}!")
print(f"Scanning time: {minutes} min {seconds} sec")
print("--------------------------------------------------")


