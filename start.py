import random
import math
import time
import sympy
from math import gcd
import string
import matplotlib.pyplot as plt
from functools import reduce
import streamlit as st
import numpy as np

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT

def define_dashboard_config():
	st.set_page_config(
		layout="wide",  
		initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
		page_title='ATTACKS ON TEXTBOOK RSA', 
		page_icon=":desktop_computer:",  
	)

	col_1, col_2 = st.columns([3,1])
	# with col_1:
	# 	st.title('Automotive Data Analysis')
	with col_2:
		st.text(time.strftime("%Y-%m-%d %H:%M"))

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

def set_keys():
    # print("===========================================================================================================")
    # print("================================== RSA Encryptor / Decrypter ==============================================")
    # print(" ")

    # p = int(input(" - Enter a prime number (17, 19, 23, etc): "))
    # q = int(input(" - Enter another prime number (Not one you entered above): "))

    p = st.number_input('Enter a prime number (17, 19, 23, etc)',value=17)
    q = st.number_input('Enter another prime number (Not one you entered above)',value=19)

    # st.write('The current number is ', number)

    st.write(" - Generating your key-pairs now . . .")
    time.sleep(1)

    public, private = generate_key_pair(p, q)

    st.write(" - Your public key is ", public, " and your private key is ", private)
    return public, private

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

def encrypt_rsa(public,key):
    # message = input(" - Enter a message to encrypt with your public key: ")
    message = st.text_input('Enter a message to encrypt with your public key',key=key)


    encrypted_msg = encrypt(public, message)
    charCipher = [chr(ascii_val) for ascii_val in encrypted_msg]
    cCipher = ''.join(map(lambda x: str(x), charCipher))
    st.write(cCipher)
    cipher = ''.join(map(lambda x: str(x), encrypted_msg))
    st.write(" - Your encrypted message is: ", cipher)

    return encrypted_msg

def printAfterJoin(arr):
    plain = [str(c) for c in arr]
    st.write(''.join(plain))

def decrypt_rsa(private, encrypted_msg):
    st.write(" - Cipher Text: ")
    printAfterJoin(encrypted_msg)
    st.write(" - Decrypting message with private key ", private, " . . .")
    st.write(" - Your message is: ", decrypt(private, encrypted_msg))

def simulate_RSA(pu,pr):
    # pu, pr = set_keys() #pu = (e, n), pr = (d, n)
    key="simulate_RSA"
    cipher = encrypt_rsa(pu,key)
    decrypt_rsa(pr, cipher)

# ----------------------------------------------------------------------------------------------------------------------------------------
#########################################   FACTORISATION ATTACK    ####################################################
def factorization_attack(pu):
    e = pu[0]
    n = pu[1]

    st.write("n: ", n)
    st.write("Naive Factorization: ")
    p1, q1 = factorize_naive(n)
    getPrivateKey(p1, q1, e, n)
    st.write("factors: ", p1, ", ", q1)
    st.write("Optimized Sympy Factorization: ")
    p2, q2 = factorize_sympy(n)
    st.write("factors: ", p2, ", ", q2)
    getPrivateKey(p2, q2, e, n)

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
    st.write("Private Key Found: ", d1, ", ", n)


###############################################     CHOSEN CIPHER TEXT ATTACK    ######################################################################

def ccta(pu,pr):
    e = pu[0]
    n = pu[1]

    x = findX(n)
    st.write("X: ", x)
    xe = mod_exp(x, e, n)
    st.write("X^e: ", xe)
    key="ccta"
    cipher = encrypt_rsa(pu,key)
    st.write("Cipher: ", cipher)
    printAfterJoin(cipher)
    mal_cipher = [int((c*xe)%n) for c in cipher]
    st.write("Malicious Cipher: ", mal_cipher)
    printAfterJoin(mal_cipher)
    d = pr[0]
    xinv = multiplicative_inverse(x, n)
    maliciousDecrypt(mal_cipher, xinv, d, n)
    
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
def printAfterJoin(arr):
    plain = [str(c) for c in arr]
    st.write(''.join(plain))


def maliciousDecrypt(mal_cipher, xinv, d, n):
    aux1 = [pow(char, d, n) for char in mal_cipher]
    st.write("Decrypted Output", aux1)
    printAfterJoin(aux1)
    st.write("X_inv: ", xinv)
    aux1 = [ (int(p)*xinv)%n for p in aux1 ]
    st.write("Transformed Output: ", aux1)
    printAfterJoin(aux1)
    # aux = [str((pow(char, d, n)*xinv)%n) for char in mal_cipher]
    plain = [chr(int(char2)) for char2 in aux1]
    st.write("Original Encoded Text: ", ''.join(plain))

