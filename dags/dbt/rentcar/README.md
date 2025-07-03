# 🚀 dbt Mobility Analytics Platform

Bienvenue dans **dbt Mobility Analytics**, une solution robuste d'analyse de données pour les entreprises de mobilité (services de moto, voiture, location et livraison) qui cherchent à obtenir des insights fiables et actionnables. 📊✨



## 🔍 Description
Ce projet utilise **dbt** pour orchestrer les transformations sur **Snowflake**, garantissant des données :

- 📥 **Brutes** (raw)
- 🧹 **Nettoyées** et **standardisées**
- 🛠️ **Enrichies** pour l’analyse

Le pipeline se décompose en trois couches modulaires : _staging_, _silver_ et _marts_.



## 📁 Structure du projet

```text
├── models/
│   ├── staging/       # Préparation et nettoyage des sources brutes
│   ├── silver/        # Tables consolidées et enrichies
│   └── marts/         # Modèles analytiques finaux (faits & dimensions)
└── macros/            # Fonctions réutilisables
````

### 1️⃣ `staging`

* Tables intermédiaires pour charger et nettoyer les données initiales :

  * `stg_cities`, `stg_countries` (géographie)
  * `stg_users`, `stg_drivers` (profils)
  * `stg_trips`, `stg_ratings`, `stg_maintenance` (opérations)
  * `stg_vehicles` (informations des véhicules)

### 2️⃣ `silver`

* Tables consolidées et appliquées aux règles métier :

  * `silver_countries`, `silver_users`, `silver_drivers`, etc.
  * Données nettoyées, validées et prêtes pour l’analyse exploratoire.

### 3️⃣ `marts`

* **Faits** et **Dimensions** organisés par domaine métier :

  * **Ride Analytics** 🚗🏍️

    * `fact_trip` + `dim_vehicle_ride`, `dim_user_ride`, `dim_driver_ride`, `dim_date_ride`, `dim_country`
  * **Rating Analytics** ⭐

    * `fact_rating` + `dim_user_rating`, `dim_driver_rating`, `dim_date_rating`
  * **Maintenance Analytics** 🔧

    * `fact_maintenance` + `dim_vehicle_maintenance`, `dim_date_maintenance`



## ⚡ Commandes rapides

* Initialiser et exécuter les modèles :

  ```bash
  dbt run
  ```
* Valider la qualité des données :

  ```bash
  dbt test
  ```
* Afficher la documentation générée :

  ```bash
  dbt docs generate && dbt docs serve
  ```



## 🔗 Ressources utiles

* 📖 **dbt Docs** : [documentation officielle](https://docs.getdbt.com/docs/introduction)
* 💬 **Communauté** : [Discourse](https://discourse.getdbt.com/) & [Slack](https://community.getdbt.com/)
* 📅 **Événements** : [dbt Events](https://events.getdbt.com)
* 📝 **Blog** : [dbt Blog](https://blog.getdbt.com/)



## 📬 Contact

* **GitHub** : [abrahamkoloboe27](https://github.com/abrahamkoloboe27) 🐙
* **LinkedIn** : [Abraham KOLOBOE](https://www.linkedin.com/in/abraham-zacharie-koloboe-data-science-ia-generative-llms-machine-learning/) 🔗
* **Email** : [abklb27@gmail.com](mailto:abklb27@gmail.com) 📧



*Améliorez votre prise de décision grâce à des données fiables et bien structurées !* 🚀📈
