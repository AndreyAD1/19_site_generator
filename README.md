# Encyclopedia

This script gets articles from `*.md` files and returns the site with
articles and table of contents.

# How to install

Python v3.5 should be already installed. Afterwards use pip to install dependencies:
```bash
pip install -r requirements.txt # alternatively try pip3
```
It is recommended to use virtual environment for better isolation.

# Quick Start

Make a `*.json` file containing information about paths of `*.md` files
and about article topics (see `config.json` located in this repository).
Put this file in the script`s directory. 

To run script on Linux:
```bash
$ python site_render.py
```

Windows usage is the same.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