###############################################     CYCLIC ATTACK    ######################################################################
def cyclic_attack(pu):
    msg = st.text_input("Enter Sample message: ")
    arrEncrypted = encrypt(pu, msg)
    origCipher = ''.join(map(lambda x: str(x), arrEncrypted))
    st.write(cyclicEncrypt(arrEncrypted, pu, origCipher))

def strings_are_equal(string1, string2):
    return string1 == string2

def cyclicEncrypt(cipher, pu, origCipher):
    e, n = pu
    cipher = [pow(c, e, n) for c in cipher]
    currCipher = ''.join(map(lambda x: str(x), cipher))
    prevCipher = cipher
    while(strings_are_equal(currCipher, origCipher) == False):
        prevCipher = cipher
        cipher = [pow(c, e, n) for c in cipher]
        currCipher = ''.join(map(lambda x: str(x), cipher))
        st.write("Cipher ", currCipher)
    plain = [chr(int(char2)) for char2 in prevCipher]
    return ''.join(plain)


###############################################     Attack 4     ######################################################################
# def known_len(pu):
#   msg = input("Enter a four digit pin: ")
#   msg= str(msg)
#   arrEncrypted = encrypt(pu, msg)
#   origCipher = ''.join(map(lambda x: str(x), arrEncrypted))
#   print("entered pin was: ",attack_len(arrEncrypted, pu, origCipher))


# def attack_len(cipher, pu, origCipher):
#   random_pins=[]
#   for i in range(10):
#     for j in range(10):
#         for k in range(10):
#             for l in range(10):
#                 random_pin = int(f"{i}{j}{k}{l}")
#                 random_pin= str(random_pin)
#                 random_pins.append(random_pin)
#   for pin in random_pins:
#     arrEncrypt = encrypt(pu, pin)
#     pinEncrypt = ''.join(map(lambda x: str(x), arrEncrypt))
#     if(pinEncrypt==origCipher):
#       break

#   return pin

###############################################     CRT   ######################################################################
def CRT(pu,pr):
  a=[]
  m=[]
  for i in range(3):
    # pu, pr = set_keys() #pu = (e, n), pr = (d, n)
    e,n= pu
    pu= 3,n
    key=f"CRT{i}"
    cipher = encrypt_rsa(pu,key)
    a.append(cipher)
    m.append(n)

  ans=[]
  size= len(a[0])
  for i in range (0,size):
    ciphers=[]
    for sublist in a:
      ciphers.append(sublist[i])
    ans.append(round(chinese_remainder_theorem(ciphers,m)))
  string = ''.join(chr(code) for code in ans)
  st.write("original text is:", string)


def chinese_remainder_theorem(ciphertexts, moduli):
    if len(ciphertexts) != len(moduli):
        raise ValueError('the number of ciphertexts must be equal to the number of moduli')
    n = reduce(lambda a, b: a * b, moduli)
    result = 0
    for i in range(len(ciphertexts)):
        ni = n // moduli[i]
        xi = modinv(ni, moduli[i])
        result += ciphertexts[i] * ni * xi
    return round((result% n) **(1/3))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    else:
        return x % m


