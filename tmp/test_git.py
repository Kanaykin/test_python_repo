# -*- coding: utf-8 -*-

from git import Repo
from github import Github
from github import PullRequest
import os

#получение текущей директории репозитория
def get_repo( ):
	path_script_dir = os.path.dirname( __file__ )
	path_script_dir = os.path.join(path_script_dir, '') #os.path.join(path_script_dir, '..')
	repo_dir = os.path.dirname(os.path.abspath(path_script_dir))
	return Repo(repo_dir)
#############################

repo = get_repo()
branch = repo.active_branch
print branch.name

exit()

# past_branch = repo.create_head("tmp/" + branch.name+"_tmp", 'HEAD')
# origin = repo.remote()
# assert origin.exists()
# origin.fetch()

# repo.git.push('origin', "tmp/" + branch.name+"_tmp")
g = Github("SergeyKanaykin", "hrenvam1")


for repo in g.get_user().get_repos():
    print(repo.name)
    if repo.name == "mansion-makeover" :
    	mansion_makeover_repo = repo

    # repo.edit(has_wiki=False)


user = g.get_user()
# repo = user.get_repo("Playrix/mansion-makeover")
commit = mansion_makeover_repo.get_commit("73ddccac8d6fdfd2304e789e34f6a238bbbeb41b")
# issue = mansion_makeover_repo.create_issue("Issue created by PyGithub")
# comment = self.pull.create_comment("Comment created by PyGithub", commit, "src/github/Issue.py", 5)
pull = mansion_makeover_repo.create_pull("Pull request created by PyGithub", "Body of the pull request", "tmp/cats_action_queue", "master", True)

# Github.PullRequest.PullRequest
# POST /repos/:owner/:repo/pulls