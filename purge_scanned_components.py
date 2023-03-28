import os, re

# Config
base_path = "/data/home/cv-admin/"
csv_path = "ip_addresses_to_purge.csv"

# Helper function: run purge-components command for given IP address
def purge_component(ip_address):
    command = f"sbs-db purge-components --network {ip_address}/32"
    os.system(command)

# Helper function: check for IP address
def is_ip_address(line):
    return re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line)

# Main script
if __name__ == "__main__":
    print(f"Purging components listed in {base_path}{csv_path}...")
    with open(f"{base_path}{csv_path}", "r") as f:
        for line in f.readlines():
            if is_ip_address(line.strip()):
                purge_component(line.strip())
    print(f"... Done.")