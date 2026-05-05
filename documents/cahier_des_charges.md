**Wazash  —  Cahier des charges**    Mai 2026

**WAZASH**

Cahier des charges fonctionnel et technique

Cybersurveillance réseau orientée SOC  —  MVP v1.2  —  Mai 2026

# **1. Objet du document**

Le présent cahier des charges formalise les besoins, le périmètre, les contraintes, les exigences fonctionnelles et non fonctionnelles ainsi que les critères de validation du projet Wazash.

Il transforme les orientations de cadrage en exigences vérifiables, suffisamment précises pour guider le développement et suffisamment lisibles pour être défendues lors d'une revue projet. Il constitue la base de dialogue entre les dimensions produit, projet et technique.

## **1.1 Contexte quantifié (mai 2026)**

Les données collectées valident les exigences du cahier des charges :

- 1 587 vulnérabilités connues et exploitées (CISA KEV) → exigence de couverture étendue

- 317 cas de ransomware identifiés (20 % des KEV) → exigence de détection proactive obligatoire

- Score d'intensité 1 114,8 (Élevé) → exigence de performance < 5 min détection

- 30 CVEs récents 2026 (7 Critiques, 6 Élevés) → exigence de support CVSS v3.1 complet

# **2. Fiche documentaire**

| **Élément** | **Valeur** |
| --- | --- |
| Projet | Wazash |
| Document | Cahier des charges fonctionnel et technique |
| Version | 1.2 |
| Statut | Version détaillée du cahier des charges MVP |
| Périmètre | Produit MVP démontrable en environnement Docker |
| Public visé | Équipe projet, parties prenantes, contributeurs techniques, responsables de validation |

## **Historique des versions**

| **Version** | **Objet** | **Statut** |
| --- | --- | --- |
| 1.0 | Formalisation initiale du périmètre, des exigences et des critères d'acceptation | Référence initiale |
| 1.1 | Enrichissement : exigences numérotées, sécurité, données, recette et traçabilité | Version consolidée |
| 1.2 | Précision des règles métier, contrats API, permissions, formats de données, critères mesurables | Version détaillée MVP |

# **3. Résumé exécutif**

Wazash est une solution de cybersurveillance réseau orientée SOC. Le produit vise à superviser un environnement de démonstration, collecter de la télémétrie depuis un endpoint, identifier des actifs, détecter des comportements suspects, corréler des signaux répétés, produire des alertes et générer des preuves exploitables sous forme d'historique, de journaux et d'exports.

Le cahier des charges retient une logique de MVP démontrable. L'objectif n'est pas de reproduire toute la complexité d'un SIEM enterprise, mais de prouver une chaîne fonctionnelle complète : observation réseau, ingestion, persistance, détection, corrélation, visualisation, audit et export de preuve.

# **4. Contexte et problématique**

Le projet répond à deux niveaux d'attente : un besoin de démonstration produit, défini par le périmètre MVP et les critères de validation ; un besoin de valorisation produit, défini par les études réalisées, le positionnement retenu et l'opportunité identifiée sur le marché.

La problématique peut être formulée ainsi : comment produire une visibilité cyber suffisamment riche pour être utile, tout en conservant une architecture simple, testable et compatible avec un environnement de démonstration contrôlé ?

# **5. Objectifs du produit**

## **Objectif général**

Concevoir une application web de supervision cyber réseau capable de démontrer une chaîne SOC minimale, depuis la collecte endpoint jusqu'à la production de preuves exportables.

## **Objectifs opérationnels**

| **ID** | **Objectif** | **Résultat attendu** |
| --- | --- | --- |
| OBJ-001 | Collecter de la télémétrie depuis un endpoint supervisé | heartbeat et events reçus, persistés et consultables |
| OBJ-002 | Découvrir le périmètre réseau observable | Actifs, ports et services identifiés dans le lab |
| OBJ-003 | Détecter des comportements suspects | Alertes générées à partir de règles simples |
| OBJ-004 | Corréler des signaux répétés | Regroupement d'événements liés à une IP, une cible ou une fenêtre temporelle |
| OBJ-005 | Restituer l'information à un analyste | Dashboard, vues d'alertes, actifs, événements et corrélations |
| OBJ-006 | Produire une preuve exploitable | Export CSV ou JSON généré pendant la démonstration |
| OBJ-007 | Soutenir une démonstration reproductible | Lab Docker en 3 conteneurs opérationnel |

# **6. Périmètre du MVP**

