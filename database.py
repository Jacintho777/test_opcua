import psycopg2

def load_data():
    
    connection = psycopg2.connect(
		host = "ec2-54-228-32-29.eu-west-1.compute.amazonaws.com",
		database = "dbc63e9s4ghqgd",
		user = "cufhmdxtaynjan",
		password = "65562226466934bbc1246b06b1349ab4abb097a5bef4d25da9ef23b616f9020b",
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