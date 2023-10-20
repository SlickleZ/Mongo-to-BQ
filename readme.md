# MongoDB to BigQuery pipeline

The demonstration to build a data pipeline from MongoDB to BigQuery in a Batch and Streaming way.

## 💻 Tech Stack

**Language:** Python

**Tools:** Airflow, MongoDB, BigQuery, Kafka, Docker

## 💡 Concept

lOtter is the lottery number generator app that helps the user decide what lottery number to buy. The project consisted of 2 parts as follows

* **Batch way**: Work with data that user random number. The MongoDB to BigQuery pipeline controlled by Airflow with daily scheduled.
* **Streaming way**: Work with like/dislike event. Stream data from MongoDB to BigQuery through Kafka.

All services run on Docker Compose.

## 📸 Screenshots

![App Screenshot](https://raw.githubusercontent.com/SlickleZ/Mongo-to-BQ/main/resources/res01.png)

![App Screenshot](https://raw.githubusercontent.com/SlickleZ/Mongo-to-BQ/main/resources/res02.png)
