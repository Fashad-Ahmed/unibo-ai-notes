s = "Viva la pappa col pomodoro"

letters = []
count = []
for l in s:
    if l not in letters:
        letters.append(l)
        count.append(1)
    else: #l is in letters
        count[letters.index(l)] += 1 #a case where is better +=

print(letters, count)


s = "Viva la pappa col pomodoro"

count = {}
for l in s:
    if l not in count:
        count[l] = 1
    else: #l is in letters
        count[l] += 1 

print(count)

s = "Viva la pappa col pomodoro"

count = {}
for l in s:
    count[l] = count.get(l, 0)+1 

print(count)

car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

x = car.get("model")

print(x)