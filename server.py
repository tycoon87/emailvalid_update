from flask import Flask, render_template,session, flash, request, redirect


from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    print "inside submit"
    query = "select email from emails"
    emaildb = mysql.query_db(query)
    print "user email:", request.form["email"]
    print "db values :", emaildb
    for email in emaildb:
        print "this is the email", email
        if request.form["email"] == email["email"]:
            print "inside validate"
            return redirect('/')
        
    putinto = "INSERT INTO emails (email,datestamp) values (:email,now())"
    data = {
        'email': request.form['email']
        }
    mysql.query_db(putinto, data)
    return redirect ("/sucsess")

@app.route('/sucsess')
def sucsess():
    query = "select email, datestamp from emails"
    emaildb = mysql.query_db(query)
    return render_template ("sucsess.html",emaildb = emaildb)

app.run(debug=True)