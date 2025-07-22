#Easyportscanner

Description:
Easyportscanner is a simple port scanner written in Python, designed for educational and authorized network security testing.
Important Information

This tool is designed solely for educational purposes and authorized network testing.
Unauthorized or illegal use of this program is strictly prohibited and may result in legal action.
The author is not liable for any damages resulting from improper use of this tool.
By using Easyportscanner, you agree to comply with applicable laws.

Requirements

Python 3.x (no additional external libraries)

Operating system with a terminal/console (Linux, macOS, Windows)

Installation and Launch

Download the scanner.py file from the repository.

Open the terminal/console.

Navigate to the directory containing the scanner.py file.

Run the scanner using the command:

python scanner.py --host <IP_address_or_domain> [options]


## Available Options

| Argument   | Description                                                                                  |
|------------|----------------------------------------------------------------------------------------------|
| `--host`   | Required. The IP address or domain name to scan                                              |
| `--ports`  | List of ports to scan, e.g., `22,80,443` or a range like `1000-2000`                         |
| `--popular`| Scans the 50 most popular ports (does not require `--ports`)                                |
| `--delay`  | Delay between scanning ports (in seconds). Default is 0.5                                   |
| `--timeout`| Timeout for connecting to a port (in seconds). Default is 0.5                               |
| `--output` | Saves the scan results to a specified text file                                             |
           


