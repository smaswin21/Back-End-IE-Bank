# Cloud Architect Documentation

# IE Bank System Requirements & Design Document

---

## Introduction

This document outlines the requirements and architecture design for the IE Bank System, including new requirements and a testing strategy. The document supports collaboration by linking each requirement to user stories in Azure DevOps and to specific tests when relevant.

---

## 1. New Requirements

The IE Bank System has several functional and non-functional requirements that guide the development process. Each requirement is listed, numerated, and linked to relevant user stories in the backlog and associated tests.

### 1.1 Functional Requirements

1. **User Authentication**
   - **Requirement**: Secure login functionality for both users and administrators.
   - **User Story**: "As a user, I want to log in securely to protect my account information."
   - **Test Link**: [Authentication Tests](#tests)
   - **Azure DevOps Link**: [User Story in Azure DevOps](link)

2. **Bank Account Management**
   - **Requirement**: Ability for users to view account balances and transaction history.
   - **User Story**: "As a customer, I want to view my account balance so that I can monitor my spending."
   - **Test Link**: [Account Management Tests](#tests)
   - **Azure DevOps Link**: [User Story in Azure DevOps](link)

3. **Home Page Access**
   - **Requirement**: The web application must display a home page at the root URL.
   - **User Story**: "As a visitor, I want to see a home page when accessing the bank system’s root URL."
   - **Test Link**: [Home Page Tests](#tests)
   - **Azure DevOps Link**: [User Story in Azure DevOps](link)

4. **Country Field in Bank Accounts**
   - **Requirement**: Users must be able to add a “country” field when creating a new bank account.
   - **User Story**: "As an admin, I want to add a country field to bank accounts to collect location information."
   - **Test Link**: [Country Field Tests](#tests)
   - **Azure DevOps Link**: [User Story in Azure DevOps](link)

5. **Transaction Logging**
   - **Requirement**: Track and log each transaction for auditing purposes.
   - **User Story**: "As a customer, I want a record of my transactions to ensure accurate tracking."
   - **Test Link**: [Transaction Logging Tests](#tests)
   - **Azure DevOps Link**: [User Story in Azure DevOps](link)

### 1.2 Non-Functional Requirements

1. **Reliability**
   - **Requirement**: System availability should be 99.9%.
   - **User Story**: N/A (General reliability requirement).
   - **Test Link**: [Reliability Tests](#tests)
   - **Azure DevOps Link**: [Reliability Requirement](link)

2. **Security**
   - **Requirement**: All sensitive data must be encrypted and securely stored.
   - **User Story**: "As an administrator, I need data encryption to ensure user information remains confidential."
   - **Test Link**: [Security Tests](#tests)
   - **Azure DevOps Link**: [Security Requirement](link)

3. **Performance**
   - **Requirement**: The system should handle peak load times efficiently with minimal delay.
   - **User Story**: N/A (Performance expectation across all services).
   - **Test Link**: [Performance Tests](#tests)
   - **Azure DevOps Link**: [Performance Requirement](link)

4. **Cost Optimization**
   - **Requirement**: Resource allocation should be cost-effective, scaling only as necessary.
   - **User Story**: N/A (General non-functional requirement).
   - **Test Link**: [Cost Optimization Tests](#tests)
   - **Azure DevOps Link**: [Cost Optimization Requirement](link)

---

## 2. Architecture Design


### 2.1 GitHub
- **Purpose**:
  - Acts as the central repository for codebase management, versioning, and collaboration.
  - Hosts **Bicep files** for defining infrastructure as code (IaC) templates.
  - Automates the CI/CD pipeline for application deployment to different environments (DEV, UAT, PROD).

- **Key Features**:
  1. **Code Repository**:
     - Enables version control for application and infrastructure code.
     - Ensures collaboration and prevents conflicts via Git branching strategies.
  2. **GitHub Actions**:
     - Automates CI/CD workflows:
       - Push code to DEV upon feature branch completion.
       - Merge Pull Requests into UAT for testing.
       - Deploy tested code to PROD upon approval.
     - Hosts workflows for container image builds, tests, and deployments to Azure App Services.
  3. **Documentation Hosting**:
     - GitHub Pages serves as a platform for team collaboration and project documentation.
     - Contains the system design, API documentation, and architecture notes.


### 2.2 App Service for Containers
- **Purpose**:
  - Hosts the backend business logic implemented in Python/Flask within Docker containers.
  - Provides a scalable, serverless environment to run containerized applications.

- **Features**:
  1. **Containerized Deployment**:
     - Each Docker container encapsulates specific microservices for modularity.
     - App Service runs these containers while handling infrastructure provisioning.
  2. **Scalability**:
     - Auto-scale capabilities based on traffic spikes.
     - Adjustable CPU and memory limits to optimize costs and performance.
  3. **Pay-as-You-Go**:
     - Serverless model eliminates upfront costs, billing only for active usage.
  4. **Environment-Specific Configurations**:
     - Containers are deployed with settings (e.g., API keys, URLs) fetched dynamically from Azure Key Vault.


### 2.3 App Service Plan
- **Purpose**:
  - Governs the hosting resources for App Services.
  - Provides the underlying compute environment for the Dockerized backend.

- **Configurations**:
  1. **Region**: Select a European Azure region to minimize latency for European customers.
  2. **Scaling Plan**:
     - Define auto-scaling rules based on application load.
     - Opt for reserved instances for production to reduce long-term costs.
  3. **Fault Tolerance**:
     - High availability with multiple instances running across availability zones.


### 2.4 PostgreSQL Database
- **Purpose**:
  - Stores all customer and administrator account information securely.

- **Key Considerations**:
  1. **Managed Service**:
     - Fully managed by Azure, ensuring minimal administrative overhead.
  2. **Data Security**:
     - Enforce encryption at rest and in transit using Azure-provided security protocols.
     - Use Azure Key Vault for secure connection string management.
  3. **Redundancy and SLAs**:
     - Deploy with **geo-redundancy** for disaster recovery.
     - Ensure SLA-backed availability (e.g., 99.99% uptime).
  4. **Performance**:
     - Optimize for high read-write throughput to handle concurrent user queries.


### 2.5 Static Website
- **Purpose**:
  - Hosts the Vue.js + HTML frontend as a static website in **Azure Static Web Apps**.

- **Key Features**:
  1. **Global Content Delivery**:
     - Azure’s built-in Content Delivery Network (CDN) ensures fast loading times globally.
  2. **Scalability**:
     - Handles high traffic volumes without performance degradation.
  3. **Ease of Integration**:
     - Directly integrates with GitHub for seamless deployment via GitHub Actions.


### 2.6 Azure Container Registry (ACR)
- **Purpose**:
  - Manages versioned Docker images used by the App Service for Containers.

- **Key Features**:
  1. **Image Repository**:
     - Stores and organizes Docker container images for backend services.
  2. **CI/CD Integration**:
     - Automates image builds and pushes new versions using GitHub Actions.
     - Triggers App Service updates upon a new image being pushed.
  3. **Security**:
     - Employs Azure RBAC and Key Vault for secure access to the registry.


### 2.7 Azure Key Vault
- **Purpose**:
  - Centralizes secrets management for all sensitive information across the application.

- **Key Features**:
  1. **Secret Management**:
     - Stores connection strings for the PostgreSQL database and Azure Container Registry credentials.
  2. **Access Control**:
     - Uses role-based access control (RBAC) to restrict secret access.
  3. **Integration**:
     - Integrated with App Services to dynamically inject configurations into the environment variables.


### 2.8 Log Analytics Workspace
- **Purpose**:
  - Provides centralized logging and monitoring for all containerized workloads.

- **Key Features**:
  1. **Log Aggregation**:
     - Consolidates logs from App Service instances and Docker containers.
  2. **Search and Analysis**:
     - Advanced querying of logs for debugging and performance analysis.
  3. **Alerts**:
     - Configurable alerts for failures or anomalies in container behavior.


### 2.9 Application Insights
- **Purpose**:
  - Delivers in-depth performance and usage insights for the application.

- **Key Features**:
  1. **KPI Monitoring**:
     - Tracks metrics like user sign-ups, session durations, and API performance.
  2. **Error Reporting**:
     - Identifies bottlenecks or issues in backend API response times.
  3. **Dashboards**:
     - Provides visualized data for operational decision-making.


---

## 3. Environment Design

The project follows the DTAP (Development, Testing, Acceptance, Production) model to ensure robust development and testing processes.

Each environment is configured using Azure Bicep templates, with environment-specific parameters for consistency and security.

---

## 4. Well-Architected Framework

The architecture adheres to Azure’s Well-Architected Framework principles:

1. **Reliability**: Implemented with high-availability services like Azure App Service and PostgreSQL, including automated backups and redundancy.
2. **Security**: Data encryption, secrets management with Azure Key Vault, and role-based access control.
3. **Cost Optimization**: Efficient resource allocation and scaling options, avoiding over-provisioning.
4. **Operational Excellence**: CI/CD pipelines automate deployment, reducing manual errors and improving workflow.
5. **Performance Efficiency**: Global distribution for frontend, optimized backend service plans, and query tuning for databases.

---

## 5. Deployment and Automation Strategy

### 5.1 Frontend CI/CD
   - **Workflow**: GitHub Actions trigger builds and deploys for commits to specific branches.
   - **Environment Triggers**: Commits to development branches deploy to Dev, while main branch merges deploy to Production.

### 5.2 Backend CI/CD
   - **Workflow**: Docker images are built, scanned, and deployed to Azure App Service based on branch policies.
   - **Testing**: Integration tests are run on each build to validate deployments in UAT.

---

## 6. Testing

Each requirement has associated tests to ensure functionality and reliability. Tests are categorized based on the type of requirement they address.

### 6.1 Functional Tests

| Test Name                    | Description                                                      | Requirement                   |
|------------------------------|------------------------------------------------------------------|-------------------------------|
| Authentication Tests         | Verifies secure login and session management                    | User Authentication           |
| Account Management Tests     | Confirms account balance and transaction history functionality  | Bank Account Management       |
| Home Page Tests              | Checks that the home page loads correctly at the root URL       | Home Page Access              |
| Country Field Tests          | Verifies addition of "country" field in bank accounts           | Country Field in Bank Accounts|
| Transaction Logging Tests    | Ensures all transactions are logged for auditing               | Transaction Logging           |

### 6.2 Non-Functional Tests

| Test Name                    | Description                                                      | Requirement                   |
|------------------------------|------------------------------------------------------------------|-------------------------------|
| Reliability Tests            | Ensures 99.9% uptime in various scenarios                       | Reliability                   |
| Security Tests               | Verifies data encryption and access control                     | Security                      |
| Performance Tests            | Measures response times under peak load                         | Performance                   |
| Cost Optimization Tests      | Validates efficient use of resources and cost monitoring        | Cost Optimization             |

Each test is implemented and tracked in Azure DevOps to ensure coverage across both functional and non-functional requirements.

---

## 7. Backlog and User Stories

All requirements are broken down into user stories in the Azure DevOps backlog, where they are prioritized for development. This backlog includes links to individual work items, acceptance criteria, and progress tracking.

- **Azure DevOps Backlog Link**: [Azure DevOps Backlog](https://dev.azure.com/your-org/your-project/_backlogs)
