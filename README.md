# The Eye
This is a microservice for collecting events from other apps. This is a project for Consumer Affairs job application.

## Requirements
* Docker
* Docker-compose
* Python 3.8

## Production Environment Setup
1. Clone the git repository
2. create an environment file named ```.env.docker```
3. edit the ```.env.docker``` values
4. run the docker-compose

```
# clone the repository
git clone https://github.com/cjasm/the_eye.git

# create an environment file
cp .env-sample .env.docker

# edit the environment values
nano .env.docker

# run the docker-compose
docker-compose up
```

## Locally Environment Setup

1. Clone the git repository
2. if you do not have a redis and celery installed
   1. create an environment file named ```.env.docker```
   2. edit the ```.env.docker``` values
   3. run the redis, celery and db
3. run the tests
4. run the server

```
# clone the repository
git clone https://github.com/cjasm/the_eye.git

# [Optional] Create an environment file
cp .env-sample .env.docker
# edit the environment values
nano .env.docker
# Run the redis, celery and db
docker-compose up -d db redis celery

# create a locally environment file
cp .env-sample .env

# edit the locally environment values
nano .env

# run the tests
python manage.py test

# run the server
python manage.py runserver
```

## Load Testing

```

locust --headless --users 1000 --spawn-rate 100 -H http://localhost:8000 -t 1m -f contrib/load_test.py
```

### Locally Results
These results can vary based on hardware, os and internet
* CPU: Intel® Core™ i5-10300H CPU @ 2.50GHz × 8
* Memory: 16 GB
* GPU: NVIDIA Corporation / GeForce GTX 1650 Ti/PCIe/SSE2 (4GB GDDR6)
* OS: Ubuntu 20.04.3 LTS
```
 Name                          # reqs      # fails  |     Avg     Min     Max  Median  |   req/s failures/s
-----------------------------------------------------------------------------------------------------------
 POST /api/events/               7809     0(0.00%)  |      59       8     557      17  |  130.55    0.00
-----------------------------------------------------------------------------------------------------------
 Aggregated                      7809     0(0.00%)  |      59       8     557      17  |  130.55    0.00

Response time percentiles (approximated)
 Type     Name                        50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|----------------------|---------|------|------|------|------|------|------|------|------|------|------|------|
 POST     /api/events/                 17     21     26     31    220    360    450    480    530    560    560   7809
--------|----------------------|---------|------|------|------|------|------|------|------|------|------|------|------|
 None     Aggregated                   17     21     26     31    220    360    450    480    530    560    560   7809
```


## Conclusion

This interesting project has contemplated common problems in many companies, such as creating endpoints and background jobs. The tool was built as simple as possible but complying with the use cases. The endpoints are documented by swagger and accessed through the main URL (e.g. http:localhost:8000). 

Furthermore, one of the requirements was the request time, and the tool should not let the request hang. Assumed that the communication protocol should be HTTP, I have implemented the background job on Celery and Redis. The Redis was chosen as a broker because it transports small messages fastly. However, if the messages are too long, it could be interesting to separate them into one event per task.

In addition, I considered that this application should be deployed on a private network since I have understood that it works as a middleware microservice. In this case, an allowed host proper configured on environment variables should work. However, if necessary, a Bearer or OAuth token can be implemented depending on the requirements.

Furthermore, I have understood that performance is a critical constraint. Thus, I have created a load test script using the Locust tool to measure it. The simulation is shown above but can vary depending on some configurations. Also, the Docker could be improved by setting fixed resource configurations.

Finally, I felt a lack of information about the error payload data and which is the proper validation. Then, I created a payload data validation based on 'host' and 'path' because of the example. Some tests cases were designed to validate the event and error creation during the beginning of the development, but they were removed after the implementation of the background task. Thus, more tests should be written to complement the existent ones.

# Code Challenge
## Story

You work in an organization that has multiple applications serving websites, but it's super hard to analyze user behavior in those, because you have no data.

In order to be able to analyze user behavior (pages that are being accessed, buttons that are being clicked, forms that are being submitted, etc..), your team realized you need a service that aggregates that data.

You're building "The Eye", a service that will collect those events from these applications, to help your org making better data-driven decisions.

## Workflow

* We don't want you to be a code monkey, some things will not be 100% clear - and that's intended. We want to understand your assumptions and approaches you've taken during the implementation - if you have questions, don't hesitate to ask
* Your commit history matters, we want to know the steps you've taken throughout the process, make sure you don't commit everything at once
* In the README.md of your project, explain what conclusions you've made from the entities, constraints, requirements and use cases of this test

## Entities

```
Application
    |
    |
  Event ---- Session
```

* An Event has a category, a name and a payload of data (the payload can change according to which event an Application is sending)
* Different types of Events (identified by category + name) can have different validations for their payloads
* An Event is associated to a Session
* Events in a Session should be sequential and ordered by the time they occurred
* The Application sending events is responsible for generating the Session identifier 
* Applications should be recognized as "trusted clients" to "The Eye"
* Appllications can send events for the same session 

Example of events:
```json
{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "pageview",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "page interaction",
  "name": "cta click",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "element": "chat bubble"
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}

{
  "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
  "category": "form interaction",
  "name": "submit",
  "data": {
    "host": "www.consumeraffairs.com",
    "path": "/",
    "form": {
      "first_name": "John",
      "last_name": "Doe"
    }
  },
  "timestamp": "2021-01-01 09:15:27.243860"
}
```

## Constraints & Requirements

* "The Eye" will be receiving, in average, ~100 events/second, so consider not processing events in real time
* When Applications talk to "The Eye", make sure to not leave them hanging
* Your models should have proper constraints to avoid race conditions when multiple events are being processed at the same time
* It must be implemented in Python with Django.
* Share a public github repository when you are done.

## Use cases:

**You don't need to implement these use cases, they just help you modelling the application**

* Your data & analytics team should be able to quickly query events from:
  * A specific session
  * A specific category
  * A specific time range

* Your team should be able to monitor errors that happen in "The Eye", for example:
  * An event that is sending an unexpected value in the payload
  * An event that has an invalid timestamp (i.e.: future)


## Pluses - if you wanna go beyond

* Your application is documented
* Your application is dockerized
* A reusable client that talks to "The Eye"
