ottawa.ca_dataset_processing
============================

data processing and visualization with Python

Ottawa.ca provides open dataset for each month.
http://data.ottawa.ca/dataset/ottawa-ca-web-visitation-monthly

This repo created to play with the dataset.

1. MapReduce.py provides processing all month datasets 

2. ottawa_across.py uses MapReduce to create list with (url, [data list for all months]) and plot for employment url data.

The graph is @:
https://plot.ly/~Peiwen/3

3. ottawa.py creates dict for each month dataset and plot.
a. top 10 Pageviews for each month
The example graph is @:
https://plot.ly/~Peiwen/72

b. bounce rate and exit rate for top 10 Pageviews URL in Aug2013.
The graph is @:
https://plot.ly/~Peiwen/7


plotly used for visualization.


