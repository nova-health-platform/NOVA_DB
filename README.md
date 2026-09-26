<div align="center">
  <img src=".github/assets/banner.png" alt="NOVA_DB banner" width="100%" />

  <h1>NOVA_DB</h1>

  <p>
    Reference database and API for symptoms, diseases and treatments used by the NOVA health platform.
  </p>

<p>
  <img src="https://img.shields.io/github/last-commit/nova-health-platform/NOVA_DB" alt="last update" />
  <img src="https://img.shields.io/github/languages/top/nova-health-platform/NOVA_DB" alt="top language" />
</p>
</div>

<br />

## :notebook_with_decorative_cover: Table of Contents

- [About](#star2-about)
  * [Tech Stack](#space_invader-tech-stack)
  * [Features](#dart-features)
  * [Environment Variables](#key-environment-variables)
- [Getting Started](#toolbox-getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
  * [Run Locally](#running-run-locally)
- [Related Repositories](#link-related-repositories)
- [Contact](#handshake-contact)

## :star2: About

NOVA_DB is the service that holds the reference medical data for NOVA: symptoms, diseases, symptom synonyms and treatments. An import script (`feed_tables.py`) loads CSV files into a PostgreSQL database, then a small Flask API (`server.py`) exposes this data for read access to the other NOVA services (notably the ML analysis module, which trains its models from these tables).

### :space_invader: Tech Stack

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
    <li><a href="https://www.psycopg.org/">psycopg2</a></li>
  </ul>
</details>

<details>
  <summary>Database</summary>
  <ul>
    <li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
    <li><a href="https://pandas.pydata.org/">Pandas</a> (CSV import into tables)</li>
  </ul>
</details>

<details>
  <summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>

### :dart: Features

- Automatic import of CSV files (symptoms, diseases, treatments in French, symptoms with English synonyms) into PostgreSQL tables, recreating the tables on each import
- `GET /symptoms`: list of referenced symptoms
- `GET /symptoms/synonyms`: list of symptom/synonym pairs
- `GET /symptoms/<symptom>/synonyms`: synonyms for a given symptom
- Containerized with Docker for simple deployment

### :key: Environment Variables

The service reads its PostgreSQL configuration from a `.env` file (not versioned):

`DB_HOST`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_PORT`

## :toolbox: Getting Started

### :bangbang: Prerequisites

Python 3.9 or a Docker image, plus an accessible PostgreSQL database.

### :gear: Installation

```bash
pip install flask psycopg2-binary python-dotenv pandas
```

### :running: Run Locally

Import the data into PostgreSQL:

```bash
python feed_tables.py
```

Start the API:

```bash
python server.py
```

Or with Docker:

```bash
docker build -t nova-db .
docker run -p 5001:5001 --env-file .env nova-db
```

## :link: Related Repositories

NOVA_DB is part of the NOVA health platform ecosystem, split across several repositories:

- [NOVA_WEB](https://github.com/nova-health-platform/NOVA_WEB): web frontend of the platform
- [NOVA_API](https://github.com/nova-health-platform/NOVA_API): main NOVA API
- [NOVA_LOGS_DB](https://github.com/nova-health-platform/NOVA_LOGS_DB): application log storage
- [NOVA_ML_ANALYSIS](https://github.com/nova-health-platform/NOVA_ML_ANALYSIS): symptom analysis ML model, trained from this repository's data
- [NOVA_ML_PREPROD](https://github.com/nova-health-platform/NOVA_ML_PREPROD): ML model training and staging environment
- [NOVA_ML_MENTAL_HEALTH](https://github.com/nova-health-platform/NOVA_ML_MENTAL_HEALTH): psychological monitoring module
- [NOVA_ML_SCAN_BODY](https://github.com/nova-health-platform/NOVA_ML_SCAN_BODY): computer vision dermatological check-up module
- [NOVA-CORE](https://github.com/nova-health-platform/NOVA-CORE): architecture overview and local orchestration for the whole platform

## :handshake: Contact

Brieuc Dumortier - [LinkedIn](https://www.linkedin.com/in/dumortier-brieuc/) - dumortier.contact@gmail.com

[https://github.com/BaditSad](https://github.com/BaditSad)
