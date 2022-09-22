import psycopg2

def load_data():
    
    connection = psycopg2.connect(
		host = "ec2-3-213-228-206.compute-1.amazonaws.com",
		database = "d4ie7d66ast1c7",
		user = "pndadghhtmavlx",
		password = "1dfcd638c2929d01b08597ed226b6a9469373bb5719f97a4f91abd314ac664b7",
		port = "5432",
		)
    cur = connection.cursor()
    cur.execute("""SELECT * FROM STATE_VALUES FETCH FIRST ROW ONLY""")
    to_be_loaded = cur.fetchall()[0]
    cur.execute("""DELETE FROM STATE_VALUES
                    WHERE ctid IN (
                    SELECT ctid
                    FROM STATE_VALUES
                    LIMIT 1
                    )""")
    connection.commit()
    connection.close()
    
    return to_be_loaded