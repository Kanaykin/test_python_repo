# -*- coding: utf-8 -*-

from git import Repo
from github import Github
from github import PullRequest
from github import GithubException
from config import Config
from os.path import expanduser
import time
import webbrowser

import os
import cmd

REPOSITORY_NAME = "test_python_repo"

#############################
#получение текущей директории репозитория
def get_repo():
	path_script_dir = os.path.dirname( __file__ )
	repo_dir = os.path.dirname(os.path.abspath(path_script_dir))
	return Repo(repo_dir)

#############################
#создаем отдельный бранч
def create_branch(login):
	repo = get_repo()
	branch = repo.active_branch
	branch_names = branch.name.split('/')
	# print branch_names[len(branch_names) - 1]
	new_branch_name = "tmp/" + branch.name + "_" + str(int(time.time()))
	past_branch = repo.create_head(new_branch_name, 'HEAD')

	origin = repo.remote()
	assert origin.exists()
	origin.fetch()

	repo.git.push('origin', new_branch_name)
	print "Create branch success " + new_branch_name
	return  {'branch_from' : new_branch_name, 'branch_to' : branch.name}

#############################
# получить имя конфигурационного файла
def get_config_name():
	home = expanduser("~")
	return home + '/githubinfo.cfg'


#############################
# получить имя и пароль от github
def get_github_authorization_info():

	filename = get_config_name() 
	if os.path.exists(filename):
		cfg = Config(file(filename))
		login = cfg.login
		password = cfg.password
	else:
		login = raw_input("Please enter login: ")
		password = raw_input("Please enter password: ")
	return {'login': login, 'password': password}

#############################
# сохранить имя и пароль от github
def save_github_authorization_info(login, password):
	f = file(get_config_name(), 'w')
	cfg = Config()
	cfg.login = login
	cfg.password = password
	cfg.save(f)

#############################
#получение нужного репозитория
def get_repository():
	
	authorization_info = get_github_authorization_info()
	g = Github(authorization_info['login'], authorization_info['password'])
	try:
		for repo in g.get_user().get_repos():
			if repo.name == REPOSITORY_NAME :
				save_github_authorization_info(authorization_info['login'], authorization_info['password'])
				return repo
	except GithubException, exception:
		print "Error : Authorization failed or Not found repository : " + REPOSITORY_NAME

	return None

def make_pull_request(repo_github, branch_from, branch_to, message, body):
	try:
		pull = repo_github.create_pull(message, body, branch_to, branch_from, True)
		print "Pull request url " + pull.url
		webbrowser.open(pull.html_url)
		return True
	except GithubException, exception:
		print "Error: Create pull error !!! branch_from: " + branch_from + " branch_to " + branch_to
		return False

def delete_branch(branch_from, branch_to):
	repo = get_repo()
	repo.delete_head(branch_from)
	# ресетим текущий бранч
	repo.git.reset('--hard','origin/'+branch_to)

def main( ):
	
	repo_github = get_repository()
	if repo_github is None:
		print "Error: Not found repository "
		return

	authorization_info = get_github_authorization_info()
	branch_info = create_branch(authorization_info['login'])

	repo = get_repo()
	commit = repo.head.commit
	commit_info =  commit.message.splitlines()
	message = commit_info[0]
	body = ""
	if len(commit_info) > 1:
		body = commit_info[1]
	request_created = make_pull_request(repo_github, branch_info['branch_from'], branch_info['branch_to'], message, body)
	if request_created == False:
		print "Make pull request error "
		return

	# удалим бранч
	delete_branch(branch_info['branch_from'], branch_info['branch_to'])

main()
