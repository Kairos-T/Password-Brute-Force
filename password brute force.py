import itertools
import time
import sys

password  = input("Enter a password: ")
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
length =  10 
max_time = 60 
start_time = time.time()

for n in range(1, length+1):
    for test in itertools.product(chars, repeat=n):
        test = "". join(test)
        if test == password:
            print("Password cracked! The password you have input is: ", test)
            sys.exit()
        
        elapsed_time = time.time() - start_time
        if elapsed_time > max_time:
            print("Time limit exceeded.")
            time.sleep(2)
            sys.exit

        progress = n / length * 100
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('=' * int(progress), progress))
        sys.stdout.flush()

print("\nPassword not found.")