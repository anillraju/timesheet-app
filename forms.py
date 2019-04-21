# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sqlite3

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class GetForm():
    incompleteFirstPatientName = ""
    incompletePatientStartDate = ""


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = GetForm
    if request.method == 'POST':
        form = GetForm
        form.incompleteFirstPatientName = ""
        form.incompletePatientStartDate = ""
        form.id = ""

        firstPatientName = request.form['firstPatientName']
        patientStartDate = request.form['patientStartDate']

        lastPatientName = request.form['lastPatientName']
        patientEndDate = request.form['patientEndDate']
        id = request.form['id']

        print firstPatientName, " ", patientStartDate, " ", lastPatientName, " ", patientEndDate
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        # Insert a row of data
        fields = (firstPatientName, patientStartDate, lastPatientName, patientEndDate)
        fieldsUpdate = (firstPatientName, patientStartDate, lastPatientName, patientEndDate, id)
        if id:
            print "going to update"
            success = c.execute(
                "UPDATE TIMESHEET set firstPatientName =? , patientStartDate = ? ,  lastPatientName = ? ,  patientEndDate = ?, endTime = datetime('now','localtime')  where id = ?",
                fieldsUpdate
            )

            success = c.execute(
                "UPDATE TIMESHEET set duration = (endtime - starttime) where id = ?", id
            )
        else:
            success = c.execute(
                "INSERT INTO TIMESHEET(firstPatientName, patientStartDate, lastPatientName, patientEndDate,startTime) VALUES (?,?,?,?,datetime('now','localtime'))",
                fields
            )

        conn.commit()

        for res in success:
            print "--> {0}".format(res)

        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        print "going to query"

        c.execute(
            "SELECT firstPatientName, patientStartDate, lastPatientName, patientEndDate,id FROM TIMESHEET order by id desc")
        result = c.fetchone()
        if (result is not None and len(result) > 1):
            print "-->" + result[0] + ":  :" + result[1] + ":  :" + result[2] + ":  :" + result[3]
            if c.rowcount is not None:
                print "rowCount was not none:" + result[2] + ":  :" + result[0] + "  " + str(len(result))
                if (not result[2] and result[0]):
                    print "going to set data"
                    form.incompleteFirstPatientName = result[0]
                    form.incompletePatientStartDate = result[1]
                    form.id = result[4]
            conn.close()

        conn.close()

    return render_template('hello.html', form=form)


@app.route("/initialize", methods=['GET'])
def initializeApp():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE TIMESHEET
             (   ID INTEGER PRIMARY KEY AUTOINCREMENT,
                firstPatientName text, 
                patientStartDate text, 
                lastPatientName text, 
                patientEndDate text,
                startTime DATETIME,
                endTime DATETIME,
                duration INTEGER 
              )''')
    conn.close()

    return "success"


@app.route("/currentData", methods=['GET'])
def currentData():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    response = "<html><table border='1'> <tr>    <td>firstPatientName</td><td>patientStartDate</td><td>lastPatientName</td><td>patientEndDate</td><td>workStartTime</td><td>workEndTime</td> <td>duration</td>  </tr>"
    print "going to run query"

    for row in c.execute(
            "SELECT firstPatientName, patientStartDate, lastPatientName, patientEndDate, startTime, endTime,(julianday(endTime) - julianday(startTime))*1000 FROM TIMESHEET order by id"):
        print row
        response = response + "<tr> <td>" + '</td><td>'.join(map(str,row)) + "</tr>"

    response = response + "</table></html>"
    conn.close()

    return response


@app.route("/reportData", methods=['GET'])
def reportData():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    response = "<html><table border='1'> <tr>    <td>day</td><td>TotalHours</td>   </tr>"
    print "going to run query"

    for row in c.execute(
            "SELECT firstPatientName, patientStartDate, lastPatientName, patientEndDate, startTime, endTime FROM TIMESHEET order by id"):
        print row
        response = response + "<tr> <td>" + '</td><td>'.join(row) + "</tr>"

    response = response + "</table></html>"
    conn.close()

    return response


if __name__ == "__main__":
    app.run()
