distance = {'ja': 2, 'ti': 4, 'on': 0, 'ona': 10}


q = 3

sorted_distances = sorted(distance.items(), key=lambda x: x[1])[0:3]

closest = []

for i in sorted_distances:
    closest.append(i[0])

print(closest)

