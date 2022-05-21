## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is dedicated to process Github events for specific period of time. Report contains daily aggreagtes for User and Repositories
	
## Technologies
Project is created with:
* Python 3.8

	
## Setup
To run this project on Windows following steps are needed:
1. Install wget.exe on your machine. You can get it from [here](https://eternallybored.org/misc/wget/)
2. Prepare your Python venv or use Anacoda package
3. Download data using script 
```
$ download_data.sh
```
Remember to not upload raw data to GitHub repository
4. Run the process_data.py
