# Software Architecture

This section details the software architecture of the IE Bank system, including its core design patterns, components, and flow.

---

# Azure Well-Architected Framework

## Reliability Pillar

The Reliability Pillar is critical to maintaining the availability and fault tolerance of the IE Bank application. This pillar ensures that the system can withstand failures, recover quickly, and continue to deliver services with minimal disruption to end users.

- **Redundancy and Failover**:  
  Key application components, such as the Azure PostgreSQL Database and backend App Services, were configured with redundancy to ensure continued operation in the event of hardware or software failures. Automatic failover mechanisms were implemented for the database, ensuring uninterrupted availability.

- **Monitoring for Downtime and Errors**:  
  Azure Monitor and Log Analytics were used to track availability metrics, error rates, and resource health. Custom dashboards in Azure Workbooks provide real-time visibility into system performance, allowing the team to detect and address potential issues proactively.

- **Backup and Recovery Plans**:  
  Scheduled backups for critical resources, including the PostgreSQL Database and Azure Key Vault, ensure data integrity and recoverability. Restore operations were tested and configured to meet an RPO (Recovery Point Objective) of less than 15 minutes, minimizing potential data loss during incidents.

- **Health Probes and Alerts**:  
  Health probes were configured in Azure Load Balancer to continuously monitor the status of App Services. Any anomalies, such as high latency or application downtime, trigger automated alerts to the response team. This enables rapid identification and resolution of issues before they impact users.

- **Resilience Through Modularization**:  
  The infrastructure was modularized using Bicep files, allowing individual components (e.g., database, web services, and monitoring tools) to be managed independently. This approach ensures that failures in one module do not cascade to the entire system, increasing overall reliability.

- **Disaster Recovery**:  
  A disaster recovery plan was developed to ensure that critical services, such as databases and authentication mechanisms, can be restored in secondary regions during catastrophic failures. The plan includes regular disaster recovery drills to ensure readiness.

- **Testing for Fault Tolerance**:  
  Chaos engineering practices were introduced to test the system's ability to recover from failures. Simulated disruptions, such as service unavailability or high latency, were injected into the system to validate the effectiveness of redundancy and failover mechanisms.

- **Automated Remediation**:  
  Automated scripts and workflows were implemented to address common issues, such as restarting services or scaling resources, without manual intervention. These self-healing mechanisms ensure faster recovery and reduce downtime.

By implementing these measures, the IE Bank application is equipped to handle failures gracefully, maintain availability, and provide a reliable user experience. Regular reviews and drills ensure that the system remains resilient to evolving challenges.



## Security Pillar

### GitHub Advanced Security

1. **GitHub Secret Scanning**:  
   Implemented to detect sensitive information like API keys and passwords in repositories, allowing prompt mitigation of exposures. This reduces the risk of credential compromise while maintaining operational continuity.

2. **Protected Main Branches**:  
   Enforced branch protection rules requiring pull requests, code reviews, and linear commit history to safeguard codebase integrity and prevent unauthorized changes.

3. **CodeQL for Code Scanning**:  
   Integrated for semantic code analysis to identify vulnerabilities in frontend (Vue.js) and backend (Python). Issues are displayed in GitHub Actions, enabling quick resolution.

4. **OSSF Scorecard**:  
   Evaluates repository security practices weekly, focusing on code reviews, dependency management, and CI/CD settings to address vulnerabilities promptly.

5. **Dependabot**:  
   Automates dependency updates and generates pull requests for secure versions, ensuring a stable development environment while addressing vulnerabilities.

6. **CODEOWNERS**:  
   Configured to assign ownership of critical code sections, ensuring only designated experts approve changes, improving accountability and security.



### Secure Secrets Management

1. **Azure Key Vault**:  
   Stores sensitive credentials like API keys and database passwords, offering centralized management, encryption, and strict access control.

2. **Managed Identities**:  
   Eliminates hard-coded credentials by providing secure, temporary resource access, enhancing security and simplifying secrets retrieval for applications.



### Security Frameworks

1. **Regex for Input Validation**:  
   Enforces strict data formatting to prevent injection attacks, particularly in sensitive areas like account registration and payments.

2. **NPM Best Practices**:  
   Followed OpenSSF guidelines by locking dependency versions, removing unused packages, and scanning for vulnerabilities to minimize risks.

3. **Evaluating Open Source Software**:  
   Established criteria for selecting secure third-party dependencies, complemented by Dependabot for vulnerability detection.

4. **Source Code Management Platform Configuration**:  
   Strengthened repository security with restricted access, branch protection, and audit logs to ensure robust control and traceability.