## **6.1 Fonctions incluses**

- Authentification utilisateur et gestion des roles

- Collecte de heartbeat et d'événements

- Découverte réseau, scan IP, ports et services

- Observation de trafic réseau et analyse de logs

- Génération d'alertes et corrélation de signaux répétés

- Consultation d'actifs, événements, alertes et historique

- Métriques de supervision, exports CSV et JSON

- Affichage des IP attaquantes (visualisation géographique en extension P3)

## **6.2 Fonctions hors périmètre initial**

- Réponse automatique avancée et orchestration SOAR

- Multi-tenant complet

- Couverture SIEM exhaustive et moteur de détection enterprise complexe

- Déploiement distribué de production

- Supervision de réseaux externes au lab Docker

## **6.3 Règles de priorisation**

| **Priorité** | **Signification** | **Règle de décision** |
| --- | --- | --- |
| P1 | Indispensable MVP | Doit être livré pour considérer la chaîne produit conforme |
| P2 | Fortement souhaitable | Peut être livré si les fonctions P1 sont stables, sans bloquer la conformité MVP |
| P3 | Extension | Peut être reporté sans remettre en cause la conformité MVP |

# **7. Parties prenantes et utilisateurs**

## **7.1 Utilisateurs cibles**

| **Profil** | **Description** | **Besoins principaux** |
| --- | --- | --- |
| Administrateur | Responsable de la configuration minimale et des accès | Authentifier, gérer les roles, consulter l'état du système |
| Analyste | Chargé de l'investigation et de la qualification des alertes | Voir les actifs, événements, alertes, corrélations et exports |
| Responsable validation | Observe les scénarios de recette | Comprendre la chaîne fonctionnelle et vérifier les preuves |

## **7.2 Matrice des permissions MVP**

| **Fonction** | **admin** | **analyst** | **Non authentifié** | **Agent authentifié** |
| --- | --- | --- | --- | --- |
| Consulter le dashboard | Oui | Oui | Non | Non |
| Consulter actifs, événements, alertes | Oui | Oui | Non | Non |
| Qualifier une alerte ou changer son statut | Oui | Oui | Non | Non |
| Consulter les corrélations | Oui | Oui | Non | Non |
| Générer un export CSV/JSON | Oui | Oui | Non | Non |
| Consulter les journaux d'audit | Oui | Non | Non | Non |
| Administrer les utilisateurs ou roles | Oui | Non | Non | Non |
| Envoyer un heartbeat ou des events | Non | Non | Non | Oui |

# **8. Glossaire**

| **Terme** | **Définition** |
| --- | --- |
| Actif | Équipement, hôte ou ressource réseau observable par le système |
| Alerte | Signal produit par une règle de détection ou par une corrélation |
| Audit log | Journal retraçant une action sensible ou significative |
| Corrélation | Regroupement de plusieurs événements liés par une IP, une cible, une fenêtre temporelle ou un comportement |
| Event | Événement technique remonté par l'endpoint |
| Heartbeat | Signal périodique indiquant qu'un endpoint est actif |
| MVP | Minimum Viable Product — version minimale démontrable du produit |
| serveur-soc | Conteneur central : interface web, API, base, Redis et worker |
| serveur-endpoint | Conteneur représentant l'hôte supervisé |
| serveur-attacker | Conteneur générant des scénarios de test contrôlés |

# **9. Hypothèses et contraintes**

## **9.1 Hypothèses**

- Le projet est réalisé dans un cadre de validation produit avec une démonstration attendue

- L'environnement Docker constitue le périmètre officiel de démonstration

- Les scénarios offensifs restent contrôlés, non destructeurs et limités au réseau de lab

- Les exports CSV et JSON sont prioritaires ; XML reste une extension P3

## **9.2 Contraintes**

- Backend Python / FastAPI imposé

- Frontend web cohérent avec la démonstration

- Dépôt structuré et documenté, lab Docker reproductible

- Architecture défendable techniquement et cohérente avec les exigences de sécurité OWASP ASVS (adaptées MVP)

# **10. Exigences fonctionnelles**

## **10.1 Règles métier MVP**

