# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import scraper
import json
import numpy as np

app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///db.sqlite"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
db = SQLAlchemy(app)

from .models import Pet


# create route that renders index.html template
@app.route("/")
def home():
    results3 = db.session.query(Pet.no, Pet.hora_salida, Pet.origen, Pet.destino, Pet.hora_llegada, Pet.desde, Pet.name, Pet.lat, Pet.lon, Pet.dmxn, Pet.mxn).all()
    no = [result3[0] for result3 in results3]
    result = np.unique(no)

    return render_template("index.html", result = result)
@app.route("/scrape",methods=["GET", "POST"])
def scrape(): 
    if request.method == "POST":
        fecha = request.form["petFecha"]
        print(fecha)
        data = json.loads(scraper.scrape_last(fecha))
        #range(len(data["Name"])):
        #for i in data["Name"].items(): 
        #    print(len(data["Name"]))
        name = [v for (k, v) in data["Name"].items()]
        lat = [float(v) for (k, v) in data["Lat"].items() ]
        lon= [float(v) for (k, v) in data["Lon"].items()]
        no = [v for (k, v) in data["No"].items()]
        hora_salida=[v for (k, v) in data["Hora_Salida"].items()]
        origen=[v for (k, v) in data["Origen"].items()]
        destino=[v for (k, v) in data["Destino"].items()]
        hora_llegada=[v for (k, v) in data["Hora_Llegada"].items()]
        desde=[float(v) for (k, v) in data["Desde"].items()]
        dmxn = [v for (k, v) in data["Dmxn"].items()]
        mxn = [float(v) for (k, v) in data["Mxn"].items()]
        for j in range(len(data["Name"])): 
            pet = Pet( no=no[j], hora_salida=hora_salida[j], origen=origen[j], destino=destino[j], hora_llegada=hora_llegada[j], desde=desde[j], name=name[j], lat=lat[j], lon=lon[j], dmxn=dmxn[j], mxn=mxn[j])
            db.session.add(pet)
            db.session.commit()
        return redirect("/", code=302)
    return render_template("forms.html")
    #return jsonify(data)

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]
        no = request.form["petNo"]
        hora_salida = request.form["petHora_salida"]
        origen = request.form["petOrigen"]
        destino = request.form["petDestino"]
        hora_llegada = request.form["petHora_llegada"]
        desde = request.form["petDesde"]
        dmxn = request.form["petDmxn"]
        mxn = request.form["petMxn"]
        pet = Pet( no=no, hora_salida=hora_salida, origen=origen, destino=destino, hora_llegada=hora_llegada, desde=desde, name=name, lat=lat, lon=lon, dmxn=dmxn, mxn=mxn)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/pals")
def pals():
    results = db.session.query(Pet.no, Pet.hora_salida, Pet.origen, Pet.destino, Pet.hora_llegada, Pet.desde, Pet.name, Pet.lat, Pet.lon, Pet.dmxn, Pet.mxn).all()

    hover_text = [result[3] for result in results]
    lat = [result[7] for result in results]
    lon = [result[8] for result in results]

    flights_data = [{
        "type": "scattergeo",
        "locationmode": "country names",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",

        "marker": {
        "color": "#DB7093",
            "size": 5,
            "line": {
                "color": "rgb(8,8,8)",
                "width": .3
            },
        }
    }]

    return jsonify(flights_data)

@app.route("/api/pal")
def pal():
    results2 = db.session.query(Pet.no, Pet.hora_salida, Pet.origen, Pet.destino, Pet.hora_llegada, Pet.desde, Pet.name, Pet.lat, Pet.lon, Pet.dmxn, Pet.mxn).all()

    no = [result2[0] for result2 in results2]
    hora_salida = [result2[1] for result2 in results2]
    destino = [result2[3] for result2 in results2]
    desde = [result2[5] for result2 in results2]
    name = [result2[6] for result2 in results2]
    lat = [result2[7] for result2 in results2]
    lon = [result2[8] for result2 in results2]
    dmxn = [result2[9] for result2 in results2]
    mxn = [result2[10] for result2 in results2]


    flight_data = [{
        "no": no,
        "hora_salida": hora_salida,
        "destino": destino,
        "desde": desde,
        "name": name,
        "lat": lat,
        "lon": lon,
        "dmxn": dmxn,
        "mxn": mxn
    }]

    return jsonify(flight_data)

