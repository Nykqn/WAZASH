**Wazash  —  Gestion de projet**    Mai 2026

**WAZASH**

Gestion de projet — Agile Scrum

Cybersurveillance réseau orientée SOC  —  Mai 2026

# **1. Objet du document**

Ce document définit l'organisation et les modalités de pilotage du projet Wazash. Il transforme le cadrage stratégique en dispositif d'exécution : méthode de travail, équipe projet, rôles Scrum, backlog produit, cérémonies, règles d'estimation, jalons, risques et indicateurs de suivi.

Son objectif est de garantir que la progression du projet reste lisible, mesurable et cohérente avec les attentes produit, le périmètre MVP et les contraintes de démonstration.

## **1.1 Justification par les données (mai 2026)**

- 90 Story Points pour couvrir 1 587 KEV + 30 CVEs 2026 → effort justifié par le volume des menaces

- 5 sprints de 1 semaine face au score d'intensité 1 114,8 → rythme soutenu nécessaire

- 9 membres d'équipe pour 7 sources + 3 conteneurs Docker → ressources adaptées au risque

- 317 ransomware KEV → vélocité cible 18-28 SP/sprint indispensable pour une protection rapide

# **2. Méthode de travail retenue : Agile Scrum**

La méthode retenue est Agile Scrum. Ce choix est adapté à Wazash car le produit doit être construit par incréments fonctionnels, validé régulièrement et ajusté en fonction de la valeur démontrée.

Chaque sprint doit produire un incrément vérifiable : une fonctionnalité utilisable, un scénario reproductible, une preuve exportable, une amélioration de l'interface ou une stabilisation technique.

| **Élément** | **Décision** |
| --- | --- |
| Durée d'un sprint | 1 semaine |
| Nombre cible de sprints MVP | 5 sprints |
| Unité d'estimation | Story points |
| Échelle d'estimation | Fibonacci simplifiée : 1, 2, 3, 5, 8, 13 |
| Revue produit | À la fin de chaque sprint |
| Rétrospective | À la fin de chaque sprint |
| Suivi quotidien | Daily scrum court |

# **3. Équipe projet et rôles**

L'équipe Wazash est organisée autour de neuf profils complémentaires. Les noms ci-dessous sont utilisés comme noms de référence pour clarifier les responsabilités, en hommage à des figures majeures de l'informatique.

| **Personne** | **Rôle** | **Responsabilité principale** |
| --- | --- | --- |
| Ada Lovelace | Product Owner | Porter la vision produit, prioriser le backlog et accepter les user stories |
| Grace Hopper | Scrum Master | Faciliter Scrum, organiser les cérémonies et lever les obstacles |
| Alan Turing | Chef de projet | Suivre les jalons, les risques, les livrables et la cohérence globale |
| Barbara Liskov | Développeuse backend 1 | Concevoir les modèles, l'API FastAPI et la persistance PostgreSQL |
| Ken Thompson | Développeur backend 2 | Développer l'ingestion endpoint, les règles de détection et les workers Celery |
| Tim Berners-Lee | Développeur frontend | Réaliser le dashboard, les vues analyste et les parcours d'export |
| Margaret Hamilton | Testeuse / QA | Définir les scénarios de test, vérifier les critères d'acceptation et produire les preuves |
| Linus Torvalds | DevOps | Maintenir Docker, l'intégration, la configuration et la reproductibilité du lab |
| Radia Perlman | Ingénieure cybersécurité | Valider les règles de détection, la sécurité applicative et les scénarios contrôlés |

## **Répartition opérationnelle**

| **Profil** | **Responsabilités** | **Exemples de tâches Wazash** |
| --- | --- | --- |
| Barbara Liskov — Backend 1 | Architecture backend, modèles, API de consultation, PostgreSQL | Modèles users/assets/events/alerts, routes lecture, migrations, validation |
| Ken Thompson — Backend 2 | Ingestion, traitements asynchrones, détection, corrélation, Redis/Celery | Endpoints heartbeat/events, workers détection, règles simples, corrélation IP/temporelle |
| Tim Berners-Lee — Frontend | Interface web intégrée au serveur-soc, lisibilité analyste | Dashboard, vues actifs/événements/alertes/corrélations, exports CSV/JSON |
| Margaret Hamilton — QA | Stratégie de test, recette, preuves de validation | Scénarios collecte→alerte→preuve, tests API, vérification critères d'acceptation |
| Linus Torvalds — DevOps | Lab Docker, configuration, scripts de lancement, stabilité | Docker Compose, variables d'environnement, réseau de lab, logs, procédure de démarrage |
| Radia Perlman — Cybersécurité | Sécurité applicative, scénarios cyber contrôlés, pertinence des alertes | Contrôle des roles, validation payloads, auth agent, règles de détection, limites de scan |

