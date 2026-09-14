---
title: "Architecting a Multi-Agent AI Ecosystem on Databricks: Bridging Genie and MCP"
date: 2026-09-14
url: "https://open.substack.com/pub/tonteria/p/architecting-a-multi-agent-ai-ecosystem?utm_source=multiple-personal-recommendations-email&utm_medium=email&token=eyJ1c2VyX2lkIjo0NzU1OTI2MjgsInBvc3RfaWQiOjIxMzQ0Mjc4MCwiaWF0IjoxNzg5MzMxNTU4LCJleHAiOjE3OTE5MjM1NTgsImlzcyI6InB1Yi00MzkwMTY5Iiwic3ViIjoicG9zdC1yZWFjdGlvbiJ9.Zf3KdxjyvfY48y5OEyfn3a2xnncKqDY484Hey8BbTdo"
keywords: ["multi-agent", "MCP", "LangGraph", "Databricks Genie", "gouvernance des données", "Unity Catalog"]
theme: "IA"
tone: "tutorial"
used_in: ["2026-09-14"]
---

## Résumé
L'article explique pourquoi une architecture Genie monolithique (l'interface conversationnelle de Databricks pour interroger des données d'entreprise en langage naturel) atteint ses limites dès que les questions métier deviennent transversales — mêlant par exemple RH, ventes et données non structurées. Il propose de la remplacer par un écosystème multi-agents : plusieurs "Genie Spaces" spécialisés par domaine sont exposés comme des outils standardisés via le Model Context Protocol (MCP), et un agent superviseur construit avec LangGraph (selon le patron ReAct) décide dynamiquement quel outil interroger avant de synthétiser la réponse finale. La gouvernance reste assurée de bout en bout par Unity Catalog et une authentification "On-Behalf-Of" (OBO), qui applique automatiquement des restrictions d'accès selon l'identité de l'utilisateur final. L'article conclut sur la mise en production via Databricks Apps, avec traçage MLflow et évaluation continue par agent.

