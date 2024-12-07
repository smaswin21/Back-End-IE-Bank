# IE Bank System GitHub Security Design Document
### Introduction
This document outlines the GitHub security strategy implemented for IE Bank System. The goal is to secure the GitHub environment to develop safe code and prevent unauthorized access to deployment workflows. This strategy includes advanced GitHub security features, dependency management, code scanning, and secrets management.

---

### 1. GitHub Hardening Strategy

#### 1.1 Secret Scanning
**Description:** Configured GitHub Secret Scanning to detect and prevent accidental inclusion of sensitive information (e.g., API keys, passwords) in repositories.
- **Configuration Link:** [Secret Scanning Configuration](#)
- **Analysis Link:** [Secret Scanning Alerts](#)

#### 1.2 Push Protection
**Description:** Enabled push protection to block contributors from pushing secrets to repositories. Configured alerts for bypassed blocks.
- **Configuration Screenshot:** Refer to the repository's settings page.

#### 1.3 CodeQL Implementation
**Description:** Integrated CodeQL for semantic code analysis of both frontend (Vue.js) and backend (Python) application code.
- **CodeQL Workflow Link:** [CodeQL Workflow](#)
- **CodeQL Analysis Link:** [CodeQL Analysis Run](#)

#### 1.4 OSSF Scorecard
**Description:** Implemented OSSF Scorecard to evaluate and improve security best practices within repositories.
- **Workflow Link:** [OSSF Scorecard Workflow](#)
- **Analysis Link:** [OSSF Scorecard Analysis](#)

#### 1.5 Dependabot
**Description:** Enabled Dependabot to ensure references to actions and reusable workflows remain up-to-date.
- **Dependency Updates:** Automatic pull requests for library and action updates.

#### 1.6 Dependency Reviews
**Description:** Configured dependency review checks to analyze and understand dependency changes and their security impact during pull requests.

#### 1.7 CODEOWNERS
**Description:** Established a CODEOWNERS file to monitor and control code changes effectively by assigning ownership to specific files and directories. Full-stack is allowed in Back-end and Front-end repositories, whilst cloud-architect is allowed in Infra, where the owner of the repos has the final say.
- **CODEOWNERS File Link:** [CODEOWNERS](#)

---

### 2. Secure Secrets Management

#### 2.1 Container Registry Credentials
**Description:** Container Registry credentials are securely managed using **Azure Key Vault** and accessed through **Managed Identities** in Azure Bicep workflows. This approach ensures robust security and simplifies credential management.

**Key Features:**
- **Centralized Secret Storage:** Azure Key Vault securely stores credentials for the Azure Container Registry (ACR), reducing the risk of exposure.
- **Access Control:** Role-Based Access Control (RBAC) is employed to restrict access to the credentials, ensuring that only authorized services and users can retrieve them.
- **CI/CD Integration:** The Azure Container Registry integrates seamlessly with GitHub Actions, automating image builds and deployments triggered by updates to the repository.
- **Dynamic Credential Injection:** App Services fetch credentials dynamically from Azure Key Vault during runtime, eliminating hardcoded secrets.

**Security Considerations:**
- Credentials are encrypted both at rest and in transit using Azure’s secure protocols.
- Admin credentials are rotated periodically and tracked in Key Vault’s audit logs.

#### 2.2 PostgreSQL Server Credentials
**Description:** PostgreSQL Server credentials are protected using **Azure Key Vault** and accessed via **Managed Identities**. This ensures the secure handling of sensitive information, such as database connection strings.

**Key Features:**
- **Data Security:** Enforced encryption at rest and in transit for all PostgreSQL server credentials, ensuring compliance with security standards.
- **Role-Based Access Control (RBAC):** Azure Key Vault manages access to database credentials, allowing only authorized services or applications to retrieve them.
- **Integration with Azure Services:** Credentials are dynamically injected into environment variables of App Services and other consuming applications.
- **Disaster Recovery:** The PostgreSQL database is deployed with geo-redundancy, ensuring credential accessibility even during regional outages.

**Performance and Redundancy:**
- Credentials are optimized for high-read and write-throughput environments, minimizing delays in concurrent queries.
- SLA-backed availability (e.g., 99.99%) guarantees uptime and access reliability.

**Security Enhancements:**
- Admin credentials are stored securely in Azure Key Vault and rotated according to organizational policies.
- Connection strings are encrypted and retrieved only during runtime, preventing hardcoding in application code.

#### 2.3 Azure Key Vault Overview
**Description:** Azure Key Vault serves as the central secret management solution for both Container Registry and PostgreSQL credentials. It provides secure, centralized storage and dynamic access control.

**Key Features:**
- **Unified Secret Management:** Centralized storage of sensitive information, including API keys, connection strings, and credentials for both the PostgreSQL database and the Container Registry.
- **Seamless Integration:** Works seamlessly with Azure App Services, Azure Container Registry, and other Azure resources for secure configuration management.
- **Audit and Monitoring:** Comprehensive logging of access to secrets, enabling detailed audit trails for compliance purposes.
- **RBAC Enforcement:** Role-based access control ensures that secrets are only accessible to authorized users and services.

By leveraging Azure Key Vault and integrating it with Managed Identities, the IE Bank System ensures a robust and secure approach to secrets management across all environments.
"""


---

### 3. Security Framework Adoption

#### 3.1 Open SSF Framework
The following guides from the Open SSF framework were implemented to enhance the security of the IE Bank System:

1. **Regex for Input Validation:**
   - Ensured input fields (e.g., user forms) validate data using regex patterns to mitigate injection attacks.
   - Integrated validation into the backend (Python) and frontend (Vue.js) codebases (front-end, back-end).

2. **Npm Best Practices:**
   - Applied npm security practices, including strict dependency versioning and automated vulnerability checks via Dependabot.

3. **Evaluating Open Source Software:**
   - Used Dependabot and OSSF Scorecard to evaluate third-party dependencies.
   - Established a process for dependency reviews during pull requests.

4. **Source Code Management Platform Configuration:**
   - Hardened the GitHub environment by enforcing branch protection rules, enabling push protection, and setting up CODEOWNERS.
  
5. **Developing More Secure Software:**
   - Continuous improvement: Monitoring and improving project scores such as OSSF Scorecard.
   - Code review: Enforce mandatory reviews for code changes using branch protection rules in platforms like GitHub or GitLab.

#### 3.2 SAFECode Framework
To enhance secure development practices, the following SAFECode principles were adopted:

1. **Standardize Identity and Access Management:**
   - Managed identities and RBAC policies in Azure Key Vault and GitHub repositories.

2. **Establish Log Requirements and Audit Practices:**
   - Centralized logs in Azure Log Analytics for security and performance monitoring.

3. **Establish Coding Standards and Conventions:**
   - Adopted secure coding standards for both Python (PEP-8 with security extensions) and Vue.js, ensuring consistent, maintainable, and secure code. Security extensions include input validation, secure error handling, and the use of linting tools to enforce these standards automatically during development.
  
4. **Use Code Analysis Tools to Find Security Vulnerabilities:**
   - Integrated CodeQL for semantic code analysis and regular scans.
   - Runs once on a weekly schedule.

5. **Handle Errors:**
   - Implemented secure error-handling practices to prevent sensitive information leakage.
   - The front-end will not release any information regarding an error, except that there is one.


---

### Summary
This GitHub security strategy aligns with best practices to ensure a robust and secure development environment. By implementing these measures, the IE Bank System is equipped to handle security challenges effectively.
"""