# **4. Artefacts Scrum**

## **Definition of Ready**

Une user story est prête à entrer dans un sprint si :

- Son objectif est clair et son utilisateur cible identifié

- Ses critères d'acceptation sont rédigés

- Ses dépendances sont connues et son effort estimé en story points

- Elle est réalisable dans un sprint ou découpée

## **Definition of Done**

Une user story est terminée si :

- Le comportement attendu est implémenté et les critères d'acceptation vérifiés

- Les erreurs principales sont gérées et les données utiles persistées ou affichées

- La fonctionnalité est intégrée au lab ou à l'interface si nécessaire

- La documentation minimale est mise à jour

- Une preuve de validation existe : capture, log, export, test ou scénario reproductible

# **5. Cérémonies agiles**

| **Cérémonie** | **Animation** | **Résultat attendu** |
| --- | --- | --- |
| Sprint planning | Grace Hopper | Sprint goal, sprint backlog, capacité engagée |
| Daily scrum | Grace Hopper | Blocages visibles, priorités du jour claires |
| Backlog refinement | Ada Lovelace + Grace Hopper | Stories prêtes, critères clarifiés, estimation ajustée |
| Sprint review | Ada Lovelace | Stories acceptées ou retournées au backlog, retours produit |
| Rétrospective de sprint | Grace Hopper | Une à trois actions d'amélioration mesurables |

# **6. Story points et estimation**

| **Story points** | **Signification** | **Exemple** |
| --- | --- | --- |
| 1 | Très simple, faible incertitude | Ajouter un champ affiché dans une vue existante |
| 2 | Simple, peu de dépendances | Ajouter une route de lecture simple |
| 3 | Moyen, effort clair | Créer une vue liste avec données persistées |
| 5 | Complexe mais maîtrisable | Implémenter une règle de détection complète |
| 8 | Complexe, plusieurs composants | Corrélation entre événements et affichage associé |
| 13 | Trop gros pour un sprint standard | Epic ou story à redécouper |

Capacité initiale indicative : 18 à 24 points par sprint. Cette valeur doit être ajustée après observation réelle de la vélocité.

# **7. Product backlog — Vue d****'****ensemble des epics**

| **Epic** | **Objectif** | **Priorité** | **Total SP** | **Sprint cible** |
| --- | --- | --- | --- | --- |
| EPIC-01 — Socle applicatif et sécurité | FastAPI, authentification, roles, configuration, santé applicative | P1 | 10 | Sprint 1 |
| EPIC-02 — Collecte endpoint et télémétrie | Recevoir heartbeat et events depuis le serveur-endpoint | P1 | 13 | Sprint 2 |
| EPIC-03 — Découverte réseau et actifs | Identifier actifs, ports et services observables dans le lab | P1 | 13 | Sprint 2-3 |
| EPIC-04 — Détection, alertes et audit | Générer, consulter et tracer les alertes et actions sensibles | P1 | 11 | Sprint 3 |
| EPIC-05 — Corrélation et enrichissement analyste | Regrouper des événements liés pour améliorer la lisibilité SOC | P2 | 18 | Sprint 4 |
| EPIC-06 — Interface web et visualisation | Dashboard et vues analyste exploitables | P1 | 13 | Sprint 4 |
| EPIC-07 — Reporting, exports et preuves | Produire des exports CSV/JSON et des preuves de validation | P1 | 9 | Sprint 4-5 |
| EPIC-08 — Lab Docker, démonstration et doc. | Stabiliser le lab, les scénarios et la documentation de lancement | P1 | 13 | Sprint 1, 5 |
| Total MVP |  |  | 90 SP | 5 sprints |

# **8. Features par epic**

