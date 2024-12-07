# GitHub Hardening Strategy Documentation
## IE Bank System GitHub Security Design Document

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
**Description:** Secured container registry credentials using Azure Key Vault. These credentials are accessible via managed identities in Azure Bicep workflows.
- **Bicep File Link:** [Container Registry Credentials Bicep](#)

#### 2.2 PostgreSQL Server Credentials
**Description:** Protected PostgreSQL credentials in Azure Key Vault with role-based access control and managed identity.
- **Bicep File Link:** [PostgreSQL Credentials Bicep](#)

#### 2.3 Documentation
**Description:** Worked with the Cloud Architect and development teams to document the secrets management strategy.
- **Documentation Link:** [Secrets Management Design Section](#)

---

### 3. Security Framework Adoption

#### 3.1 Open SSF Framework
Implemented the following five guides from the Open SSF framework:
1. Regex for Input Validation
2. Npm Best Practices
5. Evaluating Open Source Software
6. Source Code Management Platform Configuration

#### 3.2 SAFECode Framework
Adopted the following five practices from the SAFECode framework:
1. Standardize Identity and Access Management
2. Establish Log Requirements and Audit Practices
3. Establish Coding Standards and Conventions
4. Use Code Analysis Tools to Find Security Vulnerabilities
5. Handle Errors

- **Implementation Documentation:** [Framework Implementation Design Section](#)

---

### Summary
This GitHub security strategy aligns with best practices to ensure a robust and secure development environment. By implementing these measures, the IE Bank System is equipped to handle security challenges effectively.
"""
