## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is dedicated to process Github events for specific period of time. Report contains daily aggreagtes for User and Repositories
	
## Technologies
Project is created with:
* Python 3.8 using Pandas
	
## Setup
To run this project on Windows following steps are needed:
1. Install wget.exe on your machine. You can get it from [here](https://eternallybored.org/misc/wget/)
2. Prepare your Python venv or use Anacoda package
3. Download data using script 
```
$ download_data.sh
```
4. Create *.rawData* folder in the folder where script is going to be run and paste there downloaded data. Remember to not upload raw data to GitHub repository

5. Setup *config_file.json* file

6. Run following script in Python Console

```
github_events_processor.py
```