# Software Architecture

This section details the software architecture of the IE Bank system, including its core design patterns, components, and flow.

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

