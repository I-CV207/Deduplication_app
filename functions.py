import warnings
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from sqlalchemy import create_engine, Integer, Text, Float
import itertools
from rapidfuzz import process, utils, fuzz
from rapidfuzz.process import cdist
import numpy as np
pd.set_option('display.max_columns', None)
warnings.filterwarnings("ignore")

def detect_fuzzy_duplicates_optimized(df, column, index,threshold=85):
    """
    Detects fuzzy duplicates in a DataFrame using optimized fuzzy matching.
    
    Parameters:
    - df: The DataFrame to check for duplicates.
    - column: The column name to consider when identifying duplicates.
    - index:  The column index from the values to compare.
    - threshold: The similarity threshold (0-100) above which two entries are considered duplicates.
    
    Returns:
    - A DataFrame containing pairs of potentially duplicate rows with their similarity score.
    """
    potential_duplicates = []
    
    # Extract the column data as a list
    data = df[column].tolist()
    index_data=df[index].tolist()
    
    # Use itertools to create combinations of rows
    for i, j in itertools.combinations(range(len(data)), 2):
        similarity = fuzz.ratio(data[i], data[j])
        
        if similarity >= threshold:
            potential_duplicates.append((i #Generic index of analyzed column
                                         ,index_data[i] # Column choosed as index
                                         ,data[i] # Value compared
                                         ,j  #Resulting generic index who is a match
                                         ,index_data[j] # Resulting index match
                                         ,data[j] # Resulting match
                                         ,similarity#Similarity score
                                         ))
    
    duplicates_df = pd.DataFrame(potential_duplicates, columns=['Index_1',index,column, 'Index_2',index,column, 'Similarity'])
    
    return duplicates_df.sort_values(by='Similarity',ascending=False)