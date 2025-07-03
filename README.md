# 🎡 Mobility Data Platform — End‑to‑End Pipeline

![Architecture Globale](./assets/img/rentcar-pipeline.png)


1. 🏗️ **Architecture globale**  
2. ⚙️ **Composants & responsabilités**  
3. 🔄 **Orchestration Airflow**  
4. 📦 **dbt & Modélisation**  
5. 🚀 **Mise en route**  
6. 📊 **Visualisation & Monitoring**  
7. 🤝 **Ressources & Contacts**


## 1. 🏗️ Architecture Globale

```text
Source Layer         →  Extraction Layer    →  Storage & Compute   →  Transform Layer    →  Viz Layer
(MongoDB Atlas)      (Airbyte Cloud)       (Snowflake)          (dbt)                (Metabase)
````

| Couche                | Outil / Service                   | Rôle                                                |
| --------------------- | --------------------------------- | --------------------------------------------------- |
| **Source**            | MongoDB Atlas                     | Base de données opérationnelle (Users, Trips, etc.) |
| **Extraction**        | Airbyte Cloud                     | Sync incrémental MongoDB → Snowflake                |
| **Storage & Compute** | Snowflake                         | Tables RAW, Silver, Marts                           |
| **Transformations**   | dbt                               | Staging ⭢ Silver ⭢ Marts (dim/fact par domaine)     |
| **Orchestration**     | Apache Airflow (Astronomer Cloud) | Scheduling, retries, alerting                       |
| **Visualisation**     | Metabase                          | Dashboards métiers (KPI, rapports)                  |



## 2. ⚙️ Composants & Responsabilités
| Composant              | Technologie          | Description                                                                     |
| ---------------------- | -------------------- | ------------------------------------------------------------------------------- |
| **Airbyte Connection** | Airbyte Cloud        | Sync configuré : MongoDB Atlas → Snowflake                                      |
| **DAGs Airflow**       | Astronomer / Airflow | 1. AirbyteTriggerSync<br>2. Attente (Sensor)<br>3. dbt run                    |
| **dbt Models**         | dbt (YAML + SQL)     | • staging/<br>• silver/<br>• marts/ride, rating, maintenance                   |
| **Tables Snowflake**   | Snowflake            | RAW\_\<table\>, SILVER\_\<table\>, MARTS\_DIM\_\*, MARTS\_FACT\_\*            |
| **Dashboards**         | Metabase             | Tableau de bord « Ride Analytics », « Rating Analytics », « Fleet Maintenance » |

## 3. 🔄 Orchestration Airflow

<details>
<summary>Voir l’arborescence et l’aperçu du DAG</summary>

![Airflow DAG](./docs/airflow_dag.png)

| Task ID            | Description                                         |
| ------------------ | --------------------------------------------------- |
| `trigger_airbyte`  | Déclenche la sync Airbyte Cloud                     |
| `wait_for_airbyte` | Attend la fin du job Airbyte (Sensor)               |
| `run_dbt_staging`  | Exécute les modèles staging                         |
| `run_dbt_silver`   | Exécute les modèles silver                          |
| `run_dbt_marts`    | Exécute les marts par domaine (Ride, Rating, Maint) |

</details>


## 4. 📦 dbt & Modélisation

### Structure

```text
models/
├── staging/      # raw → staging (incremental)
├── silver/       # staging → silver (nettoyage, dérivés)
└── marts/
    ├── ride_analytics/        # dim_*, fact_trip
    ├── rating_analytics/      # dim_*, fact_rating
    └── maintenance_analytics/ # dim_*, fact_maintenance
```

### Tables clés

| Layer   | Exemples de modèles               | Objectif                                       |
| ------- | --------------------------------- | ---------------------------------------------- |
| staging | `stg_users`, `stg_trips`, …       | Charger & découper les raw JSON Mongo          |
| silver  | `silver_users`, `silver_trips`, … | Nettoyage, formats, calculs (durée, age, etc.) |
| marts   | `dim_user`, `fact_trip`, …        | Modèles analytiques prêts à consommer (KPI)    |


## 5. 🚀 Mise en route

1. **Cloner le repo**

   ```bash
   git clone https://github.com/abrahamkoloboe27/mobility-analytics.git
   cd mobility-analytics
   ```

2. **Configurer `.env`**

   ```dotenv
   # Airbyte
   AIRBYTE_CLOUD_WORKSPACE_ID=...
   AIRBYTE_CLOUD_CLIENT_ID=...
   AIRBYTE_CLOUD_CLIENT_SECRET=...
   AIRBYTE_CONN_ID=...

   # Snowflake
   SNOWFLAKE_ACCOUNT=...
   SNOWFLAKE_USER=...
   SNOWFLAKE_PASSWORD=...
   SNOWFLAKE_ROLE=...
   SNOWFLAKE_WAREHOUSE=...
   SNOWFLAKE_DATABASE=...
   SNOWFLAKE_SCHEMA=...

   # dbt
   DBT_PROFILES_DIR=./
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Déployer le DAG sur Astronomer**

   ```bash
   astro deploy
   ```

5. **Lancer manuellement ou attendre le Scheduler**

   * Airflow UI → Trigger → `full_pipeline_dag`

6. **Visualiser les dashboards**

   * Ouvrir Metabase → 📊 Dashboards pré‑configurés



## 6. 📊 Visualisation & Monitoring

* **Airflow** : Graph, Gantt, Logs, DAGs
* **Snowflake** : History, Query Profile
* **Metabase** : Dashboards interactifs



## 7. 🤝 Ressources & Contacts

| Ressource        | Lien                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 🐙 GitHub        | [https://github.com/abrahamkoloboe27](https://github.com/abrahamkoloboe27)                                                |
| 🔗 LinkedIn      | [https://www.linkedin.com/in/abraham-zacharie-koloboe-data](https://www.linkedin.com/in/abraham-zacharie-koloboe-data)... |
| 📖 dbt Docs      | [https://docs.getdbt.com](https://docs.getdbt.com)                                                                        |
| 🌐 Airbyte Cloud | [https://cloud.airbyte.com](https://cloud.airbyte.com)                                                                    |
| ❄️ Snowflake     | [https://www.snowflake.com](https://www.snowflake.com)                                                                    |
| 📊 Metabase      | [https://www.metabase.com](https://www.metabase.com)                                                                      |

> *Améliorez vos décisions grâce à un pipeline automatisé, fiable et extensible !* 🚀📈

