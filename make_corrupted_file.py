from random import randint
output = "RANDOM"
with open(output, 'wb') as out:
    for i in range(10408):
        n = randint(1, 5)
        out.write(int(n).to_bytes(1, "little"))
