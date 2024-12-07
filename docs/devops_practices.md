# DevOps Practices

This section outlines the DevOps methodologies, tools, and processes adopted for the project to ensure streamlined development, deployment, and operational efficiency.

---

## Adopted Practices

### SCRUM Approach
1. Using an Agile methodology for planning and working with different team members during the development the application
2. Having a definitive backlog prepared by the product owner that is updated continuously throughout each sprint 
3. Cloud architect must take the initial design decisions early on in the process
4. Conduct daily scrum meetings to keep each other updated and ensure everyone is on track
5. Sprint reviews and sprint retrospectives to show the stakeholders the progress so far and receive constructive criticism.


### Test-driven Development 
1. Tests developed for every function, using unit and function tests, to ensure that the new and old features have a strong foundation and function as intended
2. Testing after every new development to recognize bugs early on and fix them before it’s too late


### CI/CD Strategy
1. Using feature branching for new code developments, where each feature branch has a name representative of the new code being developed. 
2. Pushes to feature branches must trigger automated deployments to the DEV environment 
3. Once all changes have been tested and are completed, merge them with the main branch using a Pull request
4. Pull requests to the main branch must trigger automated deployment to the UAT environments 
5. Pushes to the main branch after completing a Pull Request must trigger automated deployment to the PROD environment
   
---

## Environment Setup

The IE Bank system employs a **DTAP (Development, Test, Acceptance, Production)** environment structure, ensuring a seamless progression from development to production with minimal risks. Each environment is tailored to specific needs, balancing cost, performance, and security.


### Environment Specifications

| **Environment**     | **Purpose**                                                                                      | **Key Features**                                                                                                                                                      | **Cost Optimization**                                                                                                                |
|----------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Development (Dev)** | Provides a sandbox for developers to experiment, learn, and validate changes.                         | - Automated provisioning via GitHub Actions.  <br>- Cost-efficient SKUs for resources.<br>- Wider access for experimentation.<br>- Logs aggregated in Log Analytics. | - Uses low-tier SKUs for services.<br>- Minimal instance count for compute resources.                                               |
| **UAT**             | Mirrors the production environment for testing by stakeholders and business users.                      | - Production-parity configuration.<br>- Controlled deployments initiated via pull requests.<br>- Limited stakeholder access for validation.<br>- SLA monitoring.    | - Balanced cost-performance ratio with mid-tier SKUs.<br>- Retains enough resources to mimic production behavior.                   |
| **Production (Prod)**| The live environment hosting the application for end users.                                      | - High availability with redundancy.<br>- Robust monitoring with Application Insights.<br>- Strict access controls.<br>- SLA: 99% uptime.<br>- Optimized scaling.   | - Scaled to handle expected load.<br>- Reserved instances where possible to reduce long-term costs.                                  |



### Resource Configurations Per Environment

1. **Azure App Service for Containers**
   - **Development**: Low-tier (B1) App Service Plan.
   - **UAT**: Standard-tier App Service Plan for performance testing.
   - **Production**: Premium-tier App Service Plan with auto-scaling for high availability.

2. **Azure PostgreSQL Database**
   - **Development**: Single-server instance with basic configuration.
   - **UAT**: Replicates production settings for realistic testing.
   - **Production**: High-availability configuration with geo-redundancy and backups.

3. **Azure Static Web Apps**
   - **Development**: Free-tier for basic functionality testing.
   - **UAT**: Standard-tier for parity with production.
   - **Production**: Standard-tier with global CDN for optimized delivery.

4. **Azure Key Vault**
   - Centralized secrets management across all environments.
   - Role-based access configured for resource-specific secrets.

5. **Azure Container Registry**
   - Shared across all environments for efficient image management.
   - Admin credentials stored securely in Azure Key Vault.

6. **Monitoring and Alerts**
   - **Development**: Basic logs in Log Analytics.
   - **UAT & Production**: Application Insights with SLO-specific dashboards and alerts.



### Modularization and Parameterization

To enhance reusability and consistency:
- **Modular Infrastructure as Code (IaC)**: Azure Bicep templates are modularized, with individual modules for App Services, PostgreSQL, Static Web Apps, and Key Vault.
- **Parameterization**: Each environment has specific JSON parameter files to define resource configurations, names, and SKUs.



