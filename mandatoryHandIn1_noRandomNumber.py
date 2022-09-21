import random

# Public Information - any adversy has full access to this
p = 6661             #prime
g = 666              #base
PK_bob = 2227        # bob public key
PK_alice = -1        #alice public key, initialized to -1

# Assignment problem 1
def aliceEncryptsMessage(superSecretMessage):
    global PK_alice 
    
    SK_alice = random.randint(1, 9999) #random integer between 1 and 999 - 999 is just arbritary
    PK_alice = pow(g, SK_alice) % p
    encryptedMessage = encrypt(superSecretMessage, PK_bob, SK_alice)

    return encryptedMessage

# Assignment problem 2
def eveReconstructsMessage(cipherText):
    # brute forces Bob's secret key
    SK_bob = bruteforceSecretKey(PK_bob)
    aliceDecryptedMessage = decrypt(cipherText, PK_alice, SK_bob)

    return (aliceDecryptedMessage, SK_bob)

# Assignment problem 3
def malloryModifiesMessage():
    # cant brute force, so we modify Alice's message
    # Change her public key and message, so Bob decrypts shit
    global PK_alice 
    fakeMessage = 6000

    SK_mallory = random.randint(1, 9999)
    PK_mallory = pow(g, SK_mallory) % p

    # change Alice's public key, which Bob will use to decrypt the message
    PK_alice = PK_mallory

    encryptedFakeMessage = encrypt(fakeMessage, PK_bob, SK_mallory)

    return encryptedFakeMessage

def encrypt(m, PK_reciever, SK_sender):
    compositeKey = pow(PK_reciever, SK_sender) % p 
    return compositeKey * m

def decrypt(c, PK_sender, SK_reciever):
    compositeKey = pow(PK_sender, SK_reciever) % p
    return int(c / compositeKey)

def bruteforceSecretKey(PK):
    # To provent never ending loop, if more than 10000 I decide that it is infeasible
    for x in range(10000):
        possiblePK = pow(g, x) % p
        if possiblePK == PK:
             return x

    raise Exception("Secret key is too secret")

def main():
    aliceMessage = 2000

    # Problem 1
    aliceCipher = aliceEncryptsMessage(aliceMessage)
    print("Alice wants to send message: " + str(aliceMessage)) 
    print("Alice has encrypted her message into: " + str(aliceCipher))

    # Problem 2
    (aliceDecryptedMessage, SK_bob) = eveReconstructsMessage(aliceCipher)
    print("Eve has intercepted and decrypted through brute force: " + 
           str(aliceDecryptedMessage) + ". Bob's secret key is " + str(SK_bob))

    #Problem 3
    malloryFakesMessage   = malloryModifiesMessage() # implicitly changes Alice's public key
    aliceCipher = malloryFakesMessage;  # changes Alice's decrypted message
    
    bobDecryptedMessage = decrypt(aliceCipher, PK_alice, SK_bob)
    print("Bob recieves his message from Alice: " + str(bobDecryptedMessage))

if __name__ == "__main__":
    main()
