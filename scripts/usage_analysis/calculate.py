#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data_file = "data_2.csv"

def load_data(dataset):
    return pd.read_csv(dataset, header=0, delimiter=';')

dataset = load_data(data_file)
dataset.head()


# In[7]:


valid_entries = dataset[(dataset['references_adoption'] > 0) & ~(pd.isnull(dataset['SHA_clone'])) & ~(pd.isnull(dataset['FT_commit']))]
print(len(valid_entries))
valid_entries.head()


# In[9]:


increased_use = valid_entries[valid_entries['references_adoption'] < valid_entries['references_current']]
print(len(increased_use))
increased_use.head()


# In[10]:


decreased_use = valid_entries[(valid_entries['references_adoption'] > valid_entries['references_current']) & (valid_entries['references_current'] != 0)]
print(len(decreased_use))
decreased_use.head()


# In[11]:


same_usage = valid_entries[valid_entries['references_adoption'] == valid_entries['references_current']]
print(len(same_usage))
same_usage.head()


# In[13]:


stopped_using = valid_entries[valid_entries['references_current'] == 0]
print(len(stopped_using))
stopped_using.head()


# In[16]:


total = len(valid_entries)
increased = (len(increased_use)/len(valid_entries)) * 100
decreased = (len(decreased_use)/len(valid_entries)) * 100
same = (len(same_usage)/len(valid_entries)) * 100
stopped = (len(stopped_using)/len(valid_entries)) * 100

print(f"Total: {total}")
print(f"Increased: {len(increased_use)}/{total}   -> {increased:.2f}%")
print(f"Decreased: {len(decreased_use)}/{total}   -> {decreased:.2f}%")
print(f"Same usage: {len(same_usage)}/{total}   -> {same:.2f}%")
print(f"Stopped using: {len(stopped_using)}/{total}   -> {stopped:.2f}%")




# In[ ]:




