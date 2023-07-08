import itertools
import time
import sys
from multiprocessing import Pool, cpu_count

def crack_password(password):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    max_length = 10

    for n in range(1, max_length+1):
        for test in itertools.product(chars, repeat=n):
            test = "".join(test)
            if test == password:
                return test

    return None

def progress_report(progress):
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('=' * int(progress), progress))
    sys.stdout.flush()

def main():
    password = input("Enter a password: ")
    max_time = 60

    pool = Pool(cpu_count())
    length_range = range(1, 11)

    start_time = time.time()
    results = []
    for length in length_range:
        result = pool.apply_async(crack_password, (password,))
        results.append(result)

        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            break

        progress = length / len(length_range) * 100
        progress_report(progress)

    pool.close()
    pool.join()

    for result in results:
        cracked_password = result.get()
        if cracked_password:
            print("\nPassword cracked! The password you entered is:", cracked_password)
            return

    print("\nPassword not found within the time limit.")

if __name__ == "__main__":
    main()
