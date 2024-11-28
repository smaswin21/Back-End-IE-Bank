# Azure Well-Architected Framework

## Security Pilar

### GitHub Advanced Security

1. **GitHub Secret Scanning**:  
   GitHub Secret Scanning was implemented across all repositories to detect sensitive information such as API keys, tokens, and passwords accidentally included in the codebase. This tool enables developers to address exposures promptly, significantly reducing the risk of compromised credentials. By avoiding the unnecessary generation of new keys unless vulnerabilities are detected, the organization ensures smooth operations while maintaining security.

2. **Protected Main Branches**:  
   To maintain the integrity of the codebase, branch protection rules were enforced on all main branches. These rules include mandatory pull requests before merging, code review approval, and linear commit history enforcement. This configuration ensures that all changes are reviewed and validated by team members, minimizing the risk of unauthorized or erroneous modifications.

3. **CodeQL for Code Scanning**:  
   CodeQL was integrated as a semantic code analysis tool to identify vulnerabilities in both the frontend (Vue.js) and backend (Python). By scanning for potential security flaws and logical errors, CodeQL provides actionable insights that facilitate the development of secure code. Issues identified are visible in the GitHub Actions tab, allowing for quick and effective resolution.

4. **OSSF Scorecard**:  
   The OSSF Scorecard is used to evaluate the security posture of workflows and repositories. This tool conducts a detailed analysis of security practices, such as code review policies, dependency management, and CI/CD configurations. Running the Scorecard weekly ensures that vulnerabilities or misconfigurations are detected and addressed promptly, contributing to a robust security framework.

5. **Dependabot**:  
   Dependabot automates the process of dependency updates, ensuring that the latest secure versions of libraries are in use. This tool generates pull requests for updates and performs dependency reviews to analyze the security implications of changes. By addressing vulnerabilities proactively, Dependabot helps maintain a secure and stable development environment.

6. **CODEOWNERS**:  
   The CODEOWNERS file was configured across repositories to assign clear ownership of critical code sections. This ensures that only designated experts can approve changes to specific parts of the codebase, enhancing accountability and compliance with security standards.

---

### Secure Secrets Management

1. **Azure Key Vault**:  
   Azure Key Vault was integrated to securely store sensitive credentials such as API keys, container registry tokens, and PostgreSQL passwords. This service provides centralized management, encryption, and strict access control, ensuring that only authorized applications and users can retrieve secrets. The integration streamlines secrets management while enhancing the overall security posture.

2. **Managed Identities**:  
   Managed Identities were employed to eliminate the need for hard-coded credentials, providing secure, temporary access to resources. This approach enhances security by reducing exposure to credential-related attacks and simplifies access to Azure services like Key Vault. Applications and workflows leverage Managed Identities to retrieve secrets without requiring explicit credentials.

---

### Security Frameworks

1. **Regex for Input Validation**:  
   To mitigate injection-based attacks, regex-based input validation was implemented across all applications. This measure enforces strict data formatting rules, ensuring that inputs conform to predefined patterns and preventing malicious entries. This approach significantly bolsters application security, particularly in areas handling sensitive user data, such as account registration and payment processing.

2. **NPM Best Practices**:  
   Adhering to OpenSSF guidelines, the team adopted NPM best practices for managing frontend dependencies. These practices include locking dependency versions, removing unused packages, and performing regular vulnerability scans using Dependabot. By maintaining a streamlined and secure dependency management process, the team minimized the potential attack surface.

3. **Evaluating Open Source Software**:  
   A structured evaluation process for third-party dependencies was established to reduce risks associated with open-source software. Criteria such as project activity, contributor reputation, and responsiveness to vulnerabilities were considered. Dependabot further complemented this process by automating the detection of vulnerabilities in dependencies.

4. **Source Code Management Platform Configuration**:  
   The source code management platform was fortified by restricting repository access, enforcing branch protection rules, and maintaining detailed audit logs. These configurations align with OpenSSF guidelines and ensure robust control and traceability of repository activities.

5. **Identity and Access Management**:  
   Role-based access control (RBAC) was implemented to enforce the principle of least privilege, ensuring users only have access to the resources necessary for their roles. This standardization simplifies management while maintaining a high level of security across systems.

6. **Logging and Auditing**:  
   Comprehensive logging and auditing practices were established to track user actions, authentication attempts, and system changes. Regular reviews of these logs support proactive detection of unusual activities, enhancing both security and compliance efforts.


---

## Operational Excellence Pillar


Operational Excellence focuses on ensuring efficient and reliable operations by streamlining processes, automating repetitive tasks, and fostering robust monitoring and logging practices. This section outlines the design decisions made to enhance operational capabilities for both frontend and backend components.

---

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

---

### Key Operational Practices

1. **Automation and CI/CD**
- Leveraged GitHub workflows to automate environment-specific deployments and testing, ensuring reliable and predictable operations.

2. **Logging and Observability**
- Centralized logging of key frontend and backend events using Application Insights for improved operational insights and error tracking.

3. **Error Mitigation**
- Implemented robust error handling across all layers (frontend Axios service, backend error routes) to mitigate operational disruptions and enhance user satisfaction.

---

This framework ensures streamlined operations, efficient debugging, and enhanced observability for IE Bank's digital banking application.