5. **Identity and Access Management**:  
   Implemented role-based access control to enforce least privilege principles, simplifying management and enhancing security.

6. **Logging and Auditing**:  
   Established comprehensive logging to track user actions and detect unusual activities, improving security and compliance.





## Cost Optimization Design Decisions

### Overview
In collaboration with the Infrastructure Developer, specific decisions were made to align our design with the Azure Well-Architected Framework's **Cost Optimization** pillar. These include leveraging scalable and efficient resource configurations, avoiding unnecessary costs, and ensuring environment-specific cost controls.

### Key Decisions
- **Resource Right-Sizing**:  
  Ensured App Service Plans and Static Web Apps use cost-effective SKUs (e.g., Free or B1) for non-production environments.

- **Shared Resources**:  
  Centralized Container Registry, Key Vault, and Log Analytics Workspace to minimize redundancy across environments.

- **Environment-Specific Configurations**:  
  - **Development**: Focused on minimal compute (low-tier SKUs) and cost efficiency for experimentation and testing.  
  - **UAT**: Balanced cost and performance to simulate production for stakeholder validation.  
  - **Production**: Allocated higher-tier SKUs and robust monitoring tools for reliability and scalability.  

- **Static Web Apps**:  
  Chosen for frontend hosting due to their low operational cost and simplicity.

- **Modularized Infrastructure**:  
  Used Bicep files with environment-specific parameterization to standardize deployments and reduce misconfigurations that could incur additional costs.

### Implementation Highlights
- **Monitoring and Alerts**:  
  Integrated Log Analytics and Application Insights to monitor resource usage and eliminate wastage.

- **Automated CI/CD Workflows**:  
  Deployed resources only on-demand using GitHub Actions, ensuring unused environments are not needlessly consuming costs.

- **Optimization Policies**:  
  - Used lifecycle management for resources like Container Registries to clean up unused images.  
  - Enforced tagging for cost attribution across all environments.


## Operational Excellence Pillar

Operational Excellence focuses on ensuring efficient and reliable operations by streamlining processes, automating repetitive tasks, and fostering robust monitoring and logging practices. This section outlines the design decisions made to enhance operational capabilities for both frontend and backend components.


### Frontend Design Decisions

1. **Environment Configuration Updates**
- Updated `.env.development` and `.env.uat` files to reflect new development and UAT URLs, ensuring environment-specific configurations are correctly applied.
- Modified `.github/workflows/ie-bank-frontend.yml` to reflect new frontend web app names for development and UAT.

2. **Monitoring and Logging**
- Integrated `@microsoft/applicationinsights-web` to log key frontend events such as page loads, user login/logout, and admin activities.
- Dynamically retrieve Application Insights connection strings from Azure to streamline configuration management.

3. **UI Enhancements and Role-Based Adjustments**
- Updated the application UI to dynamically adjust components and views based on user roles (User vs. Admin).
- Created new Vue.js components (`HomePage`, `Dashboard`, `AdminPortal`, and `UserList`) to ensure streamlined workflows for different user types, enhancing operational clarity.

4. **Error Handling and Notifications**
- Implemented a global Axios service to handle API errors (e.g., 401, 403, 404, 500) and prevent duplicate error alerts with a global flag (`isErrorShown`).



### Backend Design Decisions

1. **Configuration and Monitoring**
- Configured `APPINSIGHTS_CONNECTION_STRING` in `config.py` for seamless integration with Application Insights.
- Used `FlaskInstrumentor` from OpenTelemetry to log key application events, ensuring traceability of user actions and system events.

2. **Enhanced Data Models**
- Updated the `User` model to include attributes for user status and secure ID handling.
- Enhanced the `Account` model with unique account numbers, balances, and foreign key relationships to ensure data integrity.
- Improved the `Transaction` model to support deposits, withdrawals, and transfers, with metadata for better traceability.

3. **Routing Enhancements**
- Developed user-specific routes for account management (e.g., `register`, `login`, `dashboard`) and admin-specific routes (e.g., `list_users`, `create_user`).
- Introduced error-handling routes (`forbidden`, `not_found`, `server_error`) to streamline error management and ensure a consistent user experience.

4. **Authentication and Authorization**
- Enforced role-based access controls to ensure users access only permitted functionality.
- Redirected unauthorized users to the login page with relevant error messages for clarity.

#### HTML Template Updates
- Created separate HTML templates for local testing, enabling easier debugging and operational testing for both user and admin interfaces.



### Key Operational Practices

1. **Automation and CI/CD**
- Leveraged GitHub workflows to automate environment-specific deployments and testing, ensuring reliable and predictable operations.

