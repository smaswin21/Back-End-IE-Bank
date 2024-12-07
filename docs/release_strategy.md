# Release Strategy

## CI/CD Pipelines

The CI/CD pipeline used ensures an automated, reliable, and efficient deployment process across all environments. It integrates feature branching, automated testing, and deployment to facilitate a streamlined development lifecycle.

### GitHub Actions Workflow

- **Event Triggers**:
  - **Feature Branch Push**:
    - Automated deployments to the **Development (DEV)** environment.
    - This ensures developers can validate their changes quickly in a sandbox environment.
  - **Pull Request to Main**:
    - Initiates deployments to the **UAT environment** for acceptance testing.
    - Stakeholders and business users validate changes before they reach production.
  - **Push to Main Branch**:
    - Upon successful completion and merging of pull requests, the pipeline triggers automated deployment to the **Production (PROD)** environment.
- **Pipeline Stages**:
  1. **Build Stage**:
     - Compiles application code and infrastructure definitions (e.g., Bicep templates).
  2. **Test Stage**:
     - Executes automated unit tests, integration tests, and infrastructure preflight checks.
  3. **Deploy Stage**:
     - Applies validated changes to the targeted environment using Azure CLI and GitHub Actions workflows.

### Feature Branching Strategy
- **Naming Convention**:
  - Feature branches are named to represent the feature being developed (e.g., `feature/add-login`, `fix/transaction-bug`).
- **Automated DEV Deployments**:
  - Code pushes to feature branches automatically trigger deployments to the DEV environment, enabling immediate feedback for developers.
- **Pull Requests**:
  - Merging a feature branch into the main branch requires a pull request, enforcing peer reviews, passing tests, and adherence to coding standards.
  - Approved pull requests trigger deployments to the UAT environment.

### Quality Assurance
- **Linting**:
  - All infrastructure code is verified against best practices using `bicep linter`.
- **Testing**:
  - Unit tests validate individual components, while integration tests ensure cohesive functionality.
  - Preflight testing ensures that infrastructure changes will not introduce errors or conflicts in Azure environments.

---

## Branching Strategy

- **Version Control**: All Bicep files and application code are stored in Git repositories, leveraging Git strategies to manage changes effectively.
- **Code Reviews**: Mandatory pull request reviews are enforced to ensure code quality and adherence to standards.

---

## Deployment Workflows

### Development Environment

- Serves as a **sandbox** where developers can experiment, learn, and validate infrastructure updates.
- Features **automated provisioning** upon code commits to feature branches.
- Optimized for cost-efficiency by utilizing **low-tier SKUs**.
- Provides **wider access** to developers for rapid iteration and innovation.

### UAT Environment

- Mirrors the Production environment for **pre-production testing** by stakeholders and business users.
- Deployments are **controlled**, initiated via pull requests.
- Stakeholders perform **acceptance testing** to validate new features and infrastructure changes.
- Configurations mirror production for **realistic testing**.

### Production Environment

- Dedicated to serving **end-users** with **stable** and thoroughly tested updates.
- Designed with **high availability** and **redundancy** for maximum uptime.
- Features **strict access control** and **performance monitoring** to ensure security and optimal performance.
- Changes are applied following validation in UAT to minimize risks.

---

## Versioning and Rollbacks

- **Version Control**:
  - All infrastructure and application code versions are tracked in Git.
  - Enables rollback to previous configurations when needed.
- **Rollback Strategy**:
  - Uses IaC to redeploy consistent, stable configurations from previous versions.
  - Enhanced monitoring and alerting systems ensure rapid detection of issues for prompt rollback.

