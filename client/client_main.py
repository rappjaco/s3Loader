import sys
from client_auth import user_login_init
from client_s3 import list_files, upload_file

if len(sys.argv) < 2:
    print("Please provide action argument")
    sys.exit(0)

if sys.argv[1] == "login":
    print("Logging in")
    response = user_login_init()

elif sys.argv[1] == "list":
    response = list_files()
    print(response)
elif sys.argv[1] == "upload":
    if len(sys.argv) < 3:
        print("Provide absolute path to file")
    else: 
        response = upload_file(sys.argv[2])
        print(response)

else:
    print("Argument not a valid action option")
