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
    try:
        while varwhile != False :
            #/////////////////////////////////////////////////////////////////////////
            #--------------     Lectura MongoDB  -------------------------------------
            user_collection = mongo.db.entries
            lista = []
            oldList = []
            cont = 0
            for valFreestyle in user_collection.find():
                #   Adqisicion datos almacenados
                oldList.append(valFreestyle)
                #   Fin
                valFreestyle.pop('_id')
                valFreestyle['date'] = int(valFreestyle['date'])
                listaAux = valFreestyle.values()
                listas = tuple(listaAux)
                lista.append(listas)
                cont+=1
            print(cont)
            #-------------- Fin Lectura MongoDB  -------------------------------------
            #/////////////////////////////////////////////////////////////////////////
            #-------------- Hacer backup MongoDB -------------------------------------
            # user_collection = mongo.db.oldata
            # cont = 0
            # for oldListItem in oldList:
            #     repetido = user_collection.find_one({"date":oldListItem.get("date")})
            #     if repetido is None:
            #         # print("Puede Ingresar: ", oldListItem )
            #         doc = mongo.db.oldata.insert_one(oldListItem)
            #     # else:
            #     #     print("Esta repetido: ", oldListItem)
            #     cont+=1
            # print("Conteo backup: ",cont)
            #-------------- FIN Hacer backup MongoDB ---------------------------------
            #/////////////////////////////////////////////////////////////////////////
            #--------------     Insersión MySQL  -------------------------------------
            db2 =  mysql.connect()
            mycursor = db2.cursor()
            querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            error = ""
            try:
                mycursor.executemany(querry,lista)
                db2.commit()
                print("Number record inserted, ID:", mycursor.lastrowid)
            except:
                print("No Insersión ")
            db2.close()
            #--------------  Fin Insersión MySQL  -------------------------------------
            #//////////////////////////////////////////////////////////////////////////
            #-----     Eliminar de colecion principal MongoDB.entries  ----------------
            # user_collection = mongo.db.entries
            # for valOldDelete in oldList:
            #     user_collection.find_one_and_delete({"date":valOldDelete.get("date")})
            #-----   FIN  Eliminar de colecion principal MongoDB.entries  -------------
            #/////////////////////////////////////////////////////////////////////////
            print("Actualizacion de datos")
            time.sleep(300)
    except:
        print("algo salio malll")
    #---------------------------------------------
        # Esto es para eliminar de mongodb
    
#Usar hilos con threading
mythreading = threading.Thread(target = traspaso_datos )
mythreading.setDaemon(True)
mythreading.start()

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/bascula')
@app.route('/bascula',methods = ['POST','GET'])
def bascula():
    if request.method ==  "POST":
        iduser = request.form['idUser']
        varpeso = (request.form['peso'])
        peso = float(varpeso)
        db2 =  mysql.connect()
        mycursor = db2.cursor()
        query = "INSERT INTO pesoUsuarios (iduser, peso) VALUES (%s,%s)"
        # query = "INSERT INTO pesoUsuarios (peso) VALUES (%s)"
        arrayQuerry = ( iduser, peso )
        # print(query % (iduser,peso))
        print("entro querry:" +query%arrayQuery)
        try:
            mycursor.execute(query,arrayQuery)
            # print("Rowcont:  "+ mycursor.rowcount)
            db2.commit()
        except Exception as e :
            print("Eror: "+ e )
        db2.close() 
        return render_template('index.html')
    return render_template('bascula.html')
# query = "INSERT INTO pesoUsuarios (iduser, peso) VALUES (%s,%s)"
            # arrayQuerry = tuple( iduser, peso )
            # mycursor.execute(querry,arrayQuerry)
@app.route('/fitbit',methods = ['POST'])
def fitbit():
    if request.method == "POST":
        horafit = request.form['hora']
        id = request.form['id']
        stepsRate = request.form['stepsRate']
        caloriesRate = request.form['caloriesRate']
        heartRate = request.form['']
        print( "recived Data:  " + horafit +" "+ id +" "+stepsRate+" "+caloriesRate+" "+heartRate  )
    return "hi"

if __name__ == "__main__":
    app.run(debug=1)