@app.route("/table",methods=["GET", "POST"])
def table():
    result0 = db.session.query(Pet.no, Pet.hora_salida, Pet.origen, Pet.destino, Pet.hora_llegada, Pet.desde, Pet.name, Pet.lat, Pet.lon, Pet.dmxn, Pet.mxn).all()
 
    yno = [result0[0] for result0 in result0]
    uno = np.unique(yno)

    yhora_salida = [result0[1] for result0 in result0]
    uhora_salida = np.unique(yhora_salida)

    ydestino = [result0[3] for result0 in result0]
    udestino = np.unique(ydestino)

    ydesde = [result0[5] for result0 in result0]
    udesde = np.unique(ydesde)

    yname = [result0[6] for result0 in result0]
    uname = np.unique(yname)

    ylat = [result0[7] for result0 in result0]
    ulat = np.unique(ylat)
    
    ylon = [result0[8] for result0 in result0]
    ulon = np.unique(ylon)

    ydmxn = [result0[9] for result0 in result0]
    udmxn= np.unique(ydmxn)

    ymxn = [result0[10] for result0 in result0]
    umxn = np.unique(ymxn)

   
    if request.method == "POST":
        uno = request.form.get("petUno")
        uhora_salida = request.form.get("petUhora_salida")
        udestino = request.form.get("petUdestino")
        udesde = request.form.get("petUdesde")
        uname = request.form.get("petUname")
        ulat = request.form.get("petUlat")
        ulon = request.form.get("petUlon")
        udmxn = request.form.get("petUdmxn")
        umxn = request.form.get("petUmxn")

        name = request.form.get("petName")
        lat = request.form.get("petLat")
        lon = request.form.get("petLon")
        no = request.form.get("petNo")
        hora_salida = request.form.get("petHora_salida")
        origen = request.form.get("petOrigen")
        destino = request.form.get("petDestino")
        hora_llegada = request.form.get("petHora_llegada")
        desde = request.form.get("petDesde")
        dmxn = request.form.get("petDmxn")
        mxn = request.form.get("petMxn")
        if uno is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.no==uno)
            uno = np.unique(yno)


        if uhora_salida is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.hora_salida==uhora_salida)
            uhora_salida = np.unique(yhora_salida)
            uno = np.unique(yno)
        else:
            uno = np.unique(yno)

        if udestino is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.destino==udestino)
            udestino = np.unique(ydestino)
            uhora_salida = np.unique(yhora_salida)
        else:
            uhora_salida = np.unique(yhora_salida)


        if udesde is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.desde==udesde)
            udesde = np.unique(ydesde)
            udestino = np.unique(ydestino)
        else:

            udestino = np.unique(ydestino)


        if uname is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.name==uname)
            uname = np.unique(yname)
            udesde = np.unique(ydesde)
        else:

            udesde = np.unique(ydesde)


        if ulat is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.lat==ulat)
            ulat = np.unique(ylat)
            uname = np.unique(yname)
        else:

            uname = np.unique(yname)
 

        if ulon is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.lon==ulon)
            ulon = np.unique(ylon)
            ulat = np.unique(ylat)
        else:

            ulat = np.unique(ylat)


        if udmxn is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.dmxn==udmxn)            
            udmxn= np.unique(ydmxn)
            ulon = np.unique(ylon)
        else:

            ulon = np.unique(ylon)



        if umxn is not "":
            yno = [result0[0] for result0 in result0]
            yhora_salida = [result0[1] for result0 in result0]
            ydestino = [result0[3] for result0 in result0]
            ydesde = [result0[5] for result0 in result0]
            yname = [result0[6] for result0 in result0]
            ylat = [result0[7] for result0 in result0]
            ylon = [result0[8] for result0 in result0]
            ydmxn = [result0[9] for result0 in result0]
            ymxn = [result0[10] for result0 in result0]
            result0 = db.session.query(Pet).filter(Pet.mxn==umxn) 
            umxn = np.unique(ymxn)
            udmxn= np.unique(ydmxn)
        else:
            udmxn= np.unique(ydmxn)
            umxn = np.unique(ymxn)

        if name is not "":
            result0 = db.session.query(Pet).filter(Pet.name==name)
        if lat is not "":
            result0 = db.session.query(Pet).filter(Pet.lat==lat)
        if lon is not "":
            result0 = db.session.query(Pet).filter(Pet.lon==lon)
        if no is not "":
            result0 = db.session.query(Pet).filter(Pet.no==no)
        if hora_salida is not "":
            result0 = db.session.query(Pet).filter(Pet.hora_salida==hora_salida)
        if origen is not "":
            result0 = db.session.query(Pet).filter(Pet.origen==origen)
        if destino is not "":
            result0 = db.session.query(Pet).filter(Pet.destino==destino)
        if hora_llegada is not "":
            result0 = db.session.query(Pet).filter(Pet.hora_llegada==hora_llegada)
        if desde is not "":
            result0 = db.session.query(Pet).filter(Pet.desde==desde)
        if dmxn is not "":
            result0 = db.session.query(Pet).filter(Pet.dmxn==dmxn)
        if mxn is not "":
            result0 = db.session.query(Pet).filter(Pet.mxn==mxn)
        
    return render_template("table.html", result0 = result0, uno=uno, uhora_salida=uhora_salida, udestino=udestino, udesde=udesde, uname=uname,ulat=ulat, ulon=ulon, udmxn=udmxn, umxn=umxn)

if __name__ == "__main__":
    app.run()