### DTAP Workflow

1. **Development Environment**:
   - Triggered on feature branch push via GitHub Actions.
   - Automated deployment with basic testing and logging.

2. **UAT Environment**:
   - Deployment initiated via pull requests to the main branch.
   - Thorough testing, including integration and user acceptance tests.

3. **Production Environment**:
   - Deploys only upon successful UAT testing and pull request approval.
   - Includes a rollback strategy to ensure stability.


### SLA, SLO, and SLI Compliance

- **Development**: Monitors baseline metrics to detect development issues early.
- **UAT**: Validates SLIs such as page load times, error rates, and API response times.
- **Production**: Guarantees SLA compliance with defined SLOs, such as 99% uptime and response times under 500ms.


---

## Infrastructure as Code (IaC)

- The project uses Azure Bicep for declarative and modular infrastructure definitions.
- Modularization enables reusability and flexibility, with separate modules for core resources like App Services, Key Vault, Azure Container Registry (ACR), and PostgreSQL.
- Parameter files differentiate configurations per environment (e.g., resource naming conventions, SKUs, and access controls).

### Code Management

- **Version Control:** All Bicep files are stored in a Git repository with proper Git strategies to manage changes effectively.
- **Code Reviews:** Mandatory pull request reviews to ensure code quality and adherence to standards.
- **Template Validation:** Automated checks to validate Bicep templates for syntax and compliance before deployment.

---

## Collaboration and Tools

Efficient collaboration and streamlined workflows are critical to the success of the IE Bank project. This section details the tools and practices adopted to ensure seamless team coordination and effective version control.


### Collaboration Tools

The project leverages a suite of tools to enhance communication, tracking, and documentation:

1. **Slack and Whatsapp**
   - Real-time messaging for team communication and instant updates.
   - Slack integration with GitHub Actions and Azure DevOps to receive automated notifications for CI/CD pipeline events, pull request updates, and incident alerts.

2. **Azure DevOps**
   - Used for task and sprint management, ensuring alignment with the Scrum framework.
   - Backlog and sprint planning are centralized, allowing visibility into task progress, blockers, and completed work.

3. **GitHub**
   - Central repository for source code, infrastructure templates, and documentation.
   - Features like issues and discussions help track bugs, feature requests, and team inputs.

4. **Zoom**
   - Used for daily stand-ups, sprint planning meetings, and stakeholder presentations.
   - Facilitates collaborative decision-making with team members in remote or hybrid work setups.

5. **GitHub Pages**
   - Hosts project documentation, including architecture diagrams, functional requirements, and deployment guides.
   - Ensures stakeholders have easy access to up-to-date project details.


### Version Control Strategy

The IE Bank project employs a robust Git-based version control strategy to manage the development process effectively:

1. **Feature Branching**
   - Each new feature or bug fix is developed in an isolated branch named descriptively (e.g., `feature/add-login`, `fix/transaction-error`).
   - Branches are created off the main branch and merged back after completion and review.

2. **Pull Requests (PRs)**
   - All changes are reviewed through pull requests before merging into the main branch.
   - Pull requests require:
     - Automated CI/CD pipeline checks (e.g., build success, tests passing).
     - Peer code reviews to ensure quality and adherence to standards.

3. **Branch Protection**
   - The main branch is protected to prevent direct commits. Only approved PRs can be merged.
   - Requires a minimum of one peer review and successful CI checks.

4. **Commit Practices**
   - Descriptive commit messages follow the `type: message` format (e.g., `fix: resolve null pointer error in login`).
   - Frequent commits ensure traceability and easier debugging.

5. **Release Workflow**
   - **Development Branch**: Work in progress for new features and experimentation.
   - **UAT Branch**: Stabilized changes for stakeholder testing and validation.
   - **Production Branch**: Only thoroughly tested and approved changes reach this branch.


### Automated Integration and Notifications

To enhance collaboration and workflow visibility:
- **GitHub Actions Integration**:
  - CI/CD pipeline updates and test results are posted to Slack.
  - Deployment status for each environment is automatically shared with relevant channels.
- **Azure DevOps Integration**:
  - Sprint progress, backlog updates, and task assignments are synchronized with Slack for team-wide awareness.


