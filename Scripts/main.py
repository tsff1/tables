import TableGenerator as tg
from push import git_push

avds = "abcd"

end = "n"
while end.lower() == "n":
    avd = input("What table to update? ").lower()
    if avd == "all":
        for avd in avds:
            tg.main(avd)
            print(f"Table {avd.upper()} updated\n")
        end = "y"
    elif avd in avds:
        tg.main(avd)
        print(f"Table {avd.upper()} updated\n")
        end = input("Done? [y/n] ")
    else:
        print(f"{avd.upper()} is not a group\n")

print("Syncing updates...")
git_push()
print("Done")