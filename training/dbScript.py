def createdb(server='dbServerIP',uName='user',pwd='password',dbNmae='MyDataBase'):
    db=MySQLdb.connect(server,uName,pwd)
    cursor=db.cursor()
    createDB='CREATE DATABASE %s;' %(dbNmae)
    cursor.execute(createDB)
    createTableInDB='CREATE TABLE PROFILE(fName char(20) NOTNULL, lName char(20), AGE INT, GENDER char(1), INCOME INT)'
    cursor.execute(createTableInDB)
    addTableValues='INSERT INTO PROFILE(fName,lName,AGE,GENDER,INCOME) VALUES('vijay','M',29,'M',100000)'
    cursor.execute(addTableValues)
    getValues='(SELECT * FROM PROFILE WHERE AGE>25)'
    cursor.execute(getValues)
    results=cursor.fetchall()
    for row in results:
        fName=row[0]
        Age=row[1]
        income=row[3]
    updateTable='(UPDATE PROFILE SET AGE=AGE+1 WHERE GENDER='M')'
    cursor.execute(updateTable)
    deleteValueinTable='(DELETE FROM TABLE WHERE AGE>30)'
    cursor.execute(deleteValueinTable)
    db.commit()
    db.close()

