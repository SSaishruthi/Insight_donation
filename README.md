# Insight_donation
This repo contains program given for insight data engineer program

Problem Statement
Identify repeated donors and calculate the following for each combination of recipient, zip code and calendar year
1. Total dollars received
2. Total number of contributions received
3. Donation amount in a given percentile

Input
1. Contribution file
2. Percentile file

Language - Python

Libraries needed
1. Pandas
2. Numpy
3. re
4. csv
5. os
6. datetime
7. decimal

Input filter conditions

Eliminate records if it satisfies following conditions

1. Get only first digits from the zip code and eliminate if the field is empty or contains digits less than length 5
2. Other_id has value
3. committee id is empty 
4. Amount field is empty
5. Improper date field or date in range specified
6. Improper name field


Input needed 
1. start and end year
2. Current year for which final output processing has to be done

*** Path of input and output file needs to be updated before running ***
*** Both jupyter and py files are in src folder **

