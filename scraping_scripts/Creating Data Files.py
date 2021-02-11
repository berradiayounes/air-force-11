# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:05:33 2021

@author: nicol
"""
#Here we will create 2 files : 1 simple file that contains only the reviews. The second file will contain 
#the additional pieces of information each member of the group managed to scrap.

import pandas as pd
import numpy as np


#DF2 part
df2 = pd.read_csv('flight_report.csv')
df2 = df2.rename(columns={'review' : 'Review Body'})
df2_simple = df2['Review Body']

#DF4 PART
df4 = pd.read_csv('airlineratings.csv', sep = '\t')

#standardizing the scores /10
df4['Overall Value for Money'] = df4['Overall Value for Money'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Seat and Cabin Space'] = df4['Seat and Cabin Space'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Customer Service'] = df4['Customer Service'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['In Flight Entertainment'] = df4['In Flight Entertainment'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Baggage Handling'] = df4['Baggage Handling'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Check-in Process'] = df4['Check-in Process'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Meals and Beverages'] = df4['Meals and Beverages'].replace(['100%','90%','80%','70%','60%','50%','40%','30%','20%','10%','0%'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Rating'] = df4['Rating'].replace(['10/10', '9/10', '8/10', '7/10', '6/10','5/10', '4/10', '3/10', '2/10', '1/10','0/10'],[float(10),float(9), float(8), float(7), float(6), float(5), float(4), float(3), float(2), float(1), float(0)])
df4['Review Title'] = np.nan
df4['Route'] = np.nan

#rearranging the different columns to to append the different files after
df4_rearranged = df4[['Airline','Review Title', 'Review', 'Recommend Airline', 'Rating', 'Class', 'Country','Route',
                      'Overall Value for Money', 'Seat and Cabin Space',"Customer Service", 'In Flight Entertainment',
                      'Meals and Beverages','Date' ]]

#renaming the columns to append the different files after
df4_rearranged = df4_rearranged.rename(columns={'Review' : 'Review Body','Recommend Airline': 'Recommended', 'Rating' : 'Score',
                               'Overall Value for Money':'Score Value for Money','Seat and Cabin Space' : 'Score Seat Comfort',
                              'Customer Service':'Cabin Staff & Customer Service', 'Meals and Beverages': 'Food and Beverages', 
                                                'In Flight Entertainment' : 'Inflight Entertainment'})

df4_simple  = df4_rearranged['Review Body']
simple_master_file = df2_simple.append(df4_simple)

#DF6 PART
df6 = pd.read_excel('trip_advisor_reviews.xlsx')
df6 = df6.rename(columns={'reviews' : 'Review Body'})
df6['scores'] = df6['scores']*2 #standardizing the scores /10

df6_simple  = df6['Review Body']
simple_master_file = simple_master_file.append(df6_simple)

#DF7 PART
df7 = pd.read_csv('5thScrapping.csv', sep = '\t')
del df7['Aircraft']
del df7['Type_Of_Traveller']

#rearranging the different columns to to append the different files after
df7_rearranged = df7[['Airline', 'Review title', 'Review_Body', 'Recommended', 'Rating out of 10',
                      'Seat_Type', 'Route', 'Value For Money', 'Seat comfort', 'Cabin Staff Service',
                      'Inflight Entertainment', 'Food and Beverages', 'Date Published']]

#renaming the columns to append the different files after
df7_rearranged = df7_rearranged.rename(columns={'Review title':'Review Title','Review_Body': 'Review Body', 
                                'Rating out of 10': 'Score', 'Seat_Type':'Class', 'Value For Money' : 'Score Value for Money',
                               'Seat comfort': 'Score Seat Comfort', 'Cabin Staff Service' : 'Cabin Staff & Customer Service',
                               'Date Published' : 'Date'})

df7_simple  = df7_rearranged['Review Body']
simple_master_file = simple_master_file.append(df7_simple)

#Creating a simple master file with only the reviews
simple_master_file.to_csv('Master File Review Only.csv')

#Creating a big masterfile that tries to not loose date
master_file = pd.DataFrame(columns =['Airline', 'Review Title', 'Review Body', 'Recommended', 'Score', 'Class', 'Country','Route', 'Score Value for Money', 'Score Seat Comfort', 'Cabin Staff & Customer Service', 'Inflight Entertainment', 'Food and Beverages', 'Date'])
master_file = master_file.append(df4_rearranged)
master_file = master_file.append(df7_rearranged)
master_file.to_csv('Complete Master File.csv')