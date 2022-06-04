import json
from flask import Flask, request, jsonify

from cryptography.fernet import Fernet
import base64
import hashlib
import random
import time


# Generate mask to make the each messages different
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

# Extract the masked text
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

# Encrypt the text using password (a.k.a key.txt)
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

# Decrypt the text using password (a.k.a. key.txt)
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





# Read the key
with open('key.txt','r') as fl:
    password = fl.read()


app = Flask(__name__)

# Data that stored in the server
global data_mes
data_mes = ""
global data_time
data_time = ""

# Server functions in one endpoint
@app.route('/', methods=["POST"])
def crypto():
    global data_time
    global data_mes

    print(data_mes, data_time)

    record = json.loads(request.data)
    #print(record, type(record))

    # Decrypt the text
    de_text = decrypt(record['txt'],password)
    print(de_text)
    t = de_text[:20]
    code = de_text[20:23]
    mess = de_text[23:]

    print(t)
    print(code)
    print(mess)

    # Put function
    if code == 'put':
        if data_time == "":
            cur_t = time.time()
            print(cur_t,type(cur_t))

            cur_t2 = format(cur_t, '.4f')

            # Replay attack take care
            if abs(float(cur_t2) - float(t)) > 5.0:
                print("Ignored old message")
            else:
                data_time = t
                data_mes = mess
        else:
            # Deal with replay attack
            if float(t) == float(data_time) or float(t) < float(data_time):
                print("Ignored same time OR old time")
            else:
                cur_t = time.time()

                cur_t2 = format(cur_t, '.4f')

                # Defends against replay attack
                if abs(float(cur_t2) - float(t)) > 5.0:
                    print("Ignored old message")
                else:
                    data_time = t
                    data_mes = mess

        print(data_time, data_mes)
        return {"txt": encrypt(t+"ack"+"ok",password)}


    # Get function
    if code == 'get':
        cur_t = time.time()

        cur_t2 = format(cur_t, '.4f')

        # Just in case of replay attack
        if abs(float(cur_t2) - float(t)) > 5.0:
            print("Ignored old message")
            return {"txt": encrypt(t+"ack", password)}

        else:
            return {"txt": encrypt(t+"ack"+data_mes, password)}




# This should be debug=False
app.run(debug=True)