| **Epic** | **Feature** | **Description** | **Priorité** |
| --- | --- | --- | --- |
| EPIC-01 | FEAT-01.1 Authentification | Connexion utilisateur, session/token, endpoint /me | P1 |
| EPIC-01 | FEAT-01.2 Contrôle d'accès | Gestion des roles admin et analyst | P1 |
| EPIC-01 | FEAT-01.3 Santé applicative | Endpoint GET /health, logs applicatifs de base | P1 |
| EPIC-02 | FEAT-02.1 Heartbeat | Ingestion et affichage du dernier heartbeat | P1 |
| EPIC-02 | FEAT-02.2 Events | Ingestion, validation et persistance des événements | P1 |
| EPIC-02 | FEAT-02.3 Auth agent | Authentification du serveur-endpoint auprès de l'API | P1 |
| EPIC-03 | FEAT-03.1 Scan IP | Scan contrôlé du réseau de lab | P1 |
| EPIC-03 | FEAT-03.2 Inventaire actifs | Création et mise à jour des actifs | P1 |
| EPIC-03 | FEAT-03.3 Ports et services | Association ports/services aux actifs | P1 |
| EPIC-04 | FEAT-04.1 Règles simples | Détection de comportements suspects contrôlés | P1 |
| EPIC-04 | FEAT-04.2 Cycle de vie alertes | Liste, détail, statut minimal | P1 |
| EPIC-04 | FEAT-04.3 Audit | Journalisation connexions, exports, actions sensibles | P1 |
| EPIC-05 | FEAT-05.1 Corrélation IP | Regroupement par IP source | P2 |
| EPIC-05 | FEAT-05.2 Corrélation temporelle | Regroupement par fenêtre temporelle | P2 |
| EPIC-05 | FEAT-05.3 Vue corrélation | Consultation des groupes de corrélation | P2 |
| EPIC-06 | FEAT-06.1 Dashboard | Métriques clés : événements, alertes, endpoints, exports | P1 |
| EPIC-06 | FEAT-06.2 Vues analyste | Actifs, événements, alertes, audit | P1 |
| EPIC-06 | FEAT-06.3 Visualisation enrichie | IP attaquantes, carte géographique si faisable | P3 |
| EPIC-07 | FEAT-07.1 Export CSV | Export des événements ou alertes | P1 |
| EPIC-07 | FEAT-07.2 Export JSON | Export structuré exploitable | P1 |
| EPIC-07 | FEAT-07.3 Export XML | Extension si temps disponible | P3 |
| EPIC-08 | FEAT-08.1 Docker Compose | Lab serveur-soc, serveur-endpoint, serveur-attacker | P1 |
| EPIC-08 | FEAT-08.2 Scénarios contrôlés | Scénarios reproductibles de détection | P1 |
| EPIC-08 | FEAT-08.3 Documentation | Procédure de lancement, validation et preuves | P1 |

# **9. User stories MVP**

## **EPIC-01 — Socle applicatif et sécurité**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-01.1 | En tant qu'utilisateur, je veux me connecter à l'application afin d'accéder aux fonctions protégées. | 5 | Connexion valide acceptée, connexion invalide refusée |
| US-01.2 | En tant qu'administrateur, je veux distinguer les roles afin de limiter les actions sensibles. | 3 | Un analyste ne peut pas effectuer une action réservée à l'admin |
| US-01.3 | En tant qu'équipe produit, je veux connaître l'état de l'application afin de vérifier rapidement le lab. | 2 | /health répond et indique l'état applicatif |

## **EPIC-02 — Collecte endpoint et télémétrie**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-02.1 | En tant que serveur-endpoint, je veux envoyer un heartbeat afin d'indiquer que je suis actif. | 3 | Heartbeat visible côté serveur-soc |
| US-02.2 | En tant que serveur-endpoint, je veux envoyer des événements afin d'alimenter la détection. | 5 | Events consultables et horodatés |
| US-02.3 | En tant que système, je veux authentifier les agents afin de refuser les sources inconnues. | 5 | Requête non autorisée refusée |

## **EPIC-03 — Découverte réseau et actifs**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-03.1 | En tant qu'analyste, je veux voir les actifs détectés afin de comprendre le périmètre surveillé. | 5 | Actifs visibles avec IP et dernière observation |
| US-03.2 | En tant qu'analyste, je veux connaître les ports ouverts afin d'identifier les services exposés. | 5 | Ports associés à un actif |
| US-03.3 | En tant que responsable validation, je veux limiter les scans au lab afin d'éviter tout comportement non maîtrisé. | 3 | Scan borné au réseau Docker prévu |

## **EPIC-04 — Détection, alertes et audit**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-04.1 | En tant qu'analyste, je veux obtenir une alerte lorsqu'un comportement suspect est observé. | 5 | Scénario suspect génère une alerte visible dans dashboard |
| US-04.2 | En tant qu'analyste, je veux consulter la liste et le détail des alertes afin de qualifier la situation. | 3 | Alerte consultable avec contexte |
| US-04.3 | En tant que responsable validation, je veux tracer les actions sensibles afin de disposer d'une preuve d'audit. | 3 | Actions sensibles journalisées |

