import requests, json, os

# Fungsi untuk memuat data dari file JSON
def load_dns_records(filename="add-dns.json"):
    """
    Memuat DNS records dari file JSON.
    Mengembalikan daftar records jika berhasil, atau None jika gagal.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: Unable to parse {filename}. Please ensure the file contains valid JSON.")
            return None
    else:
        print(f"Error: {filename} not found.")
        return None

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
    if record['type'] == 'A' or record['type'] == 'CNAME':
        record['proxied'] = True

    # Mengirim request POST ke Cloudflare API
    response = requests.post(url, headers=headers, data=json.dumps(record))
    
    # Menangani response
    if response.status_code == 200:
        print(f"Record {record['name']} added successfully.")
    else:
        print(f"Failed to add record {record['name']}. Status code: {response.status_code}, Response: {response.text}")

# Fungsi untuk memproses semua DNS records
def process_dns_records(api_key, zone_id, dns_records):
    """
    Memproses dan menambahkan setiap DNS record dalam daftar dns_records ke Cloudflare.
    """
    if dns_records:
        for record in dns_records:
            add_dns_record(api_key, zone_id, record)
    else:
        print("No DNS records to add. Please check your add-dns.json file.")

# Fungsi utama untuk meminta input dan menjalankan program
def main():
    """
    Fungsi utama yang menjalankan keseluruhan proses.
    Meminta input API key dan zone ID dari pengguna, kemudian menambahkan DNS records.
    """
    # Meminta input untuk API key dan zone_id dari pengguna
    api_key = input("Enter your Cloudflare API key: ")
    zone_id = input("Enter your Cloudflare zone ID: ")

    # Memuat DNS records dari file add-dns.json (default)
    dns_records = load_dns_records()

    # Memproses DNS records jika data berhasil dimuat
    process_dns_records(api_key, zone_id, dns_records)

# Menjalankan fungsi utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
