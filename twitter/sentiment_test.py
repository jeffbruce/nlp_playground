import bokeh
import pandas as pd
import seaborn as sns
from textblob import TextBlob

from psycopg2_utilities import run_query
from constants import db, db_user, db_pw, db_host

dsn = "dbname={db} user={db_user} password={db_pw} host={db_host} port=5432".format(db=db, db_user=db_user, db_pw=db_pw, db_host=db_host)
select_query = '''select * from tweets;'''

results = run_query(q=select_query, dsn=dsn)
tweets = [t[4] for t in results]
dates = [t[2] for t in results]
search_terms = [t[3] for t in results]

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def rolling_x(df, col, groupby, x):
    df[col+'_'+str(x)] = df.groupby(groupby)[col].rolling(window=x, min_periods=x).mean().reset_index()[col]
    return df

# df = pd.DataFrame(data=tweets, columns=['tweet'])
df = pd.DataFrame(data={'tweet': tweets, 'date': dates, 'search_term': search_terms})
df = df.sort_values(by=['date', 'search_term'])

# This is slow.  Might be better to join all strings together first, then apply 
df['polarity'] = df['tweet'].apply(get_polarity)
df['subjectivity'] = df['tweet'].apply(get_subjectivity)

df = rolling_x(df=df, col='polarity', groupby='search_term', 50)
df = rolling_x(df=df, col='subjectivity', groupby='search_term', 50)

# df_wide = df.pivot(index='date', columns='search_term', values='polarity')
df_wide = df.pivot_table(values='polarity_50', index='date', columns='search_term', aggfunc='mean')
df_wide.reset_index(inplace=True)


# Takes way too long to run.
# sns.lineplot(x='date', y='polarity', hue='search_term', data=df)

from bokeh.plotting import figure, show, output_file, output_notebook
# p = figure(title="Blah", y_axis_type="linear", x_axis_type='datetime', tools = TOOLS)
p = figure(title='Crypto Polarity Sentiment', y_axis_type='linear', x_axis_type='datetime', plot_width=1200, plot_height=600)
# p.line(df_wide['date'], df_wide.bitcoin, legend="burglary", line_color="purple", line_width = 3)
p.line(df_wide['date'], df_wide.bitcoin, legend='bitcoin', line_color='purple', line_width=2)
p.line(df_wide['date'], df_wide.ethereum, legend='ethereum', line_color='green', line_width=2)
output_file('test_plot.html', title='Test Plot')

show(p)  # open a browser


# # Outdated.  bokeh.charts is now the bkcharts library which is unmaintained.
# xyvalues = pd.DataFrame(dict(
#         bitcoin=df_wide.bitcoin
#         ,ether=df_wide.ethereum
#         ,date=df_wide.date
#     ))
# output_file('test.html')
# p = TimeSeries(xyvalues, index='date', legend=True,
#                title='Crypto Polarity Over Time', ylabel='Polarity')
# show(p)