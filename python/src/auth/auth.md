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
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot -e "DROP DATABASE auth;"
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot -e "DROP USER 'auth_user'@'localhost';"
```

## Adding UNIQUE constraint

Because we don't have data in the user table yet, we can just add UNIQUE to the sql script and run it again. Remember to drop the user and database before you run the script.

```bash
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot -e "DROP USER auth_user@localhost"
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot -e "DROP DATABASE auth"
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot < init.sql
(python-Zs0VLZKm-py3.10) ➜  auth git:(main) ✗ mysql -uroot
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
