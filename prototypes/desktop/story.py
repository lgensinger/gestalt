import web
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

urls = (
    
    # rest API backend endpoints
    "(.*)/persona/(.*)/", "panel_stories",
    "(.*)/", "all_stories"
    
)

if os.environ["DATABASE_URL"] is not "":
	
	# parse stored connection string
	values = os.environ["DATABASE_URL"].split(",")
	
	connection_string = "dbname='" + values[0] + "' user='" + values[1] + "' host='" + values[2] + "' password='" + values[3] + "'"
else:
	connection_string = ""

class all_stories:
    def GET(self, persona_id):
        
        # connection string
        con_string = psycopg2.connect(connection_string)
        
        # postgres connector
        cursor = con_string.cursor(cursor_factory=RealDictCursor)
        
        # SQL query
        cursor.execute("""select distinct on (s.id) s.id,s.name,s.param from gestalt_story s,gestalt_collection c,gestalt_workspace wk where c.topics && s.topics and c.id = any(wk.topics) and wk.persona = """ + persona_id + """;""")
        
        # get rows
        data = cursor.fetchall()
        
        return json.dumps(data)
    
class panel_stories:
    def GET(self, panel_param, persona_id):
        
        # connection string
        con_string = psycopg2.connect(connection_string)
        
        # postgres connector
        cursor = con_string.cursor(cursor_factory=RealDictCursor)
        
        # SQL query
        cursor.execute("""select distinct on (s.id) s.id,s.name,s.param from gestalt_story s,gestalt_collection c,gestalt_workspace wk where c.topics && s.topics and c.id = any(wk.topics) and wk.persona = """ + persona_id + """ and '""" + panel_param + """' = c.param;""")
        
        # get rows
        data = cursor.fetchall()
        
        return json.dumps(data)
    
app_story = web.application(urls, locals())