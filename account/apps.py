from django.apps import AppConfig
from kafka import KafkaConsumer
from logpipe import Consumer, register_consumer
import threading, configparser, traceback, sys
import json

config = configparser.ConfigParser()
config.read('config.ini')

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def register_kafka_listener(self, topic, serializer_obj):
        # Poll kafka
        def poll():
            consumer = KafkaConsumer(topic, bootstrap_servers=[config['KAFKA']['BOOTSTRAP_SERVER']],
                value_deserializer=lambda m: json.loads(m.decode('ascii')))
            consumer.poll()

            for message in consumer:
                print("###########################", message.topic, message.partition,
                    message.offset, message.key, message.value)
        #         consumer = Consumer(topic)
        #         consumer.register(serializer_obj)
        #         consumer.run()

        # t1 = threading.Thread(target=poll)
        # t1.start()

        # self.reset_topic_consumer(topic, serializer_obj)

    def reset_topic_consumer(self, topic, serializer_obj):
        try:
            from logpipe.models import KafkaOffset
            kafka_offest = KafkaOffset.objects.filter(topic = topic).order_by('-partition').first()
            if kafka_offest:
                kafka_offest.offset = 0
                kafka_offest.save()

            consumer = Consumer(topic)
            consumer.register(serializer_obj)
            consumer.run()
        except Exception:
            import traceback
            traceback.print_exc()
            pass

    def ready(self, *args, **kwargs):
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)

        if (is_manage_py and is_runserver) or (not is_manage_py):
            from account.queueservice.consumer_serializers import KafkaUserSerializer

            self.register_kafka_listener('growthdbo', KafkaUserSerializer)



            
