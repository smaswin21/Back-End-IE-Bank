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

