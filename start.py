
import random
import pandas as pd
import streamlit as st
import time
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT

def define_dashboard_config():
	st.set_page_config(
		layout="wide",  
		initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
		page_title='ATTACKS ON TEXTBOOK RSA', 
		page_icon=None,  
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

def encrypt_rsa(public):
    # message = input(" - Enter a message to encrypt with your public key: ")
    message = st.text_input('nter a message to encrypt with your public key')


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
    st.write(" - Cipher Text: ", end="")
    printAfterJoin(encrypted_msg)
    st.write(" - Decrypting message with private key ", private, " . . .")
    st.write(" - Your message is: ", decrypt(private, encrypted_msg))

def simulate_RSA():
    pu, pr = set_keys() #pu = (e, n), pr = (d, n)
    cipher = encrypt_rsa(pu)
    decrypt_rsa(pr, cipher)

# ----------------------------------------------------------------------------------------------------------------------------------------


def attacks():
    tab1, tab2, tab3,tab4,tab5,tab6 = st.tabs(["Factorization Attack",
        "Chosen Cipher text Attack","Cyclic Attack","Guess Length Pin",
        "Timing Based Attack","CRT attack"])

    with tab1:
        st.header("Factorization Attack")
        # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("Chosen Cipher text Attack")

    with tab3:
        st.header("Cyclic Attack")

    with tab4:
        st.header("Guess Length Pi")

    with tab5:
        st.header("Timing Based Attack")

    with tab6:
        st.header("CRT attack")

def main():	

    define_dashboard_config()

    plt.style.use('dark_background')

    menu = ["About", "RSA Encryptor-Decrypter", "RSA Attacks Simulation"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice=="About":
        st.title('About')

    elif choice == "RSA Encryptor-Decrypter":
        st.header('RSA Encryptor-Decrypter')
        simulate_RSA()

    elif choice == "RSA Attacks Simulation":
        st.header("RSA Attacks Simulation")
        attacks()

	
main()    
