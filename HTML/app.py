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
		if case('American'):
			curs.execute("SELECT * FROM American")
			data = curs.fetchall()
		if case('Persian'):
			curs.execute("SELECT * FROM Persian")
			data = curs.fetchall()
		if case('Italian'):
			curs.execute("SELECT * FROM Italian"),
			data = curs.fetchall()
		if case('Latin'):
			curs.execute("SELECT * FROM Latin")
			data = curs.fetchall()


	print "about to get data"
	L = len(data)
	print "length: ", L
	Total = data[L-1]	
	print "Station: ", Station 
	print "Total,: ", Total[2]
	return Total[2]

#@app.route("/station_time")
#def station_time
	
@app.route("/plot_db", methods=['GET'])
def plot_db():
	print "About to get records"
        Asian, American, Persian, Italian, Latin, timezone, from_date_str, to_date_str = get_records()

        asia_adjusted = convertRecords(Asian,timezone)
        amer_adjusted = convertRecords(American,timezone)
        pers_adjusted = convertRecords(Persian,timezone)
        ital_adjusted = convertRecords(Italian,timezone)
        lati_adjusted = convertRecords(Latin,timezone)
        print "Finish converting recods"
	
	return render_template("plot_db.html",timezone               = timezone,
                                                pers                    = pers_adjusted,
                                                asia                    = asia_adjusted,
                                                ital                    = ital_adjusted,
                                                amer                    = amer_adjusted,
                                                lati                    = lati_adjusted,
                                                from_date               = from_date_str,
                                                to_date                 = to_date_str,
                                                pers_items              = len(Persian),           #len(temperatures),
                                                query_string            = request.query_string,
                                                asia_items              = len(Asian),
                                                ital_items              = len(Italian),
                                                lati_items              = len(Latin),
                                                amer_items              = len(American)
                                                )

@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
	print "About to get records"
	Asian, American, Persian, Italian, Latin, timezone, from_date_str, to_date_str = get_records()	

	asia_adjusted = convertRecords(Asian,timezone)
	amer_adjusted = convertRecords(American,timezone)
	pers_adjusted = convertRecords(Persian,timezone)
	ital_adjusted = convertRecords(Italian,timezone)
	lati_adjusted = convertRecords(Latin,timezone)
	print "Finish converting recods"		

	return render_template("lab_env_db.html",timezone		= timezone,
						pers			= pers_adjusted,
						asia 			= asia_adjusted,
						ital			= ital_adjusted,
						amer			= amer_adjusted,
						lati			= lati_adjusted,
						from_date 		= from_date_str,
						to_date 		= to_date_str,
						pers_items 		= len(Persian),           #len(temperatures),
						query_string 		= request.query_string,
						asia_items 		= len(Asian),
						ital_items		= len(Italian),
						lati_items 		= len(Latin),
						amer_items		= len(American) 
				 		)         #len(humidities))


def convertRecords(station, timezone):
	time_adjusted = []

	for record in station:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
		time_adjusted.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])
	
	return time_adjusted

def get_records():
	import sqlite3
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	timezone 	= request.args.get('timezone','Etc/UTC');
	range_h_form	= request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
	range_h_int 	= "nan"  #initialise this variable with not a number

	print "REQUEST:"
	print request.args
	print "range_h_form", range_h_form	

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

#################### Start Persian plot ##################
	print "About to start getting into the functions"
	[plot_url, per] = getPlotStation(Persian,"Persian Station",timezone)
	[plot_url2, asi] = getPlotStation(Asian,"Asian Station",timezone)
	[plot_url3, ita] = getPlotStation(Italian,"Italian Station",timezone)
	[plot_url4, usa] = getPlotStation(American,"American Station",timezone)
	[plot_url5, lat] = getPlotStation(Latin,"Latin Station",timezone)
	plot_all = getAllPlot(per,asi, ita, usa, lat)
	return plot_all

def getPlotStation(pers, plotTitle,timezone):
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
		
	with Switch(plotTitle) as case:
		if case("Persian Station"):
			plot_url = py.plot(fig, filename='persian_station_C4C')
			print "Ploting Persian"
		if case("Asian Station"):
			plot_url = py.plot(fig, filename='asian_station_C4C')
			print "Ploting Asia"
		if case("Italian Station"):
			plot_url = py.plot(fig, filename='italian_station_C4C')
			print "Ploting Italian"
		if case("American Station"):
			plot_url = py.plot(fig, filename='american_station_C4C')
			print "Ploting American"
		if case("Latin Station"):
			plot_url = py.plot(fig, filename='latin_staion_C4C')
			print "Ploting Latin"
	
	print "Finishing ", plotTitle

	return [plot_url, per]

def getAllPlot(per, asi, ita, usa, lat):
	import plotly.plotly as py
        from plotly.graph_objs import *
        import plotly.tools as pyTools
        pyTools.set_credentials_file(username='cega5137', api_key='jLRlCzSOlSOKuUtvknqD')

        data = Data([per, asi, ita, usa, lat])
	
	layout = Layout(
			title="Count of people for all stations",
			xaxis=XAxis(
					type='date',
					autorange=True),

			yaxis=YAxis(
					title='Number of People',
					type='linear',
					autorange=True),
			)

	fig = Figure(data=data, layout=layout)
	plot_all_url = py.plot(fig, filename='C4C_count')

	return plot_all_url	

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

