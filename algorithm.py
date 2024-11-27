def numtonums(n: int) -> str:
    s = ''
    for i in range(1,n+1):
        s = s + i*str(i)
    return s

if __name__ == '__main__':
    number = int(input())
    print(numtonums(number))
