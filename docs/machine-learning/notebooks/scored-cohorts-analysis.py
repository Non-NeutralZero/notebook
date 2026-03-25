import pandas as pd
import numpy as np
import plotly as py
import time
import json, urllib
from sklearn import model_selection
from time import mktime
from datetime import datetime
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings(action='once')

def add_score_class(row):
    """
    Creates a `scoring class/group` column, which is the one used in cohorts analysis, 
    based on the "true score".
    Won't be easily generalized, depends on model and use case
    
    Example
        df1["scoreClass"] = df1.apply(add_score_class, axis = 1)
    """
    if row['prediction2'] >= 0.95 :
        val = "High"
    elif row['prediction2'] >= 0.9 :
        val = "MHigh"
    elif row['prediction2'] >= 0.8 :
        val = "Medium"
    else:
        val = "Low"
    return val

path = ""
project_folder = ""
project_alias = ""
my_scoring_dates_list =  ["apr2019", "mar2019", "feb2019"]

def LoadCleanDataSet(scoring_dates_list) :
    frames = []
    for date in scoring_dates_list :
        file = path + project_folder + project_alias +  date + ".csv"
        df = pd.read_csv(file,  sep="|",  dtype={'0': np.str}, header = 0)
        df["scoreDate"] = my_scoring_dates_list[scoring_dates_list.index(date)]
        df['scoreDate'] = df.scoreDate.apply(lambda x:datetime.fromtimestamp(mktime(time.strptime(x,'%b%Y'))))
        df["scoreClass"] = df.apply(add_score_class, axis = 1)
        #df.columns = [str(col) + str(date) for col in df.columns]
        ## Make sure df is observation distrinct
        assert df['id' + str(date)].count() == df['id' + str(date)].drop_duplicates().count()
        frames.append(df)
    return frames

from functools import partial, reduce
# Process and structure into one dataframe
## load
loaded_dfs = LoadCleanDataSet(my_scoring_dates_list)

## assemble
concat_dfs = pd.concat(loaded_dfs , ignore_index=True)
concat_dfs = dict(tuple(concat_dfs.groupby([concat_dfs['scoreDate'].dt.year,
                                            concat_dfs['scoreDate'].dt.month])))
concat_dfs_reduce = partial(pd.merge, on = "id", how='outer')
ids_df  = reduce(concat_dfs_reduce, concat_dfs.values())
## clean
date_cols = [datecol for datecol in list(ids_df.columns) if ('Date') in datecol]
scoreClass_cols = [classcol for classcol in list(ids_df.columns) if ('Class') in classcol]

for i in range(len(date_cols)):
    ids_df.loc[ids_df[date_cols[i]].isnull(),date_cols[i]] = ids_df[date_cols[i]].dropna().unique()[0]

for i in range(len(scoreClass_cols)):
    ids_df.loc[ids_df[scoreClass_cols[i]].isnull(),scoreClass_cols[i]] = 'Unscored'

## done
print("Completed: ids_df {0} ready!".format(ids_df.shape))
