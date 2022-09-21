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
def eveReconstructsMessage(c_1, c_2):
    # brute forces Bob's secret key
    SK_bob = bruteforceSecretKey(PK_bob)
    aliceDecryptedMessage = decrypt(c_1, c_2, PK_alice, SK_bob)

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

    (fake_c1, fake_c2) = encrypt(fakeMessage, PK_bob, SK_mallory)

    return (fake_c1, fake_c2)

def encrypt(m, PK_reciever, SK_sender):
    r = random.randint(1, 99)
    print("picked random number: " + str(r))

    c_1 = pow(g, r);
    c_2 = (pow(PK_reciever, SK_sender) % p) * m
    return (c_1, c_2)

def decrypt(c_1, c_2, PK_sender, SK_reciever):
    r = bruteforceRandomNumber(c_1)
    print("brute forced random number: " + str(r))

    compositeKey = pow(PK_sender, SK_reciever) % p
    return int(c_2 / compositeKey)

def bruteforceRandomNumber(c_1):
    counter = 0;
    while c_1 >= g:
        counter = counter + 1
        c_1 = c_1 / g
            
    return counter;

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
    (alice_c1, alice_c2) = aliceEncryptsMessage(aliceMessage)
    print("Alice wants to send message: " + str(aliceMessage)) 
    print("Alice has encrypted her message into:");
    print("--- C_1:" + str(alice_c1))
    print("--- C_2:" + str(alice_c2))

    # Problem 2
    (aliceDecryptedMessage, SK_bob) = eveReconstructsMessage(alice_c1, alice_c2)
    print("Eve has intercepted and decrypted through brute force: " + 
           str(aliceDecryptedMessage) + ". Bob's secret key is " + str(SK_bob))

    #Problem 3
    (fake_c1, fake_c2) = malloryModifiesMessage() # implicitly changes Alice's public key
    alice_c1 = fake_c1;  # changes Alice's decrypted message
    alice_c2 = fake_c2;  # changes Alice's decrypted message
    
    bobDecryptedMessage = decrypt(alice_c1, alice_c2, PK_alice, SK_bob)
    print("Bob recieves his message from Alice: " + str(bobDecryptedMessage))

if __name__ == "__main__":
    main()
