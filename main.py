
import os
import re
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlsplit

import dns.resolver
import dns.exception


SUBDOMAINS = [
    "www", "mail", "smtp", "imap", "pop",
    "ftp", "api", "dev", "test", "staging",
    "app", "admin", "portal", "dashboard",
    "vpn", "remote", "blog", "shop",
    "cdn", "static", "webmail", "autodiscover",
    "ns1", "ns2", "cpanel", "www2"
]

resolver = dns.resolver.Resolver()
resolver.timeout = 1.5
resolver.lifetime = 3


def banner():
    os.system("cls" if os.name == "nt" else "clear")

    print(r"""
 __  __ ____  _   _   ____  _   _ ____
|  \/  | __ )| | | | |  _ \| \ | / ___|
| |\/| |  _ \| |_| | | | | |  \| \___ \
| |  | | |_) |  _  | | |_| | |\  |___) |
|_|  |_|____/|_| |_| |____/|_| \_|____/

 _____ ___ _   _ ____  _____ ____
|  ___|_ _| \ | |  _ \| ____|  _ \
| |_   | ||  \| | | | |  _| | |_) |
|  _|  | || |\  | |_| | |___|  _ <
|_|   |___|_| \_|____/|_____|_| \_\

        MBH DNS FINDER v1.0
       DNS RECONNAISSANCE TOOL
    --------------------------------
    """)


def normalize_domain(value):
    value = value.strip().lower()

    if not value:
        raise ValueError("Inserisci un dominio.")

    if "://" not in value:
        value = "http://" + value

    hostname = urlsplit(value).hostname

    if not hostname:
        raise ValueError("Dominio non valido.")

    hostname = hostname.rstrip(".").encode("idna").decode("ascii")

    if len(hostname) > 253 or not re.fullmatch(
        r"(?=.{1,253}$)[a-z0-9-]+(?:\.[a-z0-9-]+)+",
        hostname
    ):
        raise ValueError("Formato del dominio non valido.")

    if any(part.startswith("-") or part.endswith("-")
           or len(part) > 63 for part in hostname.split(".")):
        raise ValueError("Dominio non valido.")

    return hostname


def query(host, record_type):
    try:
        return resolver.resolve(host, record_type)
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.exception.Timeout,
        dns.exception.DNSException,
    ):
        return []


def find_ips(host):
    found = set()

    for record_type in ("A", "AAAA"):
        for answer in query(host, record_type):
            found.add(str(answer))

    return found


def find_dns_hosts(domain):
    hosts = {}

    for record in query(domain, "MX"):
        host = str(record.exchange).rstrip(".").lower()
        hosts.setdefault(host, set()).add("MX")

    for record in query(domain, "NS"):
        host = str(record.target).rstrip(".").lower()
        hosts.setdefault(host, set()).add("NS")

    return hosts


def ip_sort(ip):
    address = ipaddress.ip_address(ip)
    return address.version, int(address)


def scan(domain):
    print(f"\n[+] TARGET: {domain}")
    print("[+] Caricamento record DNS...")

    dns_hosts = find_dns_hosts(domain)

    hosts = {domain}
    hosts.update(f"{sub}.{domain}" for sub in SUBDOMAINS)
    hosts.update(dns_hosts)

    print(f"[+] Host da controllare: {len(hosts)}")
    print("[+] Avvio DNS lookup...\n")

    results = {}

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(find_ips, host): host
            for host in hosts
        }

        for future in as_completed(futures):
            host = futures[future]

            try:
                ips = future.result()
            except Exception:
                ips = set()

            if ips:
                results[host] = ips

    unique_ips = set()

    print("=" * 65)
    print(" DNS RESULTS")
    print("=" * 65)

    if not results:
        print("\n[-] Nessun indirizzo IP trovato.")
        return

    lines = [
        f"MBH DNS FINDER - {domain}",
        "=" * 65
    ]

    for host in sorted(results, key=lambda h: (h != domain, h)):
        ips = sorted(results[host], key=ip_sort)
        unique_ips.update(ips)

        labels = dns_hosts.get(host, set())
        label = f" [{', '.join(sorted(labels))}]" if labels else ""

        print(f"\n[+] {host}{label}")
        lines.append(f"\n{host}{label}")

        for ip in ips:
            version = ipaddress.ip_address(ip).version
            print(f"    IPv{version}: {ip}")
            lines.append(f"    IPv{version}: {ip}")

    print("\n" + "=" * 65)
    print(" UNIQUE IP ADDRESSES")
    print("=" * 65)

    lines.append("\n" + "=" * 65)
    lines.append("UNIQUE IP ADDRESSES")

    for ip in sorted(unique_ips, key=ip_sort):
        print(f"  [+] {ip}")
        lines.append(ip)

    print("\n" + "=" * 65)
    print(f"[+] Host risolti: {len(results)}")
    print(f"[+] IP unici:    {len(unique_ips)}")

    filename = f"dns_results_{domain}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")

    print(f"[+] Risultati salvati: {filename}")
    print("=" * 65)


def main():
    while True:
        banner()

        print("[1] START DNS SCAN")
        print("[0] EXIT")

        choice = input("\nMBH > ").strip()

        if choice == "0":
            break

        if choice != "1":
            continue

        raw = input("\n[?] Enter domain: ")

        try:
            domain = normalize_domain(raw)
            scan(domain)
        except ValueError as error:
            print(f"\n[!] {error}")
        except KeyboardInterrupt:
            print("\n[!] Scansione interrotta.")

        input("\nPremi INVIO per continuare...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Uscita.")
