from github import Github

g = Github("tsff1", "TSFFgit123")

repo = g.get_user().get_repo("tables")
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open('Avd_A_table.png', 'r') as file:
    content = file.read()

# Upload to github
git_prefix = 'H22/AvdA/'
git_file = git_prefix + 'Avd_A_table.png'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, "committing files", content, branch="master")
    print(git_file + ' CREATED')