2. **Logging and Observability**
- Centralized logging of key frontend and backend events using Application Insights for improved operational insights and error tracking.

3. **Error Mitigation**
- Implemented robust error handling across all layers (frontend Axios service, backend error routes) to mitigate operational disruptions and enhance user satisfaction.



## Performance Efficiency Pillar

The **Performance Efficiency Pillar** focuses on building a scalable and responsive infrastructure that effectively utilizes resources to support application demands. This ensures that the IE Bank application remains performant and responsive even during periods of high traffic or unexpected demand. 

- **Scalable Architecture**:  
  Azure App Service Plan configurations were chosen to enable automatic scaling based on incoming traffic patterns. This ensures that both backend APIs and frontend static content are dynamically allocated resources during peak usage while minimizing costs during low activity periods. Horizontal scaling was implemented to allow the system to increase capacity seamlessly.

- **Optimized Resource Allocation**:  
  Different SKUs were used across environments based on their usage requirements. Lower-cost SKUs (e.g., B1) were applied to Development and UAT environments to reduce costs, while Production environments were provisioned with higher-tier SKUs to ensure reliability and responsiveness for end users.

- **Concurrency Optimization**:  
  Leveraged Azure App Services’ process model for handling multiple concurrent requests. This allows backend and frontend services to scale out by adding additional instances during periods of high demand. Each instance operates independently, supporting efficient resource utilization.

- **Monitoring and Metrics**:  
  Application Insights was integrated to monitor key performance metrics such as request response times, throughput, and CPU usage. These metrics are analyzed against Service Level Objectives (SLOs), ensuring that 95% of API requests are processed within 500ms.

- **Automated Testing for Load and Stress**:  
  Load and stress testing were conducted regularly using automated tools to simulate peak traffic scenarios. This ensures the infrastructure can handle maximum load without degradation in performance. Test results informed adjustments to scaling policies and resource configurations.

- **Caching and Content Delivery**:  
  Static content delivery was optimized using Azure Static Web Apps, which reduces latency for end-users by hosting content closer to their location. API responses were cached to reduce unnecessary load on the database and backend services.

---

## Architectural Patterns

The IE Bank system follows a **modular, service-oriented architecture**, leveraging modern cloud-native design principles to ensure scalability, reliability, and maintainability. Below are the key architectural patterns implemented:

### Microservices Architecture

- Each service is independently deployable and focuses on a specific business domain.
- Enables loose coupling and independent scaling for components such as:
  - **Authentication Service**: Handles user and admin authentication and authorization.
  - **Transaction Service**: Manages all user transactions and financial operations.
  - **Account Management Service**: Maintains user account data, balances, and transaction history.

### Serverless Architecture

- The frontend is hosted as an **Azure Static Web App**, taking advantage of serverless capabilities like global distribution and auto-scaling.
- Backend services run in **Azure App Services** with containerized deployments, ensuring quick startup times and resource optimization.

### Layered Architecture

The system adopts a traditional **three-layered architecture** to separate concerns and improve maintainability:
1. **Presentation Layer**:
   - Built using **Vue.js** for the frontend, delivering a responsive and interactive user experience.
   - Communicates with the backend via RESTful APIs.
2. **Business Logic Layer**:
   - Implemented in **Python/Flask**, this layer contains the core application logic for transactions, user account management, and admin operations.
3. **Data Access Layer**:
   - Uses **Azure PostgreSQL** as the database for persistent storage.
   - Ensures efficient data querying and maintains integrity for user and transaction records.

### Event-Driven Architecture (Optional)

- Future-proofing the system by planning for an **event-driven approach** using Azure Event Grid for asynchronous communication.
- Allows for decoupled event producers (e.g., transactions) and consumers (e.g., audit logging or notification services).

### Resilience and Fault Tolerance

- **Redundancy and Failover**:
  - Backend and database services are configured with failover mechanisms, leveraging Azure's high availability zones.
  - Load balancing ensures that traffic is distributed evenly and mitigates single points of failure.
- **Health Monitoring**:
  - Continuous health checks using **Azure Monitor** to detect and handle faults proactively.
- **Retry Policies**:
  - All API requests and database operations implement retry mechanisms to recover from transient failures.

### Scalability and Auto-Healing

- Auto-scaling enabled for backend services to handle dynamic workloads efficiently.
- Containerized backend ensures resource isolation and rapid recovery during failures.


---

## Application Design
---

## Frontend

The frontend is built using **Vue.js**, offering a modern, responsive user interface. It incorporates the following key features and enhancements:

