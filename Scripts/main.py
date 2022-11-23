from TableGenerator import main
from push import git_push

end = "n"
while end.lower() == "n":
    avd = input("What table to update? ")
    if avd.lower() == "a":
        avd = 0
        main(avd)
        print("Table A updated\n")
        end = input("Done? [y/n] ")
    elif avd.lower() == "b":
        avd = 1
        main(avd)
        print("Table B updated\n")
        end = input("Done? [y/n] ")
    else:
        print(f"{avd} is not a group\n")

print("Syncing updates...")
git_push()
print("Done")