# Protocol_Library

Repository for Internal Protocol Development.

## Sample Protocol Development Workflow:

1- Create Trello Ticket

2- Create Branch with ticket number and name. For example: `5-hampton-creek-olga-etc-3-protocols`

3- Team members working on protocol check out that branch.
	
* Navigate to local protocol_lib directory in terminal, make sure you have the most recent online version of repo.
```
cd [local protocol folder]
git pull
```

* fetch/list any new branches
```
git fetch --all
```

* check which branch you are currently on locally
```
git branch
```

* switch to proper protocol branch (never work directly off master)
```
git checkout 5-hampton-creek-olga-etc-3-protocols
```
6- If it does not currently exist, create a folder for the new/current protocol being developed in this branch. Create a file called `README.md`

5- Generate plain text description of protocol science in google docs and link to it in protocol folder's README file. 
	Adding a link in markdown:
	```
	[Text For Link](URL FOR DOC)
	```
6- Add protocol.py file and jupyter notebook file to protocol

7- Edit README.md for appropriate meta information.

### Basic editing workflow

* Switch to appropriate branc (see step 3)

* Make sure your local branch is up to date
```
git pull
```

* Make changes

* Check to see what files have changed
```
git status
```

* Add your changes to git
```
git add [file name]
```
* Commit them
```
git commit -m "useful commit message"
```
* Push your changes to github
```
git push 
```






