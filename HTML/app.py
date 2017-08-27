from flask import Flask, render_template, request
import random
import time
import datetime
import arrow
import subprocess
import sqlite3
from switch import Switch 	

app = Flask(__name__)

databasePath = 'var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db'

@app.route('/')
def index():
	message = random.randint(1,100)
	return render_template('index.html', message=message)

@app.route("/lab_temp")
def lab_temp():
	T = datetime.datetime.now()
	
	print "Get the last total"
	Asia = getLastTotal('Asian')
	amer = getLastTotal('American')
	per = getLastTotal('Persian')
	ita = getLastTotal('Italian')
	Latin =  getLastTotal('Latin')

	humidity = random.randint(1,100)
	return render_template("lab_temp.html",America=amer,asian=Asia,latin=Latin,italian=ita,persian=per )

def getLastTotal(Station):
	conn = sqlite3.connect("/var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db")
	curs = conn.cursor()	
	with Switch(Station) as case:
		if case('Asian'):
			curs.execute("SELECT * FROM Asian")
			data = curs.fetchall()
			print "getting asian"
		if case('American'):
			curs.execute("SELECT * FROM American")
			data = curs.fetchall()
			print "getting american"
		if case('Persian'):
			curs.execute("SELECT * FROM Persian")
			data = curs.fetchall()
			print "getting Persian"
		if case('Italian'):
			curs.execute("SELECT * FROM Italian"),
			data = curs.fetchall()
			print "getting Italian"
		if case('Latin'):
			curs.execute("SELECT * FROM Latin")
			data = curs.fetchall()
			print "getting Latin"


	print "about to get data"
	L = len(data)
	print "length: ", L
	Total = data[L-1]	
	print "Station: ", Station 
	print "Total,: ", Total[2]
	return Total[2]

#@app.route("/station_time")
#def station_time
	


@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
	Asian, American, Persian, Italian, Latin, timezone, from_date_str, to_date_str = get_records()	
#	temperatures, humidities, timezone, from_date_str, to_date_str = get_records()
	
	time_adjusted_temperatures = []
	time_adjusted_humidities   = []

	for record in Persian:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
		time_adjusted_temperatures.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])

#	for record in humidities:
#		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
#		time_adjusted_humidities.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])

	
#	humidity = random.randint(1,100)
#       temperature = random.randint(30.80)
	return render_template("lab_env_db.html",timezone	= timezone,
						temp	= time_adjusted_temperatures,
						hum 	= time_adjusted_humidities,
						from_date = from_date_str,
						to_date = to_date_str,
						temp_items = random.randint,#len(temperatures),
						query_string = request.query_string,
						hum_items = random.randint)#len(humidities))


