from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flaskext.mysql import MySQL
import time
import threading

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Prueba:prueba@cluster0.xv7cj.mongodb.net/Prueba?retryWrites=true&w=majority'
mongo = PyMongo(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'bec43b382c6e22'
app.config['MYSQL_DATABASE_PASSWORD'] ='9e83483e'
app.config['MYSQL_DATABASE_DB'] = 'heroku_9b4bacbd64cc96f'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'

mysql.init_app(app)

def transpaso_datos():
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
mythreading = threading.Thread(target = transpaso_datos )
mythreading.setDaemon(True)
mythreading.start()

@app.route('/')
def recoger_datos_y_enviar():
    # for item in lista:
    #     print(item)
    return render_template('index.html')

@app.route('/bascula',methods = ['POST','GET'])
def bascula():
    # iduser = request.form['iduser']
    peso = request.form['peso']
    # print(peso + " y id: " + iduser)
    print(peso)
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    # querry = "INSERT INTO pesoUsuario (iduser, peso) VALUES (%s,%s)"
    querry = "INSERT INTO pesoUsuario (peso) VALUES (%s)"
    error = ""
    try:
        print(querry % peso)
        # print(querry % iduser,peso)
        mycursor.execute(querry,peso)
        # arrayQuerry = [ iduser, peso ]
        # mycursor.execute(querry,arrayQuerry)
        db2.commit()
        print("Number record inserted, ID:", mycursor.lastrowid)
    except:
        print("Eror: "+ error)
    db2.close() 
    return render_template('bascula.html')

# @app.route('/pruebabascula',methods = ['POST'])
# def pruebabascula():
#     return render_template('pruebabascula.html')
#if request.method ==  "POST":
if __name__ == "__main__":
    app.run(debug=1)