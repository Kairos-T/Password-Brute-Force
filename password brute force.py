import itertools
import time
import sys
import concurrent.futures

def crack_password(password):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    max_length = 10

    for n in range(1, max_length + 1):
        for test in itertools.product(chars, repeat=n):
            test = "".join(test)
            if test == password:
                return test

    return None

def progress_report(progress):
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('=' * int(progress), progress))
    sys.stdout.flush()

def divide_workload(length_range, num_processes):
    workload = [list() for _ in range(num_processes)]
    for i, length in enumerate(length_range):
        workload[i % num_processes].append(length)
    return workload

def process_workload(lengths):
    results = []
    for length in lengths:
        result = crack_password(password)
        if result:
            return result
        progress = length / max_length * 100
        progress_report(progress)
    return None

def main():
    password = input("Enter a password: ")
    max_time = 60

    length_range = list(range(1, 11))  # Password length range
    num_processes = min(len(length_range), concurrent.futures.cpu_count())

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        workload = divide_workload(length_range, num_processes)
        start_time = time.time()

        future_to_length = {executor.submit(process_workload, workload[i]): workload[i] for i in range(num_processes)}
        completed_futures = []

        while True:
            for future in concurrent.futures.as_completed(future_to_length):
                completed_futures.append(future)
                result = future.result()

                if result:
                    executor.shutdown(wait=False)
                    print("\nPassword cracked! The password you entered is:", result)
                    return

                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    executor.shutdown(wait=False)
                    break

                progress = len(completed_futures) / len(length_range) * 100
                progress_report(progress)

            if len(completed_futures) == num_processes or elapsed_time > max_time:
                break

    print("\nPassword not found within the time limit.")

if __name__ == "__main__":
    main()
