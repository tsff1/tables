from git import Repo

PATH_OF_GIT_REPO = r"C:\Users\Simen\Tables2\tables"
COMMIT_MESSAGE = 'Updated table'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occurred while pushing the code')