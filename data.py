import pymssql

server = "dubhacks.caxrnm3xl7lt.us-west-2.rds.amazonaws.com:1433"
user = "sa"
password = "GoHuskies!"
db = "dubhacksSex"

def open_connection():
	conn = pymssql.connect(server, user, password, db)
	cursor = conn.cursor()
	return [conn, cursor]

def close_connection(conn):
	conn.close()

def get_question_for_tag(tag):
	[conn, cursor] = open_connection()
	cursor.execute("SELECT * FROM fn_GetQuestionsFromTag('%d')" % tag)
	ret_val = []
	row = cursor.fetchone()
	while row:
		ret_val.append(row[0])
		row = cursor.fetchone()
	close_connection(conn)
	return ret_val

