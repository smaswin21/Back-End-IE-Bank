# GitHub Advanced Security
## GitHub Secret Scanning
GitHub Secret Scanning was configured across repositories to detect and prevent the accidental inclusion of sensitive data such as API keys, tokens, and passwords in the codebase. This scanning tool alerts developers to potential exposures, enabling immediate remediation and reducing the risk of compromised credentials. It was implemented with the idea that we do not need to generate new keys.

## Protected Main Branches
To secure the main branches, branch protection rules were implemented. We required a pull request before merging, enforced code review approval, and mandated a linear commit history. This configuration was applied across all main branches to maintain code integrity.

## CodeQL for Code Scanning
CodeQL was integrated as a semantic code analysis tool to detect vulnerabilities in both the frontend (Vue.js) and backend (Python). The tool systematically scans for potential security flaws and logical errors, providing insights into code safety while facilitating secure development practices. We can easily see the faults in the Actions tab and resolve them quickly.

## OSSF Scorecard
The OSSF Scorecard was utilized to evaluate the security posture of workflows and repositories. This tool provided a detailed analysis of security practices, including checks on code reviews, dependency management, and CI/CD configurations, enabling the team to identify and address areas for improvement. This is run weekly to ensure there are no underlying vulnerabilities.

## Dependabot
To automate dependency updates and maintain up-to-date packages, Dependabot was activated. It automatically generates pull requests for updates to dependencies, mitigating risks posed by outdated or vulnerable libraries. Alongside this, dependency reviews were set up to analyze changes and assess their security implications during the pull request process. This proved highly effective in addressing potential issues promptly.

## Dependency Reviews
Dependency reviews were set up to analyze changes and assess their security implications during the pull request process. This ensured unwanted dependencies were identified and addressed before merging.

## CODEOWNERS
The CODEOWNERS file was configured in each repository to establish clear ownership of code sections. This ensures that changes to critical areas of the codebase are reviewed by designated experts, maintaining accountability and adherence to security standards.

# Secure Secrets Management

## Key Vault
For robust secrets management, Azure Key Vault was integrated into the infrastructure to securely store credentials such as API keys, container registry tokens, and PostgreSQL server passwords. This approach centralizes sensitive information, encrypts it, and provides fine-grained access control to authorized entities only. Azure Key Vault was seamlessly integrated into our project, providing a reliable and secure solution.

## Managed Identity
We also leveraged Managed Identities to eliminate the need for hard-coded credentials. By granting applications and services secure, temporary access to resources, this solution enhances security while simplifying credential management. Managed identities were implemented in workflows to access Key Vault securely and efficiently.

# Security Frameworks
## OpenSSF
### Regex for Input Validation
To enhance security through the OpenSSF framework, we implemented regex-based input validation across our applications. This measure enforces strict formatting rules for data inputs, preventing malicious injections such as SQL, XML, or script-based attacks. By defining regular expressions tailored to expected input patterns, we reduced vulnerabilities stemming from unvalidated user input, bolstering both application reliability and security. This was primarily implemented in our front-end input forms, particularly on the accounts page and during bank account addition.

### Npm Best Practices
As part of OpenSSF guidelines, we adopted npm best practices to secure the management of frontend dependencies. This included locking dependency versions, running regular vulnerability scans with Dependabot, and removing unused packages to minimize the attack surface. Additionally, we enforced strict review processes for package additions to ensure that third-party libraries met security and maintenance standards.

### Evaluating Open Source Software
We implemented a structured process for evaluating open-source software to minimize risks from third-party dependencies. This included assessing project activity levels, reviewing contributor trustworthiness, and checking for regular updates or responses to reported vulnerabilities. Dependabot was instrumental in ensuring that vulnerabilities in open-source software are identified and addressed promptly.

### Source Code Management Platform Configuration
To align with OpenSSF practices, we fortified our source code management platform with robust configuration settings. Repository access was restricted based on roles, branch protection rules were enforced, and detailed audit logs were maintained. These configurations ensured controlled access to critical resources and provided traceability for all repository activities.

## SAFECode
### Standardize Identity and Access Management
Under SAFECode principles, we standardized identity and access management practices to ensure secure and consistent access control. By implementing role-based access control (RBAC), we enforced the principle of least privilege, granting users only the permissions necessary for their roles.

### Establish Log Requirements and Audit Practices
Logging and auditing requirements were defined to track system activities comprehensively. Logs included information on user actions, authentication attempts, and system changes. Audit practices ensured that logs were regularly reviewed for unusual activities or potential breaches, providing a foundation for proactive threat detection and compliance. Refer to the Site Reliability section for further details.

### Establish Coding Standards and Conventions
SAFECode principles guided the creation of coding standards and conventions that prioritized security. These standards mandated secure patterns for error handling, input sanitization, and encryption. By standardizing these practices, the front-end team ensured that our project adhered to stringent security protocols.

### Use Code Analysis Tools to Find Security Vulnerabilities
We integrated CodeQL into our project to quickly identify security vulnerabilities. This tool is further complemented by third-party audits, allowing us to enhance our security posture continuously.

### Handle Errors
Error handling practices were established to ensure sensitive information was not exposed through system-generated messages. Errors were logged for internal debugging but raised as generic messages to end-users. This approach prevents attackers from gathering system details while providing developers with sufficient context for troubleshooting.
