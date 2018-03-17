
# coding: utf-8

# In[1]:


# Dependencies
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd
import numpy as np


# In[2]:


# Save file path to variable
year_2015 = "CSV Data/2015data.csv"
year_2016 = "CSV Data/2016data.csv"
year_2017 = "CSV Data/2017data.csv"


# In[3]:


# Read with Pandas in to Dataframes
df_2015 = pd.read_csv(year_2015)
df_2016 = pd.read_csv(year_2016)
df_2017 = pd.read_csv(year_2017)


# In[4]:


# Print first five rows in 2015
df_2015.head()


# In[5]:


# Print first five rows in 2016
df_2016.head()


# In[6]:


# Print first five rows in 2017
df_2017.head()


# In[7]:


data_all = pd.concat([df_2015,df_2016,df_2017])
data_all.head()


# In[8]:


# Extract year, division, and quantity data
division_data = data_all.loc[:,["Year", "Division", "quantity"]]
division_data.head()


# In[9]:


# Group data by divison
men = division_data.loc[(division_data["Division"] == "Mens")]
women = division_data.loc[(division_data["Division"] == "Womens")]


# In[10]:


men_df = pd.DataFrame(men)
women_df = pd.DataFrame(women)


# In[11]:


men_q = men_df.groupby(["Year"]).sum()
men_q.reset_index(level=0, inplace=True)
men_q


# In[12]:


women_q = women_df.groupby(["Year"]).sum()
women_q.reset_index(level=0, inplace=True)
women_q


# In[13]:


# Plot men and women quantities
fig = plt.figure(dpi=200)
x = women_q['Year']
y = women_q['quantity']
z = men_q['quantity']
ax = plt.subplot(111)
ax.plot(x, y,color='r', marker='o',linewidth=2,alpha = 0.4, label = "Women")
ax.plot(x, z,color='b', marker='X',linewidth=2,alpha = 0.4, label = "Men")
x_axis = np.arange(len(women_q['Year']))
plt.xlim(2014.8,2017.2)
plt.xticks(np.arange(2015,2017.5))
legend=ax.legend()
plt.xlabel('Year')
plt.ylabel('Quantity ( in Hundred Millions)')
plt.title('Quantity by Division (2015 to 2017)')
sns.set_style("whitegrid")
plt.grid()
plt.savefig("quantity_division.png",bbox_extra_artists=(legend,), bbox_inches='tight')
plt.show()

