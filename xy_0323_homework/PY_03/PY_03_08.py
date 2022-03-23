a, b, c = input().split(' ')
a = int(a)
if a > 120:
    a_state = 2
elif a >= 80:
    a_state = 1
else:
    a_state = 0

b = int(b)
if b > 280:
    b_state = 2
elif b >= 200:
    b_state = 1
else:
    b_state = 0

c = int(c)
if c > 480:
    c_state = 2
elif c >= 320:
    c_state = 1
else:
    c_state = 0

print(a_state, b_state, c_state)
