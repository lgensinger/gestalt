import web
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

urls = (
    
    # rest API backend endpoints
    "", "persona"
    
)

if os.environ["DATABASE_URL"] is not "":
	
	# parse stored connection string
	values = os.environ["DATABASE_URL"].split(",")
	
	connection_string = "dbname='" + values[0] + "' user='" + values[1] + "' host='" + values[2] + "' password='" + values[3] + "'"
else:
	connection_string = ""

class persona:
    def GET(self):
        
        # connection string
        con_string = psycopg2.connect(connection_string)
        
        # postgres connector
        cursor = con_string.cursor(cursor_factory=RealDictCursor)
        
        # SQL query
        cursor.execute("""select * from gestalt_persona;""")
        
        # get rows
        data = cursor.fetchall()
        
        return json.dumps(data)
    
app_persona = web.application(urls, locals())