def get_records():
	import sqlite3
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	timezone 	= request.args.get('timezone','Etc/UTC');
	range_h_form	= request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
	range_h_int 	= "nan"  #initialise this variable with not a number

	print "REQUEST:"
	print request.args
	
	try: 
		range_h_int	= int(range_h_form)
	except:
		print "range_h_form not a number"


	print "Received from browser: %s, %s, %s, %s" % (from_date_str, to_date_str, timezone, range_h_int)
	
	if not validate_date(from_date_str):	# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Validate date before sending it to the DB
	print '2. From: %s, to: %s, timezone: %s' % (from_date_str,to_date_str,timezone)
	# Create datetime object so that we can convert to UTC from the browser's local time
	from_date_obj       = datetime.datetime.strptime(from_date_str,'%Y-%m-%d %H:%M')
	to_date_obj         = datetime.datetime.strptime(to_date_str,'%Y-%m-%d %H:%M')

	# If range_h is defined, we don't need the from and to times
	if isinstance(range_h_int,int):	
		arrow_time_from = arrow.utcnow().replace(hours=-range_h_int)
		arrow_time_to   = arrow.utcnow()
		from_date_utc   = arrow_time_from.strftime("%Y-%m-%d %H:%M")	
		to_date_utc     = arrow_time_to.strftime("%Y-%m-%d %H:%M")
		from_date_str   = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M")
		to_date_str	    = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M")
	else:
		#Convert datetimes to UTC so we can retrieve the appropriate records from the database
		from_date_utc   = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")	
		to_date_utc     = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")

	conn 			= sqlite3.connect('/var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db')
	curs 			= conn.cursor()
	curs.execute("SELECT * FROM Asian WHERE date BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	Asian			= curs.fetchall()
	curs.execute("SELECT * FROM American WHERE date BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	American		= curs.fetchall()
	curs.execute("SELECT * FROM Persian WHERE date BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
        Persian			= curs.fetchall()
	curs.execute("SELECT * FROM Italian WHERE date BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
        Italian         	= curs.fetchall()
	curs.execute("SELECT * FROM Latin WHERE date BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
        Latin			= curs.fetchall()	 
	conn.close()

	return [Asian, American, Persian, Italian, Latin, timezone, from_date_str, to_date_str]

@app.route("/to_plotly", methods=['GET'])
def to_plotly():
	import plotly.plotly as py
	from plotly.graph_objs import *
  	import plotly.tools as pyTools
	pyTools.set_credentials_file(username='cega5137', api_key='jLRlCzSOlSOKuUtvknqD')

	Asian, American, Persian, Italian, Latin, timezone, from_date_str, to_date_str = get_records()

	# Create new record tables so that datetimes are adjusted back to the user browser's time zone.
	time_series_adjusted_Persian  = []
	time_series_adjusted_Asian 	= []
	time_series_Persian_values 	= []
	time_series_Asian_values 		= []

#	for record in Persian:
#		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
#		time_series_adjusted_Persian.append(local_timedate.format('YYYY-MM-DD HH:mm'))
#		time_series_Persian_values.append(round(record[2],2))

#	for record in Asian:
#		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
#		time_series_adjusted_Asian.append(local_timedate.format('YYYY-MM-DD HH:mm')) #Best to pass datetime in text																			  #so that Plotly respects it
#		time_series_Asian_values.append(round(record[2],2))


#################### Start Persian plot ##################
	print "About to start getting into the functions"
	plot_url = getPlotStation(Persian,"Persian Station")
	plot_url2 = getPlotStation(Asian,"Asian Station")
	plot_url3 = getPlotStation(Italian,"Italian Station")
	plot_url4 = getPlotStation(American,"Persian Station")
	plot_url5 = getPlotStation(Latin,"Latin Station")
	'''
	per = Scatter(
        		x=time_series_adjusted_Persian,
        		y=time_series_Persian_values,
        		name= 'Number of People'
    				)
#	hum = Scatter(
#        		x=time_series_adjusted_humidities,
#        		y=time_series_humidity_values,
#        		name='Humidity',
#        		yaxis='y2'
#			)

	data = Data([per]) # change from Data([temp, hum]) --> Data([temp])

	layout = Layout(
					title="Persian Station",
				    xaxis=XAxis(
				        type='date',
				        autorange=True
				    ),
				    yaxis=YAxis(
				    	title='Number of People',
				        type='linear',
				        autorange=True
				    ),
#				    yaxis2=YAxis(
#				    	title='Percent',
#				        type='linear',
#				        autorange=True,
#				        overlaying='y',
#				        side='right'
#				    )

					)
	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='lab_temp_hum')
	
############## Asian Plot ######################

	hum = Scatter(
		x = time_series_adjusted_Asian,
		y = time_series_Asian_values,
		name = 'HUM'
	)

	data2 = Data([hum])


	layout2 = Layout(
			title="Asian station",
			xaxis=XAxis(
					type='date',
					autorange=True
				),
			yaxis=YAxis(
					title='Number of People',
					type='linear',
					autorange=True
				),
			)

	fig2 = Figure(data=data2,layout=layout2)
	plot_url2 = py.plot(fig2,filename='lab_temp_hum2')

	
##### Italian Station #####
	layout3 = Layout(
			title="Italian Station"
			xaxis=XAxis(
					type='date',
					autorange=True
				),
			yaxis=YAxis(
					title='Number of People'
					type='linear'
					autorange=True
				),
			)
	
	fig3 = Figure(data=data3,layout=layout3)
        plot_url3 = py.plot(fig3,filename='lab_temp_hum2')

#### American Station ####
	layout4 = Layout(
                        title="American Station"
                        xaxis=XAxis(
                                        type='date',
                                        autorange=True
                                ),
                        yaxis=YAxis(
                                        title='Number of People'
                                        type='linear'
                                        autorange=True
                                ),
                        )

	fig4 = Figure(data=data4,layout=layout4)
        plot_url4 = py.plot(fig4,filename='lab_temp_hum2')

#### Latin Station ##### 
	layout5 = Layout(
                        title="Latin Station"
                        xaxis=XAxis(
                                        type='date',
                                        autorange=True
                                ),
                        yaxis=YAxis(
                                        title='Number of People'
                                        type='linear'
                                        autorange=True
                                ),
                        )

	fig5 = Figure(data=dat5,layout=layout5)
        plot_url5 = py.plot(fig5,filename='lab_temp_hum2')



	'''
	return plot_url2

def getPlotStation(pers, plotTitle):
	import plotly.plotly as py
    	from plotly.graph_objs import *
    	import plotly.tools as pyTools
	pyTools.set_credentials_file(username='cega5137', api_key='jLRlCzSOlSOKuUtvknqD')
	
	time_series_adjusted  = []
	time_series_values    = []

        for record in pers:
                local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
                time_series_adjusted.append(local_timedate.format('YYYY-MM-DD HH:mm'))
                time_series_values.append(round(record[2],2))


        per = Scatter(
                        x=time_series_adjusted,
                        y=time_series_values,
                        name= 'Number of People'
                                )

        data = Data([per]) # change from Data([temp, hum]) --> Data([temp])

        layout = Layout(title=plotTitle,
                        xaxis=XAxis(
										type='date',
                 						autorange=True
                                   ),
                        yaxis=YAxis(
		        		title='Number of People',
                                        type='linear',
                                        autorange=True
                                    ),
                                    )
        fig = Figure(data=data, layout=layout)
		
	switcher = {"Persian Station":py.plot(fig, filename='persian_station_C4C'),
			"Asian Station":py.plot(fig, filename='asian_station_C4C'),
			"Italian Station":py.plot(fig, filename='italian_station_C4C'),
			"American Station":py.plot(fig, filename='american_station_C4C'),
			"Latin Station":py.plot(fig, filename='latin_staion_C4C'),			
	}
	plot_url = switcher[plotTitle]	
		
  #      plot_url = py.plot(fig, filename='lab_temp_hum')
	return plot_url
	

def validate_date(d):
	try:
		datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
		return True
	except ValueError:
		return False

if __name__ == '__main__':
	# change the ip address everytime
	arg = 'ip route list'
	p = subprocess.Popen(arg,shell = True, stdout = subprocess.PIPE)
	data = p.communicate()
	split_data = data[0].split()
	ipaddr = split_data[split_data.index('src')+1]
	my_ip = '%s' % ipaddr

	app.run(debug=True, host=my_ip,port=4996) # '10.0.0.151'

