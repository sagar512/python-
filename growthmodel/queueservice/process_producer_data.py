from kafka import KafkaProducer
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ProduceGrowthModelDataThread(threading.Thread):
    def __init__(self, topic, key, data, **kwargs):
        self.topic = topic
        self.key = key
        self.data = data
        self.extra_dict = kwargs
        kwargs = {}
        super(KafkaProducerThread, self).__init__(**kwargs)

    def run(self):
        producer = KafkaProducer(
            bootstrap_servers=[config['KAFKA']['BOOTSTRAP_SERVER'], ],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(self.topic, key=self.key, value=self.data)
        producer.flush()


def produce_growth_model_data_thread(topic, key, data):
    ProduceGrowthModelDataThread(topic, key, data).start()


def produce_growth_model_data(topic, key, data):
    produce_growth_model_data_thread(topic, key, data)
