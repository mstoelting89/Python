from datetime import datetime

def inner():
    s = 0
    for i in range(0, 10000000):
        s = s + 1
    print(s)

start = datetime.now()

inner()

end = datetime.now()

print(end - start)