## Points clés
- Un agent unique ("monolithe") souffre de confusion de schéma (ex. "rétention" RH vs. commerciale), de surcharge d'instructions qui dilue son raisonnement, et viole le principe de moindre privilège en donnant accès à toutes les tables à une seule application.
- La solution : diviser la logique métier en agents spécialisés par domaine (ventes, RH, etc.), orchestrés par un agent superviseur unique.
- Le MCP (porté par Anthropic) permet à l'agent superviseur de découvrir dynamiquement les outils disponibles via des schémas JSON auto-descriptifs, sans coder en dur les endpoints API — rendant chaque Genie Space "plug-and-play" pour n'importe quel framework (LangGraph, AutoGen, CrewAI).
- L'orchestrateur est implémenté avec LangGraph en boucle ReAct (raisonnement du superviseur ⇄ appel d'outil), avec traçage MLflow intégré pour l'observabilité.
- La sécurité repose sur Unity Catalog et l'authentification OBO : l'identité de l'utilisateur métier est propagée jusqu'à l'entrepôt SQL, qui applique des filtres de sécurité au niveau ligne (RLS) sans jamais exposer au LLM des données non autorisées.
- Déployé comme Databricks App, le système bénéficie nativement du traçage MLflow (traçabilité complète de chaque appel d'outil et requête SQL générée) et de l'évaluation continue (Mosaic AI Agent Evaluation) agent par agent.

## Analyse approfondie

### Le problème du monolithe : pourquoi un agent unique ne tient pas la charge
L'IA générative passe des interfaces conversationnelles simples à des workflows agentiques autonomes et intégrés, déplaçant le goulot d'étranglement technique du raisonnement pur vers l'accès au contexte : un LLM n'est utile que dans la mesure où il peut interagir de façon sûre, fiable et précise avec les données de l'entreprise.

Databricks Genie offre une interface qui traduit le langage naturel en requêtes SQL optimisées sur la Data Intelligence Platform. Mais dès qu'un dirigeant pose une question transversale — l'exemple donné est celui d'un Chief Revenue Officer demandant si le pic des ventes Entreprise du T3 aux États-Unis est lié à l'embauche de nouveaux Senior Account Executives, et quel est le sentiment autour des contrats de renouvellement — un Genie Space unique ne suffit plus : il faudrait combiner des données commerciales structurées, des données RH structurées et du texte juridique non structuré.

Trois raisons expliquent l'échec d'un "Genie tout-puissant" unique :
1. **Confusion de schéma** : un agent monolithique peine à lever l'ambiguïté d'un terme comme "rétention", qui peut désigner la rétention des employés (RH) ou celle des clients (Ventes).
2. **Surcharge d'instructions** : entasser la logique métier, les cas particuliers et les définitions de métriques de tous les départements dans un seul prompt système dilue la capacité de raisonnement de l'agent sur chacun d'eux ; la fenêtre de contexte gonfle, ce qui favorise les hallucinations et du SQL erroné.
3. **Gouvernance des données** : donner à une seule application un accès global à toutes les tables de l'entreprise viole le principe de moindre privilège.

### La solution multi-agents : diviser pour mieux régner
Plutôt qu'un agent unique qui fait tout, mais mal, un système multi-agents utilise un point d'entrée unique qui route les requêtes vers des sous-agents spécialisés. Cette architecture s'appuie sur des nœuds spécialisés travaillant de concert, chacun responsable d'un domaine métier précis.

### L'avantage du Model Context Protocol (MCP)
Pour construire cet écosystème sans écrire des wrappers d'API REST fragiles pour chaque domaine, l'article s'appuie sur le Model Context Protocol (MCP), un standard ouvert porté par Anthropic et largement adopté, qui permet aux modèles d'IA de découvrir et d'interagir avec des sources de données externes sous forme d'outils standardisés.

L'agent superviseur ne code pas en dur les endpoints d'API : il interroge le serveur MCP avec une question du type "quels outils as-tu ?". Le serveur MCP de Databricks Genie répond alors avec des schémas JSON auto-descriptifs de ses capacités, à la volée. Cela transforme des Genie Spaces spécialisés en outils "plug-and-play" utilisables par n'importe quel framework — LangGraph, AutoGen ou CrewAI.

### Construire l'orchestrateur ReAct avec LangGraph
L'orchestrateur est implémenté avec LangGraph et le client MCP de Databricks. Dans ce montage, un LLM superviseur évalue le prompt et décide quel outil MCP Genie spécifique au domaine il doit exécuter, avant de synthétiser la réponse finale. Un traçage MLflow est injecté pour obtenir une observabilité complète.

**1. Connexion des clients MCP** — On commence par se connecter aux Genie Spaces spécifiques via le client MCP de Databricks, et par récupérer dynamiquement leurs outils disponibles :

```python
import os
import mlflow
from langchain_openai import ChatOpenAI
from databricks.mcp.client import DatabricksMCPClient

# Active le traçage MLflow pour LangChain afin de surveiller le raisonnement de l'agent
mlflow.langchain.autolog()

# Initialise le LLM (via les Databricks Foundation Model APIs)
llm = ChatOpenAI(
    base_url=f"https://{os.environ['DATABRICKS_HOST']}/serving-endpoints",
    api_key=os.environ['DATABRICKS_TOKEN'],
    model="databricks-meta-llama-3-3-70b-instruct"
)

# Connexion aux Genie Spaces spécialisés via MCP
# Ce sont des déploiements Genie entièrement distincts, optimisés chacun pour son domaine
sales_mcp = DatabricksMCPClient(url="https://<workspace>/api/2.0/mcp/sales_genie")
hr_mcp = DatabricksMCPClient(url="https://<workspace>/api/2.0/mcp/hr_genie")

# Récupère dynamiquement les outils des deux Genie Spaces
all_genie_tools = sales_mcp.list_tools() + hr_mcp.list_tools()

# Lie les outils au LLM afin qu'il sache comment les invoquer
llm_with_tools = llm.bind_tools(all_genie_tools)
```

**2. Définition de la boucle ReAct dans LangGraph** — On définit ensuite l'état et les nœuds du graphe. Celui-ci fait alterner un nœud Superviseur (raisonnement) et un nœud ToolNode (action) jusqu'à ce que toutes les données nécessaires pour répondre à la question soient réunies :

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Définit l'état du graphe
class State(TypedDict):
    # Ajoute les nouveaux messages à la liste existante au lieu de l'écraser
    messages: Annotated[list, add_messages]

def supervisor_node(state: State):
    """Le cerveau : évalue la requête et décide quel outil appeler, ou synthétise la réponse finale."""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Construit le graphe ReAct
workflow = StateGraph(State)

# Ajoute les nœuds
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("tools", ToolNode(all_genie_tools))

# Définit le flux d'exécution
workflow.add_edge(START, "supervisor")
# tools_condition vérifie si le LLM a décidé d'appeler un outil.
# Si oui -> vers "tools". Sinon -> vers END.
workflow.add_conditional_edges("supervisor", tools_condition)
workflow.add_edge("tools", "supervisor")

# Compile le graphe en agent exécutable
multi_agent_app = workflow.compile()
```

**3. Exécution d'une requête transversale** — Une fois le graphe compilé, on peut lui soumettre la question complexe du CRO ; le superviseur LangGraph route automatiquement les requêtes en langage naturel vers les Genie Spaces Databricks appropriés, attend l'exécution du SQL, puis synthétise les données :

```python
user_prompt = (
    "Did the recent spike in Q3 Enterprise Sales correlate with the "
    "hiring of new Senior Account Executives in the US region?"
)

# Exécute la boucle ReAct
final_state = multi_agent_app.invoke(
    {"messages": [{"role": "user", "content": user_prompt}]}
)

# Affiche la réponse synthétisée
print(final_state["messages"][-1].content)
```

### L'impératif de sécurité : Unity Catalog et OBO
Une architecture multi-agents ne fonctionne à l'échelle de l'entreprise que si la gouvernance des données suit. Comme l'ensemble du dispositif reste dans l'écosystème Databricks, Unity Catalog sert de couche universelle de gouvernance.

Le superviseur LangGraph n'envoie pas un principal de service générique lorsqu'il appelle le MCP de Sales Genie : il utilise une authentification **On-Behalf-Of (OBO)**. L'identité de l'utilisateur métier à l'origine de la question est propagée à travers l'orchestrateur, puis le serveur MCP, jusqu'à l'entrepôt SQL Databricks qui produit la réponse.

Ainsi, quand le CRO interroge les ventes globales, Unity Catalog le permet ; mais quand un manager régional pose la même question au même agent, Unity Catalog applique automatiquement des filtres de sécurité au niveau ligne (Row-Level Security) pour ne délivrer que les données de sa région. Le LLM ne voit jamais de données auxquelles l'utilisateur n'a pas droit, ce qui élimine le risque de fuite accidentelle de données lors de la synthèse.

### Passer en production
Pour aller en production, il faut sortir du notebook : on héberge le système multi-agents directement à côté des données en empaquetant l'orchestrateur ReAct LangGraph dans une **Databricks App**, qui gère nativement la propagation d'identité OBO, fournit un backend de calcul scalable et une interface utilisateur fluide pour dialoguer avec l'agent superviseur.

Au-delà du simple déploiement, l'enjeu porte sur la gestion du cycle de vie, l'observabilité et l'évaluation continue. Les Databricks Apps fournissent la couche de calcul et de routage, mais la vraie valeur vient de leur intégration profonde avec le reste de l'écosystème ML de Databricks : déployer l'agent LangGraph comme Databricks App fait que MLflow Tracing capture automatiquement chaque interaction, chaque appel d'outil et chaque génération du LLM. Il n'est donc plus nécessaire de deviner ce qui s'est passé lorsqu'un utilisateur signale une réponse confuse sur le revenu du T3 : on peut ouvrir l'interface MLflow, retracer le chemin d'exécution exact du superviseur LangGraph, voir le payload exact envoyé au serveur MCP, et la requête SQL exacte générée par le Genie Space concerné.

Ce dispositif bénéficie en outre nativement de l'évaluation d'agents (Mosaic AI Agent Evaluation). Comme la logique de chaque domaine est isolée dans des endpoints MCP distincts, on peut évaluer le Sales Genie indépendamment du HR Genie, générer des jeux de données de référence (questions en langage naturel et SQL attendu) et exécuter des pipelines d'évaluation continue. Si la précision du système multi-agents chute sur des questions transversales, les traces permettent d'identifier immédiatement si l'échec provient du niveau routage du superviseur (mauvais choix d'outil MCP) ou du niveau sous-agent (SQL erroné généré par l'outil MCP). C'est cette architecture découplée — orchestrateur, agents de domaine et couche de gouvernance indépendants mais interconnectés — qui permet aux équipes IA d'entreprise de passer du prototype à la production critique avec confiance.

## Pourquoi ça compte
Ce billet illustre une tendance de fond de la veille IA d'entreprise en 2026 : le passage des chatbots analytiques monolithiques vers des architectures multi-agents modulaires appuyées sur des standards ouverts comme le MCP, où la gouvernance des données (Unity Catalog, OBO, RLS) devient une brique de conception aussi centrale que le raisonnement du LLM lui-même.
