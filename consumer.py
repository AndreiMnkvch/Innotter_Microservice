import pika


def consume():
    connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@rabbitmq:5672'))
    print('micro connection: ', connection)
    channel = connection.channel()
    channel.queue_declare(queue='statistics_publish', durable=True)
    print('micro channel:', channel)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='statistics_publish',
on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    print('connection to be closed')
    connection.close()
