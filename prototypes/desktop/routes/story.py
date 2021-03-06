import json
import os
import psycopg2
import psycopg2.extras
import web

import helper

urls = (
    
	# /api/data/story/idea/metric/#/, where # == storyidea.id
	"idea/(\d+)/metric/(\d+)/", "story_idea_metrics",
    
    # 0.0.0.0:8000/api/data/story/persona/#/panel/#/, where first # == persona.id and second # == panel.id
    "persona/(\d+)/panel/(\d+)/", "persona_panel_stories",
    
)

class persona_panel_stories:
    """ Extract all the stories from a specific panel with a particular persona.
    input:
        * persona.id
        * panel.id
    output:
        * story.id
        * story.name
        * story.url_name
        * story_ideas
    """
    def GET(self, persona_id, panel_id, connection_string=helper.get_connection_string(os.environ['DATABASE_URL'])):
        # connect to postgresql based on configuration in connection_string
        connection = psycopg2.connect(connection_string)
        # get a cursor to perform queries
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)    
        # execute query
        self.cursor.execute("""
		select pps.*,
		s.name,
		s.url_name,
        s.intro,
		array_agg(row_to_json(si)) as ideas
		from """ + helper.table_prefix + """persona_panel_story pps
		left join """ + helper.table_prefix + """story s on s.id = pps.story_id
		left join (
		select sti.*,
		vt.url_name as vis_type_name,
		array_agg(row_to_json(c)) as controls
		from """ + helper.table_prefix + """story_idea sti
		left join """ + helper.table_prefix + """vis_type vt on vt.id = sti.vis_type_id
		left join (
		select sac.*,
		case
		when sac.story_action_id = 1 then g.name
		when sac.story_action_id = 2 then g.name
		when sac.story_action_id = 3 then g.name
		when sac.story_action_id = 4 then h.name
        when sac.story_action_id = 5 then g.name
        when sac.story_action_id = 6 then g.name
		when sac.story_action_id = 7 then g.name
		end
		as name
		from """ + helper.table_prefix + """story_action_control sac
		left join """ + helper.table_prefix + """group g on g.id = sac.name_id
		left join """ + helper.table_prefix + """heuristic h on h.id = sac.name_id
		) c on c.story_action_id = sti.action_id
		group by sti.id,
		vt.url_name
		) si on si.story_id = pps.story_id
		where pps.persona_id = """ + persona_id + """ and pps.panel_id = """ + panel_id + """
		group by pps.id,
		s.name,
		s.url_name,
        s.intro,
        s.story_order
        order by s.story_order;
        """)
        # obtain the data
        data = self.cursor.fetchall()
        # convert data to a string
        return json.dumps(data)

class story_idea_metrics:
    def GET(self, story_idea_id, control_id, connection_string=helper.get_connection_string(os.environ['DATABASE_URL'])):
        # connect to postgresql based on configuration in connection_string
        connection = psycopg2.connect(connection_string)
        # get a cursor to perform queries
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # execute query
        self.cursor.execute("""
        select sac.id,
		sim.label,
		sim.description,
		si.id as story_idea_id,
		g.name as control_name,
		sa.name as action_name,
		sim.name as metric_name,
		array_agg(row_to_json(m)) as metrics
		from """ + helper.table_prefix + """story_action_control sac
		left join """ + helper.table_prefix + """story_action sa on sa.id = sac.story_action_id
		left join """ + helper.table_prefix + """story_idea si on si.action_id = sac.story_action_id
		left join """ + helper.table_prefix + """group g on g.id = sac.name_id
		left join """ + helper.table_prefix + """vertex v on v.id = sac.name_id
		left join """ + helper.table_prefix + """flow f on f.id = sac.name_id
		left join """ + helper.table_prefix + """story_idea_metric sim on sim.control_id = sac.id
		left join (
		select * from """ + helper.table_prefix + """story_idea_metric_value
		) m on m.control_id = sac.id
		where si.id = """ + story_idea_id + """ and sac.id = """ + control_id + """
		group by sac.id,
		sim.label,
		sim.description,
		si.id,
		g.name,
		v.name,
		f.name,
		sa.name,
		sim.name;
        """)
        # obtain the data
        data = self.cursor.fetchall()
        # convert data to a string
        return json.dumps(data)

# instantiate the application
app = web.application(urls, locals())
