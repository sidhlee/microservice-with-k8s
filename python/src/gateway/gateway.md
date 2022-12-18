# Gateway

## How RabbitMQ is integrated with overall system

![system diagram](./docs/queue-in-overall-system.png 'Queue in the overall system')

1. User uploads a video file.
2. Gateway calls the auth service to authenticate request
3. Gateway uploads the video to storage DB and puts the message to the queue when the image is uploaded.
4. Video-to-mp3 service (downstream) picks up the message, then download and process the video.
5. The service puts the message back to the queue after uploading converted mp3 to the storage, then puts the message back to the queue.
6. Notification service picks up the message and sends email to the client.
7. Client uses the request id from the message combined with their JWT to make request to the gateway to download the converted mp3.
8. Gateway service pulls the mp3 from the DB and serves it to the client.

![rabbitmq](./docs/rabbitmq.png, 'RabbitMQ')

- Producer: your application that sends the message to the broker
- Broker (RabbitMQ): service that takes the message to the exchange and distributes them into different queues.
- Consumer: worker process that takes the message from the RabbitMQ queue.
- By default, RabbitMQ will evenly distribute the messages in the queue to multiple consumers in round-robin fashion. This way, we can scale up our system easily by adding more consumers
