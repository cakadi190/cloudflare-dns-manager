import requests

# Fungsi untuk menambahkan DNS record ke Cloudflare
def add_dns_record(api_key, zone_id, record):
    """
    Menambahkan satu DNS record ke Cloudflare menggunakan API.
    Mencetak status keberhasilan atau kegagalan penambahan record.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    # Header untuk autentikasi
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Mengaktifkan proxy untuk jenis A dan CNAME
    if record['type'] in ['A', 'CNAME']:
        record['proxied'] = True

    # Mengirim request POST ke Cloudflare API
    response = requests.post(url, headers=headers, json=record)
    
    # Menangani response
    if response.status_code == 200:
        print(f"Record {record['name']} added successfully.")
    else:
        print(f"Failed to add record {record['name']}. Status code: {response.status_code}, Response: {response.text}")

# Fungsi untuk meminta input dari pengguna untuk DNS record
def get_dns_record_input():
    """
    Meminta input dari pengguna untuk membuat DNS record baru.
    Mengembalikan dictionary yang berisi informasi DNS record.
    """
    record_type = input("Enter DNS record type (A, AAAA, CNAME, MX, TXT, SRV): ").strip().upper()
    name = input("Enter DNS record name: ").strip()
    ttl = int(input("Enter TTL (in seconds): ").strip())
    
    if record_type in ['A', 'AAAA', 'CNAME']:
        content = input("Enter record content (IP address or CNAME): ").strip()
        return {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": ttl
        }
    elif record_type == 'MX':
        priority = int(input("Enter MX record priority: ").strip())
        content = input("Enter MX record content (mail server): ").strip()
        return {
            "type": record_type,
            "name": name,
            "priority": priority,
            "content": content,
            "ttl": ttl
        }
    elif record_type == 'TXT':
        content = input("Enter TXT record content: ").strip()
        return {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": ttl
        }
    elif record_type == 'SRV':
        service = input("Enter service (e.g., _http): ").strip()
        proto = input("Enter protocol (e.g., _tcp): ").strip()
        priority = int(input("Enter priority: ").strip())
        weight = int(input("Enter weight: ").strip())
        port = int(input("Enter port: ").strip())
        target = input("Enter target (e.g., mail.example.com): ").strip()
        return {
            "type": record_type,
            "name": name,
            "data": {
                "service": service,
                "proto": proto,
                "name": name,
                "priority": priority,
                "weight": weight,
                "port": port,
                "target": target
            },
            "ttl": ttl
        }
    else:
        print("Invalid DNS record type. Please enter A, AAAA, CNAME, MX, TXT, or SRV.")
        return None

# Fungsi utama untuk meminta input dan menjalankan program
def main():
    """
    Fungsi utama yang menjalankan keseluruhan proses.
    Meminta input API key dan zone ID dari pengguna, kemudian menambahkan DNS records.
    """
    # Meminta input untuk API key dan zone_id dari pengguna
    api_key = input("Enter your Cloudflare API key: ")
    zone_id = input("Enter your Cloudflare zone ID: ")

    # Loop untuk menambahkan DNS records
    while True:
        print("\nAdding a new DNS record:")
        dns_record = get_dns_record_input()
        if dns_record:
            add_dns_record(api_key, zone_id, dns_record)

        # Tanya apakah ingin menambah record lagi
        another = input("Do you want to add another DNS record? (y/n): ").strip().lower()
        if another != 'y':
            break

# Menjalankan fungsi utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
