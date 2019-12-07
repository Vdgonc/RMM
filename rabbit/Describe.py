import requests
from requests.auth import HTTPBasicAuth

class Describe:
	def __init__(self, hostname: str, username: str, password: str, virtualhost: str):
		self.hostname = hostname
		self.virtualhost = virtualhost
		self.auth = HTTPBasicAuth(username, password)

	def _list_queues(self):
		response = requests.get(f'http://{self.hostname}/api/queues', auth=self.auth)

		queues = [q['name'] for q in response.json()]
		return queues

	def describe_queues(self):
		queues = self._list_queues()
		response = []
		final = []

		for queue in queues:
			request = requests.get(f'http://{self.hostname}/api/queues/{self.virtualhost}/{queue}/bindings',
								   auth=self.auth)
			# print(request.json())

			for r in request.json():
				queue = r["destination"] if r["destination"] != "" else ""
				exchange = r["source"] if r["source"] != "" else ""
				rk = r["routing_key"] if r["routing_key"] != "" else ""


				if queue != "" and exchange != "":

					response.append({
						"queue": request.json()[1]['destination'],
						"exchange": request.json()[1]['source'],
						"rk": request.json()[1]['routing_key']
					})

		for q in response:
			if q not in final:
				final.append(q)

		return final
