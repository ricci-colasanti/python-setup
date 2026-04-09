# python-setup
Simple jupyter notebook

## Install python on Mac 
[Homebrew](https://brew.sh/)

To install on your Mac, copy, paste, and then execute the following in your terminal:   
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

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

