import pika


class Migrate:
	def __init__(self, consumer: dict, publisher: dict):
		self.consumer = consumer
		self.publisher = publisher

	def _create_connection(self, config: dict):
		credentials = pika.PlainCredentials(
			username=config["user"],
			password=config["password"]
		)

		parameters = pika.ConnectionParameters(
			host=config["host"],
			virtual_host=config["virtualhost"],
			port=config["port"],
			credentials=credentials,
			stack_timeout=90,
			heartbeat=600,
			socket_timeout=60

		)

		return pika.BlockingConnection(parameters)

	def publish(self, batch: list, queue: dict):
		connection = None

		connection = self._create_connection(config=self.consumer)
		channel = connection.channel()
		channel.basic_qos(prefetch_count=1)

		for i in batch:
			channel.basic_publish(exchange=queue['exchange'], routing_key=queue['rk'], body=str(i))

	def migrate(self, queue: dict):
		consumerConnection = None
		publisherConnection = None

		consumerConnection = self._create_connection(config=self.consumer)
		channelConsumer = consumerConnection.channel()
		channelConsumer.basic_qos(prefetch_count=1)

		publisherConnection = self._create_connection(config=self.publisher)
		channelPublisher = publisherConnection.channel()
		channelPublisher.basic_qos(prefetch_count=1)

		for method_frame, properties, body in channelConsumer.consume(queue['queue'], inactivity_timeout=3):

			if method_frame is None and properties is None and body is None:
				break
			else:

				msg = body.decode()

				try:
					channelPublisher.basic_publish(exchange=queue['exchange'], routing_key=queue['rk'], body=msg)
					channelConsumer.basic_ack(method_frame.delivery_tag, multiple=True)
				except Exception as err:
					print(err)
					channelConsumer.basic_nack(method_frame.delivery_tag)
