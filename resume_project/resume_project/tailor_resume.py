from confluent_kafka import Producer, Consumer, KafkaException
import json
import logging
import time

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"

# Kafka Producer Configuration
producer_conf = {"bootstrap.servers": KAFKA_BROKER}
producer = Producer(producer_conf)

# Kafka Consumer Configuration
consumer_conf = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "resume-processing-group",
    "auto.offset.reset": "earliest",
}

# Function to send data to Kafka
def kafka_produce(topic, message):
    producer.produce(topic, json.dumps(message).encode("utf-8"))
    producer.flush()
    logging.info(f"✅ Sent message to Kafka topic {topic}: {message}")

# Function to consume messages from Kafka
def kafka_consume(topic):
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(10.0)
        if msg is None:
            logging.info(f"⚠️ No messages found in topic {topic}")
            continue
        if msg.error():
            raise KafkaException(msg.error())
        
        message = json.loads(msg.value().decode("utf-8"))
        logging.info(f"🔄 Consumed message from {topic}: {message}")
        return message

# Function 1: Process LaTeX and generate job description
def function1(latex_file_path, job_id):
    logging.info(f"📄 Function 1: Processing job_id={job_id}, file={latex_file_path}")
    job_description = {
        "job_id": job_id,
        "status": "processed",
        "description": "Job description derived from LaTeX content"
    }
    kafka_produce("job_description_topic", job_description)

# Function 2: Generate resume in LaTeX
def function2():
    job_desc = kafka_consume("job_description_topic")
    if job_desc:
        resume_latex = f"\\begin{{resume}} Resume for job {job_desc['job_id']} \\end{{resume}}"
        kafka_produce("resume_topic", {"job_id": job_desc['job_id'], "resume": resume_latex})

# Function 3: Enhance and update the resume
def function3():
    resume_data = kafka_consume("resume_topic")
    if resume_data:
        updated_resume = resume_data["resume"] + "  % Enhanced with additional details"
        kafka_produce("updated_resume_topic", {"job_id": resume_data['job_id'], "updated_resume": updated_resume})

# Main execution flow
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Step 1: Produce job description
    function1("/path/to/input.tex", "JOB12345")
    time.sleep(2)  # Simulate processing delay

    # Step 2: Consume job description and produce resume
    function2()
    time.sleep(2)

    # Step 3: Consume resume and produce enhanced resume
    function3()
