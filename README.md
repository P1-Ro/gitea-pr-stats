

# Gitea PR stats

This is a tool/server to compute some metrics of pull requests on a [Gitea](https://gitea.io/en-us/) repository inside a time span (timespan is optional).

## Development environment
Install [pip](https://pypi.python.org/pypi/pip).

Create a new virtual environment:

    python3 -m venv venv
    
Activate the environment:

    source venv/bin/activate

Install the requirements:

    pip install -r requirements.txt


## Usage
An API token is required for making calls to the Gitea API, so you will need to generate an API token from the Gitea GUI and provide it in the config file.

All configuration is inside git_config.py. Create one for yourself from .sample file provided. It should look like this.

	username = "USERNAME"
	password = "PASSWORD"	
	repositories = ["owner/repo", "owner/repo"]  # repositories to which you want to be able create reports
	port = 8000  # port of report server
	gitea_url = "https://try.gitea.io"  # url to your gitea instance
	token = "abcdefabcdefabcdefabcdefabcdef" # API token you generated in the Gitea GUI

Build client

	cd client
	npm install
	npm run build

And then server

    python run.py


## Viewing the results

The `client` folder contains a very simple Vue.js based client.
 You need to compile it before first run. Through this client new reports can be generated and also viewed.

 You can view it on: `http://localhost:8000/` 

