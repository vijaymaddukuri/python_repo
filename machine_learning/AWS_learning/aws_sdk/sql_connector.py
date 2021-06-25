import mysql.connector

dbc = mysql.connector.connect(
    host = "test-instance.ctiigg07fppy.us-east-1.rds.amazonaws.com",
    user = "master",
    passwd = "vijaynov18",
    port = 3306,
    database = "celebrities"
)

# Defining the cursor object
cur = dbc.cursor()

# Creating the table
cur.execute("CREATE TABLE celebrities (image VARCHAR(255), celebrity VARCHAR(255))")

file_name = 'bezos-image.jpg'
celebrity_name = "Jeff Bezos"
# Inserting the values into columns
sql = "INSERT INTO celebrities(image, celebrity) VALUES (%s, %s)"
val = (file_name, celebrity_name)
cur.execute(sql, val)

# Read the stored values from RDS ​
cur.execute("SELECT image, celebrity FROM celebrities")
result = cur.fetchall()

print(result)