## **EPIC-05 — Corrélation et enrichissement analyste**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-05.1 | En tant qu'analyste, je veux regrouper des événements par IP source afin d'identifier une activité répétée. | 8 | Groupe créé pour événements liés, visible côté analyste |
| US-05.2 | En tant qu'analyste, je veux corréler des événements dans une fenêtre temporelle. | 8 | Répétition temporelle visible |
| US-05.3 | En tant qu'analyste, je veux consulter les corrélations afin de comprendre pourquoi une alerte est enrichie. | 5 | Corrélation consultable et explicable |

## **EPIC-06 — Interface web et visualisation**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-06.1 | En tant qu'analyste, je veux un dashboard synthétique afin de lire rapidement l'état du système. | 5 | Dashboard affiche endpoints, events, alertes, exports |
| US-06.2 | En tant qu'analyste, je veux naviguer entre actifs, événements et alertes afin d'investiguer efficacement. | 5 | Parcours analyste complet |
| US-06.3 | En tant qu'analyste, je veux voir les IP attaquantes afin d'identifier les sources récurrentes. | 3 | IP sources visibles avec fréquence |

## **EPIC-07 — Reporting, exports et preuves**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-07.1 | En tant qu'analyste, je veux exporter les alertes en CSV afin de produire une preuve exploitable. | 3 | CSV généré et téléchargeable |
| US-07.2 | En tant qu'analyste, je veux exporter les données en JSON afin de conserver une preuve structurée. | 3 | JSON généré et exploitable |
| US-07.3 | En tant que responsable validation, je veux relier un export à un scénario afin de vérifier la cohérence des preuves. | 3 | Export compréhensible et rattaché au scénario |

## **EPIC-08 — Lab Docker, démonstration et documentation**

| **Story** | **User story** | **SP** | **Critères d****'****acceptation** |
| --- | --- | --- | --- |
| US-08.1 | En tant qu'équipe produit, je veux démarrer les trois conteneurs afin de disposer d'un lab reproductible. | 5 | serveur-soc, serveur-endpoint, serveur-attacker démarrent |
| US-08.2 | En tant que responsable validation, je veux un scénario contrôlé afin de rejouer la chaîne complète. | 5 | Scénario collecte→alerte→preuve reproductible |
| US-08.3 | En tant que contributeur, je veux une documentation claire afin de lancer et vérifier le produit. | 3 | Documentation suffisante pour relancer le lab |

# **10. Découpage prévisionnel par sprint**

| **Sprint** | **Sprint goal** | **Stories prioritaires** | **Livrable attendu** |
| --- | --- | --- | --- |
| Sprint 1 | Poser le socle applicatif sécurisé | US-01.1, US-01.2, US-01.3, US-08.1 | Application lançable, auth minimale, santé API, Docker initial |
| Sprint 2 | Ingestion et inventaire initial | US-02.1, US-02.2, US-02.3, US-03.1 | Heartbeat/events persistés, agents authentifiés, actifs visibles |
| Sprint 3 | Détection, alertes et audit | US-03.2, US-03.3, US-04.1, US-04.2, US-04.3 | Scénario suspect produisant une alerte consultable et auditée |
| Sprint 4 | Interface analyste, corrélation et exports | US-05.1, US-06.1, US-06.2, US-07.1, US-07.2 | Dashboard, alertes, corrélation IP, exports CSV/JSON |
| Sprint 5 | Stabilisation, preuve et validation complète | US-05.2, US-05.3, US-06.3, US-07.3, US-08.2, US-08.3 | Chaîne complète reproductible, documentation et preuves prêtes |

## **Répartition des tâches par sprint**

| **Sprint** | **Backend 1 (B. Liskov)** | **Backend 2 (K. Thompson)** | **Frontend (T. Berners-Lee)** | **QA (M. Hamilton)** | **DevOps (L. Torvalds)** | **Cybersec (R. Perlman)** |
| --- | --- | --- | --- | --- | --- | --- |
| Sprint 1 | Modèles user, routes auth, /health | Préparer structure ingestion | Login, base dashboard, navigation initiale | Cas de test auth et santé API | Docker Compose initial, variables, logs | Règles roles, exigences secrets, routes protégées |
| Sprint 2 | Modèles assets/events, routes consultation | Endpoints heartbeat/events, auth agent | Vues endpoints, actifs et événements | Tests ingestion, payloads invalides | Stabilité réseau Docker, config agent | Validation payloads, limitation sources inconnues |
| Sprint 3 | Modèles alertes, audit log, routes alertes | Règles détection, scan contrôlé, worker | Vues alertes, détail alerte, audit | Recette scénario suspect→alerte | Scripts scénario contrôlé, logs reproductibles | Limites scan, pertinence règles, sécurité audit |
| Sprint 4 | API métriques, corrélations, exports | Corrélation IP, génération CSV/JSON, worker export | Dashboard, corrélations, parcours export | Tests dashboard, exports, cohérence preuves | Vérification volumes, chemins exports, relance lab | Vérification données exposées, traçabilité export |
| Sprint 5 | Stabilisation API, corrections, doc technique | Corrélation temporelle, finalisation scénario | Finitions UX, états vides, IP attaquantes | Recette complète, non-régression, captures finales | Procédure lancement, reset lab, troubleshooting | Revue sécurité finale et limites documentées |

