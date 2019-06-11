# Pub/Sub RabbitMQ

## Instal·lació

Per utilitzar el programa es necessiten instalar els següents paquets de Python3.

```bash
pip3 install pika, os, pywren_ibm_cloud, time, random, sys, json
```

També serà necessari el fitxer de configuració del PyWren per connectar-nos al Cloud.

```
ibm_cf:
    # Obtain all values from https://cloud.ibm.com/openwhisk/learn/api-key
    endpoint    : https://eu-gb.functions.cloud.ibm.com
    namespace   : <namespace>
    api_key     : <api_key>

ibm_cos:
    # Region endpoint example: https://s3.us-east.cloud-object-storage.appdomain.cloud
    endpoint   : https://s3.eu-gb.cloud-object-storage.appdomain.cloud
    # this is preferable authentication method for IBM COS
    api_key    :  <api_key>
    # alternatively you may use HMAC authentication method
    # access_key : <access_key>
    # secret_key : <secret_key>
	
rabbitmq:
    amqp_url : <amqp_url>
```

## Execució

Per executar el programa (pubsub.py en el nostre cas) utilitzem la següent comanda, on per defecte s'utilitzen 4 slaves.

```bash
python3 pubsub.py 
```

Si volem un número personalitzat de "slaves" fem servir la següent comanda, sent el límit superior 18 i 1'inferior 1. Qualsevol altre valor que superi aquests limits quedara limitat.

```bash
python3 pubsub.py 15
```

## Autors

* **David Sánchez Benaiges**  [david.sanchezb@estudiants.urv.cat](mailto:david.sanchezb@estudiants.urv.cat)
* **Tomàs Biarnés Gaig**  [tomas.biarnes@estudiants.urv.cat](mailto:tomas.biarnes@estudiants.urv.cat)
