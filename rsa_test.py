import random
import math
import time
import sympy

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
# Extended Euclidean
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_phi == 1:
        return d + phi
# Prime Testing
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True
# Generate Public and Private key pair 
def generate_key_pair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q

    # Phi is the totient of n
    phi = (p-1) * (q-1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private key_pair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [pow(ord(char), key, n) for char in plaintext]
    # Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    aux = [str(pow(char, key, n)) for char in ciphertext]
    # Return the array of bytes as a string
    plain = [chr(int(char2)) for char2 in aux]
    return ''.join(plain)

def set_keys():
    print("===========================================================================================================")
    print("================================== RSA Encryptor / Decrypter ==============================================")
    print(" ")

    p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
    q = int(input(" - Enter another prime number (Not one you entered above): "))

    print(" - Generating your key-pairs now . . .")
    time.sleep(1)

    public, private = generate_key_pair(p, q)

    print(" - Your public key is ", public, " and your private key is ", private)
    return public, private

def simulate_rsa(public, private):
    message = input(" - Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)
    print(" - Your encrypted message is: ", ''.join(map(lambda x: str(x), encrypted_msg)))
    # print(encrypted_msg)
    print(" - Decrypting message with private key ", private, " . . .")
    print(" - Your message is: ", decrypt(private, encrypted_msg))

def encrypt_rsa(public):
    message = input(" - Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)
    cipher = ''.join(map(lambda x: str(x), encrypted_msg))
    print(" - Your encrypted message is: ", cipher)
    return encrypted_msg

def decrypt_rsa(private, encrypted_msg):
    print(" - Decrypting message with private key ", private, " . . .")
    print(" - Your message is: ", decrypt(private, encrypted_msg))

#########################################   Attack 1    ####################################################
def factorize_naive(n):
    # Check if n is even
    if n % 2 == 0:
        return 2, n // 2

    # Find the smallest odd divisor of n
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return i, n // i
        i += 2

    # If n is prime, return n as both factors
    return n, 1

def factorize_sympy(n):
    # Check if n is even
    if n % 2 == 0:
        return 2, n // 2

    # Use sympy's factorint function to factorize n
    factors = sympy.factorint(n)

    # If there are more than two factors, we cannot use them as p and q
    if len(factors) != 2:
        raise ValueError("n cannot be factorized into exactly two prime factors.")

    # Extract the two factors from the dictionary of factors
    p, q = factors.keys()

    # Check that p and q are prime
    if not sympy.isprime(p) or not sympy.isprime(q):
        raise ValueError("p and q are not prime.")

    return p, q

def getPrivateKey(p1, q1, e, n):
    phi = (p1-1)*(q1-1)
    d1 = multiplicative_inverse(e, phi)
    print("Private Key Found: ", d1, ", ", n)

###############################################     Attack 2    ######################################################################

def mod_exp(base, exp, modulus):
    """
    Computes (base^exp) % modulus efficiently using repeated squaring.
    """
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exp = exp // 2
    return result

def findX(n):
    while True:
        x = random.randint(2, n-1)  # Choose a random integer between 2 and n-1
        if gcd(x, n) == 1:          # Check if x is relatively prime to n
            return x

def maliciousDecrypt(mal_cipher, xinv, d, n):
    aux1 = [pow(char, d, n) for char in mal_cipher]
    print("Decrypted Output", aux1)
    print("X_inv: ", xinv)
    aux1 = [ (int(p)*xinv)%n for p in aux1 ]
    print("Transformed Output: ", aux1)
    # aux = [str((pow(char, d, n)*xinv)%n) for char in mal_cipher]
    plain = [chr(int(char2)) for char2 in aux1]
    print("Original Encoded Text: ", ''.join(plain))

def printMenu():
    print("===========================================================================================================")
    print("================================== RSA Attacks Simulation ==============================================")
    print(" ")
    print(
        '''
        Chose the relevant action
        1. Factorization Attack
        2. Chosen Cipher text Attack
        3. 
        4.
        5.
        6. EXIT
        '''
    )
    choice = int(input("Enter your choice: "))
    print(" ")
    print("==========================================================================================================")
    print("======================================================================================================")
    return choice


if __name__ == '__main__':
    pu, pr = set_keys() #pu = (e, n), pr = (d, n)
    # print("Public Key: ", pu)
    # simulate_rsa(pu, pr)
    cipher = encrypt_rsa(pu)
    decrypt_rsa(pr, cipher)
    while True:
        choice = printMenu()
        e = pu[0]
        n = pu[1]
        if choice == 1:
            print("n: ", n)
            print("Naive Factorization: ")
            p1, q1 = factorize_naive(n)
            getPrivateKey(p1, q1, e, n)
            print("factors: ", p1, ", ", q1)
            print("Optimized Sympy Factorization: ")
            p2, q2 = factorize_sympy(n)
            print("factors: ", p2, ", ", q2)
            getPrivateKey(p2, q2, e, n)
            time.sleep(7)
        elif choice == 2:
            x = findX(n)
            print("X: ", x)
            xe = mod_exp(x, e, n)
            print("X^e: ", x)
            print("Cipher: ", cipher)
            mal_cipher = [int((c*xe)%n) for c in cipher]
            print("Malicious Cipher: ", mal_cipher)
            d = pr[0]
            xinv = multiplicative_inverse(x, n)
            maliciousDecrypt(mal_cipher, xinv, d, n)
        elif choice == 3:
            print(3)
        else:
            break
            


    