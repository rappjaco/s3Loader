import socket
import os
import re
from backend_upload import upload_file_s3
from sqlmodel import SQLModel, Field, Session, create_engine

CLAM_AV_PORT = 3310
CLAM_AV_HOST = "localhost"
CLAM_AV_HOST_CONNECTION = (CLAM_AV_HOST, CLAM_AV_PORT)
SCAN_DIR = "/tmp/scan_dir/"

engine = create_engine("sqlite:///./sqlite.db")
SQLModel.metadata.create_all(engine)

class ScanBase(SQLModel):
    uploaded_by_user: str = Field(index=True)
    file_name: str = Field(index=True)

class Scan(ScanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Scanner:
    def __init__(self, filename, user_email):
        self.filename = filename
        self.user_email = user_email

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
    
    def scanner_audit(self):
        scan_dict = {
            "uploaded_by_user": self.user_email,
            "file_name": self.filename
        }
        with Session(engine) as session:
            valid_scan_model = Scan.model_validate(scan_dict)
            if valid_scan_model:
                session.add(valid_scan_model)
                session.commit()
                session.refresh(valid_scan_model)
            return Exception("Unable to add scan to DB")


    def clam_av_scan(self):
        try:
            _scanner_file = f"nSCAN {SCAN_DIR}{self.filename}\n"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(CLAM_AV_HOST_CONNECTION)
            s.send(_scanner_file.encode("utf-8"))
            clamav_byte_response = s.recv(2048)
            return clamav_byte_response
        except Exception as e:
            return {f"error:{e}"}
