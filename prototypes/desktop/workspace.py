import json
import os
import psycopg2
import psycopg2.extras
import web

import helper

urls = (

    "workspace_name/", "all_workspace_names",
    "", "all_workspaces",
    # 0.0.0.0:8000/api/workspace/#/, where # == workspace.url_name
    "([a-fA-F\d]{32})/", "single_workspace",
    # 0.0.0.0:8000/api/workspace/persona/#/, where # == persona.id
    "persona/(\d+)/", "persona_workspaces",
    # 0.0.0.0:8000/api/workspace/#/panels/, where # == workspace.url_name
    "(.*)/panels/", "workspace_panels",

)

class single_workspace:
    """ Extract a single workspace with a specific url_name.
    input:
        * workspace.url_name
    output:
        * workspace.id
        * workspace.name
        * persona.name        
        * workspace.url_name
    """
    def GET(self, workspace_url_name, connection_string=helper.get_connection_string(os.environ['DATABASE_URL'])):
        # connect to postgresql based on configuration in connection_string
        connection = psycopg2.connect(connection_string)
        # get a cursor to perform queries
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # execute query
        self.cursor.execute("""
            SELECT DISTINCT ON (w.id) w.id, wn.name, p.name AS persona_name, w.url_name
            FROM gestalt_workspace AS w
            LEFT JOIN gestalt_workspace_name AS wn
            ON w.workspace_name_id = wn.id
            LEFT JOIN gestalt_persona AS p
            ON w.persona_id = p.id
            WHERE w.id IS NOT NULL 
            AND w.url_name = '""" + workspace_url_name + """'
            ORDER BY w.id;        
        """)
        # obtain the data
        data = self.cursor.fetchall()
        # convert data to a string
        return json.dumps(data)


class persona_workspaces:
    """ Extract all the workspaces for a particular persona.
        The output includes each workspace's information, each workspace's default panel, and each workspace's panels.
    input:
        * persona.id
    output:
        * workspace's information
            * workspace.id
            * workspace.name
            * persona.id
            * workspace.url_name
            * workspace.is_default
        * workspace's default panel
            * panel.url_name
        * workspace's panels
            * ?
            * ?
            * ?
            * ?
            * ?
    """
    """
        SELECT w.id, wn.name, w.url_name, w.is_default, pl.url_name
        FROM workspace w
        LEFT JOIN workspace_name wn
        ON w.workspace_name_id = wn.id
        LEFT JOIN workspace_panel wp
        ON w.id = wp.workspace_id
        LEFT JOIN panel pl
        ON wp.panel_id = pl.id
        WHERE wp.is_default = 't'
        AND w.persona_id = 1
        ORDER BY w.id;
    """
    def GET(self, persona_id, connection_string=helper.get_connection_string(os.environ['DATABASE_URL'])):
        # connect to postgresql based on configuration in connection_string
        connection = psycopg2.connect(connection_string)
        # get a cursor to perform queries
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # execute query
        self.cursor.execute("""
            SELECT DISTINCT ON (w.id) w.id, wn.name, w.is_default, p.id AS persona_id, w.url_name, pl.url_name AS default_panel, array_agg(row_to_json(r)) as panels
            FROM gestalt_workspace w
            LEFT JOIN gestalt_workspace_name wn
            ON w.workspace_name_id = wn.id
            LEFT JOIN gestalt_workspace_panel wp
            ON wp.workspace_id = w.id
            LEFT JOIN gestalt_persona p
            ON w.persona_id = p.id
            JOIN gestalt_panel pl
            ON pl.id = wp.panel_id
            left join (
            select wp.panel_id, wp.workspace_id, wp.is_default, pl.name, pl.url_name, w.persona_id
            from gestalt_workspace_panel wp
            left join gestalt_panel pl
            on pl.id = wp.panel_id
            left join gestalt_workspace w
            on w.id = wp.workspace_id
            ) r
            on r.workspace_id = w.id
            AND wp.is_default = true
            WHERE w.id IS NOT NULL 
            AND w.persona_id = """ + persona_id + """
            group by w.id, wn.name, w.is_default, p.id, w.url_name, pl.url_name;   
        """)
        # obtain the data
        data = self.cursor.fetchall()
        # convert data to a string
        return json.dumps(data)

class workspace_panels:
    """ Extract all the panels for a particular workspace.
    input:
        * workspace.url_name
    output:
        * panel.id
        * panel.name
        * panel.url_name
        * workspace.url_name
        * workspace.persona_id
    """
    """
        SELECT DISTINCT ON (p.id) p.id, p.name, p.url_name 
        FROM panel p
        RIGHT JOIN workspace_panel wp
        ON wp.panel_id = p.id
        AND wp.workspace_id = 
        WHERE p.id IS NOT NULL
        ORDER BY p.id;
    """
    def GET(self, workspace_url_name, connection_string=helper.get_connection_string(os.environ['DATABASE_URL'])):
        # connect to postgresql based on configuration in connection_string
        connection = psycopg2.connect(connection_string)
        # get a cursor to perform queries
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # execute query
        self.cursor.execute("""
            SELECT DISTINCT ON (p.id) p.id as panel_id, p.name, p.url_name, w.url_name as workspace_url_name, w.persona_id
            FROM gestalt_panel AS p
            RIGHT JOIN gestalt_workspace_panel AS wp
            ON wp.panel_id = p.id
            right join """ + helper.table_prefix + """workspace w
            on w.id = wp.workspace_id
            and w.url_name = '""" + workspace_url_name + """'
            WHERE p.id IS NOT NULL
            ORDER BY p.id;
        """)
        # obtain the data
        data = self.cursor.fetchall()
        # convert data to a string
        return json.dumps(data)
    
# instantiate the application
app = web.application(urls, locals())
