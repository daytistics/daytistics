# Technologies

This document covers the technologies (infrastructure, tech- and toolstack) which is used by us to ensure maximal availability, scalability and rapid development.

## Techstack

- **Frontend**: Alpine.js, HTMX & Tailwind CSS
- **Backend**: Django (Core-Service) & FastAPI (Modeler-Service)
- **Database**: PostgreSQL (Production); SQLite for development
- **AI-Integration**: ChatGPT & Scikit-Learn
- **Visualization**: Plotly-Dash

> **Why do we use Django and FastAPI?** We want to benefit from both the incredibly fast development time with Django for our core service and the incredible performance of FastAPI for our modeler service.

## Toolstack

- **Version control**: Git(hub)
- **CI/CD**: Github Actions
- **Containerization**: Docker
- **Documentation**: MKDocs
- **LLM (€20/month)**: ChatGPT

## Infrastructure

> Hosted by [**Scaleway**](https://www.scaleway.com/en/) in the Paris 1 data center.

- **Webserver (€23.04/month)**: DEV1-M, 3 vCPUs, 4 GB RAM, 50 GB Storage
- **ML-Server (€21.87/month)**: DEV1-M, 3 vCPUs, 4 GB RAM, 10 GB Storage
- **Block-Storage (€8.496/month)**: Block Storage SSD, 100 GB Storage
- **Database (€79.20/month)**: Cost-optimized DB-PRO2-XXS, 2 vCPUs, 8 GB RAM
- **Documentation (free)**: Github Pages

Overall, this calculation results in a total monthly amount of around **€153**. That doesn't sound like much, but please keep in mind that Daytistics is a non-profit project. If you would like to [support us](https://patreon.com/daytistics), we would be very grateful. We are also open to partnerships with hosting providers (<partnership@daytistics.com>).
