from kafka import KafkaConsumer
import json
from kafka.structs import OffsetAndMetadata, TopicPartition


server = [ "kafka.eng.vmware.com:9092"]
topic = "unified-test-triage-details"
reader = KafkaConsumer(
    topic,
    group_id="demo",
    bootstrap_servers=server,
    auto_offset_reset="earliest"
)
topics = reader.topics()
print(topics)
for msg in reader:
    data = json.loads(msg.value.decode("utf-8"))
    print(data)
    # tp = TopicPartition(msg.topic, msg.partition)
    # offsets = {tp: OffsetAndMetadata(msg.offset, None)}
    # reader.commit(offsets=offsets)

