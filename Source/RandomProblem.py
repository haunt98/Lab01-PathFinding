import random


def createRandomProblem(name_rand, minSize, maxSize):
    # seed de moi lan random khac nhau
    random.seed()

    f_rand = open(name_rand, 'w')

    # random size
    size = random.randrange(minSize, maxSize)
    f_rand.write(str(size) + '\n')

    # random SPoint, GPoint
    SPoint = (random.randrange(0, size), random.randrange(0, size))
    GPoint = (random.randrange(0, size), random.randrange(0, size))
    f_rand.write(str(SPoint[0]) + ',' + str(SPoint[1]) + '\n')
    f_rand.write(str(GPoint[0]) + ',' + str(GPoint[1]) + '\n')

    # random arr
    arr = []
    for i in range(size):
        row = []
        for j in range(size):
            temp = random.randrange(1024) % 3
            if temp > 0:
                row.append(0)
            else:
                row.append(1)
        arr.append(row)

    # SPoint, GPoint la o trong
    arr[SPoint[0]][SPoint[1]] = 0
    arr[GPoint[0]][GPoint[1]] = 0

    for row in arr:
        for word in row:
            f_rand.write(str(word) + ' ')
        f_rand.write('\n')

    f_rand.close()