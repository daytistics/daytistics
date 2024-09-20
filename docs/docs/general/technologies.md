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

> Hosted by [**Hetzner**](https://www.hetzner.com/cloud) and .

- **Frontend (€4.51/month)**: CX22 (2 vCPUs, 4 GB RAM, 40 GB Storage)
- **Backend (€8.09/month)**: CX32 (4 vCPUs, 8 GB RAM, 80 GB Storage)
- **ML-API (€19.52/month)**: CX42 (8 vCPUs, 16 GB RAM, 160 GB Storage)
- **Webspace (€2.09/month)**: Webspace Level 1 (1 TB Storage)
- **SupaBase (€33.15/month)**: Pro Level
    - **PostgreSQL**: 48 GB Storage
    - **Storage**: 250 GB Storage
- **Documentation (free)**: Github Pages

Overall, this calculation results in a total monthly amount of around **68 €**. That doesn't sound like much, but please keep in mind that Daytistics is a non-profit project. If you would like to [support us](https://patreon.com/daytistics), we would be very grateful. We are also open to partnerships with hosting providers (<partnership@daytistics.com>).
