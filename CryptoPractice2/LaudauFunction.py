# Python3 program for the above approach
import sys
import time
 
# To store Landau's function of the number
Landau = -sys.maxsize - 1
 
# Function to return gcd of 2 numbers
def gcd(a, b):
    if (a == 0):
        return b
    return gcd(b % a, a)
 
# Function to return LCM of two numbers
def lcm(a, b):
    return (a * b) // gcd(a, b)
 
# Function to find max lcm value
# among all representations of n
def findLCM(arr):
    global Landau
    nth_lcm = arr[0]
    for i in range(1, len(arr)):
        nth_lcm = lcm(nth_lcm, arr[i])
    # Calculate Landau's value
    Landau = max(Landau, nth_lcm)
     
# Recursive function to find different
# ways in which n can be written as
# sum of atleast one positive integers
def findWays(arr, i, n):
    # Check if sum becomes n,
    # consider this representation
    if (n == 0):
        findLCM(arr)
    # Start from previous element
    # in the representation till n
    for j in range(i, n + 1):
        # Include current element
        # from representation
        arr.append(j)
        # Call function again
        # with reduced sum
        findWays(arr, j, n - j)
        # Backtrack - remove current
        # element from representation
        arr.pop()
     
# Function to find the Landau's function
def Landau_function(n):
    arr = []
    # Using recurrence find different
    # ways in which n can be written
    # as a sum of atleast one +ve integers
    findWays(arr, 1, n)
    # Print the result
    print(Landau)
 
# Driver Code

time_start = time.time()
# Given N
N = 40
 
# Function call
Landau_function(N)
print("Time cost: ", time.time() - time_start)
 
# This code is contributed by chitranayal