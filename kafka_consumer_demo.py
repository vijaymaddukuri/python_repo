import json

from kafka import KafkaConsumer
from kafka.structs import OffsetAndMetadata, TopicPartition

consumer = KafkaConsumer(bootstrap_servers=['0.0.0.0:9092'],
                         key_deserializer=lambda m: m.decode('utf8'),
                         value_deserializer=lambda m: json.loads(m.decode('utf8')),
                         auto_offset_reset="earliest",
                         group_id='1')

consumer.subscribe(['topic1'])

for msg in consumer:
    print(msg)

    tp = TopicPartition(msg.topic, msg.partition)
    offsets = {tp: OffsetAndMetadata(msg.offset, None)}
    consumer.commit(offsets=offsets)