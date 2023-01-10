# FPVQ Scraper
> Webscraper using BeautifulSoup, requests, selenium, and pandas.  Takes results from every national-level speed skating competition in Canada and returns skaters personal bests for each distance.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
In speed skating, skaters are ranked based on their fastest 500m and 1500m times.  However, at a national competition, there can be more than 100 skaters, skating 
each distance 4 or 5 times.  As a result, it can be hard to keep track of skaters' best times, and makes it difficult to maintain an accurate ranking of skaters.  
This program intends to automate the process of ranking skaters by parsing through the entire competition and returning their best times.  I undertook this project 
to help skaters better prepare to qualify for competitions.  Many competitions only take the top x amount of skaters, and this ranking program would help coaches 
determine the time improvements needed for their skaters to qualify.


## Technologies Used
- Python 3.1


## Features
- Allows users to rank per distance to avoid confusion
- Exports all data to an Excel file formatted properly


## Setup
pip install bs4  
pip install selenium  
download chromedriver for selenium  

## Usage
How does one go about using it?
Provide various use cases and code examples here.

Follow the prompts provided by program.  
'**>**' Denotes user input  
Enter the distance you would like to rank:  
\> **1500** *note you will only input the numbers, you do not add 'm' after*  

Enter 'a, b, c' for the level of competition you would like the results for   
a) National   
b) Elite   
c) Collegial  
\> **b**   

Enter 'a, b, c' for the competition you would like the results for   
a) Canadian Champs   
b) Canadian Juniors   
c) Invitational   
\> **c**  

The results are about to be saved in a file, please name the file:  
\> **Top 1500m results from Invitational competition**  

And a file should be downloaded called *Top 1500m results from Invitational competition.xlsx* where you can find the results.  

## Project Status
Project is: _complete_.


## Room for Improvement
Allow program to retake user input if the input does not meet the guidelines.  
Output Men's and Women's results separately.

## Acknowledgements
This project was inspired by Adam Law's Spreadsheets.

## Contact
Helios He: h22he@uwaterloo.ca  
Sharang Goel: s4goel@uwaterloo.ca