| **ID** | **Règle** | **Description** | **Critère** |
| --- | --- | --- | --- |
| RM-001 | Auth utilisateur | Identifiant, mot de passe haché, role | Accès sans session refusé |
| RM-002 | Auth agent | Le serveur-endpoint présente un secret agent | Requête sans secret valide → erreur contrôlée |
| RM-003 | Scan borné | Découverte limitée au réseau Docker de lab configuré | Scan hors plage autorisée refusé |
| RM-004 | Détection scan de ports | ≥ 3 ports observés sur une même cible → alerte | Scénario contrôlé génère une alerte |
| RM-005 | Détection répétition | ≥ 3 événements similaires depuis une même IP dans une fenêtre configurable → corrélation | Groupe de corrélation créé |
| RM-006 | Fenêtre de corrélation | Fenêtre par défaut : 10 minutes pour le MVP | Événements hors fenêtre non regroupés |
| RM-007 | Statuts d'alerte | Statuts : new, in_review, closed | Statut visible et modifiable par utilisateur autorisé |
| RM-008 | Preuve exportable | Export contient données, date, format, identifiant | Fichier CSV/JSON permet de retrouver le scénario joué |
| RM-009 | Audit obligatoire | Connexion, export, changement de statut, action admin → entrée d'audit | Actions sensibles dans audit_logs |
| RM-010 | Scénarios offensifs contrôlés | serveur-attacker génère des comportements non destructeurs | Scénario documenté et limité au réseau Docker |

## **10.2 Authentification et contrôle d****'****accès**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-AUTH-001 | Authentification sécurisée des utilisateurs | P1 | Utilisateur valide accède au dashboard après connexion |
| F-AUTH-002 | Distinction des roles admin et analyst | P1 | Permissions différentes selon le role |
| F-AUTH-003 | Restriction des actions sensibles par role | P1 | Un analyste ne peut pas exécuter une action réservée à l'admin |

## **10.3 Collecte endpoint**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-TEL-001 | Le serveur-endpoint doit émettre un heartbeat | P1 | Dernier heartbeat visible côté serveur-soc |
| F-TEL-002 | Le serveur-endpoint doit remonter des événements | P1 | Events persistés et consultables |
| F-TEL-003 | Collecte de journaux utiles à la détection | P2 | Au moins une entrée de log transformée en événement exploitable |
| F-TEL-004 | Remontée d'indicateurs de comportements suspects | P1 | Scénario contrôlé produit un événement suspect |

## **10.4 Découverte réseau et actifs**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-DISC-001 | Scanner une plage IP définie dans le lab | P1 | Plage IP configurée analysée |
| F-DISC-002 | Identifier des équipements observables | P1 | Au moins un actif créé ou mis à jour |
| F-DISC-003 | Détecter les ports ouverts | P1 | Ports détectés associés à un actif |
| F-DISC-004 | Récupérer des informations de services | P2 | Services observés dans le détail d'un actif |
| F-ASSET-001 | Maintenir un inventaire d'actifs | P1 | Interface affiche les actifs connus |

## **10.5 Détection et alerting**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-ALERT-001 | Produire des alertes issues de règles simples | P1 | Événement suspect génère une alerte |
| F-ALERT-002 | Vue de liste des alertes | P1 | Alertes consultables dans l'interface |
| F-ALERT-003 | Vue de détail d'une alerte | P1 | Alerte affiche contexte, source et horodatage |
| F-ALERT-004 | Cycle de vie minimal des alertes | P1 | Alerte peut changer de statut ou être qualifiée |

## **10.6 Corrélation**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-COR-001 | Corréler plusieurs événements d'une même IP | P1 | Plusieurs événements regroupés dans une corrélation |
| F-COR-002 | Corréler des répétitions dans une fenêtre temporelle | P2 | Répétition produit un groupe de corrélation |
| F-COR-003 | Associer une corrélation à une ou plusieurs alertes | P2 | Alerte enrichie référence un groupe de corrélation |
| F-COR-004 | Afficher les corrélations dans l'interface | P1 | Analyste consulte les corrélations détectées |

## **10.7 Interface web**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-UI-001 | Dashboard de synthèse | P1 | Dashboard affiche des métriques utiles à la démonstration |
| F-UI-002 | Consultation des actifs | P1 | Liste et détail des actifs accessibles |
| F-UI-003 | Consultation des événements | P1 | Événements collectés visibles |
| F-UI-004 | Consultation des alertes | P1 | Alertes générées visibles |
| F-UI-005 | Consultation des journaux d'audit | P2 | Actions sensibles journalisées consultables |
| F-UI-006 | Carte géographique des attaques | P3 | Vue géographique si enrichissement réalisé |

