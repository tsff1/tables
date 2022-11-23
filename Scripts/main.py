from TableGenerator import main
from git import Repo

PATH_OF_GIT_REPO = r"C:\Users\Simen\Tables2\tables"
COMMIT_MESSAGE = 'Updated table'

def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()   

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

git_push()