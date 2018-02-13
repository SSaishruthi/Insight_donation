
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import csv
import os
import datetime
import re
from decimal import Decimal


# In[2]:


#Input File read and create dataframe using the input
with open("C://Users//saish//Documents//insight//itcont.txt","r") as data:
    df = pd.DataFrame(l.rsplit("|") for l in data)


# In[3]:


#Renaming necessary columns
df.rename(columns={df.columns[0]: 'CMTE', df.columns[7]: 'NAME', df.columns[10]: 'ZIP',  
                   df.columns[13]: 'DATE', df.columns[14]: 'AMT', df.columns[15]:'OTHER'},inplace=True)


# In[4]:


#Selecting only necessary columns for processing
df_in = df[['CMTE', 'NAME', 'ZIP', 'DATE', 'AMT', 'OTHER' ]].copy()
df_in.head()


# # Input Consideration

# In[5]:


#Converting data frame to numpy array
inp_ar = df_in.as_matrix()


# In[6]:


def zip_code(in_arr):
    
    """
    This function performs zip_code evaluation.
    1. Get only first five digits from zip_code field
    2. Store index of data points whose zip has length less than 5 or not having any value 
    3. Delete data points corresponding to the indexes
    """

    for i in range (len(in_arr)):
        in_arr[i][2] = (in_arr[i][2][0:5])
    
    index = []
    for i in range(len(in_arr)):
        if (len(in_arr[i][2]) < 5) or in_arr[i][2] == '' :
            index.append(i)
    
    
    in_arr1 = np.delete(in_arr, index, axis=0)
        
    if len(index) == 0:
        return in_arr
    else:
        return in_arr1


# In[7]:


def empty_check(in_arr):
    
    """
    This function checks for the presence of any empty string in the following fields and delete those invalid data points
    1. other_id is not empty
    2. Committee id is empty
    3. Amount is empty
    
    Index corresponding to the data points satisfying above conditions are stored in an array.
    Data points corresponding to the indexes are removed
    """
    
    index = []
    for i in range(len(in_arr)):
        if in_arr[i][5] != '' or in_arr[i][0] == '' or in_arr[i][4] == '':
            index.append(i)
            
    
    in_arr1 = np.delete(in_arr, index, axis=0)
    
    if len(index) == 0:
        return in_arr
    else:
        return in_arr1


# In[8]:


def date_check(in_arr, start_date, end_date):
    
    """
    Below is the logic for date check
    - Check if the date field is empty, if yes then index corresponding to the data point is stored
    - If date has value, it is checked for valid format using datetime python module. If it is not valid, its corresponding 
      index value is stored.
    - If date has valid format it is checked whether it is in the specified year range which is obtained as 'input'. 
      If not in range, its index is stored in a list.
    - Data points corresponding to the indexes are removed
    """
    
    index = []
    for i in range(len(in_arr)):
        
        if in_arr[i][3] == '':
           index.append(i)
           continue
        else:
        
            year_val = int(in_arr[i][3][4:])
            date_val = int(in_arr[i][3][2:4])
            month_val = int(in_arr[i][3][0:2])
    
            try:
                date = datetime.datetime(year_val, month_val,date_val)
            #
                if (datetime.datetime(year=start_date, month=1,day=1) < 
                    datetime.datetime(year=year_val,month=month_val,day=date_val) <= 
                    datetime.datetime.now()) == False:
                
                    index.append(i)
                
            except ValueError:
                index.append(i)
      
    
    in_arr1 = np.delete(in_arr, index, axis=0)
    
    if len(index) == 0:
        return in_arr
    else:
        return in_arr1
            


# In[9]:


def name_check(in_arr):
    """
    Below function checks for proper name format. Any character other than a-Z/A-Z/' '/, are considered to be improper.
    Indexes of the data point holding proper name is stored and these data points are removed. 
    """
    index = []
    for i in range(len(in_arr)):
        
        if in_arr[i][1] != '':
            if re.match("^[a-zA-Z, ]*$",in_arr[i][1]):
                #print('valid')
                continue
            else:
                #print('invalid')
                index.append(i)
        else:
            #print('invalid')
            index.append(i)
            
    
    in_arr1 = np.delete(in_arr, index,axis=0)
    
    if len(index) == 0:
        return in_arr
    else:
        return in_arr1


# In[10]:


inp = zip_code(inp_ar)
#
inp1 = empty_check(inp)
#Give input for the start and stop date 
s_date = int(input())
e_date = int(input())
#
inp2 = date_check(inp1, s_date, e_date)
#
inp3 =  name_check(inp2)


