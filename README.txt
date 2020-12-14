README

Please have a 'password.txt' file to connect to YOUR own postgres account
format:
username
password

first command to run on your machine (on terminal) for dependencies on python: 

***Assuming you have python 3 on your machine:***

WINDOWS:
Pip3 install pyqt5

MAC:
python3 -m pip install PyQt5

***TO RUN:***
CD into folder you saved I.E. airline_project
Run this command to run GUI: python airline_gui.py

1) INITIALIZE DATABASE USING \i new_temp_db.sql on your postgres account

Flight Availability:
December 2020 and January 2021

flights are available on these specific dates:
December: 
7th on Monday 
15th on Tuesday 
18th on Friday
23rd on Wednesday
31st on Thurday

January: 
4th on Monday
12th on Tuesday
20th on Wednesday
28th on Thursday
15th on Friday

Inserting new Flight:
Flight id, airline name, departure day(Monday,tuesday...etc)
then... insert
Flight_leg (look at sql file or er diagram)

In case GUI was not able to run in your machine:
Video Link: https://youtu.be/7ih-Csuvk5M
