from kafka import KafkaProducer
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ProduceGrowthModelDataThread(threading.Thread):
    def __init__(self, topic, key, data, model, master_id, **kwargs):
        self.topic = topic
        self.key = key
        self.data = data
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

    def process_data(self, data):
        processed_data = {}
        data['master_id'] = self.master_id
        for col, val in data.items():
            column_name = self.underscore_to_camelcase(col)
            processed_data.update({column_name: val})
        return processed_data

    def get_processed_data(self):
        query = ""
        data = self.data
        if data:
            data = self.process_data(self.data)

        if self.key.lower() in ['update', 'delete']:
            query = {
                "where": {
                    "masterId": self.master_id
                }
            }

        return {
            "data": data,
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


def produce_growth_model_data_thread(topic, key, data, model, master_id):
    ProduceGrowthModelDataThread(topic, key, data, model, master_id).start()


def produce_growth_model_data(topic, key, data, model, master_id):
    produce_growth_model_data_thread(key, model, data, model, master_id)
