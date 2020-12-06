from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flaskext.mysql import MySQL
import json
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

# def traspaso_datos():
#     varwhile = True
#     try:
#         while varwhile != False :
#             #/////////////////////////////////////////////////////////////////////////
#             #--------------     Lectura MongoDB  -------------------------------------
#             user_collection = mongo.db.entries
#             lista = []
#             oldList = []
#             cont = 0
#             for valFreestyle in user_collection.find():
#                 #   Adqisicion datos almacenados
#                 oldList.append(valFreestyle)
#                 #   Fin
#                 valFreestyle.pop('_id')
#                 valFreestyle['date'] = int(valFreestyle['date'])
#                 listaAux = valFreestyle.values()
#                 listas = tuple(listaAux)
#                 lista.append(listas)
#                 cont+=1
#             print(cont)
#             #-------------- Fin Lectura MongoDB  -------------------------------------
#             #/////////////////////////////////////////////////////////////////////////
#             #-------------- Hacer backup MongoDB -------------------------------------
#             # user_collection = mongo.db.oldata
#             # cont = 0
#             # for oldListItem in oldList:
#             #     repetido = user_collection.find_one({"date":oldListItem.get("date")})
#             #     if repetido is None:
#             #         # print("Puede Ingresar: ", oldListItem )
#             #         doc = mongo.db.oldata.insert_one(oldListItem)
#             #     # else:
#             #     #     print("Esta repetido: ", oldListItem)
#             #     cont+=1
#             # print("Conteo backup: ",cont)
#             #-------------- FIN Hacer backup MongoDB ---------------------------------
#             #/////////////////////////////////////////////////////////////////////////
#             #--------------     Insersión MySQL  -------------------------------------
#             db2 =  mysql.connect()
#             mycursor = db2.cursor()
#             querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#             # error = ""
#             try:
#                 mycursor.executemany(querry,lista)
#                 db2.commit()
#                 print("Number record inserted, ID:", mycursor.lastrowid)
#             except:
#                 print("No Insersión ")
#             db2.close()
#             #--------------  Fin Insersión MySQL  -------------------------------------
#             #//////////////////////////////////////////////////////////////////////////
#             #-----     Eliminar de colecion principal MongoDB.entries  ----------------
#             # user_collection = mongo.db.entries
#             # for valOldDelete in oldList:
#             #     user_collection.find_one_and_delete({"date":valOldDelete.get("date")})
#             #-----   FIN  Eliminar de colecion principal MongoDB.entries  -------------
#             #/////////////////////////////////////////////////////////////////////////
#             print("Actualizacion de datos")
#             time.sleep(300)
#     except:
#         print("algo salio malll")
#     #---------------------------------------------
#         # Esto es para eliminar de mongodb
    
# #Usar hilos con threading
# mythreading = threading.Thread(target = traspaso_datos )
# mythreading.setDaemon(True)
# mythreading.start()

@app.route('/')
def home():
    countSensor = coutData("sensorFreeStyle")
    countPeso = coutData("pesousuarios")
    print("Bienvenido")
    return render_template("index.html", sensor = countSensor, peso = countPeso)

@app.route('/bascula',methods = ['POST','GET'])
def bascula():
    if request.method ==  "POST":
        iduser = request.form['idUser']
        print(iduser)
        varpeso = (request.form['peso'])
        peso = float(varpeso)
        db2 =  mysql.connect()
        mycursor = db2.cursor()
        query = "INSERT INTO pesoUsuarios (iduser, peso) VALUES (%s,%s)"
        # query = "INSERT INTO pesoUsuarios (peso) VALUES (%s)"
        arrayQuery = ( iduser, peso )
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

@app.route('/fitbit',methods = ['POST','GET'])
def fitbit():
    response = request.get_json()
    print(response)
    fecha = response['hora']
    calories = response['caloriesRate']
    heartRate = response['heartRate']
    steps = response['stepsRate']
    print( "recived Data:  " + fecha + " " + str(steps) + " " + str(calories) + " " + str(heartRate) )
        #/////////////////////////////////////////////////////////////////////////
        #--------------     Insersión MySQL  -------------------------------------
        # db2 =  mysql.connect()
        # mycursor = db2.cursor()
        # querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # # error = ""
        # try:
        #     mycursor.executemany(querry,lista)
        #     db2.commit()
        #     print("Number record inserted, ID:", mycursor.lastrowid)
        # except:
        #     print("No Insersión ")
        # db2.close()
