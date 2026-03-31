#!/usr/bin/python3
# Python program to display all the prime numbers within an interval

# Define the range of numbers to check
lower = 1  # Starting point of the range
upper = 500  # Ending point of the range

# Display a message indicating what will be printed
print("Prime numbers between", lower, "and", upper, "are:")

# Iterate through each number in the range [lower, upper]
for num in range(lower, upper + 1):
   # All prime numbers are greater than 1
   # Numbers <= 1 are not prime by definition
   if num > 1:
       # Check if 'num' has any divisors from 2 to num-1
       for i in range(2, num):
           # If num is divisible by i (remainder is 0), it's not prime
           if (num % i) == 0:
               break  # Exit the inner loop, num is not prime
       else:
           # This else belongs to the for loop (not the if)
           # It executes only if the loop completes WITHOUT hitting break
           # This means num has no divisors, so it IS prime
           print(num)  # Print the prime number
