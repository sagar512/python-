from django.apps import AppConfig
from kafka import KafkaConsumer
import threading
import configparser
import traceback
import sys
import json


config = configparser.ConfigParser()
config.read('config.ini')


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def register_kafka_listener(self, topic, parser):
        # Poll kafka
        def poll():
            consumer = KafkaConsumer(
                topic, bootstrap_servers=[
                    config['KAFKA']['BOOTSTRAP_SERVER'], ],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')))
            consumer.poll()

            for message in consumer:
                action = message.key.decode('utf-8')
                payload = message.value
                obj = parser(action, payload)
                obj.process_growth_model_dbo()

        t1 = threading.Thread(target=poll)
        t1.start()

        self.reset_topic_consumer(topic)

    def reset_topic_consumer(self, topic):
        try:
            from logpipe.models import KafkaOffset
            kafka_offest = KafkaOffset.objects.filter(
                topic=topic).order_by('-partition').first()
            if kafka_offest:
                kafka_offest.offset = 0
                kafka_offest.save()
        except Exception:
            import traceback
            traceback.print_exc()
            pass

    def ready(self, *args, **kwargs):
        is_manage_py = any(arg.casefold().endswith("manage.py")
                           for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)

        if (is_manage_py and is_runserver) or (not is_manage_py):
            from account.queueservice.process_data import ProcessGrowthdboData

            self.register_kafka_listener('growthdbo', ProcessGrowthdboData)
