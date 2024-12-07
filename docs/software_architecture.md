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

### Frontend
<!-- Details about the frontend design, technologies used, and components. -->

### Backend
<!-- Details about the backend design, APIs, and business logic. -->

---

## Twelve-Factor App Principles
<!-- Briefly discuss alignment with the Twelve-Factor App principles. -->

---

## Diagrams
### Data Flow Diagram
<!-- Include or describe the data flow diagram. -->

### Entity Relationship Diagram
<!-- Include or describe the entity relationship diagram. -->

### Use Case Diagram
<!-- Include or describe the use case diagram. -->
