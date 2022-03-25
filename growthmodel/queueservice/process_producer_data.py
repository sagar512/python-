from kafka import KafkaProducer
import threading
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')


class ProduceGrowthModelDataThread(threading.Thread):
    def __init__(self, topic, key, payload_data, model, master_id, **kwargs):
        self.topic = topic
        self.key = key
        self.payload_data = payload_data
        self.master_id = master_id
        self.model = model
        self.extra_dict = kwargs
        kwargs = {}
        super(ProduceGrowthModelDataThread, self).__init__(**kwargs)

    def underscore_to_camelcase(self, value):
        def camelcase():
            yield str.lower
            while True:
                yield str.capitalize

        c = camelcase()
        return "".join(next(c)(x) if x else '_' for x in value.split("_"))

    def process_data(self, payload_data):
        processed_data = {}
        for col, val in payload_data.items():
            column_name = self.underscore_to_camelcase(col)
            processed_data.update({column_name: val})
        processed_data['masterId'] = self.master_id
        return processed_data

    def get_processed_data(self):
        query = ""
        payload_data = self.payload_data
        if payload_data:
            payload_data = self.process_data(self.payload_data)

        if self.key in [b'update', b'delete']:
            query = {
                "where": {
                    "masterId": self.master_id
                }
            }

        return {
            "data": payload_data,
            "model": self.model,
            "query": query
        }

    def run(self):
        value = self.get_processed_data()
        producer = KafkaProducer(
            bootstrap_servers=[config['KAFKA']['BOOTSTRAP_SERVER'], ],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(self.topic, key=self.key, value=value)
        producer.flush()


def produce_growth_model_data_thread(topic, key, payload_data, model, master_id):
    ProduceGrowthModelDataThread(topic, key, payload_data, model, master_id).start()


def produce_growth_model_data(topic, key, payload_data, model, master_id):
    produce_growth_model_data_thread(topic, key, payload_data, model, master_id)