#             #--------------  Fin Insersión MySQL  -------------------------------------
    return '{"status":"funciona"}'
#-----------------------------------------------------------------
@app.route('/peso')
# @app.route('/index',methods = ['POST','GET'])
def peso():
    read = readTables("pesousuarios")
    return render_template("peso.html", read = read)
@app.route('/sensor')
# @app.route('/index',methods = ['POST','GET'])
def sensor():
    read = readTables("sensorFreeStyle")
    return render_template("sensor.html", read = read )
@app.route('/graficainsulina')
# @app.route('/index',methods = ['POST','GET'])
def graficainsulina():
    read = readLastData("sensorFreeStyle","dateString")
    (date,valGlucosa) = ordenarGrafica(read, 1 , 5 )
    return render_template("graficainsulina.html",dateGlucosa = date, glucosa = valGlucosa)
@app.route('/graficapeso')
# @app.route('/index',methods = ['POST','GET'])
def graficapeso():
    read = readLastData("pesousuarios","fecha")
    (date,valPeso) = ordenarGrafica( read, 2, 1)
    return render_template("graficapeso.html",datePeso = date, peso = valPeso)
@app.route('/graficacircular')
def graficacircular():
    read = readTables("sensorFreeStyle")
    zonasGraficaC = datacircular(read,5, 80, 120)
    return render_template("graficacircular.html",zonasGraficaC = zonasGraficaC)
@app.route('/graficacircularpeso')
def graficacircularpeso():
    read = readTables("pesousuarios")
    zonasGraficaC = datacircular(read,1,60,80)
    return render_template("graficacircularpeso.html",zonasGraficaC = zonasGraficaC)

#-----------------------------------------------------------------
def coutData(tabla):
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    querry = "select count(*) from "+ tabla
    error = ""
    try:
        mycursor.execute(querry)
        countData = mycursor.fetchone()
        print(countData[0])
        print("count row :", mycursor.rowcount)
        db2.commit()
        db2.close()
        return countData[0]
    except:
        print("Eror: "+ error)
        db2.close()
        countData = "vacio"
        return countData
    print(" ")

def readTables(tabla):
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    querry = "select * from " + tabla
    error = ""
    try:
        mycursor.execute(querry)
        readData = mycursor.fetchall()
        print("count row :", mycursor.rowcount)
        db2.commit()
        db2.close()
        return readData
    except:
        print("Eror: "+ error)
        db2.close()
        readData = "vacio"
        return readData
def datacircular(tuplaMySQL, indice, bajaNormal, normalAlta):
    zonasDataUser =[0,0,0]
    for valData in tuplaMySQL:
        if valData[indice] >= bajaNormal and valData[indice] <= normalAlta :
            zonasDataUser[1] += 1#   Zona media (Nivel sanoooo)
        elif valData[indice] > normalAlta:
            zonasDataUser[2] += 1#   Zona Alta (Hiperglucemico)
        elif valData[indice] < bajaNormal:
            zonasDataUser[0] += 1#   Zona Baja (Hipoglucemico)
        # print("0-"+ str(zonasDataUser[0]) + " 1-"+ str(zonasDataUser[1]) + " 2-"+ str(zonasDataUser[2]))
    return zonasDataUser
def readLastData(tabla,campo):
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    lecturaDesc = "order by "+ campo +" desc limit 7"
    querry = "select * from " + tabla +" "+ lecturaDesc
    error = ""
    try:
        mycursor.execute(querry)
        readData = mycursor.fetchall()
        print("count row :", mycursor.rowcount)
        db2.commit()
        db2.close()
        return readData
    except:
        print("Eror: "+ error)
        db2.close()
        readData = "vacio"
        return readData
#   Return (Date, Val peso)
def ordenarGrafica(tuplaMySQL,indDate,indVal):
    dataVal     = []
    dataDate    = []
    print(tuplaMySQL)
    for dataTable in tuplaMySQL:
        dataDate.append(str(dataTable[indDate]))
        dataVal.append(int(dataTable[indVal]))
    return (dataDate, dataVal)
    
if __name__ == "__main__":
    app.run(debug=1)