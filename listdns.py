import requests, textwrap
from tabulate import tabulate

# Fungsi untuk melakukan wrapping pada kolom yang terlalu panjang
def wrap_text(text, width=30):
    """
    Membungkus teks panjang agar sesuai dengan lebar tabel.
    """
    return "\n".join(textwrap.wrap(text, width=width))

# Fungsi untuk mendapatkan daftar DNS records dari Cloudflare
def list_dns_records(api_key, zone_id):
    """
    Mengambil daftar DNS records dari Cloudflare dan menampilkannya dalam bentuk tabel dengan wrapped content.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    # Header untuk autentikasi
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Mengirim request GET ke Cloudflare API
    response = requests.get(url, headers=headers)
    
    # Menangani response
    if response.status_code == 200:
        dns_records = response.json().get('result', [])
        if dns_records:
            # Menyiapkan data untuk ditampilkan dalam bentuk tabel
            table_data = []
            for record in dns_records:
                # Membungkus teks panjang dalam kolom "Content"
                wrapped_content = wrap_text(record['content'], width=40)
                table_data.append([record['type'], record['name'], wrapped_content, record['ttl']])
            
            # Menampilkan tabel
            print(tabulate(table_data, headers=["Type", "Name", "Content", "TTL"], tablefmt="grid"))
        else:
            print("No DNS records found.")
    else:
        print(f"Failed to retrieve DNS records. Status code: {response.status_code}, Response: {response.text}")

# Fungsi utama untuk meminta input dan menjalankan program
def main():
    """
    Fungsi utama yang menjalankan keseluruhan proses.
    Meminta input API key dan zone ID dari pengguna, kemudian menampilkan daftar DNS records.
    """
    # Meminta input untuk API key dan zone_id dari pengguna
    api_key = input("Enter your Cloudflare API key: ")
    zone_id = input("Enter your Cloudflare zone ID: ")

    # Meminta daftar DNS records
    list_dns_records(api_key, zone_id)

# Menjalankan fungsi utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