# In[11]:


inp3


# # Creating index column

# Below are the functions performed 
# - create index column is created by combining name and zip code
# - Sort data points based on index
# - Remove unique data points which will give "repeated donors" 
# - Another indicator is created combining committee id and zip code for final output purpose.

# In[19]:


inp_df = pd.DataFrame(inp3)
inp_df.rename(columns={inp_df.columns[0]: 'CMTE', inp_df.columns[1]: 'NAME', inp_df.columns[2]: 'ZIP',  
                   inp_df.columns[3]: 'DATE', inp_df.columns[4]: 'AMT', inp_df.columns[5]:'OTHER'},inplace=True)
inp_df["Ind"] = inp_df[['NAME', 'ZIP']].apply(lambda x: '_'.join(x), axis=1)


# In[20]:


inp_df


# In[21]:


inp_df = inp_df.sort_values('Ind')
inp_df.head()


# In[22]:


inp_df1 = inp_df[inp_df['Ind'].duplicated(keep=False)]
inp_df1.head()


# In[23]:


inp_df1['check'] = inp_df1['CMTE'] + '_' + inp_df1['ZIP']
inp_df1 = inp_df1.sort_values('check')
inp_df1.head()


# # program logic

# In[25]:


final_inp = inp_df1.as_matrix()
current_year = int(input())


# In[26]:


#This is to get only contributions made by the repeated in the current year
index = []
for i in range (len(final_inp)):
    if final_inp[i][3][4:] != str(current_year):
        index.append(i)
    
final_int = np.delete(final_inp, index, axis=0) 


# In[27]:


final_int


# In[28]:


#percentile file read
with open("C://Users//saish//Documents//insight//percentile.txt","r") as data:
    for i in data:
        percentile = int(i)/100


# In[29]:


"""
Below is the process followed to obtain final output
- two arrays are created one to hold output(output_fl) and other temporary array(temp_arr) to hold value
- amt_lst : will hold amount of all contributor for a particular committee which is used to fill total amount field of output
- if committe id, zip code is same then percentile, total amount are calculated for output. The loop will run till committe id
  and zip code change. Since, date is filtered before it is not taken into consideration
"""
output_fl = np.empty((0,6), dtype=object)
temp_arr = np.empty((1,6), dtype=object)
amt_lst = []


# In[30]:


cnt = 1
for i in final_int:
    if cnt == 1:
        temp = i[7]
        temp_arr[0][0] = i[0]
        temp_arr[0][1] = i[2]
        temp_arr[0][2] = str(current_year)
        temp_arr[0][3] = i[4]
        temp_arr[0][4] = i[4]
        temp_arr[0][5] = str(cnt)
        #
        output_fl = temp_arr
        amt_lst.append(i[4])
        #print('list',amt_lst)
        #
        temp_arr = np.empty((1,6), dtype=object)
        cnt = cnt + 1
        #print('1',output_fl)
    else:
        if(temp == i[7]):
            #
            amt_lst.append(i[4])
            #
            temp_arr[0][0] = i[0]
            temp_arr[0][1] = i[2]
            temp_arr[0][2] = str(current_year)
            #
            
            perc = round(cnt*(percentile)) - 1
            temp_arr[0][3] = amt_lst[perc]
            #
            temp_arr[0][4] = str(sum(int(i) for i in amt_lst))
            temp_arr[0][5] = str(cnt)
            #
            output_fl = np.append(output_fl, temp_arr, axis=0)
            temp_arr = np.empty((1,6), dtype=object)
            cnt = cnt + 1
            #
        else:
            cnt = 1
            temp = i[7]
            #
            amt_lst = []
            amt_lst.append(i[4])
            #
            temp_arr[0][0] = i[0]
            temp_arr[0][1] = i[2]
            temp_arr[0][2] = str(current_year)
            temp_arr[0][3] = i[4]
            temp_arr[0][4] = i[4]
            temp_arr[0][5] = str(cnt)
            #
            output_fl = np.append(output_fl, temp_arr, axis=0)
            #
            temp_arr = np.empty((1,6), dtype=object)
            cnt = cnt + 1
            


# In[31]:


output_fl


# In[32]:


with open('C://Users//saish//Documents//insight//repeat_donors.txt','w+') as result:
    for i in range (len(output_fl)):
        result.write(output_fl[i][0] + '|' +
                     output_fl[i][1] + '|' + 
                     output_fl[i][2] + '|' +
                     output_fl[i][3] + '|' +
                     output_fl[i][4] + '|' +
                     output_fl[i][5] +  '\n')                       


# In[ ]:




