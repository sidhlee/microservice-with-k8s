# Auth

## Init

Follow these steps to run the init.sql script and create a db admin and a user table:

```bash
mysql -uroot < init.sql

mysql -uroot
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 46
Server version: 8.0.30 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| auth               |
| information_schema |
| mavenfuzzyfactory  |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
6 rows in set (0.00 sec)

mysql> use auth
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> show tables;
+----------------+
| Tables_in_auth |
+----------------+
| user           |
+----------------+
1 row in set (0.01 sec)

mysql> describe user;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| email    | varchar(255) | NO   |     | NULL    |                |
| password | varchar(255) | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

mysql> select * from user;
+----+------------------+----------+
| id | email            | password |
+----+------------------+----------+
|  1 | hayoun@email.com | Admin123 |
+----+------------------+----------+
1 row in set (0.00 sec)
```

If you run into an error while running the script eg. syntax error, you need to drop the database and the user before running the script again:

```bash
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot -e "DROP DATABASE auth;"
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot -e "DROP USER 'auth_user'@'localhost';"
```

## Adding UNIQUE constraint

Because we don't have data in the user table yet, we can just add UNIQUE to the sql script and run it again. Remember to drop the user and database before you run the script.

```bash
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot -e "DROP USER auth_user@localhost"
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot -e "DROP DATABASE auth"
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot < init.sql
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? mysql -uroot
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 50
Server version: 8.0.30 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use auth
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> describe user;
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int          | NO   | PRI | NULL    | auto_increment |
| email    | varchar(255) | NO   | UNI | NULL    |                |
| password | varchar(255) | NO   |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)
```

## Building a docker image and push to the docker hub repository

For using poetry inside a docker container, refer to [this S.O. answer](https://stackoverflow.com/a/54763270).

After creating `Dockerfile` and a repository from the docker hub, run the follow commands to build an image and push to the docker hub repo:

```bash
(python-Zs0VLZKm-py3.10) ???  auth git:(main) ??? docker build
.
[+] Building 2.5s (12/12) FINISHED
 => [internal] load build definition from Dockerfile  0.0s
 => => transferring dockerfile: 566B                  0.0s
 => [internal] load .dockerignore                     0.0s
 => => transferring context: 2B                       0.0s
 => [internal] load metadata for docker.io/library/p  2.4s
 => [auth] library/python:pull token for registry-1.  0.0s
 => [1/6] FROM docker.io/library/python:3.10-slim-bu  0.0s
 => [internal] load build context                     0.0s
 => => transferring context: 8.38kB                   0.0s
 => CACHED [2/6] RUN apt-get update   && apt-get ins  0.0s
 => CACHED [3/6] WORKDIR /app                         0.0s
 => CACHED [4/6] COPY ./pyproject.toml ./poetry.lock  0.0s
 => CACHED [5/6] RUN   poetry config virtualenvs.cre  0.0s
 => [6/6] COPY . /app                                 0.0s
 => exporting to image                                0.0s
 => => exporting layers                               0.0s
 => => writing image sha256:0ed848774eca280f52c768c4  0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
```

Now tag the image hash with the docker hub repo you created.

```bash
(python-Zs0VLZKm-py3.10) ??? auth git:(main) ??? docker tag 0ed848774eca280f52c768c4 sidhlee/auth:latest
```

Check the image you just built:

```bash
(python-Zs0VLZKm-py3.10) ??? auth git:(main) ??? docker image
ls
REPOSITORY TAG IMAGE ID CREATED SIZE
sidhlee/auth latest 0ed848774eca About an hour ago 466MB
docker101tutorial latest f555e4b975e0 2 weeks ago 27.5MB
alpine/git latest 9793ee61fc75 2 weeks ago 43.4MB
gcr.io/k8s-minikube/kicbase v0.0.36 c87ac1e75807 6 weeks ago 1.02GB
<none> <none> 47de9cc6479e 20 months ago 188MB
<none> <none> c37bbdcdc117 20 months ago 175MB
<none> <none> bf1504586cf6 20 months ago 175MB
<none> <none> a59cc6169293 20 months ago 199MB
docker/getting-started latest 3ba8f2ff0727 21 months ago 27.9MB
node 13-alpine 8216bf4583a5 2 years ago 114MB
```

Finally, push the image to the docker hub repo :

```bash
(python-Zs0VLZKm-py3.10) ??? auth git:(main) ??? docker push s
idhlee/auth:latest
The push refers to repository [docker.io/sidhlee/auth]
a3bd0e3d30a3: Pushed
f6a429654b92: Layer already exists
baf81bcab7c7: Layer already exists
1031c79e8822: Layer already exists
003082490e66: Layer already exists
3d8713a79b44: Layer already exists
9eeed6361b54: Layer already exists
a7fc70a8dbf0: Layer already exists
49fa38a13b0d: Layer already exists
6b1c0df0b436: Layer already exists
latest: digest: sha256:2023152c7ac044548004320992d6b5a68fe99779055f6b527a3b89a0efb86c6f size: 2419

```

If you are getting `denied: requested access to the resource is denied` error, you need to run `docker login` with your docker hub credentials.

You can pull the image from the hub using `docker pull sidhlee/auth:latest` command, but we are going to use minikube to orchestrate the docker images.

## Kubernetes Manifests

A Kubernetes manifest is a YAML file that describes each resource (eg. deployment, services, pods, etc..) you want to create, and how you want those resources to run inside a cluster.

Currently, if you run `k9s` in terminal, there is no clusters running.

To allow manifest files to interact with docker hub and create our application, run the following command inside the `manifests/` folder:

Make sure `minikube` is running before using applying the manifest with `kubectl`. Otherwise, you would get "The connection to the server localhost:8080 was refused - did you specify the right host or port?" error.

```bash
???  manifests git:(main) ??? kubectl apply -f ./
deployment.apps/auth created
configmap/auth-configmap unchanged
secret/auth-secret configured
service/auth unchanged

```

## Advantages of using K8S

With Kubernetes, we can cluster together multiple containerized services and easily orchestrate the deployment and management of these services within the cluster using the Kubernetes Objects.

- Automates running/recycling many containers
- Auto-detects failures in individual pods and maintains the predefined scale.
- Manual scaling is as easy as running a command. It also configures load balancer and registers new pods for you.
- Keeps track of all individual containers status and matches that to the configuration specified in manifest files.

## Kubectl and minikube

`kubectl` CLI makes necessary Kubernetes API calls for running CRUD operation on your K8S objects. This is because your deployments usually live inside a cloud environment.
`minikube` allows you to run clusters locally for development, and `kubectl` command will be directed towards the local clusters.

- `minikube service auth --url` will return the address you can connect to the auth service running inside minikube.
