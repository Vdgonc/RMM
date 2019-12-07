from json import loads
from sys import argv
from rabbit import Describe, Migrate

__author__ = "Vinicius Justino"
__version__ = "1.0.0"
__banner__ = '''
\t ____  __  __ __  __
\t|  _ \|  \/  |  \/  |
\t| |_) | |\/| | |\/| |
\t|  _ <| |  | | |  | |
\t|_| \_\_|  |_|_|  |_|

\tRabbitMQ Message Migrator  author: Vinicius Justino | github: @Vdgonc | Twitter: @VdGonc\n
\tUsage:
\t\trmm.py -c config.json
'''

__help__ = '''
\tFlags:
\t\t-h or --help 	help for rmm
\t\t-c or --config 	Json path configuration
'''


if __name__ == '__main__':
	if len(argv) > 1:
		__option = argv[1]

		if __option == '-h' or __option == '--help':
			print(__banner__)
			print(__help__)
			pass
		elif __option == '-c' or __option == '--config':
			__file = argv[2]
			print(__banner__)

			with open(__file, 'r') as file:
				configfile = loads(file.read())

			consumer = configfile["consumer"]
			publisher = configfile["publisher"]
			server = configfile["server"]

			migrator = Migrate(consumer=consumer, publisher=publisher)
			describer = Describe(hostname=server["host"],
								 username=server["username"],
								 password=server["password"],
								 virtualhost=server["virtualhost"])

			queues = describer.describe_queues()
			if queues != []:
				for queue in queues:
					print(f'Migrating ...')
					print(f'Queue: {queue["queue"]} exchange: {queue["exchange"]} routing key: {queue["rk"]}')
					migrator.migrate(queue=queue)
					print(f'Done!\n')
			else:
				print(f'No queues found!')
		else:
			print(__banner__)
			print(__help__)
			pass
	else:
		print(__banner__)
		print(__help__)