## **10.8 Reporting et exports**

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| F-EXP-001 | Produire un export CSV | P1 | Fichier CSV généré avec colonnes obligatoires |
| F-EXP-002 | Produire un export JSON | P1 | Fichier JSON généré avec métadonnées obligatoires |
| F-EXP-003 | Export XML (extension P3) | P3 | Export XML disponible sans remplacer CSV/JSON |
| F-EXP-004 | Exports utilisables comme preuve opérationnelle | P1 | Export contient des données cohérentes avec le scénario joué |

# **11. Exigences non fonctionnelles**

| **ID** | **Catégorie** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- | --- |
| NF-QUAL-001 | Qualité | Code structuré par domaines fonctionnels | P1 | Structure suit les modules définis dans l'architecture |
| NF-QUAL-002 | Qualité | Données d'entrée validées | P1 | Payload invalide rejeté proprement |
| NF-PERF-001 | Performance | Parcours de démonstration fluides | P1 | Dashboard répond en < 2 s sur jeu de données MVP |
| NF-PERF-002 | Performance | Traitements lourds différés | P2 | Tâches de détection ou d'export passent par Redis/Celery |
| NF-PERF-003 | Performance | Export compatible démonstration | P1 | Export de 100 lignes généré en < 5 s |
| NF-OBS-001 | Observabilité | Endpoint de santé exposé | P1 | GET /health retourne statut API et worker |
| NF-DEP-001 | Déployabilité | Projet lançable dans Docker reproductible | P1 | Les 3 conteneurs démarrent sur une commande documentée |
| NF-TEST-001 | Testabilité | Chaque exigence P1 reliée à au moins un scénario de recette | P1 | Matrice de traçabilité couvre les P1 |

# **12. Exigences de sécurité**

Les exigences de sécurité s'inspirent des bonnes pratiques OWASP ASVS, adaptées au niveau MVP du projet.

| **ID** | **Exigence** | **Priorité** | **Critère d****'****acceptation** |
| --- | --- | --- | --- |
| SEC-001 | L'accès à l'interface doit nécessiter une authentification | P1 | Page protégée inaccessible sans session valide |
| SEC-002 | Actions sensibles contrôlées par role | P1 | Un analyst ne peut pas effectuer une action réservée à admin |
| SEC-003 | Routes d'ingestion agent séparées des routes utilisateur | P1 | Endpoints agent identifiables et isolés fonctionnellement |
| SEC-004 | Le serveur-endpoint doit s'authentifier auprès de l'API | P1 | Requête agent non autorisée refusée |
| SEC-005 | Payloads entrants validés strictement | P1 | Payload mal formé produit une erreur contrôlée |
| SEC-006 | Secrets non exposés dans le dépôt | P1 | Aucun secret réel versionné |
| SEC-007 | Actions sensibles produisent une entrée d'audit | P1 | Connexions, exports et actions admin tracés |
| SEC-008 | Scénarios offensifs bornés au lab Docker | P1 | Aucun test ne cible un réseau externe au lab |
| SEC-009 | Exports accessibles uniquement à des utilisateurs autorisés | P1 | Utilisateur non autorisé ne peut pas générer ou consulter un export |

# **13. Données manipulées**

| **Donnée** | **Description** | **Source** | **Sensibilité** |
| --- | --- | --- | --- |
| users | Comptes utilisateurs | Interface / initialisation | Élevée |
| assets | Actifs réseau observés | Découverte réseau / événements | Moyenne |
| events | Événements remontés par endpoint | serveur-endpoint | Moyenne |
| network_findings | Résultats de scan et observation réseau | Module découverte | Moyenne |
| alerts | Alertes générées par règles ou corrélations | Backend / worker | Moyenne |
| correlation_groups | Groupes d'événements liés | Worker de corrélation | Moyenne |
| attacker_profiles | Profils d'IP ou sources attaquantes | Corrélation / enrichissement | Moyenne |
| audit_logs | Traces d'actions sensibles | API | Élevée |
| exports | Fichiers ou métadonnées d'exports | Module reporting | Moyenne |

## **13.1 Champs minimaux attendus**

| **Entité** | **Champs minimaux MVP** |
| --- | --- |
| users | id, username, password_hash, role, created_at, last_login_at, is_active |
| assets | id, ip_address, hostname, first_seen_at, last_seen_at, status |
| events | id, source_ip, target_ip, event_type, severity, message, raw_payload, created_at, asset_id |
| alerts | id, title, severity, status, source_ip, target_ip, description, created_at, updated_at |
| correlation_groups | id, correlation_type, source_ip, window_start, window_end, event_count, created_at |
| audit_logs | id, user_id, role, action, target_type, target_id, result, created_at |
| exports | id, format, requested_by, scope, file_path, created_at, row_count |

