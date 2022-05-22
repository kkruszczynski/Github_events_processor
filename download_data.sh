#!/bin/bash
#Select the month and the year in line 5. This script can be later automatically created with Python and subprocess
#First loop is responsible for days, second for hours. Feel free to adjust according to your needs
for i in {01..31}; do
	for j in {0..23}; do
		wget http://data.gharchive.org/2022-01-${i}-${j}.json.gz;
	done
done