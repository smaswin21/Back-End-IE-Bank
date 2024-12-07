# Infrastructure Architecture

This section outlines the cloud infrastructure design for the IE Bank system, highlighting the Azure services used, modular infrastructure as code (IaC) approach, and environment-specific configurations.

---

## Overview of Azure Services
### 1 GitHub
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


### 2 App Service for Containers
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


### 3 App Service Plan
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


### 4 PostgreSQL Database
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


### 5 Static Website
- **Purpose**:
  - Hosts the Vue.js + HTML frontend as a static website in **Azure Static Web Apps**.

- **Key Features**:
  1. **Global Content Delivery**:
     - Azure’s built-in Content Delivery Network (CDN) ensures fast loading times globally.
  2. **Scalability**:
     - Handles high traffic volumes without performance degradation.
  3. **Ease of Integration**:
     - Directly integrates with GitHub for seamless deployment via GitHub Actions.


### 6 Azure Container Registry (ACR)
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


### 7 Azure Key Vault
- **Purpose**:
  - Centralizes secrets management for all sensitive information across the application.

- **Key Features**:
  1. **Secret Management**:
     - Stores connection strings for the PostgreSQL database and Azure Container Registry credentials.
  2. **Access Control**:
     - Uses role-based access control (RBAC) to restrict secret access.
  3. **Integration**:
     - Integrated with App Services to dynamically inject configurations into the environment variables.


### 8 Log Analytics Workspace
- **Purpose**:
  - Provides centralized logging and monitoring for all containerized workloads.

- **Key Features**:
  1. **Log Aggregation**:
     - Consolidates logs from App Service instances and Docker containers.
  2. **Search and Analysis**:
     - Advanced querying of logs for debugging and performance analysis.
  3. **Alerts**:
     - Configurable alerts for failures or anomalies in container behavior.


### 9 Application Insights
- **Purpose**:
  - Delivers in-depth performance and usage insights for the application.

- **Key Features**:
  1. **KPI Monitoring**:
     - Tracks metrics like user sign-ups, session durations, and API performance.
  2. **Error Reporting**:
     - Identifies bottlenecks or issues in backend API response times.
  3. **Dashboards**:
     - Provides visualized data for operational decision-making.


### 10 Workbook

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

## Modular Infrastructure as Code (IaC)

Our infrastructure is defined and managed using **Infrastructure as Code (IaC)** principles, leveraging **Azure Bicep** templates for declarative resource provisioning. The modular approach enhances reusability, maintainability, and clarity across all environments.


### Modularization Strategy

Modularity is key to designing infrastructure code that is scalable and easy to manage. Each module represents an Azure service, encapsulating its configuration and deployment logic. 

#### Goals of Modularization:
- **Maintainability**: Isolate components for easier updates and debugging.
- **Reusability**: Enable modules to be reused across environments and projects.
- **Scalability**: Allow new modules to be added without impacting existing ones.
- **Testability**: Simplify testing by isolating modules.
- **Flexibility**: Allow easy swapping of modules with the same interface.

#### Directory Structure

The infrastructure is broken into logical components, with each module in its respective directory:

- **`modules/`**: The root directory for modular templates.
  - **`applications/`**: Modules for application services (e.g., App Services for backend and frontend).
  - **`databases/`**: Modules for deploying PostgreSQL resources.
  - **`infrastructure/`**: Shared modules for Key Vault, Log Analytics, and Application Insights.
- **`main.bicep`**: Orchestrates the deployment of all modules using input parameters.



### Benefits of Modularization

1. **Maintainability**: Centralized changes in modules without affecting the overall infrastructure.
2. **Reusability**: Modules are shared across environments, saving effort.
3. **Scalability**: Easy addition of services to support new features.
4. **Testability**: Isolated modules allow for focused testing and validation.
5. **Flexibility**: Swappable components with the same interface ensure seamless integration.



### Resource Dependency Graph

The following diagram illustrates the dependencies between modules:

