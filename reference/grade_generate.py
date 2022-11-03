year = int(input("current year:"))
print(" Grade | YStart")
for grade in range(-5, 15):
    print(str(grade).rjust(7)+"|"+str(year-grade).rjust(6).ljust(1))

