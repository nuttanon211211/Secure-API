import time


t = time.time()
print(t,type(t))

st = format(t, '.4f')
st = (20 - len(st))*'0'+ st
print(st, type(st))

t2 = float(st)
print(t2, type(t2))


