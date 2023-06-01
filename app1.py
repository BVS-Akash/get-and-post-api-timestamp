from flask import Flask,request,render_template,redirect,url_for,jsonify
from flask_cors import CORS
from hdbcli import dbapi
from datetime import datetime
import os
app=Flask(__name__)
CORS(app)



cf_port = os.getenv("PORT")

@app.route('/')
def home():
    return ""

@app.route('/get_latesttimestamp', methods=['POST'])
def get_latesttimestamp():
    data = request.json
    botname = data.get("botName")
    pswd=data.get("db_password")
    conn = dbapi.connect(address="c36fee0b-6867-4726-af51-9e54a218b5a8.hana.trial-us10.hanacloud.ondemand.com",
                             port=443, user="DBADMIN", password=pswd)
    cursor = conn.cursor()
    sql1 ="SELECT max(lastTime) FROM botdetails WHERE botName = :s1"
    cursor.execute(sql1, {"s1": botname})
    res = cursor.fetchone()
    if res is not None:
        latest_timestamp = res[0]
        cursor.close()
        conn.close()
    if res is None:
        latest_timestamp="None"
    return jsonify({"Latest Timestamp": str(latest_timestamp)})

    
        



@app.route('/post_botdata',methods=['POST'])
def post_botdata():
    data = request.json
    aid = int(data.get('actionID'))
    bn = data.get('botName')
    uid = data.get('userID')
    lt = data.get('lastTime')
    pswd=data.get('db_password')
    conn = dbapi.connect(address="c36fee0b-6867-4726-af51-9e54a218b5a8.hana.trial-us10.hanacloud.ondemand.com",
                         port=443, user="DBADMIN", password=pswd)
    cursor = conn.cursor()

    # Check if the actionID already exists
    sql_check = "SELECT COUNT(*) FROM botdetails WHERE actionID = :a1"
    cursor.execute(sql_check, {"a1": aid})
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        return jsonify({"status": "Fail"})
    else:
        sql_insert = "INSERT INTO botdetails VALUES (:d1, :d2, :d3, :d4)"
        cursor.execute(sql_insert, {"d1": aid, "d2": bn, "d3": uid, "d4": lt})
        conn.commit()
        conn.close()
        return jsonify({"status": "Success"})
        

    










if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=8007, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port))