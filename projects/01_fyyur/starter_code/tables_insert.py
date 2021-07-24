import pandas as pd
from sqlalchemy import create_engine

# create db engine
engine = create_engine('postgresql://postgres@localhost:5432/fyyur-final')

# read excel files to separate dataframe
xls = pd.ExcelFile('data.xlsx')
venue_df = pd.read_excel(xls, 'venues')
artist_df = pd.read_excel(xls, 'artists')
show_df = pd.read_excel(xls, 'shows')

# Add data to tables
venue_df.to_sql(name='Venue', con=engine, if_exists='append', index=False)
artist_df.to_sql(name='Artist', con=engine, if_exists='append', index=False)
show_df.to_sql(name='Show', con=engine, if_exists='append', index=False)

