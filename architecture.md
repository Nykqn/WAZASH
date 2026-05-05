```
flowchart LR
    Attaquant["Attaquant<br/>Docker"]
    AdminSOC["Admin Sys / SOC"]
    EP1["Endpoints"]
    EP2["Endpoints"]

    subgraph Docker_Container
        Frontend["Frontend<br/>Bootstrap"]
        Backend["Backend<br/>FastAPI"]
        Postgres[("Postgres")]
        Celery["Celery<br/>Redis"]
    end

    Attaquant -..-> EP1
    EP1 -..-> Backend
    Backend -..-> EP2

    AdminSOC --> Frontend

    Frontend <--> Backend
    Backend --> Postgres
    Backend --> Celery
```
