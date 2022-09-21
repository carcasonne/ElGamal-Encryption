import random

# Public Information - any adversy has full access to this
p = 6661             #prime
g = 666              #base
PK_bob = 2227        #bob public key
PK_alice = -1        #alice public key, initialized to -1

# Assignment problem 1
def aliceEncryptsMessage(superSecretMessage):
    global PK_alice 
    
    SK_alice = random.randint(1, 99999) #random integer between 1 and 99999 - 99999 is just arbritary
    PK_alice = generate(g, SK_alice)
    encryptedMessage = encrypt(superSecretMessage, PK_bob)

    return encryptedMessage

# Assignment problem 2
def eveReconstructsMessage(c_1, c_2):
    # brute forces Bob's secret key
    SK_bob = bruteforceSecretKey(PK_bob)
    aliceDecryptedMessage = decrypt(c_1, c_2, SK_bob)

    return (aliceDecryptedMessage, SK_bob)

# Assignment problem 3
def malloryModifiesMessageTo(fakeMessage):
    # cant brute force, so we modify Alice's message
    # Change her public key and message, so Bob decrypts shit
    global PK_alice 

    SK_mallory = random.randint(1, 9999)
    PK_mallory = generate(g, SK_mallory)

    # change Alice's public key, which Bob will use to decrypt the message
    PK_alice = PK_mallory

    (fake_c1, fake_c2) = encrypt(fakeMessage, PK_bob)

    return (fake_c1, fake_c2)

def encrypt(m, PK_reciever):
    r = random.randint(1, 9999) # if r gets bigger it starts taking a lot of time to run this

    c_1 = pow(g, r);
    c_2 = (generate(PK_reciever, r) * m); 
    return (c_1, c_2)

def decrypt(c_1, c_2, SK_reciever):
    compositeKey = generate(c_1, SK_reciever)
    return int(c_2 / compositeKey)

def generate(base, powerTo):
    return pow(base, powerTo) % p

def bruteforceSecretKey(PK):
    # To provent never ending loop, if more than 10000 I decide that it is infeasible
    for x in range(10000):
        possiblePK = generate(g, x)
        if possiblePK == PK:
             return x

    raise Exception("Secret key is too secret")

def main():
    aliceMessage = 2000

    # Problem 1
    (alice_c1, alice_c2) = aliceEncryptsMessage(aliceMessage)
    print("Alice wants to send message: " + str(aliceMessage)) 
    print("Alice has encrypted her message into:");
    #print("--- C_1:" + str(alice_c1)) #this can get very large, so annoying to print
    print("- C_2:" + str(alice_c2))

    # Problem 2
    (aliceDecryptedMessage, SK_bob) = eveReconstructsMessage(alice_c1, alice_c2)
    print("Eve has intercepted and decrypted through brute force: " + 
           str(aliceDecryptedMessage) + ". Bob's secret key is " + str(SK_bob))

    #Problem 3
    malloryMessage = 6000;

    (fake_c1, fake_c2) = malloryModifiesMessageTo(malloryMessage) # implicitly changes Alice's public key
    alice_c1 = fake_c1;  # changes Alice's decrypted message
    alice_c2 = fake_c2;  # changes Alice's decrypted message
    
    bobDecryptedMessage = decrypt(alice_c1, alice_c2, SK_bob)
    print("Bob recieves his message from Alice: " + str(bobDecryptedMessage))

if __name__ == "__main__":
    main()
