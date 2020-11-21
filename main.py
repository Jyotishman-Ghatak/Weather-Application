from flask import Flask,render_template,request,redirect
import urllib.request,urllib.parse,urllib.error
import json
import ssl
import datetime
import calendar

def find_day(date):
    day = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
    return (calendar.day_name[day]) 

def find_month(date):
    datee=datetime.datetime.strptime(date,'%Y-%m-%d')
    return (calendar.month_abbr[datee.month])
def find_date(date):
    datee=datetime.datetime.strptime(date,'%Y-%m-%d')
    return(datee.day)

def find_time(date):
    hrs=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour()
    return(hrs)

def assign(location):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    apikey="6ca7eb32f125bf8ef4560ef0d30e7b0e"
    parms=dict()
    url="https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}".format(location,apikey)
    uh=urllib.request.urlopen(url,context=ctx)
    data=uh.read().decode()
    try:
        js=json.loads(data)
    except:
        js=None
    
    if(js!=None): 
        #Current temperature  
        parms['location']=js['city']['name']
        parms['temp1']=int(js['list'][0]['main']['temp'])
        parms['wind_speed']=js['list'][0]['wind']['speed']
        parms['wind_dir']=js['list'][0]['wind']['deg']
        parms['icon']=str(js['list'][0]['weather'][0]['icon'])
        parms['humidity']=js['list'][0]['main']['humidity']
        parms['day']=find_day(js['list'][0]['dt_txt'].split(" ")[0])        #datetime
        parms['month']=find_month(js['list'][0]['dt_txt'].split(" ")[0])
        parms['date']=find_date(js['list'][0]['dt_txt'].split(" ")[0])
        parms['country']=js['city']['country']
        #end Current temperature
        #Day2
        date=parms['date']
        count=1
        for i in range(4):
            date=date+1
            print("date {}".format(date))
            count=count+1
            min_temp=100
            max_temp=-100
            for j in js['list']:
                dt=j['dt_txt'][8:10]
                hrs=j['dt_txt'][11:13]
                if(int(date)==int(dt)):
                    if(min_temp>int(j['main']['temp_min'])):
                        min_temp=j['main']['temp_min']
                    if(max_temp<int(j['main']['temp_max'])):
                        max_temp=j['main']['temp_max']
                    parms["min_temp"+str(count)]=int(min_temp)
                    parms["max_temp"+str(count)]=int(max_temp) 
                    parms['day'+str(count)]=find_day(j['dt_txt'].split(" ")[0])
                    parms['icon'+str(count)]=j['weather'][0]['icon']


    else:
        print("No Data")
    

    return parms    


app=Flask(__name__)
@app.route('/')
def index():
    parms=dict()
    location="New Delhi"
    parms=assign(location)
    return render_template('index.html',**parms)


@app.route('/get_loc', methods=["POST","GET"])
def get_loc():
    if request.method=="POST":
        location=request.form['location']
        try:   
            parms=assign(location)
        except:
            return render_template("404.html")
            
        return render_template('index.html',**parms)
        
    else:
        return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)