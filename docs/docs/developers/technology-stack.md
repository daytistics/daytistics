# Technology Stack

## 🎨 Frontend

Our frontend is built with TypeScript and Nuxt. We use Tailwind CSS and it's plugin Flowbite for styling. For the visualization of the data, we use Chart.js. Our JavaScript runtime is Bun.

## 💻 Backend

Our backend is built in Python with the Django framework. To provide a powerful REST API we use Django Ninja. The database is managed by PostgreSQL. We will use a large language model from a cloud provider but we are still in the process of deciding which one to use. Our Python packages are managed by Poetry.

## 📄 Documentation

Our documentation is written in Markdown and hosted on GitHub Pages. We use MkDocs to generate the documentation. 

## 🚀 Deployment

Our deployment process is managed by GitHub Actions. We use Docker to containerize our application (we use Lando during development). Our application is hosted on a kernel-based virtual machine from AitchSystems.

## 🖨️ Infrastructure

The majority of our infrastructure is hosted on a kernel-based virtual machine from AitchSystems. As a cheap alternative to Heroku, we use a self-hosted Coolify instance to host our services. Our Llama 3 8B LLM model is hosted on a separate server from Groq. Our domain and email are also managed by AitchSystems.

### 💸 Expenses

| Service                      | Costs       |
| ---------------------------- | ----------- |
| Kernel-based Virtual Machine | ≈25/month   |
| Webspace                     | ≈2€/month   |
| Domain                       | ≈2€/month   |
| LLM                          | ≈100€/month |
| **Total**                    | ≈130€/month |
