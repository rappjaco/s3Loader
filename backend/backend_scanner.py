import socket
import os
import re
from backend_upload import upload_file_s3
from sqlmodel import SQLModel, Field, Session, create_engine, select

CLAM_AV_PORT = 3310
CLAM_AV_HOST = "localhost"
CLAM_AV_HOST_CONNECTION = (CLAM_AV_HOST, CLAM_AV_PORT)
SCAN_DIR = "/tmp/scan_dir/"

engine = create_engine("sqlite:///./sqlite.db")
SQLModel.metadata.create_all(engine)

class ScanBase(SQLModel):
    uploaded_by_user: str = Field(index=True)
    scan_complete: bool = Field(default=False)
    scan_passed: bool = Field(default=False)
    file_name: str = Field(index=True)

class Scan(ScanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class Scanner:
    def __init__(self, filename, user_email):
        self.filename = filename
        self.user_email = user_email
        self.scan_complete = False
        self.scan_passed = False

    def scanner_init(self):
        scan_results = self.clam_av_scan()
        if scan_results: 
            self.scanner_audit(scan_complete=True)
        virus_found = re.search(b"FOUND", scan_results)
        if virus_found:
            print(f"VIRUS FOUND: {self.filename}")
            self.delete_file()
        else:
            print(f"CLEAN: {self.filename}")
            self.scanner_audit(scan_passed=True)
            upload_file_s3(self.filename)
            self.delete_file()

    def delete_file(self):
        try:
            os.remove(f"{SCAN_DIR}{self.filename}")
        except Exception as e:
            return {f"error: {e}"}
    
    def scanner_audit(self, scan_complete=False, scan_passed=False):
        
        def audit_updater(scan_dict, update=False):
            with Session(engine) as session:
                if update:
                    statement = select(Scan).where(Scan.file_name == self.filename)
                    results = session.exec(statement)
                    scan = results.one()
                    scan.scan_complete = self.scan_complete
                    scan.scan_passed = self.scan_passed
                    session.add(scan)
                    session.commit()
                    session.refresh(scan)
                else:
                    valid_scan_model = Scan.model_validate(scan_dict)
                    session.add(valid_scan_model)
                    session.commit()
                    session.refresh(valid_scan_model)

        scan_dict = {
            "uploaded_by_user": self.user_email,
            "file_name": self.filename
        }
        if scan_complete:
            scan_dict["scan_complete"] = True
            self.scan_complete = True
            audit_updater(scan_dict, update=True)
            return True
        if scan_passed:
            scan_dict["scan_passed"] = True
            self.scan_passed = True
            audit_updater(scan_dict, update=True)
            return True
        audit_updater(scan_dict)
        


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
