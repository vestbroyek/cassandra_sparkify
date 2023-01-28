from cassandra.cluster import Cluster
import logging
logging.basicConfig(level=logging.INFO)

class Cassandra:
	def __init__(self, host='127.0.0.1', port=9042):
		self.host=host
		self.port=port
		self.cluster=Cluster([self.host], self.port)

	def connect(self):
		try:
			self.session=self.cluster.connect()
			return self.session
		except:
			logging.error("Could not connect to cluster.")
			raise

	def create_keyspace(self, keyspace:str):
		try:
			logging.info(f"Creating keyspace {keyspace}...")
			self.session.execute(f"""
			create keyspace if not exists {keyspace} """+
			"""with replication=
			{'class': 'SimpleStrategy', 'replication_factor':1}
			""")
			self.session.set_keyspace(keyspace)
		except Exception as e:
			logging.info(e)

	def shutdown(self):
		self.session.shutdown()
