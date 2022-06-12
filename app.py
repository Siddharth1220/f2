from flask import Flask, render_template, request, redirect,jsonify
from bson.objectid import ObjectId
import pymongo
import json
client = pymongo.MongoClient("mongodb+srv://siddharth:1220@cluster0.w0hhi.mongodb.net/?retryWrites=true&w=majority")
mydb = client["mydatabase"]
mycol = mydb["customers"]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('read.html')



@app.route('/delete/<int:rollno>')
def delete(rollno):
    id = str(rollno)
    myquery = {"rollno":id}
    mycol.delete_one(myquery)
    return redirect('/')



@app.route('/update/<int:rollno>')
def update(rollno):
    id = str(rollno)
    return render_template('update.html',rollno=rollno)


@app.route('/updata/<int:rollno>', methods=['GET', 'POST'] )
def updata(rollno):
    if request.method=='POST':
        id = str(rollno)
        myquery = {"rollno":id}
        mycol.delete_one(myquery)
        newvalues = { "rollno": rollno,"FirstName": request.form['fn'], "LastName": request.form['ln'],"dob": request.form['dob'],"email":request.form['email'],"phone":request.form['phone'], "pwd" : request.form['pwd'] , "gender":request.form['gender'] , "Language":request.form['lan'] , "address": request.form['address'], "country": request.form['country'],"state": request.form['state'],"city": request.form['city']} 
        mycol.insert_one(newvalues)
    return redirect('/')


    
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        mydict = { "rollno" : request.form['rollno'] , "FirstName": request.form['fn'], "LastName": request.form['ln'],"dob": request.form['dob'],"email":request.form['email'],"phone":request.form['phone'], "pwd" : request.form['pwd'] , "gender":request.form['gender'] , "Language":request.form['lan'] , "address": request.form['address'], "country": request.form['country'],"state": request.form['state'],"city": request.form['city']}
        x = mycol.insert_one(mydict)
        return redirect('/')
    return render_template('index.html')
    
@app.route('/data')
def data():
    o = []
    for i in mycol.find():
        o.append({"_ID":str(ObjectId(i['_id'])), "FirstName": i['FirstName'], "LastName": i['LastName'],"dob": i['dob'],"email":i['email'],"phone":i['phone'], "pwd" : i['pwd'] , "gender":i['gender'] , "Language":i['Language'] , "address": i['address'], "country": i['country'],"state": i['state'],"city": i['city'] ,"rollno": i['rollno']})
    return jsonify(o)

if __name__ == "__main__":
    app.run(debug='false', port=8000)