import sys
from client_auth import user_login

if len(sys.argv) < 2:
    print("Please provide action argument")
    sys.exit(0)


if sys.argv[1] == "login":
    print("Logging in")
    user_login()
else:
    print("Argument not a valid action option")
