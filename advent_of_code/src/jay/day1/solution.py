list1 = []
list2 = []

input = open('input.txt','r')
for line in input:
    data = line.split()
    list1.append(int(data[0]))
    list2.append(int(data[1]))

list1.sort()
list2.sort()

distance = 0
similarity = 0
for i in range(len(list1)):
    distance += abs(list1[i] - list2[i])
    similarity += list1[i] * list2.count(list1[i])

print("Problem 1: " + str(distance))
print("Problem 2: " + str(similarity))


