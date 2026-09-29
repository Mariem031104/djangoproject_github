prenom = str(input("donner votre prenom"))
age= int(input("donner votre age"))
print(f"Hello {prenom}, you are {age} years old.")

num =  int(input("donner un nombre"))
if num % 2==0 :
    print(f"{num} est pair")
else :
    print(f"{num} est impair")

ch = 'abc'
for i in range (0,len(ch)):
    print(ch[i])


sum = 0
for i in range (1,100):
    sum=sum+i
print(sum)

l= [12, 15, 9, 18, 14]
s = 0
moy=0
min =l[0]
max =l[0]


for i in l:
    s=s+i
    if i < min:
        min=i
    if i > max:
        max=i
    
moy=s/5


print(f"moy est {moy} , min est {min} et max est {max}")

student = {
    "name": "Ali",
    "age": 20,
    "study field": "computer science"
}

student["email"] = "ali@gmail.com"
print(student)

animaux = {"cat", "dog", "bird", "cat"}

print(animaux)

personne = ("Ali", 20, "Tunis")

for element in personne:
    print(element)