import requests, json

# Fungsi untuk mendapatkan daftar DNS records dari Cloudflare
def list_dns_records(api_key, zone_id):
    """
    Mengambil daftar DNS records dari Cloudflare dan menampilkannya dalam format [DNS TYPE] <name>.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    # Header untuk autentikasi
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Mengirim request GET ke Cloudflare API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        dns_records = response.json().get('result', [])
        if dns_records:
            for i, record in enumerate(dns_records, start=1):
                print(f"{i}. [{record['type']}] {record['name']}")
            return dns_records
        else:
            print("No DNS records found.")
            return []
    else:
        print(f"Failed to retrieve DNS records. Status code: {response.status_code}, Response: {response.text}")
        return []

# Fungsi untuk memilih dan mengedit DNS record
def edit_dns_record(api_key, zone_id, dns_records):
    """
    Memilih DNS record yang akan diedit, dan mengirim perubahan ke Cloudflare API.
    """
    try:
        record_index = int(input("\nSelect DNS record number to edit: ")) - 1
        if record_index < 0 or record_index >= len(dns_records):
            print("Invalid selection.")
            return
        
        selected_record = dns_records[record_index]

        # Menampilkan record yang dipilih
        print(f"\nEditing [{selected_record['type']}] {selected_record['name']}:")

        # Meminta input untuk mengedit berdasarkan tipe record
        if selected_record['type'] == "SRV":
            service = input(f"Enter service (default: {selected_record['data']['service']}): ") or selected_record['data']['service']
            proto = input(f"Enter protocol (default: {selected_record['data']['proto']}): ") or selected_record['data']['proto']
            name = input(f"Enter name (default: {selected_record['data']['name']}): ") or selected_record['data']['name']
            priority = input(f"Enter priority (default: {selected_record['data']['priority']}): ") or selected_record['data']['priority']
            weight = input(f"Enter weight (default: {selected_record['data']['weight']}): ") or selected_record['data']['weight']
            port = input(f"Enter port (default: {selected_record['data']['port']}): ") or selected_record['data']['port']
            target = input(f"Enter target (default: {selected_record['data']['target']}): ") or selected_record['data']['target']
            ttl = input(f"Enter TTL (default: {selected_record['ttl']}): ") or selected_record['ttl']

            # Membuat JSON data baru
            updated_record = {
                "type": "SRV",
                "name": selected_record['name'],
                "data": {
                    "service": service,
                    "proto": proto,
                    "name": name,
                    "priority": int(priority),
                    "weight": int(weight),
                    "port": int(port),
                    "target": target
                },
                "ttl": int(ttl)
            }

        elif selected_record['type'] == "TXT":
            content = input(f"Enter content (default: {selected_record['content']}): ") or selected_record['content']
            ttl = input(f"Enter TTL (default: {selected_record['ttl']}): ") or selected_record['ttl']

            updated_record = {
                "type": "TXT",
                "name": selected_record['name'],
                "content": content,
                "ttl": int(ttl)
            }

        else:
            content = input(f"Enter content (default: {selected_record['content']}): ") or selected_record['content']
            ttl = input(f"Enter TTL (default: {selected_record['ttl']}): ") or selected_record['ttl']
            proxied = input(f"Enable proxy for this record? (y/n, default: {'y' if selected_record.get('proxied', False) else 'n'}): ").lower() == 'y'

            updated_record = {
                "type": selected_record['type'],
                "name": selected_record['name'],
                "content": content,
                "ttl": int(ttl),
                "proxied": proxied
            }

        # Mengirim perubahan ke Cloudflare API
        update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{selected_record['id']}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.put(update_url, headers=headers, data=json.dumps(updated_record))

        if response.status_code == 200:
            print(f"\nDNS record {updated_record['name']} successfully updated.")
        else:
            print(f"\nFailed to update DNS record. Status code: {response.status_code}, Response: {response.text}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except KeyError:
        print("Unexpected response format from Cloudflare.")

# Fungsi utama
def main():
    """
    Fungsi utama yang menjalankan keseluruhan proses.
    Meminta input API key dan zone ID dari pengguna, menampilkan daftar DNS records, dan mengedit record.
    """
    # Meminta input untuk API key dan zone_id dari pengguna
    api_key = input("Enter your Cloudflare API key: ")
    zone_id = input("Enter your Cloudflare zone ID: ")

    # Meminta daftar DNS records
    dns_records = list_dns_records(api_key, zone_id)

    # Jika ada DNS records, lanjutkan untuk edit
    if dns_records:
        edit_dns_record(api_key, zone_id, dns_records)

# Menjalankan fungsi utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
