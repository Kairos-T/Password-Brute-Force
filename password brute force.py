import itertools
import time
import sys

def crack_password(password, length, max_time):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    start_time = time.time()

    for n in range(1, length+1):
        for test in itertools.product(chars, repeat=n):
            test = "".join(test)
            if test == password:
                return test

            elapsed_time = time.time() - start_time
            if elapsed_time > max_time:
                return None

            progress = n / length * 100
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('=' * int(progress), progress))
            sys.stdout.flush()

    return None


def main():
    password = input("Enter a password: ")
    length = 10
    max_time = 60

    cracked_password = crack_password(password, length, max_time)

    if cracked_password:
        print("\nPassword cracked! The password you entered is:", cracked_password)
    else:
        print("\nPassword not found within the time limit.")


if __name__ == "__main__":
    main()
