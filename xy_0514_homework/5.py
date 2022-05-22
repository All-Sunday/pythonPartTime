# @Description: 分数四则运算
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/5/15 14:36
# @File : 5.py
import re
import time

# expression_list = re.split(r'/+|/-|/*|//',input().strip())
# print(expression_list)
# for i in expression_list:
#     if i =='':
#         expression_list.remove(i)
# print(expression_list)


expression = input().strip()
# print(expression)
times = 0
nums = []
num = ''
op = ''
for i in expression:
    if i in ('+', '-', '*', '/'):
        nums.append(eval(num))
        num = ''
        times += 1
        if times == 2:
            op = i
    else:
        num += i
nums.append(eval(num))
a, b, c, d = nums
print(a, b, op, c, d)
if (b == 0) or (d == 0):
    print('分母为0输入错误!')
if op == '+':
    y = a * d + c * b
    x = b * d
elif op == '-':
    y = a * d - c * b
    x = b * d
elif op == '*':
    y = a * c
    x = b * d
elif op == '/':
    y = a * d
    x = b * c
print(y, x)
a, b = y, x
while b > 0:
    a, b = b, a % b
y = int(y / a)
x = int(x / a)
print(y, x)
print(expression + '=' + str(y) + '/' + str(x))
time.sleep(100)

# char op;
# printf("两分数b/a,d/c作+，-，*，/四则运算，结果为分数。\n");
# printf("请输入分数运算式。\n");
# scanf("%ld/%ld%c%ld/%ld",&b,&a,&op,&d,&c);
# if(a==0||c==0) {printf("分母为0输入错误!");exit(0);}
# if(op=='+'){y=b*c+d*a;x=a*c;}
# if(op=='-'){y=b*c-d*a,x=a*c;}
# if(op=='*'){y=b*d;x=a*c;}
# if(op=='/'){y=b*c;x=a*d;}
# z=x;
# if(x>y) z=y;
# i=z;
# while(i>1)
#     {
#     if(x%i==0&&y%i==0){x=x/i;y=y/i;continue;}
# i--;
# }
# printf("%ld/%ld%c%ld/%ld=%ld/%ld.\n",b,a,op,d,c,y,x);
#
#
#
#
#
#
#
#
# a = input()
# l = len(a)
# b2 = "\\"
# cont = 0
# for j in a:
#     cont += 1
#     if j == '+':
#         x = Fraction(a[:cont - 1]) # x为运算符前面的数
#         y = Fraction(a[cont:l])# y位运算符后面的数
#         print(x + y)  # 切片左取右不取
#         break
#     elif j == '-':
#         x = Fraction(a[:cont - 1])
#         y = Fraction(a[cont:l])
#         print(x - y)
#         break
#     elif j == '*':
#         x = Fraction(a[:cont - 1])
#         y = Fraction(a[cont:l])
#         print(x * y)
#         break
#     elif j == b2:
#         x = Fraction(a[:cont - 1])
#         y = Fraction(a[cont:l])
#         print(x / y)
#         break
#
#