# **14. Interfaces, API et flux**

## **14.1 Flux principaux**

| **Flux** | **Source** | **Destination** | **Description** |
| --- | --- | --- | --- |
| FLUX-001 | serveur-endpoint | serveur-soc | Envoi de heartbeat |
| FLUX-002 | serveur-endpoint | serveur-soc | Envoi d'événements et observations |
| FLUX-003 | Interface web | API FastAPI | Consultation actifs, événements, alertes, exports |
| FLUX-004 | API FastAPI | PostgreSQL | Persistance et lecture des données |
| FLUX-005 | API FastAPI | Redis / Celery | Planification de traitements différés |
| FLUX-006 | Celery Worker | PostgreSQL | Création ou mise à jour d'alertes, corrélations, exports |

## **14.2 Contrat API MVP**

| **Méthode** | **Endpoint** | **Usage** | **Accès** | **Priorité** |
| --- | --- | --- | --- | --- |
| POST | /auth/login | Authentification utilisateur | Public | P1 |
| GET | /auth/me | Informations utilisateur courant | admin, analyst | P1 |
| GET | /health | Santé applicative | Public | P1 |
| POST | /telemetry/heartbeat | Réception heartbeat endpoint | Agent authentifié | P1 |
| POST | /telemetry/events | Réception événements endpoint | Agent authentifié | P1 |
| GET | /assets | Liste des actifs | admin, analyst | P1 |
| GET | /assets/{id} | Détail d'un actif | admin, analyst | P1 |
| GET | /events | Liste des événements | admin, analyst | P1 |
| GET | /alerts | Liste des alertes | admin, analyst | P1 |
| GET | /alerts/{id} | Détail d'une alerte | admin, analyst | P1 |
| PATCH | /alerts/{id} | Qualification ou changement de statut | admin, analyst | P2 |
| GET | /correlations | Liste des corrélations | admin, analyst | P1 |
| POST | /exports | Génération d'un export CSV/JSON | admin, analyst | P1 |
| GET | /audit-logs | Consultation des journaux d'audit | admin | P2 |

# **15. Architecture de démonstration retenue**

L'environnement de démonstration comporte trois conteneurs : serveur-soc, serveur-endpoint et serveur-attacker.

Le serveur-soc embarque pour le MVP : frontend web, backend FastAPI, PostgreSQL, Redis et Celery. Cette architecture compacte est retenue pour faciliter le lancement, la validation et la reproductibilité de la démonstration.

## **15.1 Conditions minimales de lancement**

| **Élément** | **Condition attendue** |
| --- | --- |
| Réseau Docker | Un réseau dédié au lab, par exemple wazash_net |
| serveur-soc | Interface web, API, PostgreSQL, Redis et worker disponibles |
| serveur-endpoint | Agent démarré, authentifié et capable d'envoyer un heartbeat |
| serveur-attacker | Scénario contrôlé disponible sans charge destructive |
| Santé applicative | GET /health vérifie au minimum API, base de données et worker |
| Données de démonstration | Un compte admin, un compte analyst et un scénario de test reproductible |

# **16. Scénarios de recette**

## **16.1 Critères d****'****acceptation globaux**

Le produit sera considéré comme conforme si les points suivants sont démontrés :

- Un endpoint remonte correctement heartbeat et events

- Le système détecte des actifs, ports ou services

- Des comportements suspects sont observés depuis le serveur-endpoint

- Des alertes sont générées

- Au moins une logique de corrélation fonctionne

- L'interface permet la consultation des données clés

- Un export exploitable est produit

- La démonstration fonctionne dans le lab Docker prévu

## **16.2 Scénarios de recette**

