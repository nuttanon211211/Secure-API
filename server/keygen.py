import random
import os

# Generate random text of length le
def randomtext(le):
    out = ""
    for i in range(le):
        out += random.sample("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM",1)[0]
    return out

# Check that the text has at least 2 non-space character
def checktext(txt):
    count = 0
    out = ""
    for e in txt:
        if e != " ":
            count+= 1
            out += e
        if count >= 2:
            return True , out

    return False

# confirm if the key is already exists
if 'key.txt' in os.listdir():
    confirm = input("Key is already exist, type 'yes' to overwrite?:")
    if confirm != 'yes':
        print("Invalid code",confirm)
        exit(0)


input_t = ""
while checktext(input_t) == False:
    input_t = input("Randomly smash the keyboard then hit enter:").strip()

# Generate the key
_, f3 = checktext(input_t)
f1 = randomtext(500)
f2 = ""
random.seed(input_t)
for i in range(10):
    f2 += random.sample("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM",1)[0]

print(f1)
print(f2)
print(f3)

# Save the key
with open('key.txt','w') as f:
    f.write(f1+f2+f3)

