import pika, os
import pywren_ibm_cloud as pywren
import time
import random
import sys
import json

#config

entrades =0
numSlaves=4
if(len(sys.argv)>1):
	numSlaves=int(sys.argv[1])
	if(numSlaves>18):
		numSlaves=18
	if(numSlaves<1):
		numSlaves=1
iterMaster=numSlaves
consumits=0
dicc=[]
escrit=[]
for x in range(20):
	escrit.append(False)

#funcio master
def master(num):
	pw_config = json.loads(os.environ.get('PYWREN_CONFIG', ''))
	url = pw_config['rabbitmq']['amqp_url']
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel() # start a channel
	channel.exchange_declare(exchange='master', exchange_type='fanout')
	channel.queue_delete('leader')
	channel.queue_declare(queue='leader')
	def callback_master(ch, method, propieties, body):
		global iterMaster
		global dicc		
		global consumits
		print('Callback Master')
		iterMaster=iterMaster-1
		part=str(body)
		elem=part.split(':')
		dicc.append(elem[1])
		if(iterMaster==0):
			print(dicc)
			lenght=len(dicc)
			posicio=random.randint(0, lenght)
			semafor='sem:'+dicc[posicio-1]
			semafor=semafor[:-1]
			print(semafor)
			channel.basic_publish(exchange='master', routing_key='', body=str(semafor))
			consumits=consumits+1
			dicc=[]
			iterMaster=numSlaves-consumits
			if(consumits==numSlaves):
				channel.stop_consuming()
	channel.basic_consume(callback_master, queue='leader', no_ack=True)
	channel.start_consuming()
	return dicc

#funcio slave
def slave(num):
	pw_config = json.loads(os.environ.get('PYWREN_CONFIG', ''))
	url = pw_config['rabbitmq']['amqp_url']
	params = pika.URLParameters(url)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	cua='cua'+str(num)
	channel.exchange_declare(exchange='master', exchange_type='fanout')
	channel.queue_delete(cua)
	channel.queue_declare(queue=cua) 
	channel.queue_bind(exchange='master', queue=cua)
	dic=[]
	time.sleep(5)
	channel.basic_publish(exchange='', routing_key='leader', body='sem:'+str(num))
	esc=escrit
	def callback_slave(ch, method, propieties, body):
		global escrit
		global numSlaves
		prova=str(body)
		elem=prova.split(":")
		comparador=elem[0]
		comparador=comparador[2:]
		comparador2=elem[1]
		comparador2=comparador2[:-1]

		if(comparador=='sem'):
			if(int(comparador2) ==int(num)):
				escrit[num]=True
				x=random.randint(0,9999)
				channel.basic_publish(exchange='master', routing_key='', body='num:'+str(x))
				
		if(comparador=='num'):
			dic.append(comparador2)
			if(escrit[num]==False):
				channel.basic_publish(exchange='', routing_key='leader', body='sem:'+str(num))
		if(len(dic)==int(numSlaves)):
			channel.stop_consuming()

	channel.basic_consume(callback_slave, queue=cua, no_ack=True)
	channel.start_consuming()
	return dic

#codi
pwSlave = pywren.ibm_cf_executor(rabbitmq_monitor=True)
pwSlave.map(slave, range(numSlaves))
pwMaster = pywren.ibm_cf_executor(rabbitmq_monitor=True)
pwMaster.call_async(master, numSlaves)

print(pwSlave.get_result())

