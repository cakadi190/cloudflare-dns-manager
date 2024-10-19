import msvcrt
from addbydns import main as add_by_dns
from convertjson import main as convert_json
from adddnsmanual import main as add_dns_manual
from listdns import main as list_dns
from editdns import main as edit_dns
from deletedns import main as delete_dns

def main():
    options = [
        "Add by DNS",
        "Convert JSON",
        "Add DNS Manually",
        "List DNS",
        "Edit DNS",
        "Delete DNS",
        "Exit"
    ]
    
    current_option = 0

    while True:
        print("\033[H\033[J", end='')  # Membersihkan layar

        ascii_art = r"""
 __        __        __   ___            __   ___     __        __                           __   ___  __  
/  ` |    /  \ |  | |  \ |__  |     /\  |__) |__     |  \ |\ | /__`     |\/|  /\  |\ |  /\  / _` |__  |__) 
\__, |___ \__/ \__/ |__/ |    |___ /~~\ |  \ |___    |__/ | \| .__/     |  | /~~\ | \| /~~\ \__> |___ |  \ 
        """

        print(ascii_art)
        print("Cloudflare DNS Manager")
        print("By Catatan Cak Adi\n")

        for idx, option in enumerate(options):
            if idx == current_option:
                print(f"-> {option}")  # Tandai pilihan yang aktif
            else:
                print(f"   {option}")

        key = msvcrt.getch()  # Mendapatkan input dari keyboard

        if key == b'\xe0':  # Menangani tombol arah
            key = msvcrt.getch()
            if key == b'H' and current_option > 0:  # Tombol arah atas
                current_option -= 1
            elif key == b'P' and current_option < len(options) - 1:  # Tombol arah bawah
                current_option += 1
        elif key == b'\r':
            if current_option == 0:
                add_by_dns()
            elif current_option == 1:
                convert_json()
            elif current_option == 2:
                add_dns_manual()
            elif current_option == 3:
                list_dns()
            elif current_option == 4:
                edit_dns()
            elif current_option == 5:
                delete_dns()
            elif current_option == 6:
                print("\nThank you for using my tools! See you next time!")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user (CTRL+C).")
