# python-setup
Simple jupyter notebook


## Python Virtual Environment & Jupyter Setup1. Set Up Virtual Environment
python3 -m venv venv

## Activate Virtual Environment
On macOS/Linux:
source venv/bin/activate

## Install Jupyter & Run
pip install jupyter
jupyter notebook


## .gitignore for Virtual Environments
.gitignore file tells Git to ignore specific files. In this case the venv which is set up for indvidual computers.

Git will stop showing the folder in your file list.  
You won't accidentally upload it.

