import pandas as pd
import cassandra
from cassandra.cluster import Cluster
import re
import os
import glob
import numpy as np
import json
import csv


# connect
try:
    cluster=Cluster(['127.0.0.1'], port=9042)
    session=cluster.connect()
except Exception as e:
    raise

try:
	session.execute("""
		create keyspace if not exists test_keyspace
		with replication = 
		{'class': 'SimpleStrategy', 'replication_factor':1}"""
	)

except:
    pass

session.shutdown()

pass