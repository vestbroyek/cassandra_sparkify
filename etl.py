import pandas as pd
import cassandra
from cassandra.cluster import Cluster
import re
import os
import glob
import numpy as np
import json
import csv

# create list of filepaths 
filepath = os.getcwd() + '/event_data'

# create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    file_path_list = glob.glob(os.path.join(root,'*'))

pass