from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://Prueba:prueba@cluster0.xv7cj.mongodb.net/Prueba?retryWrites=true&w=majority'
mongo = PyMongo(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'bec43b382c6e22'
app.config['MYSQL_DATABASE_PASSWORD'] ='9e83483e'
app.config['MYSQL_DATABASE_DB'] = 'heroku_9b4bacbd64cc96f'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'


mysql.init_app(app)


@app.route('/')
def recoger_datos_y_enviar():

    user_collection = mongo.db.entries
    lista = []
    for valFreestyle in user_collection.find():
        valFreestyle.pop('_id')
        valFreestyle['date'] = int(valFreestyle['date'])
        listaAux = valFreestyle.values()
        listas = tuple(listaAux)
        lista.append(listas)

    for item in lista:
        print(item)
    
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    error = ""
    querry = "INSERT INTO sensorFreeStyle (date,dateString,rssi,device,direction,rawbg,sgv,type,utcOffset,sysTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        mycursor.executemany(querry,lista)
        db2.commit()
    except:
        print("Error: "+ error)
    
    print("Number record inserted, ID:", mycursor.lastrowid)
    db2.close() 
    return render_template('index.html')

    
@app.route('/bascula',methods=['POST'])
def Recibir_Datos_Bascula():
    peso = request.form["peso"]
    db2 =  mysql.connect()
    mycursor = db2.cursor()
    # querry_tabla = "create table IF NOT EXIST 'pesoUsuario' (PESO INT)"
    querry = "INSERT INTO pesoUsuario (%s)"
    error = ""  
    try:
        # mycursor.executemany(querry_tabla)
        # db2.commit()
        mycursor.executemany(querry,peso)
        db2.commit()
    except:
        print("Error: "+ error)
    
    print("Number record inserted, ID:", mycursor.lastrowid)
    db2.close() 
    return render_template('bascula.html')

    

    

if __name__ == "__main__":
    app.run(debug=1)