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
- By default, RabbitMQ will evenly distribute (dispatch) the messages in the queue to multiple consumers in round-robin fashion. This way, we can scale up our system easily by adding more consumers

## Building and pushing Docker image

1. Create a `Dockerfile` that specifies the python base layer, installs OS dependencies (eg. poetry), defines `WORKDIR`, copies local files to container, installs project dependencies, documents the port, and provides command for running the app.

2. Build the docker image with `docker build .`

3. Tag the image in the docker repository with the image hash.
   `docker tag 2e60b3124bfd668112b863f315bde6c5454ee8e02483e6eea859844a01ab2d0f sidhlee/gateway:
latest`

4. Push the image using the hash. A repo will automatically be created in docker hub. `docker push sidhlee/gateway:latest`

## Applying manifest files and managing deployments

After adding all the necessary manifest files for creating Kubernetes objects, you can deploy your cluster by `kubectl apply -f ./` in the directory containing manifest files.

- We added `ingress.yaml` to set routing rules to access `gateway` service from outside the cluster.
- For testing, we also mapped the hostname from the ingress file to the localhost using `/etc/hosts` file.
- `minikube tunnel` redirects requests made to the localhost to the ingress resources. For this, you need to enable ingress addon for minikube.
- `minikube dashboard` opens up a dashboard in a browser where you can easily manage the Kubernetes workload. You can also monitor and manage the deployments on `k9s`.
- If the deployment is not running successfully due to errors, Kubernetes will retry running the deployment with exponential backoff. In this case, you can scale down the deployment by running `kubectl scale deployment --replicas=0 <service>` and fix the issue.
- If you edited immutable manifest (eg. pvc), you can delete the resources created and re-apply the manifests by running `kubectl delete -f ./`
