row_num = 0
for x in range(1, 1001):
    is_prime = True
    if x == 1:
        continue
    for i in range(2, x):
        if x % i == 0:
            is_prime = False
            break
    if is_prime:
        print('%-5d' % x, end='')
        row_num += 1
        if row_num % 10 == 0:
            print()