![Resource Dependency Graph](https://github.com/user-attachments/assets/92a9b070-910e-45c5-9441-1105de680d01)



### Example Modules

#### Applications Modules

1. **App Service Plan Module**:
   - **File**: `app-service-plan.bicep`
   - Deploys an App Service Plan.
   - Parameters include:
     - `location`
     - `appServicePlanName`
     - `skuName`
   - Outputs include:
     - `id` (Resource ID).

2. **Backend App Service Module**:
   - **File**: `backend-app-service.bicep`
   - Deploys the backend in a Docker container.
   - Parameters include:
     - `appServicePlanId`
     - `dockerRegistryCredentials`
     - `appSettings` for environment variables.

3. **Frontend Static Web App Module**:
   - **File**: `frontend-app-service.bicep`
   - Deploys the frontend Static Web App.
   - Parameters include:
     - `name` (Static Web App name)
     - `sku` (tier).

#### Database Modules

1. **PostgreSQL Flexible Server Module**:
   - **File**: `postgres-sql-server.bicep`
   - Deploys a PostgreSQL server.
   - Includes parameters for SKUs, locations, and access control.

2. **Database Deployment Module**:
   - **File**: `postgres-sql-database.bicep`
   - Creates a PostgreSQL database within an existing server.



### Parameterization

Each environment (Development, UAT, Production) is defined using environment-specific JSON parameter files. These files include:
- Resource names.
- Locations.
- SKUs and configurations.



---

## Environment Design and Configuration

The IE Bank system employs a **DTAP (Development, Test, Acceptance, Production)** environment structure, ensuring a seamless progression from development to production with minimal risks. Each environment is tailored to specific needs, balancing cost, performance, and security.


### Environment Specifications

| **Environment**     | **Purpose**                                                                                      | **Key Features**                                                                                                                                                      | **Cost Optimization**                                                                                                                |
|----------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Development (Dev)** | Provides a sandbox for developers to experiment, learn, and validate changes.                         | - Automated provisioning via GitHub Actions.  <br>- Cost-efficient SKUs for resources.<br>- Wider access for experimentation.<br>- Logs aggregated in Log Analytics. | - Uses low-tier SKUs for services.<br>- Minimal instance count for compute resources.                                               |
| **UAT**             | Mirrors the production environment for testing by stakeholders and business users.                      | - Production-parity configuration.<br>- Controlled deployments initiated via pull requests.<br>- Limited stakeholder access for validation.<br>- SLA monitoring.    | - Balanced cost-performance ratio with mid-tier SKUs.<br>- Retains enough resources to mimic production behavior.                   |
| **Production (Prod)**| The live environment hosting the application for end users.                                      | - High availability with redundancy.<br>- Robust monitoring with Application Insights.<br>- Strict access controls.<br>- SLA: 99% uptime.<br>- Optimized scaling.   | - Scaled to handle expected load.<br>- Reserved instances where possible to reduce long-term costs.                                  |



### Resource Configurations Per Environment

1. **Azure App Service for Containers**
   - **Development**: Low-tier (B1) App Service Plan.
   - **UAT**: Standard-tier App Service Plan for performance testing.
   - **Production**: Premium-tier App Service Plan with auto-scaling for high availability.

2. **Azure PostgreSQL Database**
   - **Development**: Single-server instance with basic configuration.
   - **UAT**: Replicates production settings for realistic testing.
   - **Production**: High-availability configuration with geo-redundancy and backups.

3. **Azure Static Web Apps**
   - **Development**: Free-tier for basic functionality testing.
   - **UAT**: Standard-tier for parity with production.
   - **Production**: Standard-tier with global CDN for optimized delivery.

4. **Azure Key Vault**
   - Centralized secrets management across all environments.
   - Role-based access configured for resource-specific secrets.

5. **Azure Container Registry**
   - Shared across all environments for efficient image management.
   - Admin credentials stored securely in Azure Key Vault.

6. **Monitoring and Alerts**
   - **Development**: Basic logs in Log Analytics.
   - **UAT & Production**: Application Insights with SLO-specific dashboards and alerts.



### Details Per Environment

#### **Development Environment**
- **Purpose**: A sandbox for developers to experiment, learn, and validate changes.
- **Resource Configuration**:
  - App Service: Basic-tier (B1) for low-cost experimentation.
  - PostgreSQL Database: Basic configuration with minimal capacity.
  - Static Web Apps: Free-tier hosting for frontend testing.
  - Monitoring: Basic logging via Log Analytics.
  - Key Vault: Stores development-specific secrets for database and services.
- **Cost Optimization**:
  - Minimal instances for compute resources.
  - Use of shared resources to reduce costs.

#### **UAT Environment**
- **Purpose**: A pre-production environment for integration testing and stakeholder validation.
- **Resource Configuration**:
  - App Service: Standard-tier to match production configurations.
  - PostgreSQL Database: Standard capacity with production-like performance.
  - Static Web Apps: Standard-tier for frontend parity with production.
  - Monitoring: Application Insights integrated for SLO monitoring.
  - Key Vault: Securely manages secrets for UAT configurations.
- **Key Features**:
  - Production-parity configuration for realistic testing.
  - Stakeholder access is limited to ensure controlled validation.
- **Cost Optimization**:
  - Balanced performance-cost ratio with mid-tier SKUs.
  - Resources scaled to mimic production without overprovisioning.

#### **Production Environment**
- **Purpose**: The live environment hosting the application for end-users.
- **Resource Configuration**:
  - App Service: Premium-tier for high availability and scalability.
  - PostgreSQL Database: Geo-redundant configuration for disaster recovery.
  - Static Web Apps: Standard-tier with Azure CDN for optimized delivery.
  - Monitoring: Application Insights for real-time telemetry and issue tracking.
  - Key Vault: Manages critical secrets with strict RBAC policies.
- **Key Features**:
  - Auto-scaling and redundancy for handling peak traffic.
  - Strict access controls to ensure data and application security.
  - SLA-backed uptime of 99% or higher.
- **Cost Optimization**:
  - Reserved instances for long-term cost efficiency.
  - Resources provisioned to handle expected loads without excess.

---

## Security and Monitoring

### GitHub Advanced Security

#### GitHub Secret Scanning
GitHub Secret Scanning was configured across repositories to detect and prevent the accidental inclusion of sensitive data such as API keys, tokens, and passwords in the codebase. This scanning tool alerts developers to potential exposures, enabling immediate remediation and reducing the risk of compromised credentials.

#### Protected Main Branches
To secure the main branches, branch protection rules were implemented. We required a pull request before merging, enforced code review approval, and mandated a linear commit history. This configuration was applied across all main branches to maintain code integrity.

#### CodeQL for Code Scanning
CodeQL was integrated as a semantic code analysis tool to detect vulnerabilities in both the frontend (Vue.js) and backend (Python). The tool systematically scans for potential security flaws and logical errors, providing insights into code safety while facilitating secure development practices.

#### OSSF Scorecard
The OSSF Scorecard was utilized to evaluate the security posture of workflows and repositories. This tool provided a detailed analysis of security practices, including checks on code reviews, dependency management, and CI/CD configurations, enabling the team to identify and address areas for improvement.

#### Dependabot
To automate dependency updates and maintain up-to-date packages, Dependabot was activated. It automatically generates pull requests for updates to dependencies, mitigating risks posed by outdated or vulnerable libraries. Alongside this, dependency reviews were set up to analyze changes and assess their security implications during the pull request process.

#### Dependency Reviews
Dependency reviews were set up to analyze changes and assess their security implications during the pull request process. This ensured unwanted dependencies were identified and addressed before merging.

#### CODEOWNERS
The CODEOWNERS file was configured in each repository to establish clear ownership of code sections. This ensures that changes to critical areas of the codebase are reviewed by designated experts, maintaining accountability and adherence to security standards.



### Secure Secrets Management

#### Key Vault
For robust secrets management, Azure Key Vault was integrated into the infrastructure to securely store credentials such as API keys, container registry tokens, and PostgreSQL server passwords. This approach centralizes sensitive information, encrypts it, and provides fine-grained access control to authorized entities only.

#### Managed Identity
We also leveraged Managed Identities to eliminate the need for hard-coded credentials. By granting applications and services secure, temporary access to resources, this solution enhances security while simplifying credential management.



### Security Frameworks

#### OpenSSF

##### Regex for Input Validation
To enhance security through the OpenSSF framework, we implemented regex-based input validation across our applications. This measure enforces strict formatting rules for data inputs, preventing malicious injections such as SQL, XML, or script-based attacks.

##### Npm Best Practices
As part of OpenSSF guidelines, we adopted npm best practices to secure the management of frontend dependencies. This included locking dependency versions, running regular vulnerability scans with Dependabot, and removing unused packages to minimize the attack surface.

##### Evaluating Open Source Software
We implemented a structured process for evaluating open-source software to minimize risks from third-party dependencies. This included assessing project activity levels, reviewing contributor trustworthiness, and checking for regular updates or responses to reported vulnerabilities.

##### Source Code Management Platform Configuration
To align with OpenSSF practices, we fortified our source code management platform with robust configuration settings. Repository access was restricted based on roles, branch protection rules were enforced, and detailed audit logs were maintained.

#### SAFECode

##### Standardize Identity and Access Management
Under SAFECode principles, we standardized identity and access management practices to ensure secure and consistent access control. By implementing role-based access control (RBAC), we enforced the principle of least privilege, granting users only the permissions necessary for their roles.

##### Establish Log Requirements and Audit Practices
Logging and auditing requirements were defined to track system activities comprehensively. Logs included information on user actions, authentication attempts, and system changes.

##### Establish Coding Standards and Conventions
SAFECode principles guided the creation of coding standards and conventions that prioritized security. These standards mandated secure patterns for error handling, input sanitization, and encryption.

##### Use Code Analysis Tools to Find Security Vulnerabilities
We integrated CodeQL into our project to quickly identify security vulnerabilities. This tool is further complemented by third-party audits, allowing us to enhance our security posture continuously.

##### Handle Errors
Error handling practices were established to ensure sensitive information was not exposed through system-generated messages. Errors were logged for internal debugging but raised as generic messages to end-users.



### Monitoring and Alerting

#### Application Insights
- **Purpose**: Monitors application performance, availability, and user behavior.
- **Features**:
  - Collects telemetry data from applications.
  - Configured with alert rules for critical metrics.
  - Integrated with Logic Apps for alert notifications.

#### Alert Rules
- **Login Response Time Alert**:
  - **Name**: `Login-SLO-Alert`
  - **Description**: Triggers when login response time exceeds 5 seconds.
  - **Severity**: 2
  - **Action**: Sends an alert via the Logic App to Slack.

- **Page Load Time Alert**:
  - **Name**: `Page-Load-Time-Alert`
  - **Description**: Triggers when page load time exceeds 5 seconds.
  - **Severity**: 4
  - **Action**: Sends an alert via the Logic App to Slack.

