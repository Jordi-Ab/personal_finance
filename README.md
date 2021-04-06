# Personal Finance Project
This project is intended for personal use and so the code and features were not programmed with User Interaction in mind.

Backend is developed in Python mainly using pandas to handle information as DataFrames, for the frontend and database storages I use GoogleSheets (I know it might not be the best solution but then again, the objective is to be used as a personal guide to keep my finances and spends well tracked, and so, GoogleSheets is enough for my personal needs).

The objective of the project is very simple, classify my Expenses on some main categories that I have spotted I spend the most, assign an expenses plan for each category and be able to know how much I have already spent on each category before the account statement arrives. All of this in an easy and least painful way.

The manual things one has to do are:
1) Download the movements of certain credit or debit cards from your bank page, 
2) Upload them to 'input_data' folder, 
3) Run the script and 
4) Provide the information for each expense throuch a Dialog Box.

## Front End
For the Front End and database storages I use GoogleSheets. 

The reason for choosing GoogleSheets is mainly because of its Cloud Storage capabilities and security issues. That is, I can have a private document only accesible by me through my GoogleDrive, connect to it using Python to read from it and modify it, and also have it on the Cloud to access it on any of my devices to consult the expenses I have made on each category so far.

The Backend connects and consumes information from this GoogleSheet, and so, an initial GoogleSheet template should be in place in order for the backend to work correctly. This template is provided as an excel document on this repo with the name ´frontend_template.xlsx´ but it is important that this template is saved on your GoogleDrive as a GoogleSheet. (as a personal recommendation, make sure your document is private).

The First Tab, named "Biweekly Plan" contains the categories that the backend will consume along with the planned spends for each category divided fortnightly.

### Categories and Subcategories
Categories are found on the First Tab, named "Biweekly Plan" under the "Variable Expenses" title (Cell 29). They are divded is Categories and Subcategories.
A category, for example, is "Food" and subcategories might be "Supermarket", "Restaurants", etc. Another Cateogry, Subcategory or both might be added by inserting new cells below "Variable Expenses" title (Cell 29) and writing the name of the Category and/or Subcategory. By doing this, the rest of the GoogleSheet tabs will get modified and the backend will consume all categories below "Variable Expenses" title.

## Backend