### Environment Configuration Updates
- Updated `VUE_APP_ROOT_URL` in `.env.development` and `.env.uat` to point to the new Development and UAT URLs.
- Modified `FRONTEND_WEBAPP_DEV`, `FRONTEND_WEBAPP_UAT`, and `USER_ALIAS` in `.github/workflows/ie-bank-frontend.yml` to reflect new frontend web app names.

### Dependency Updates
- Added new dependencies:
  - `@azure/identity`
  - `@azure/keyvault-secrets`
  - `@microsoft/applicationinsights-web`
- Updated versions of:
  - `vue`
  - `vue-router`
  - `vuex` in `package.json`.

### Vue.js Component Updates
#### User Components
- **HomePage**:
  - Displays landing page information.
  - Allows users to access the dashboard, transfer money, register, and log in.
  - Includes logout functionality and displays the logged-in username.
- **Dashboard**:
  - Displays user accounts and transactions.
  - Includes account creation functionality.
- **Login and Register Pages**:
  - Custom pages for authentication.
  - Logout functionality is available across all major pages, including the Dashboard and Admin Portal.
- **Removed AppAccounts Component**:
  - Previously handled account management; its functionality has been integrated into other components.

#### Admin Components
- **AdminPortal**:
  - Provides administrators with enhanced capabilities to monitor, modify, create, edit, and delete user accounts.
- **UserList**:
  - Displays a table of all users, accounts, and related details.
  - Includes editing and deletion functionalities via the **UserEdit** component.
- **UserCreate**:
  - Allows administrators to create user accounts.

### Backend Integration
- Each page connects to the backend to validate user authentication status and role.
- Unauthorized users are redirected to the Homepage with appropriate error messages.
- The application dynamically adjusts the UI based on the logged-in user's role (User vs. Admin).

### Services Added
- **Axios Service (axios.js)**:
  - Implements global error handling for API calls.
  - Redirects unauthorized users to the login page.
  - Displays error messages for HTTP status codes `401`, `403`, `404`, and `500`.
  - Prevents duplicate error alerts using a global flag (`isErrorShown`).
- **AppInsights Service**:
  - Logs key frontend events (e.g., page loads, user login/logout, account registration).
  - Retrieves the Azure connection string dynamically.
  - Tracks admin activities (e.g., user creation, editing, and deletion).

### Minor Code Changes
- Updated `src/App.vue`:
  - Included a script section.
  - Improved routing and component structure by modifying the `router-view` tag.

---

## Backend

The backend is built using **Python/Flask**, providing robust APIs and backend functionalities to support the IE Bank application.

### Models
- **User Model**:
  - Attributes for status (active/inactive).
  - Relationships with Account and Transaction models.
  - Includes methods for user deactivation and secure ID handling.
- **Account Model**:
  - Enhanced with foreign key relationships to associate accounts with users.
  - Attributes:
    - Balance
    - Currency
    - Country
    - Status
  - Functionality to generate unique 20-digit account numbers and deactivate accounts.
- **Transaction Model**:
  - Supports deposit, withdrawal, and transfer transactions using the `TransactionType` Enum.
  - Tracks metadata:
    - Sender/recipient account IDs.
    - Amount
    - Currency
    - Optional descriptions.
  - Established relationships between accounts and transactions.

### Routes
- **User Routes**:
  - `register`, `login`, `logout`, `create_account`, `dashboard`, `view_transactions`, `transfer`.
- **Admin Routes**:
  - `admin_portal`, `list_users`, `create_user`, `get_user`, `update_user`, `delete_user`.
- **Error Routes**:
  - `forbidden (403)`, `not_found (404)`, `server_error (500)`.

### Application Insights Integration
- Configured Azure Monitor with `APPINSIGHTS_CONNECTION_STRING` in `iebank_api/__init__.py`.
- Instrumented the Flask application using `FlaskInstrumentor` from OpenTelemetry.
- Logged key events:
  - Application startup
  - Request handling
  - Custom error messages
- Excluded certain loggers to ensure cleaner monitoring data.

### Configuration Updates
- Updated `config.py` to include `APPINSIGHTS_CONNECTION_STRING` for seamless integration with Azure Application Insights.
- Adjusted environment variables in `.github/workflows/ie-bank-backend.yml` for new backend web app names and user alias.
- Added environment-specific configurations for local, development, and UAT modes.

### HTML Templates
- Created templates for local testing:
  - Error Pages
  - User Pages
  - Admin Pages

### Key Enhancements
- **Security and Authentication**:
  - Enforces user authentication and role-based access controls.
  - Unauthorized access redirects users to the login page with error messages.
- **Detailed Models**:
  - Robust models for managing user accounts and transactions with clear relationships and utility methods.
- **Monitoring and Logging**:
  - Integrated Application Insights for tracking application performance and logging key events.
