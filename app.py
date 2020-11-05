from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flaskext.mysql import MySQL
import time
import threading , sys

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Prueba:prueba@cluster0.xv7cj.mongodb.net/Prueba?retryWrites=true&w=majority'
mongo = PyMongo(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'bdb20eaa9eef3c'
app.config['MYSQL_DATABASE_PASSWORD'] ='d0387f2a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_42078ca09a517b2'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'

mysql.init_app(app)

def traspaso_datos():
    varwhile = True
    # varwhile = 1
    while varwhile != False :
        # user_collection = mongo.db.entries
        # lista = []
        # for valFreestyle in user_collection.find():
        #     valFreestyle.pop('_id')
        #     valFreestyle['date'] = int(valFreestyle['date'])
        #     listaAux = valFreestyle.values()
        #     listas = tuple(listaAux)
        #     lista.append(listas)
        # db2 =  mysql.connect()
        # mycursor = db2.cursor()
        # querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # error = ""
        # try:
        #     mycursor.executemany(querry,lista)
        #     db2.commit()
        #     print("Number record inserted, ID:", mycursor.lastrowid)
        # except:
        #     print("Eror: "+ error)
        # db2.close()
        time.sleep(300)     # similar a delay(segundos)
        print("Actualizacion de datos")
    else:
        print("algo salio malll")

#Usar hilos con threading
mythreading = threading.Thread(target = traspaso_datos )
mythreading.setDaemon(True)
mythreading.start()

@app.route('/')
def home():
    user_collection = mongo.db.entries
    lista = []
    for valFreestyle in user_collection.find():
        valFreestyle.pop('_id')
        valFreestyle['date'] = int(valFreestyle['date'])
        listaAux = valFreestyle.values()
        listas = tuple(listaAux)
        lista.append(listas)
    print("Datos leidos de MongoDB: " + len(lista))
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    error = ""
    try:
        mycursor.executemany(querry,lista)
        db2.commit()
        print("Number record inserted, ID:", mycursor.lastrowid)
    except:
        print("Eror: "+ error)
    db2.close()
    # time.sleep(300)     # similar a delay(segundos)
    print("Actualizacion de datos")

    return render_template('index.html')

# @app.route('/bascula')
@app.route('/bascula',methods = ['POST','GET'])
def bascula():
    if request.method ==  "POST":
        # iduser = request.form['idUser']
        varpeso = (request.form['peso'])
        peso = float(varpeso)
        print(type(peso))
        db2 =  mysql.connect()
        mycursor = db2.cursor()
        querry = "INSERT INTO pesoUsuarios (peso) VALUES (%s)"
        # arrayQuerry = ( iduser, peso )
        # print(querry % (iduser,peso))
        print("entro querry:" +querry%peso)
        try:
            mycursor.execute(querry,(peso))
            # print("Rowcont:  "+ mycursor.rowcount)
            db2.commit()
        except Exception as e :
            print("Eror: "+ e )
        db2.close() 
        return render_template('index.html')
    return render_template('bascula.html')
# querry = "INSERT INTO pesoUsuarios (iduser, peso) VALUES (%s,%s)"
            # arrayQuerry = tuple( iduser, peso )
            # mycursor.execute(querry,arrayQuerry)
#if request.method ==  "POST":
if __name__ == "__main__":
    app.run(debug=1)