## 6. Infrastructure Architecture

This section outlines the cloud infrastructure design for the IE Bank system, highlighting the Azure services used, modular infrastructure as code (IaC) approach, and environment-specific configurations.

---

### 6.1 Overview of Azure Services
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


## 2.10 Workbook

- **Purpose**:
  - Provides real-time visualization of key application metrics and logs for enhanced monitoring and insights.

- **Key Features**:
  1. **Custom Dashboards**:
     - Enables teams to create tailored visualizations for specific metrics such as API performance, database queries, and user activities.
  2. **Integration**:
     - Connects seamlessly with **Log Analytics Workspace** for data aggregation and analysis.
  3. **Collaboration**:
     - Shared with stakeholders for better decision-making during operations and sprint reviews.


---

### 6.2 Modular Infrastructure as Code (IaC)
<!-- Describe how IaC is implemented using tools like Azure Bicep -->

---

### 6.3 Environment Design and Configuration
#### Development Environment
<!-- Details about the Development environment -->
#### UAT Environment
<!-- Details about the UAT environment -->
#### Production Environment
<!-- Details about the Production environment -->

---

### 6.4 Security and Monitoring
#### Security
<!-- Include details on secure credential management and access control -->
#### Monitoring
<!-- Describe the monitoring tools and strategies implemented -->