# **11. Jalons projet**

| **Jalon** | **Description** | **Preuve attendue** |
| --- | --- | --- |
| J1 | Cadrage validé | Feuille de cadrage, gestion de projet, cahier des charges, architecture |
| J2 | Socle technique opérationnel | Application démarrée, auth minimale, endpoint santé |
| J3 | Collecte endpoint fonctionnelle | Heartbeat et events persistés |
| J4 | Découverte et actifs visibles | Actifs, ports ou services consultables |
| J5 | Détection et alertes opérationnelles | Alerte générée depuis un scénario contrôlé |
| J6 | Corrélation visible | Groupe de corrélation consultable |
| J7 | Exports et audit prêts | CSV/JSON produits et journalisés |
| J8 | Démonstration finale stabilisée | Chaîne complète rejouable dans Docker |

# **12. Risques projet**

| **Risque** | **Impact** | **Mesure de maîtrise** | **Responsable** | **Statut** |
| --- | --- | --- | --- | --- |
| Dérive du périmètre | Retard sur le MVP | Prioriser P1, reporter P3, arbitrer en sprint planning | Alan Turing | Ouvert |
| Sous-estimation de la corrélation | Valeur SOC affaiblie | Commencer par IP source et fenêtre temporelle simple | Ken Thompson | Ouvert |
| Instabilité du lab Docker | Démonstration difficile à reproduire | Stabiliser Docker dès Sprint 1 et tester à chaque sprint | Linus Torvalds | Mitigé |
| Complexité excessive du frontend | Perte de temps sur le visuel | Prioriser lisibilité analyste et parcours de preuve | Tim Berners-Lee | Ouvert |
| Sécurité insuffisante | Produit cyber peu crédible | Intégrer auth, roles, auth agent, validation payloads et audit dès le MVP | Radia Perlman | Ouvert |
| Données de test non maîtrisées | Scénarios peu réalistes | Limiter aux IP lab, documenter, simuler sans destructivité | Margaret Hamilton | Mitigé |
| Documentation tardive | Produit difficile à relancer | Mettre à jour la documentation dans la Definition of Done | Alan Turing | Ouvert |

# **13. Indicateurs de suivi Scrum**

## **Tableau de bord de vélocité (prévisionnel)**

| **Sprint** | **SP planifiés** | **SP terminés** | **Vélocité** | **Taux réussite** |
| --- | --- | --- | --- | --- |
| Sprint 1 | 18 | 16 | 16 | 89 % |
| Sprint 2 | 22 | 20 | 20 | 91 % |
| Sprint 3 | 24 | 22 | 22 | 92 % |
| Sprint 4 | 26 | 24 | 24 | 92 % |
| Sprint 5 | 28 | 26 | 26 | 93 % |
| Moyenne | 24 | 22 | 22 | 91 % |

## **Indicateurs détaillés**

| **Indicateur** | **Usage** | **Cible** |
| --- | --- | --- |
| Vélocité par sprint | Mesurer la capacité réelle de l'équipe | 20-24 SP/sprint |
| SP terminés / engagés | Détecter la surcharge ou la sous-estimation | > 90 % |
| Nombre de stories P1 terminées | Vérifier la couverture MVP | 100 % P1 done |
| Nombre de blockers ouverts | Suivre les obstacles critiques | 0 blocker en fin de sprint |
| Taux de stories respectant la DoD | Suivre la qualité réelle des incréments | 100 % |
| Stabilité du lab Docker | Vérifier la reproductibilité de la démonstration | 100 % démarrage réussi |
| Nombre de preuves produites | Relier développement, validation et démonstration | 1 preuve par story |

# **14. Conclusion**

La gestion de projet de Wazash repose sur Agile Scrum afin de maintenir une exécution itérative, mesurable et orientée valeur. Le découpage en epics, features, user stories et tasks permet de relier directement le pilotage projet aux exigences du cahier des charges et aux choix d'architecture.

Les cérémonies Scrum, les story points, la Definition of Ready et la Definition of Done doivent être utilisés comme des mécanismes de maîtrise : ils rendent l'avancement visible, limitent la dérive du périmètre et garantissent que chaque incrément produit une preuve exploitable.

Page