def extended_euclidean_algorithm(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_euclidean_algorithm(b, a % b)
        return d, y, x - (a // b) * y

#######################################     GUESS LENGTH PIN    ######################################################
# ['0000','0001'...........]
def generate_n_digit_numbers(n):
    """
    Generates n-digit numbers starting from 0 as strings.
    """
    if n < 1:
        return []

    # Calculate the maximum number for n digits
    max_num = 10 ** n

    # Generate the numbers
    numbers = []
    for num in range(max_num):
        numbers.append(f"{num:0{n}}")
    return numbers

def attackLength(cipher, pu, origCipher, n):
  random_pins = generate_n_digit_numbers(n)
  for pin in random_pins:
    arrEncrypt = encrypt(pu, pin)
    pinEncrypt = ''.join(map(lambda x: str(x), arrEncrypt))
    if(pinEncrypt==origCipher):
      return pin
  

def knownLengthAttack(pu):
  msg = st.number_input("Enter n digit pin: ",value=5894)
  msg= str(msg)
  arrEncrypted = encrypt(pu, msg)
  origCipher = ''.join(map(lambda x: str(x), arrEncrypted))
  n = int(st.number_input("Enter guessed Password length: ",value=4))
  st.write("entered pin was: ",attackLength(arrEncrypted, pu, origCipher, n))

#######################################################     TIME BASED ATTACK   ###################################################
def generatePlot(x, y1, y2):
    fig = plt.figure(figsize = (10,5))
    plt.plot(x,y1, label="Encryption")
    plt.plot(x,y2, label="Decryption")
   

    max_ticks = 30

    if(len(x)>max_ticks):
        x_ticks = np.arange(0,len(x),5, dtype=int)
    else:
        x_ticks = x

    plt.xticks(ticks=x_ticks, labels=x_ticks, rotation =0)

    plt.xlabel('Length of PT')
    plt.ylabel('Time')

    plt.title('Comparative analysis for time required in encryption and decryption of RSA')

    plt.legend()
    # plt.show()
    st.write(fig)


def generate_random_string(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def timeBasedAttack(pu, pr):
    n = int(st.number_input("Enter your analysis range: ",value=20))
    letter = []
    enc = []
    dec = []
    for i in range (1, n):
        letter.append(i)
        stime = time.time()
        arrEncrypted = encrypt(pu, generate_random_string(i))
        charCipher = [chr(ascii_val) for ascii_val in arrEncrypted]
        # print(charCipher)
        etime = time.time()
        enc.append(etime-stime)
        stimed = time.time()
        decrypted = decrypt(pr, arrEncrypted)
        # print(decrypted)
        etimed = time.time()
        dec.append(etimed - stimed)
    generatePlot(letter, enc, dec )
    # print(letter)
    # print(enc)
    # print(dec)

# =====================================================================================================================================
def attacks(pu,pr):

    # pu, pr = set_keys()

    # e = pu[0]
    # n = pu[1]

    tab1, tab2, tab3,tab4,tab5,tab6 = st.tabs(["Factorization Attack",
        "Chosen Cipher text Attack","Cyclic Attack","Guess Length Pin",
        "Timing Based Attack","CRT attack"])

    with tab1:
        st.header("Factorization Attack")
        factorization_attack(pu)
        
        
        # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("Chosen Cipher text Attack")
        ccta(pu,pr)

    with tab3:
        st.header("Cyclic Attack")
        cyclic_attack(pu)

    with tab4:
        st.header("Guess Length Pi")
        knownLengthAttack(pu)

    with tab5:
        st.header("Timing Based Attack")
        timeBasedAttack(pu, pr)

    with tab6:
        st.header("CRT attack")
        CRT(pu,pr)

def main():	

    define_dashboard_config()

    plt.style.use('dark_background')

    # First sidebar
    with st.sidebar:
        st.sidebar.title("Set Keys")
        pu,pr = set_keys()
        # st.sidebar.write("This is the content of the first sidebar.")
        # Set properties for the first sidebar

    # Main content
    st.title("RSA")

    # Second Sidebar
    menu = ["About", "RSA Encryptor-Decrypter", "RSA Attacks Simulation"]
    st.sidebar.title("Menu")
    choice = st.sidebar.selectbox("Menu",menu)  

    if choice=="About":
        with st.container():
            st.subheader("Digital Forensics and Cyber Laws [22B12CS412]")
            st.write("Project Based Learning")
            st.title('About')
            st.write(
            "Preventing an attack is a crucial aspect of ensuring the security and integrity of computer systems and networks. Attacks can range from simple brute force attempts to sophisticated social engineering tactics, and can have a wide variety of goals, such as stealing sensitive information, disrupting operations, or damaging reputation. To prevent an attack, it is important to have a comprehensive security strategy that includes multiple layers of defense. This can include implementing strong access controls, regularly updating software and systems, monitoring and analyzing system logs, training employees on security best practices, and using advanced threat detection technologies. By proactively identifying and addressing vulnerabilities, organizations can significantly reduce the likelihood and impact of successful attacks."
            )
        

    elif choice == "RSA Encryptor-Decrypter":
        st.header('RSA Encryptor-Decrypter')
        simulate_RSA(pu,pr)

    elif choice == "RSA Attacks Simulation":
        st.header("RSA Attacks Simulation")
        attacks(pu,pr)

	
if __name__ == '__main__':
    main()




