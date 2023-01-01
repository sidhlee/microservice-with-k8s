# RabbitMQ

## Kubernetes StatefulSets

Unlike other services that create `deployment` resources, we need a `StatefulSet` for managing RabbitMQ server. In order to make the message queue durable against system failures, we need to persist our messages.
[docs](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)

- Like a `Deployment`, a `StatefulSet` manages Pods based on the same container spec.
- Unlike a `Deployment`, a `StatefulSet` assigns persistent ids to each pod so that existing db volumes can be mounted to the new pod that replaces the failed ones.
- With `StatefulSet`, we can have one pod that reads & writes to a master db and other pods that only reads from slave/replica db.
- With multiple replicas, each pod is deployed one at a time in a pre-determined order. This is good for preventing race conditions.

## Setting up RabbitMQ in Kubernetes

To deploy a RabbitMQ cluster to Kubernetes, create the following manifest files and apply them:

- `statefulset.yaml` - creates a `StatefulSet` resource for mounting persistent volume to the container. We can use rabbitmq's public image and set ports for admin panel and amqp server.
- `pvc.yaml` - creates a `PersistentVolumeClaim` resource that defines spec for the persistent volume for the container. (eg. storage size, access mode, ..)
- `service.yaml` - creates a `Service` that makes the cluster accessible to the client connections (eg. for sending messages, accessing admin panel, ..). It defines the access type, ports, and container app to connect to (app template defined in statefulset.yaml).
- `ingress.yaml` - creates a `Ingress` object that sits in the top-most layer of the cluster and exposes HTTP and HTTPS routes for the outside request coming through a load balancer. This file defines the rules for routing request to the services within the cluster. We also need to map the specified host (eg. rabbitmq-manager.com) to the localhost so that we can access the RabbitMQ's admin port via browser.
- `configmap.yaml` and `secret.yaml` - for providing environment variables to the context.

## Minikube tunnel

After deploying the kubernetes cluster for RabbitMQ, we need to route the request coming from the defined host to the address specified in the ingress object(s). Run `minikube tunnel` to expose `gateway-ingress` and `rabbitmq-ingress`.

> If you are on macOS, the tunnel command also allows DNS resolution for Kubernetes services from the host.

## Adding a new queue

On the RabbitMQ admin panel accessed from the browser, you can add a new queue whose name matches the `routing_key` provided from the code that publishes a message with `pika.adapters.blocking_connection.BlockingChannel.basic_publish()`.
Configure the new queue with the following key-value:

- Type - Classic
- Name - 'video'
- Durability - Durable

After adding the new queue, re-deploy the gateway service we scaled back earlier.
