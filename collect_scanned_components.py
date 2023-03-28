import os, re

# Config
base_path = "/data/home/cv-admin/"
csv_path = "ip_addresses_to_purge.csv"

# Helper function: write SQL query to path
def write_sql_query(query, path):
    with open(base_path + path, "w") as f:
        f.write(query)

# Helper function: execute SQL query from path
def launch_sql_query_from_path(path, component_ips=False):
    print("Starting SQL query from path...")
    stream = os.popen("sbs-db load " + path)
    if component_ips:
        with open(f"{base_path}{csv_path}" ,'w') as f:
            while True:
                line = stream.readline().strip()
                if is_ip_address(line):
                    f.write(line + "\n")
                if not line:
                    break
    else:
        output = stream.read()
        print("SQL query response: " + output)
        return output

# Helper function: check for IP address
def is_ip_address(line):
    return re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line)

### 1. Find creation time (START) ###
def write_get_creation_time():
    query = """
    WITH alltags AS (
                SELECT tag.id
                FROM tag
                JOIN category ON
                        tag.category_id = category.id
                        AND category.label IN ('Device - Level 0-1', 'Device - Level 2', 'Device - Level 3-4', 'Software', 'System')
                        AND tag.t_type = 'component'
        )
        SELECT COUNT(DISTINCT d.id) AS counted, d.creation_time
        FROM device AS d
        WHERE EXISTS (
                        SELECT 1 FROM component_internal AS c
                        INNER JOIN component_device ON component_device.component_id = c.id
                        WHERE component_device.device_id = d.id AND c.last_active_time BETWEEN (NOW() - '60 days'::interval) AND NOW()
                ) AND EXISTS (
                        SELECT 1 FROM component_internal AS c
                        INNER JOIN component_tag ON component_tag.component_id = c.id
                        INNER JOIN component_device ON component_device.component_id = c.id
                        WHERE component_device.device_id = d.id AND component_tag.tag_id IN (SELECT id FROM alltags)
                )
        GROUP BY d.creation_time
        ORDER BY counted DESC
        LIMIT 20;
    """
    write_sql_query(query, "get_creation_time.sql")

def get_creation_time():
    write_get_creation_time()
    launch_sql_query_from_path(base_path + "get_creation_time.sql")
    creation_time = input("Copy creation time to delete components for: ").strip()
    return creation_time
### 1. Find creation time (END) ###

### 2. Find component IPs (START) ###
def write_get_component_ips(creation_time):
    query = """
    SELECT DISTINCT c.ip
    FROM component AS c
    WHERE CAST(c.creation_time AS varchar) LIKE """ + "'" + creation_time[:10] + "%'" + """;
    """
    write_sql_query(query, "get_component_ip.sql")

def get_component_ips(creation_time):
    print("Getting IP addresses for selected creation time...")
    write_get_component_ips(creation_time)
    launch_sql_query_from_path(base_path + "get_component_ip.sql", component_ips=True)
    print("... Done")
    print(f"Consult IP address list in {base_path}{csv_path}, in this directory")
### 2. Find component IPs (END) ###

### 3. Cleanup (START) ###
def cleanup():
    os.remove(base_path + "get_creation_time.sql")
    os.remove(base_path + "get_component_ip.sql")
### 3. Cleanup (END) ###

# Main script
if __name__ == "__main__":
    # 1. Find out creation time
    creation_time = get_creation_time()

    # 2. Find component IPs
    get_component_ips(creation_time)

    # 3. Cleanup
    cleanup()