# CNR-VGF — Continuous Net Risk Vulnerability Governance Framework

Plateforme de priorisation des vulnérabilités qui combine les données publiques de menace (NVD, EPSS, CISA KEV) avec le contexte d'un inventaire d'actifs pour calculer un **score de risque net** par couple *CVE × actif*, puis attribuer une priorité de remédiation (P1 à P4).

Le projet comprend :

- un **pipeline de données** qui construit les jeux de données enrichis ;
- un **modèle de scoring** pondéré (technique, menace, métier, exposition) ;
- des **modèles ML** (Random Forest, XGBoost) qui prédisent les vulnérabilités à risque élevé ;
- un **graphe Neo4j** des relations actifs / vulnérabilités ;
- un **assistant IA** (LLM local via Ollama) exposé par une API FastAPI.

## Architecture

```
CNR-VGF/
├── backend/
│   ├── scripts/   # Pipeline de données (extraction, enrichissement, scoring)
│   ├── ml/        # Préparation du dataset, entraînement et évaluation des modèles
│   │   └── models/        # rf_model.pkl, xgb_model.pkl
│   ├── graph/     # Connexion et import dans Neo4j
│   ├── ai/        # Assistant IA (LLM + prompts)
│   └── api/       # API FastAPI (routes, schémas)
├── data/
│   ├── raw/       # Sources brutes (NVD, EPSS, KEV, CWE, inventaire d'actifs)
│   └── processed/ # Jeux de données générés
├── requirements.txt
└── .env.example
```

## Score de risque net

Chaque couple CVE × actif reçoit quatre sous-scores sur 100 :

| Facteur | Calcul | Poids |
|---|---|---|
| **Technique** | CVSS × 10 | 30 % |
| **Menace** | 40 % EPSS + 60 % présence dans CISA KEV | 25 % |
| **Métier** | Criticité de l'actif | 25 % |
| **Exposition** | 60 % exposition Internet + 20 % EDR + 20 % pare-feu | 20 % |

Le score net détermine la priorité :

| Score | Priorité |
|---|---|
| ≥ 80 | P1 - Critical |
| ≥ 60 | P2 - High |
| ≥ 30 | P3 - Medium |
| < 30 | P4 - Low |

## Installation

Prérequis : Python 3.12, [Neo4j](https://neo4j.com/) (pour le graphe) et [Ollama](https://ollama.com/) avec le modèle `llama3.1:8b` (pour l'assistant IA).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install langchain-ollama
ollama pull llama3.1:8b
```

Copier `.env.example` en `.env` et renseigner les identifiants Neo4j :

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=change-me
```

## Données

Les fichiers de plus de 100 Mo ne sont pas versionnés et doivent être régénérés :

| Fichier | Comment l'obtenir |
|---|---|
| `data/raw/nvdcve-2.0-2026.json` | À télécharger depuis les [flux NVD](https://nvd.nist.gov/vuln/data-feeds) |
| `data/processed/exposure_dataset.csv` | `build_exposure_dataset.py` |
| `data/processed/net_risk_dataset.csv` | `build_net_risk_model.py` |

Ordre d'exécution du pipeline, depuis la racine du projet :

```bash
python backend/scripts/extract_nvd.py             # NVD JSON        -> vulnerabilities.csv
python backend/scripts/enrich_dataset.py          # + EPSS + KEV    -> vulnerability_dataset.csv
python backend/scripts/generate_assets.py         # inventaire d'actifs synthétique -> asset_inventory.csv
python backend/scripts/build_exposure_dataset.py  # CVE x actifs    -> exposure_dataset.csv
python backend/scripts/build_net_risk_model.py    # scoring         -> net_risk_dataset.csv

python backend/ml/prepare_dataset.py              # -> ml_training_dataset.csv
python backend/ml/train_random_forest.py          # -> models/rf_model.pkl
python backend/ml/train_xgboost.py                # -> models/xgb_model.pkl
python backend/ml/evaluate_models.py              # -> model_comparison.csv

python backend/graph/import_graph.py              # import dans Neo4j
```

> `generate_assets.py` écrit vers un chemin absolu Windows : adapter `OUTPUT_FILE` avant de l'exécuter sur une autre machine.

## Modèles ML

Les modèles prédisent si une vulnérabilité est à risque élevé (`Risk_Label`, dérivé de la priorité) à partir de CVSS, EPSS, KEV, des quatre sous-scores et du type d'actif.

| Modèle | Accuracy | F1 | ROC AUC |
|---|---|---|---|
| Random Forest | 0.9998 | 0.9989 | 0.99999 |
| XGBoost | 0.99985 | 0.9991 | 0.99999 |

Ces scores quasi parfaits s'expliquent par le fait que le label est calculé de façon déterministe à partir des mêmes sous-scores utilisés comme variables : les modèles réapprennent la formule de scoring.

## API

```bash
uvicorn backend.api.main:app --reload
```

Documentation interactive : http://localhost:8000/docs

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Statut de l'application |
| GET | `/health` | Vérification de santé |
| POST | `/advisor` | Question à l'assistant IA (`{"question": "..."}`) |

## Stack

Python · pandas · scikit-learn · XGBoost · FastAPI · Neo4j · LangChain · Ollama (Llama 3.1)

## Auteur

Aya Belkhaoua — projet réalisé dans le cadre d'un stage chez Swiss Life.
