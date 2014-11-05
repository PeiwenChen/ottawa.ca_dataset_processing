
"""
process all datasets and extract interesting info for visualization
Author: Peiwen Chen
Date: Nov 04, 2014
"""

from xlrd import open_workbook
from xlrd import XL_CELL_EMPTY, XL_CELL_NUMBER, XL_CELL_DATE, XL_CELL_BOOLEAN, XL_CELL_ERROR, XL_CELL_BLANK

import plotly.plotly as myplotly 
from plotly.graph_objs import *

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

def creat_webvisit(filename):
	# create webvisit dict {url: values} for filename
	wb =  open_workbook(filename)
	webvisit = {}
	s = wb.sheet_by_index(0)
	# print 'file: %s, Sheet: %s' %(filename, s.name)
	# find the row idx starting with Pageviews
	PageIdx = 8 # default start with colume 7
	
	for row in range(s.nrows):
		values = [] 
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
			webvisit[urlstr] = values
	# print webvisit
	return webvisit 

# dict for all datasets {filename: {url: values}}
dictall = {}

def creat_dictall():
	'return dictall' 
	for filename in filenames:
		webvisit = creat_webvisit(filename)
		dictall[filename] = webvisit


############## Applications ################

attributes = ['Pageviews', 'Unique Pageviews', 'Avg. Time on Page', 'Entrances', 'Bounce Rate', '% Exit']

def top10_att_month(attribute, month):
	'view top10 for attribute in month and visualize'
	webvisit = creat_webvisit(month)
	att = attributes.index(attribute)
	top10_att = sorted(webvisit.items(), key=lambda x:(x[1])[att], reverse=True)
	top10 = top10_att[:9]
	x0 = [item[0] for item in top10]  # url
	y = [item[1][att] for item in top10] # top10 sorted by att
	y0 = [item[1][0] for item in top10] # Pageviews
	y1 = [item[1][1] for item in top10] # Unique Pageviews
	y2 = [item[1][2] for item in top10] # Avg Time on 
	y3 = [item[1][3] for item in top10] # Entrances
	y4 = [item[1][4] for item in top10] # Bounce rate
	y5 = [item[1][5] for item in top10] # Exit 
	myplotly.sign_in("Peiwen", "mwhf8szqka")
	trace = Bar(x=x0, y=y, name = attribute)
	trace0 = Bar(x=x0, y=y0, name = 'Pageviews')
	trace1 = Bar(x=x0, y=y1, name = 'Unique Pageviews')
	trace2 = Bar(x=x0, y=y2, name = 'Avg Time on')
	trace3 = Bar(x=x0, y=y3, name = 'Entrances')
	trace4 = Bar(x=x0, y=y4, name = 'Bounce Rate')
	trace5 = Bar(x=x0, y=y5, name = 'Exit')
	# plot for top10 attribute for month
	data = Data([trace])
	plot_url = myplotly.plot(data, filename='Top10 '+attribute+' in '+month) 
	"""	
	# plot Bounce and Exit for top10 attribute for month
	# can also plot other attributes
	data1 = Data([trace4, trace5]) 
	layout = Layout(barmode='group')
	plot_url = myplotly.plot(data1, filename='Bounce and Exit for top10 Pageviews in '+month)
	"""


def top10_across_months(attribute):
	att = attributes.index(attribute)
	for f in filenames:
		top10_att_month(attribute, f)


if __name__ == '__main__':
	# read all files
	read_filenames()
	#app 1. view top10 Pageviews across months
	top10_across_months('Pageviews')  
	#app 3. view top10 Pageviews for month 
	top10_att_month('Pageviews','April2013.xlsx')
