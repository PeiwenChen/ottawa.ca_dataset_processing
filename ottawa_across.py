
"""
Use MapReduce to read all files and get the list of data across months.
Author: Peiwen Chen
Date: Nov 4th, 2014
"""

import MapReduce
import sys

from xlrd import open_workbook
from xlrd import XL_CELL_EMPTY, XL_CELL_NUMBER, XL_CELL_DATE, XL_CELL_BOOLEAN, XL_CELL_ERROR, XL_CELL_BLANK

import plotly.plotly as myplotly 
from plotly.graph_objs import *

mr = MapReduce.MapReduce()

filenames = []

def read_filenames():
	'read filenames list'
	filenames.append('January2013.xls')
	filenames.append('February2013.xls')
	filenames.append('March2013.xlsx')
	filenames.append('April2013.xlsx')
	filenames.append('May2013.xlsx')
	filenames.append('June2013.xls')
	filenames.append('July2013.xls')
	filenames.append('August2013.xlsx')
	filenames.append('Sept2013.xls')
	filenames.append('Oct2013.xls')
	filenames.append('Nov2013.xls')
	filenames.append('Dec2013.xls')
	filenames.append('Jan2014.xls')
	filenames.append('Feb2014.xls')
	filenames.append('Mar2014.xlsx')
	filenames.append('Apr2014.xlsx')
	filenames.append('May2014.xlsx')
	filenames.append('June2014.xls')
	filenames.append('July2014.xlsx')
	filenames.append('Aug2014.xlsx')
	filenames.append('Sep2014.xlsx')
	
	# print filenames
	# print 'there are 21 files'

# record can be a line, a doc or a dict
def mapper(filename):
    # key: document identifier
    # value: document contents
	wb =  open_workbook(filename)
	# print 'file: %s has %d sheets' %(filename, wb.nsheets)
	s = wb.sheet_by_index(0) # only sheet0 is valid
	# print 'file: %s, Sheet: %s' %(filename, s.name)
	# find the row idx starting with Pageviews
	PageIdx = 8 # default start with colume 7
	
	for row in range(s.nrows):
		values = [] 
		values.append(filename)
		url = [] 
		for col in range(s.ncols):
			cell = s.cell(row, col)
			ctype = cell.ctype
			cvalue = cell.value
			
			## add the new value into dict 	
			if col < PageIdx and ctype != XL_CELL_EMPTY and ctype != XL_CELL_BLANK:
				if ctype == XL_CELL_NUMBER or ctype == XL_CELL_DATE or ctype == XL_CELL_BOOLEAN: #float
					add = str(cvalue)
				elif ctype == XL_CELL_ERROR:
					continue
				else: # XL_CELL_TEXT
					add = cvalue.encode('utf-8') 
				
				if add == 'Pageviews':
					# print 'Pageviews starting with col %d' %col
					PageIdx = col
				# add into url as key
				url.append(add+'/')
			elif col >= PageIdx:
				# add numbers into values directly	
				if ctype == XL_CELL_NUMBER: #float
					add = cvalue
				elif ctype == XL_CELL_DATE:
					add = cvalue
				elif ctype == XL_CELL_BOOLEAN:
					add = cvalue
				elif ctype == XL_CELL_ERROR:
					add = 0
				elif ctype == XL_CELL_EMPTY or ctype == XL_CELL_BLANK:
					add = 0
				else: # XL_CELL_TEXT
					add = cvalue.encode('utf-8') 
			
				# add into values list
				values.append(add)
			else:
				continue
		urlstr = ''.join(url)
		# filter
		if urlstr and urlstr != 'en/' and urlstr != 'fr/' \
				and urlstr != 'en' and urlstr != 'fr' \
				and (urlstr.startswith('en/') or urlstr.startswith('fr/')) :
			# key is urlstr, value is its data
			mr.emit_intermediate(urlstr, values)

def reducer(key, list_of_values):
    # key: urlstr 
    # value: url data 
    url_data = []
    for v in list_of_values:
      url_data.append(v)
    mr.emit((key, url_data))

# MapReduce results 
url_across_months_data = []

def url_across_months():
	' mapreduce get each url info from all files, write to output file'
	url_across_months_data = mr.execute(filenames, mapper, reducer)
	print url_across_months_data

############## Applications ################

attributes = ['Pageviews', 'Unique Pageviews', 'Avg. Time on Page', 'Entrances', 'Bounce Rate', '% Exit']

def view_employment():
	'view employment info across months and visualize'
	url = 'en/long-range-financial-plans/economy-and-demographics/employment/'
	content = []
	for item in url_across_months_data:
		if item[0] == url:
			content = item[1]
	# print content
	
	myplotly.sign_in("Peiwen", "mwhf8szqka")
	x0 = [row[0] for row in content] # filename
	y1 = [row[1] for row in content] # Pageviews
	y2 = [row[2] for row in content] # Unique Pageviews
	trace1 = Bar(x=x0, y=y1, name='Pageviews')
	trace2 = Bar(x=x0, y=y2, name='Unique Pageviews')
	data = Data([trace1, trace2])
	layout = Layout(barmode='stack')
	fig = Figure(data = data,  layout=layout)
	plot_url = myplotly.plot(fig, filename='employment view Pageviews across all months')

if __name__ == '__main__':
	# 1. read all files
	read_filenames()
	# 2. mapreduce create the url_across_months_data list
	url_across_months()
	#app 1. view employment Pageviews across months
	#view_employment()
