import requests, inquirer, getpass

# Fungsi untuk mendapatkan daftar DNS records dari Cloudflare
def list_dns_records(api_key, zone_id):
    """
    Mendapatkan daftar DNS records dari Cloudflare.
    Mengembalikan daftar records jika berhasil, atau None jika gagal.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Failed to retrieve DNS records. Status code: {response.status_code}, Response: {response.text}")
        return None

# Fungsi untuk menghapus DNS record dari Cloudflare
def delete_dns_record(api_key, zone_id, record_id):
    """
    Menghapus satu DNS record dari Cloudflare menggunakan API.
    Mencetak status keberhasilan atau kegagalan penghapusan record.
    """
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Mengirim request DELETE ke Cloudflare API
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print(f"Record with ID {record_id} deleted successfully.")
    else:
        print(f"Failed to delete record with ID {record_id}. Status code: {response.status_code}, Response: {response.text}")

# Fungsi utama untuk meminta input dan menjalankan program
def main():
    """
    Fungsi utama yang menjalankan keseluruhan proses.
    Meminta input API key dan zone ID dari pengguna, kemudian menghapus DNS record.
    """
    # Meminta input untuk API key dan zone_id dari pengguna
    api_key = getpass.getpass("Enter your Cloudflare API key: ")
    zone_id = getpass.getpass("Enter your Cloudflare zone ID: ")

    # Mendapatkan dan menampilkan daftar DNS records
    dns_records = list_dns_records(api_key, zone_id)
    
    if dns_records:
        choices = [
            f"{record['name']} ({record['id']})"  # Menyimpan ID di dalam string tapi tidak ditampilkan
            for record in dns_records
        ]

        # Menggunakan inquirer untuk memilih record yang ingin dihapus
        questions = [
            inquirer.Checkbox(
                'records',
                message="Select DNS records to delete:",
                choices=choices,
            ),
        ]
        
        answers = inquirer.prompt(questions)

        if answers and 'records' in answers:
            # Menyimpan ID dari pilihan yang dipilih dalam variabel
            record_ids_to_delete = [
                choice.split('(')[-1].strip(')')  # Mengambil ID dari string
                for choice in answers['records']
            ]

            for record_id in record_ids_to_delete:
                delete_dns_record(api_key, zone_id, record_id)
        else:
            print("No records selected for deletion.")
    else:
        print("No DNS records found.")

# Menjalankan fungsi utama
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
