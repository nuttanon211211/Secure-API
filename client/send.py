import requests
import json

from cryptography.fernet import Fernet
import base64
import hashlib
import random
import time

# Generate mask to make each message different
def gen_mask(txt):
    lent = random.randint(1,1000)
    lent2 = int(lent)
    mask_out = ""
    rand_out = ""

    for e in txt:
        if lent2 > 0:
            if lent2 % 2 == 1:
                mask_out += 'x'
            else:
                mask_out += e
            lent2 = lent2//2
        else:
            mask_out += e

    for i in range(lent):
        rand_out += random.sample("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM",1)[0]

    return mask_out , rand_out , lent

# Extract the text from the masked text
def extract_text(txt):
    #sha224 = 56 l
    mask_out = txt[-56:]

    counter = 1
    count = 0
    for e in mask_out:
        if e == "x":
            count += counter
        counter *= 2

    return txt[56:-(56+count)]

# Encrypt the text using symmetric key
def encrypt(text,password):
    h_pass = hashlib.sha224(password.encode()).hexdigest()
    #print(h_pass, type(h_pass) )
    h_mask, rand_mask, lent = gen_mask(h_pass)
    #print(h_mask, rand_mask , lent)
    #print(len(password)//32)

    enc_fs = []
    for i in range(len(password)//32):
        key = base64.urlsafe_b64encode(password[32*i:32*i +32].encode())
        #print(key)
        enc_f = Fernet(key)
        enc_fs.append(enc_f)

    #pre_text = "hello"
    text_post = h_pass+text+rand_mask+h_mask
    text_post = text_post.encode()
    #print(text.decode())

    for key_f in enc_fs:
        text_post = key_f.encrypt(text_post)
    #print(text.decode())
    #print(text.decode())
    return text_post.decode()

# Decrypt the text using symmetric key
def decrypt(text,password):
    text = text.encode()
    enc_fs = []
    for i in range(len(password)//32):
        key = base64.urlsafe_b64encode(password[32*i:32*i +32].encode())
        #print(key)
        enc_f = Fernet(key)
        enc_fs.append(enc_f)


    for key_f in enc_fs[::-1]:
        #print()
        #print()
        text = key_f.decrypt(text)
        #print(text.decode())


    return extract_text(text.decode())
    #return text.decode()





# Load the key
with open('key.txt','r') as fl:
    password = fl.read()


# API endpoint
url = 'http://127.0.0.1:5000'

t1 = ""
#code = 'put'

code = ""

# Main program code loop
while code != "exit":
    # Input the user code
    code = input('>')

    # Code equals Put
    if code == 'put':
        t1 = input('put>')

        t = time.time()
        st = format(t, '.4f')
        st = (20 - len(st))*'0'+ st


        #print(t1)
        #print(st)

        # Encrypt the message
        t2 = encrypt(st+code+t1, password)


        body = {
            "txt": t2
        }

        response = requests.post(url, json = body)

        response2 = json.loads(response.text)
        #print(response.text, type(response.text))
        #print(response2, type(response2))

        # Decrypt the response
        de_text = decrypt(response2['txt'],password)
        #print(de_text)

        res_t = de_text[:20]
        res_code = de_text[20:23]
        mess = de_text[23:]

        #print(res_t)
        #print(res_code)
        #print(mess)

        # Possible of replay attack, when this code is executed
        if res_code != 'ack' or res_t != st:
            print("error: Insecure connection ",res_code,res_t,st)
        else:
            print(mess)


    # Get function
    if code == 'get':
        t = time.time()
        st = format(t, '.4f')
        st = (20 - len(st))*'0'+ st

        t1 = ''

        # Encrypt the text befor sending
        t2 = encrypt(st+code+t1, password)


        body = {
            "txt": t2
        }

        response = requests.post(url, json = body)

        response2 = json.loads(response.text)
        #print(response.text, type(response.text))
        #print(response2, type(response2))

        # Decrypt the response
        de_text = decrypt(response2['txt'],password)
        #print(de_text)

        res_t = de_text[:20]
        res_code = de_text[20:23]
        mess = de_text[23:]

        #print(res_t)
        #print(res_code)
        #print(mess)

        # Warning against extremely likely replay attack
        if res_code != 'ack' or res_t != st:
            print("error: Insecure connection ",res_code,res_t,st)
        else:
            print(mess)

    # Display invalid code
    if code not in ['get', 'put', 'exit']:
        print('Valid code: get put exit')







