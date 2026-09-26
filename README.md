<div align="center">
  <h1>NOVA DB</h1>
  <p>Base de données et API de reference pour les symptomes, maladies et traitements utilises par la plateforme de sante NOVA.</p>

<p>
  <img src="https://img.shields.io/github/last-commit/BaditSad/NOVA_DB" alt="last update" />
  <img src="https://img.shields.io/github/languages/top/BaditSad/NOVA_DB" alt="top language" />
</p>
</div>

<br />

# Table des matieres

- [A propos](#a-propos)
  * [Stack technique](#stack-technique)
  * [Fonctionnalites](#fonctionnalites)
  * [Variables d'environnement](#variables-denvironnement)
- [Demarrage](#demarrage)
  * [Prerequis](#prerequis)
  * [Installation](#installation)
  * [Lancer en local](#lancer-en-local)
- [Depots lies](#depots-lies)
- [Contact](#contact)

## A propos

NOVA DB est le service qui porte les donnees medicales de reference de NOVA : symptomes, maladies, synonymes de symptomes et traitements. Un script d'import (`feed_tables.py`) charge des fichiers CSV dans une base PostgreSQL, puis une petite API Flask (`server.py`) expose ces donnees en lecture pour les autres services NOVA (notamment le module d'analyse ML qui entraine ses modeles a partir de ces tables).

### Stack technique

<details>
  <summary>Backend</summary>
  <ul>
    <li><a href="https://www.python.org/">Python</a></li>
    <li><a href="https://flask.palletsprojects.com/">Flask</a></li>
    <li><a href="https://www.psycopg.org/">psycopg2</a></li>
  </ul>
</details>

<details>
  <summary>Base de donnees</summary>
  <ul>
    <li><a href="https://www.postgresql.org/">PostgreSQL</a></li>
    <li><a href="https://pandas.pydata.org/">Pandas</a> (import des CSV vers les tables)</li>
  </ul>
</details>

<details>
  <summary>DevOps</summary>
  <ul>
    <li><a href="https://www.docker.com/">Docker</a></li>
  </ul>
</details>

### Fonctionnalites

- Import automatique de fichiers CSV (symptomes, maladies, traitements FR, symptomes avec synonymes EN) vers des tables PostgreSQL, avec recreation des tables a chaque import
- API `GET /symptoms` : liste des symptomes references
- API `GET /symptoms/synonyms` : liste des couples symptome/synonymes
- API `GET /symptoms/<symptom>/synonyms` : synonymes d'un symptome precis
- Conteneurisation via Docker pour un deploiement simple du service

### Variables d'environnement

Le service lit sa configuration PostgreSQL depuis un fichier `.env` (non versionne) :

`DB_HOST`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_PORT`

## Demarrage

### Prerequis

Python 3.9 ou une image Docker, ainsi qu'une base PostgreSQL accessible.

### Installation

```bash
pip install flask psycopg2-binary python-dotenv pandas
```

### Lancer en local

Importer les donnees dans PostgreSQL :

```bash
python feed_tables.py
```

Demarrer l'API :

```bash
python server.py
```

Ou via Docker :

```bash
docker build -t nova-db .
docker run -p 5001:5001 --env-file .env nova-db
```

## Depots lies

NOVA DB fait partie de l'ecosysteme de la plateforme de sante NOVA, reparti sur plusieurs depots :

- [NOVA_WEB](https://github.com/BaditSad/NOVA_WEB) : frontend web de la plateforme
- [NOVA_API](https://github.com/BaditSad/NOVA_API) : API principale de NOVA
- [NOVA_LOGS_DB](https://github.com/BaditSad/NOVA_LOGS_DB) : stockage des logs applicatifs
- [NOVA_ML_ANALYSIS](https://github.com/BaditSad/NOVA_ML_ANALYSIS) : modele ML d'analyse de symptomes, entraine a partir des donnees de ce depot
- [NOVA_ML_PREPROD](https://github.com/BaditSad/NOVA_ML_PREPROD) : environnement d'entrainement/preproduction des modeles ML
- [NOVA_ML_MENTAL_HEALTH](https://github.com/BaditSad/NOVA_ML_MENTAL_HEALTH) : module de suivi psychologique
- [NOVA_ML_SCAN_BODY](https://github.com/BaditSad/NOVA_ML_SCAN_BODY) : module de check-up dermatologique par computer vision

## Contact

Brieuc Dumortier - [LinkedIn](https://www.linkedin.com/in/dumortier-brieuc/) - dumortier.contact@gmail.com

[https://github.com/BaditSad](https://github.com/BaditSad)
