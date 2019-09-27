import psycopg2

def run_query(q, dsn):
	"""
	Run a query q, against a database specified by dsn.
	"""
	query_type = q.split(' ')[0]

	try:
		conn = psycopg2.connect(dsn=dsn)
		conn.autocommit = True  # Prevent from being stuck in a rollback state
	except Exception as e:
		print("Cannot connect to db: " + repr(e))
		return

	cur = conn.cursor()

	try:
		cur.execute(q)
		# TODO: refactor to be more robust than looking for the word 'select', needs to handle newline characters, etc.
		if query_type.lower() == 'select': 
			results = cur.fetchall()
		else:
			results = []
	except Exception as e:
		print("Query failed: " + repr(e))
		conn.close()
		return

	conn.close()
	return results