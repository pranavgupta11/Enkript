# Enkript
### Implement the attacks on RSA (Rivest, Shamir & Adleman)
1. best known & widely used public-key scheme
2. based on exponentiation in a finite (Galois) field over integers modulo a prime
- exponentiation takes O((log n)3) operations (easy)
3. uses large integers (eg. 1024 bits)
4. security due to cost of factoring large numbers
5. factorization takes O(e ^ log n log log n) operations (hard)

## Potential Attacks
1. Factorization - The obvious way to do this attacks is to factor the public modulus, n, into its two prime factors, p and q. From p, q and e, the attacker can easily get d. The hard part is factoring n:
    1.1 Security on RSA depends on factoring being difficult.
    1.2 In fact, the task of recovering the private key is equivalent to the task of factoring the modulus.
    1.3. It should be noted that the hardware improvements alone will not weaken the RSA, as long as appropriate key length are used.
2. Chosen Cipher Text
3. Encryption Exponent
4. Decryption Exponent
5. Plaintext
6. Modulus
7. Implementation

