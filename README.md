# MBH DNS Finder

**A lightweight, Python-based DNS reconnaissance and IP discovery tool.**

MBH DNS Finder is a command-line tool designed to retrieve DNS records, discover IP addresses, and resolve common subdomains associated with a target domain.

Built with Python, it features an ASCII terminal interface, multithreaded DNS lookups, IPv4/IPv6 support, and automatic TXT report generation.

## Features

- **DNS Enumeration** — Retrieve A, AAAA, MX, and NS records.
- **IP Discovery** — Identify IPv4 and IPv6 addresses.
- **Subdomain Discovery** — Resolve a predefined list of common subdomains.
- **Multithreaded Scanning** — Perform concurrent DNS lookups for faster results.
- **Duplicate Removal** — Generate a unique list of discovered IP addresses.
- **Report Export** — Automatically save scan results to a TXT file.
- **Windows Support** — Launch the tool using a `.bat` file.
- **Interactive CLI** — Simple terminal interface featuring an ASCII banner.

## Requirements

- Python 3.9 or newer
- pip
- Internet connection
- Windows for the batch launcher (Python script also supports other operating systems)

**Python dependency:**

```text
dnspython
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/marco3bh/MBH-DNS-Finder.git
cd MBH-DNS-Finder
```


### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Alternatively:

```bash
python -m pip install dnspython
```

## Usage

### Windows

Double-click `start.bat` or execute:

```cmd
start.bat
```

### Linux / macOS

Run the Python script directly:

```bash
python3 main.py
```

### Scan a domain

1. Select `[1] START DNS SCAN`.
2. Enter a domain, for example `example.com`.
3. The tool performs DNS lookups and displays discovered IP addresses.
4. Results are automatically exported to a TXT file.

## Example Output

```text
MBH DNS FINDER v1.0
DNS RECONNAISSANCE TOOL
--------------------------------

[1] START DNS SCAN
[0] EXIT

MBH > 1

[?] Enter domain: example.com

[+] TARGET: example.com
[+] Caricamento record DNS...
[+] Avvio DNS lookup...

=================================================================
 DNS RESULTS
=================================================================

[+] example.com
    IPv4: 192.0.2.10
    IPv6: 2001:db8::10

[+] api.example.com
    IPv4: 192.0.2.20

=================================================================
 UNIQUE IP ADDRESSES
=================================================================

  [+] 192.0.2.10
  [+] 192.0.2.20
  [+] 2001:db8::10

[+] Host risolti: 2
[+] IP unici: 3
[+] Risultati salvati: dns_results_example.com.txt
```

*The addresses above are illustrative documentation examples, not live DNS results.*

## How It Works

MBH DNS Finder uses the `dnspython` library to resolve publicly available DNS information.

The tool follows these steps:

1. Validates and normalizes the supplied domain.
2. Retrieves MX and NS records.
3. Generates candidate hostnames from a predefined subdomain list.
4. Resolves A and AAAA records using a thread pool.
5. Groups discovered IP addresses by hostname.
6. Removes duplicate IP addresses.
7. Displays results and exports them to a TXT report.

**Note:** The tool performs DNS-based discovery, not exhaustive subdomain enumeration. DNS responses may include third-party CDN, email, and DNS provider infrastructure rather than servers owned by the target organization.

## Limitations

- Uses a predefined subdomain wordlist.
- Does not perform brute-force DNS enumeration.
- Does not guarantee discovery of every IP address or subdomain.
- Does not identify origin servers behind CDNs or reverse proxies.
- Does not scan ports or test vulnerabilities.

## Disclaimer

This project is intended for educational purposes, network administration, and authorized security reconnaissance.

Only assess infrastructure you own or have permission to evaluate. The author is not responsible for misuse.
