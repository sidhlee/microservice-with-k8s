# Microservice Architecture and System Design with Python & Kubernetes – Full Course

[FCC youtube course](https://youtu.be/hmkF77F9TLw) about microservice architectures and distributed systems using Python, Kubernetes, RabbitMQ, MongoDB, mySQL.

## Using Flake8 with BLack on VSCode

When working with Black, you need to set linter rules according to Black's settings.

In order to modify flake8's default rules, you need to download an extension called `flake8` by Microsoft. Then, you can add the rules to `settings.json` as the following:

```json
"flake8.args": [
    "--max-line-length=100",
    "--ignore=E501,W503,W504,E203",
    "--max-complexity=10",
  ],
```