| **ID** | **Scénario** | **Résultat attendu** | **Preuve attendue** |
| --- | --- | --- | --- |
| REC-001 | Connexion utilisateur | Connexion valide acceptée, accès sans session refusé | Capture dashboard, réponse de refus, entrée audit_logs |
| REC-002 | Contrôle des permissions | Accès refusé pour analyst, accès autorisé pour admin | Réponse API ou capture interface |
| REC-003 | Heartbeat endpoint | Heartbeat reçu, horodaté, persisté et visible côté serveur-soc | Vue interface, ligne PostgreSQL ou log applicatif |
| REC-004 | Rejet agent non autorisé | Requête refusée proprement, aucune donnée persistée | Réponse d'erreur contrôlée et log applicatif |
| REC-005 | Découverte réseau bornée | Actif, port ou service détecté sans sortir du réseau autorisé | Vue actif, résultat de scan, configuration Docker |
| REC-006 | Détection suspecte | Événement suspect puis alerte créée | Vue alerte, événement source, log worker |
| REC-007 | Corrélation IP source | Groupe de corrélation créé avec event_count >= 3 | Vue corrélation ou ligne correlation_groups |
| REC-008 | Cycle de vie alerte | Statut mis à jour (new → in_review → closed) et action auditée | Vue alerte et entrée audit_logs |
| REC-009 | Export preuve CSV/JSON | Fichier généré avec métadonnées et données cohérentes | Fichier exporté et entrée audit_logs |
| REC-010 | Santé et reproductibilité Docker | API, base, worker et agent opérationnels | Sortie Docker, réponse /health, démonstration complète |
| REC-011 | Démonstration complète | Chaîne complète visible et explicable | Captures, logs, export CSV/JSON, support de validation |

# **17. Priorisation**

## **Priorité 1 — Indispensable**

- Authentification

- Collecte endpoint

- Découverte réseau minimale

- Alertes

- Corrélation minimale par IP source

- Historique

- Audit minimal

- Export CSV et JSON

- Démonstration Docker

## **Priorité 2 — Fortement souhaitable**

- Corrélation par fenêtre temporelle et enrichissement avancé

- Métriques SOC

- Consultation des journaux d'audit

- Visualisation des IP attaquantes

## **Priorité 3 — Extension si temps disponible**

- Export XML

- Enrichissement géographique

- Corrélation plus poussée

- Raffinements visuels supplémentaires

# **18. Matrice de traçabilité**

| **Besoin initial** | **Exigences associées** | **Recette** | **Preuve attendue** |
| --- | --- | --- | --- |
| Sécuriser l'accès | F-AUTH-001, F-AUTH-002, F-AUTH-003, SEC-001, SEC-002 | REC-001, REC-002 | Test connexion, refus d'accès, audit log |
| Collecter la télémétrie endpoint | F-TEL-001, F-TEL-002, SEC-004 | REC-003, REC-004 | Heartbeat, event persisté, rejet agent invalide |
| Identifier les équipements réseau | F-DISC-001, F-DISC-002, F-ASSET-001 | REC-005 | Vue actifs, résultat de scan, base PostgreSQL |
| Détecter des comportements suspects | F-ALERT-001, F-ALERT-002, F-ALERT-003 | REC-006 | Vue alerte, événement source, log worker |
| Comprendre les répétitions | F-COR-001, F-COR-002, F-COR-004 | REC-007 | Vue corrélation, groupe correlation_groups |
| Qualifier les alertes | F-ALERT-004, F-AUD-003 | REC-008 | Statut alerte et audit log |
| Produire des preuves | F-EXP-001, F-EXP-002, F-EXP-004, F-AUD-002 | REC-009 | Fichier CSV/JSON, métadonnées export, audit log |
| Démontrer le produit | NF-DEP-001, NF-DEP-002, SEC-008 | REC-010, REC-011 | Lab Docker, /health, chaîne complète |

# **19. Livrables attendus**

| **Livrable** | **Description** | **Critère de validation** |
| --- | --- | --- |
| Application Wazash MVP | Application web de supervision cyber | Chaîne fonctionnelle démontrable |
| Lab Docker | Environnement serveur-soc, serveur-endpoint, serveur-attacker | Démarrage reproductible |
| Documentation technique | Instructions et architecture | Cohérente avec les documents de gestion de projet et d'architecture |
| Exports de preuve | Fichiers CSV ou JSON | Exploitables en revue produit |
| Support de présentation | Support produit structuré | Clair, structuré, défendable |
| Dépôt GitHub | Code, documentation et historique | Dépôt propre et traçable |

# **20. Conclusion**

Ce cahier des charges fixe un périmètre clair, vérifiable et cohérent avec le positionnement produit, la gestion de projet et l'architecture retenue. Il constitue la base opérationnelle du développement de Wazash.

Il relie explicitement le besoin initial, la conception technique, la démonstration et les preuves attendues en validation produit, au moyen d'exigences numérotées, de critères d'acceptation, d'une matrice de permissions, de règles métier, de contrats API, de formats de données, d'une matrice de traçabilité, de scénarios de recette et d'exigences de sécurité adaptées au contexte cyber.

Page
