from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib as plt

engine = create_engine('postgresql://postgres:hollyleaf@localhost:5432/nhltest')

df = pd.read_sql_query('select * from gameresults', con=engine)

