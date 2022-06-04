from cryptography.fernet import Fernet
import base64
import hashlib
import random

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

with open('key.txt','r') as fl:
    password = fl.read()

h_pass = hashlib.sha224(password.encode()).hexdigest()
print(h_pass, type(h_pass) )

h_mask, rand_mask, lent = gen_mask(h_pass)
print(h_mask, rand_mask , lent)

print(len(password)//32)

enc_fs = []
for i in range(len(password)//32):
    key = base64.urlsafe_b64encode(password[32*i:32*i +32].encode())
    print(key)
    enc_f = Fernet(key)
    enc_fs.append(enc_f)

pre_text = "hello"
text = h_pass+pre_text+rand_mask+h_mask
text = text.encode()
#print(text.decode())

for key_f in enc_fs:
    text = key_f.encrypt(text)
    #print(text.decode())


print(text.decode())


for key_f in enc_fs[::-1]:
    #print()
    #print()
    text = key_f.decrypt(text)
    #print(text.decode())
