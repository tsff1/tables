import TableGenerator as tg
import UpdateStats as us
from push import git_push

avds = {"a": 6,
        "b": 6,
        "c": 6,
        "d": 6,
        "e": 7}


end = "n"
while end.lower() == "n":
    avd = input("What table to update? ").lower()
    if avd == "all":
        for avd, n_teams in avds.items():
            tg.main(avd, n_teams)
            print(f"Table {avd.upper()} updated\n")
        end = "y"
    elif avd in avds:
        tg.main(avd, avds[avd])
        print(f"Table {avd.upper()} updated\n")
        end = input("Done? [y/n] ")
    else:
        print(f"{avd.upper()} is not a group\n")

stats = input("Update stats? [y/n] ").lower()
if stats == "y":
    us.main()

print("\nSyncing updates...")
git_push()
print("Done")