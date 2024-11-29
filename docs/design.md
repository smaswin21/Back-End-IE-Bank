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

---

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



---

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

---

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

---

This framework ensures streamlined operations, efficient debugging, and enhanced observability for IE Bank's digital banking application.

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

By implementing these strategies, the infrastructure is designed to adapt dynamically to varying workloads, optimize resource use, and maintain high responsiveness, ensuring a seamless user experience.

