# Daniel Sillar 26879026
import random
import math
import sys

m = int(sys.argv[1])


# n = number to test primality of
# k = accuracy of test (1/(4^k) chance of composite being labelled a prime
# output = 0 if composite, 1 if prime
def miller_rabin(n, k):
    if n % 2 == 0:
        return 0
    s = 0
    t = n-1

    while t % 2 == 0:
        s += 1
        t = t/2

    for j in range(0, k):
        a = random.randint(2, n-2)
        if repeated_squaring(a, n-1, n) != 1:
            return 0
        for i in range(1, s+1):
            # as 2^i is just 1 followed by i zeros in binary, just convert string to binary to save exponentiating
            temp = repeated_squaring(a, 2**(i - 1) * t, n)  # maybe don't convert to binary like this?
            if repeated_squaring(a, 2**i * t, n) % n == 1 \
                    and temp != 1 \
                    and temp != n-1:
                return 0

    return 1


def decimal_to_binary(num):
    return bin(int(num)).replace("0b", "")


def repeated_squaring(base, exponent, modulo):
    bin_exp = str(decimal_to_binary(exponent))
    # set initial number we will be multiplying powers we care about by
    if bin_exp[-1] == '1':
        ans = base
    else:
        ans = 1
    # repeated squaring, multiplying the values we care about to cur
    cur = base
    for digit in range(len(bin_exp) - 2, -1, -1):
        cur = cur**2 % modulo
        # if the digit is a 1 in the binary, need to multiply this value to the return
        if bin_exp[digit] == '1':
            ans = ans*cur % modulo

    return ans


def find_twin_prime(m):
    # c2 = 0.6601618158  # from wikipedia, the assignment sheet is missing the 0 (3rd significant digit)
    # expected = (2*c2*2**m-1)/((math.log(2**m-1))**2) - (2*c2*2**(m-1))/((math.log(2**(m-1)))**2)

    # as m = 2 gives range 2-3 which is not large enough to have a pair, m<3
    if m < 3:
        raise Exception('m must be greater than 2')

    # with m >= 3, every pair must be (6x-1, 6x+1), hence only gen rand multiples of 6 in range, and check either side
    low_bound = 2**(m-1)
    # get lower bound of the random number generator
    if (low_bound + 2) % 6 == 0:
        rand_min = (low_bound + 2)/6
    else:
        rand_min = (low_bound + 4)/6

    upper_bound = 2**m - 1
    # get upper bound of random number generator
    if (upper_bound - 1) % 6 == 0:
        rand_max = (upper_bound - 1)/6
    else:
        rand_max = (upper_bound - 3)/6

    while True:
        # get a random multiple of 6 in range
        mult_six = 6 * random.randint(rand_min, rand_max)

        # 1/(4^k) chance of incorrect prime labelling, over range of 2^(m-1) - 1 numbers. hence if k = sqrt(m), there is
        # expected to be 1/(2^(m-1) - 1) chance of incorrectly returning prime. This equates to 1 incorrect return over
        # the range. however we are only sampling 1/6 of the range, so actually 1/6 chance of incorrect prime label.
        # want > 1% wrong return, so will make k = 3*sqrt(m) [4^3 = 64, 64*6 = 384, hence approx 1/384 wrong label]
        if miller_rabin(mult_six - 1, 3*math.floor(math.sqrt(m))) == 1:
            if miller_rabin(mult_six + 1, 3*math.floor(math.sqrt(m))) == 1:
                return mult_six - 1, mult_six + 1


# print(miller_rabin(101, 3))
# print(find_twin_prime(7))
f = open('output_twin_prime.txt', 'w')
first_prime, second_prime = find_twin_prime(m)
f.write(str(first_prime) + '\n' + str(second_prime))
f.close()
