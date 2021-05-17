f = open("test.csv", "w")
f.write("word,status\n")
val = None
while val != 'matt':
    val = input("Enter your value: ")
    if val != 'matt':
        f.write(val + "\n")

f.close()