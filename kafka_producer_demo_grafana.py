import json
from ssl import SSLContext
import ssl
from kafka import KafkaProducer, TopicPartition
from kafka.errors import KafkaError
context_ssl = SSLContext(ssl.PROTOCOL_SSLv23)
context_ssl.verify_mode = ssl.CERT_NONE
kafka_topics = ["udm-product-recommendation-development"]
# kafka_url = "localhost:9092"

def produce_kafka_message(message):
    # producer = KafkaProducer(bootstrap_servers=kafka_url)
    producer = KafkaProducer(
        bootstrap_servers=["b-1.vdmkafka-2.eh14to.c7.kafka.us-west-2.amazonaws.com:9094",
                           "b-2.vdmkafka-2.eh14to.c7.kafka.us-west-2.amazonaws.com:9094",
                           "b-3.vdmkafka-2.eh14to.c7.kafka.us-west-2.amazonaws.com:9094"
                           ],
        security_protocol='SSL',
        ssl_context=context_ssl,
        api_version=(0, 11, 5))

    # Store data in all topics listed in kafka_topics
    # for kafka_topic in kafka_topics:
    #     future = producer.send(kafka_topic, json.dumps(
    #         message).encode('utf-8'))

    # Store data in all topics listed in kafka_topics
    for kafka_topic in kafka_topics:
        future = producer.send(kafka_topic, json.dumps(message).encode('utf-8'))
        # Block for 'synchronous' sends
        try:
            record_metadata = future.get(timeout=10)
            print("Topic = ", record_metadata.topic)
            print("Partition = ", record_metadata.partition)
            print("Offset = ", record_metadata.offset)
            print("The data was successfully sent to the above location in kafka.")
            producer.flush()
        except KafkaError:
            # Decide what to do if produce request failed...
            message = "Looks like there is some problem while sending a message in KAFKA"
            print(message)


if __name__ == '__main__':
    recommendationData = {
        "stage": 'SMOKE',
    "pipeline_build_number": 6666,
    "bu": 'cpbu',
    "pipeline_fk": '5fb46399fc1b4f291c242913',
    "_id": '5fb464a1fc1b4f291c244d3b',
    "product": 'sddc-bundle',
    "recommendation": True,
    "pass_percentage": 100,
    "timestamp": 1605657761417,
    "change_details": [{
        "_id": '5fb46489fc1b4f291c244ac6',
        "buildweb_id": 41613679,
        "buildweb_system": "sb",
        "branch": 'main-highline',
        "build_type": 'obj',
        "buildstate": "storing",
        "canonical": True,
        "changeset": 8537866,
        "changeset_name": '8537866',
        "product": 'sddc-bundle',
        "target": 'vdm-dummy-target',
    }, {
        "_id": '5fb464a0fc1b4f291c244cd9',
        "buildweb_id": 41613680,
        "buildweb_system": "sb",
        "branch": 'main',
        "build_type": 'obj',
        "buildstate": "storing",
        "canonical": True,
        "changeset": 8537866,
        "changeset_name": '8537866',
        "product": 'vpxd',
        "target": 'vdm-dummy-target',
    }],
    }
    produce_kafka_message(message=recommendationData)
    # with open(r'/Users/vmaddukuri/Desktop/output.json') as json_data:
    #     data = json.load(json_data)
    #     produce_kafka_message(data)