- **Testing and Debugging**:
  - Comprehensive HTML templates and route testing ensure seamless frontend-backend integration.


---

## Twelve-Factor App Principles

The IE Bank system adopts the **12 Factor App principles** to ensure a scalable, maintainable, and modern application architecture. These principles guide the design and implementation of the application, enabling seamless development, deployment, and operation.

---

### 1. Codebase
- **Single Codebase, Multiple Environments**:  
  The application is maintained in a single code repository, leveraging environment-specific configurations for Development, UAT, and Production.  
  - **Repository Structure**: Separate branches for features, bug fixes, and releases.
  - **Source Control**: GitHub repository with strict branch policies.


### 2. Dependencies
- **Explicitly Declare Dependencies**:  
  All dependencies are explicitly managed using `requirements.txt` for Python (backend) and `package.json` for Vue.js (frontend).  
  - Dependency management tools: `pip` for backend and `npm` for frontend.
  - Automated updates: Dependabot integration ensures dependencies remain up-to-date and secure.


### 3. Config
- **Configuration in the Environment**:  
  Environment-specific configurations are stored securely in **Azure Key Vault** and accessed dynamically using **Managed Identities**.  
  - Secrets like database credentials, API keys, and connection strings are injected at runtime.
  - Separation of configurations ensures portability across environments.



### 4. Backing Services
- **Treat Backing Services as Attached Resources**:  
  Backing services, such as the PostgreSQL database, Azure Container Registry, and Azure Key Vault, are treated as interchangeable resources.  
  - Services are bound to the application using environment-specific settings.



### 5. Build, Release, Run
- **Strict Separation Between Build and Run Stages**:  
  - **Build**: GitHub Actions builds Docker images and bundles static assets.
  - **Release**: Releases are tagged and deployed to UAT for stakeholder validation.
  - **Run**: Applications are executed in Azure App Services with the latest configuration.



### 6. Processes
- **Execute the App as One or More Stateless Processes**:  
  The backend (Python/Flask) and frontend (Vue.js) services are stateless, with persistent data stored in PostgreSQL.  
  - Session data is offloaded to client-side storage or the database.



### 7. Port Binding
- **Export Services via Port Binding**:  
  - The backend exposes APIs through dynamically assigned ports in Docker containers.
  - The frontend is served via **Azure Static Web Apps** with HTTPS enabled.



### 8. Concurrency
- **Scale Out via the Process Model**:  
  - Horizontal scaling is achieved by running multiple instances of backend and frontend services.
  - Azure App Services auto-scale configurations dynamically adjust to handle traffic spikes.



### 9. Disposability
- **Maximize Robustness with Fast Startup and Graceful Shutdown**:  
  - Docker containers ensure fast application startup.
  - Azure App Services implement health probes to detect failures and restart processes as needed.



### 10. Dev/Prod Parity
- **Keep Development, Staging, and Production as Similar as Possible**:  
  - UAT mimics production configurations to ensure realistic testing.
  - Feature branching and CI/CD pipelines enforce consistency across environments.



### 11. Logs
- **Treat Logs as Event Streams**:  
  Logs are centralized using **Azure Log Analytics Workspace**, where application logs, server logs, and metrics are aggregated.  
  - Real-time monitoring is enabled via Azure Monitor and Application Insights.



### 12. Admin Processes
- **Run Admin/Management Tasks as One-Off Processes**:  
  Administrative tasks, such as database migrations, are executed through CI/CD pipelines or one-off scripts invoked in Docker containers.



### Implementation Summary
By adhering to the **12 Factor App principles**, the IE Bank system achieves:
- **Scalability**: Modular design and auto-scaling.
- **Maintainability**: Simplified configurations and dependency management.
- **Portability**: Seamless deployments across multiple environments.


---

## Diagrams
### Data Flow Diagram

![image](https://github.com/user-attachments/assets/c0da8c07-718d-4a58-9f5b-953d2608d616)


### Entity Relationship Diagram

![image](https://github.com/user-attachments/assets/ffcdd8c2-57b5-438b-b221-9db52fbc93af)


### Use Case Diagrams

#### User Registration

![image](https://github.com/user-attachments/assets/3b019588-7c44-4451-8874-263680f1af17)


#### User Login

![image](https://github.com/user-attachments/assets/694c632c-4f56-47f5-b1ac-0dadfb490636)


#### Deposit

![image](https://github.com/user-attachments/assets/19ef5308-a864-451a-bb75-101f355f22be)


#### Transfer

![image](https://github.com/user-attachments/assets/1a350471-9e8c-4045-bc25-9609c02654b5)

