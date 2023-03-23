from random import randint

arr = [randint(0, 100) for i in range(10)]
print(arr)
for index, item in enumerate(arr):
    print(index, item)
