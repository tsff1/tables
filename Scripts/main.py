from TableGenerator import main

# Velg avdeling: A = 0, B = 1
inp = False

while not inp:
    avd = input("What table to update? ")
    if avd.lower() == "a":
        inp = True
        avd = 0
    elif avd.lower() == "b":
        inp = True
        avd = 1
    else:
        print(f"{avd} is not a group\n")
        
main(avd)