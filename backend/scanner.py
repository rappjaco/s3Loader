import socket
import os, re
from upload import upload_file_s3

CLAM_AV_PORT = 3310
CLAM_AV_HOST = "localhost"
CLAM_AV_HOST_CONNECTION = (CLAM_AV_HOST, CLAM_AV_PORT)
SCAN_DIR = "/tmp/scan_dir/"


class Scanner: 
    def __init__(self, filename: str):
        self.filename = filename
    def scanner_init(self):
        scan_results = self.clam_av_scan()
        virus_found = re.search(b"FOUND", scan_results)
        if virus_found:
            print(f"VIRUS FOUND: {self.filename}")
            self.delete_file()
        else:
            print(f"CLEAN: {self.filename}")
            upload_file_s3(self.filename)
            self.delete_file()

    def delete_file(self):
        try: 
            os.remove(f"{SCAN_DIR}{self.filename}")
        except Exception as e:
            return {f"error: {e}"}
        

    def clam_av_scan(self) -> bytes:
        try:
            _scanner_file = f"nSCAN {SCAN_DIR}{self.filename}\n"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(CLAM_AV_HOST_CONNECTION)
            s.send(_scanner_file.encode("utf-8"))
            clamav_byte_response = s.recv(2048)
            return clamav_byte_response
        except Exception as e:
            return {f"error:{e}"}
    
    
