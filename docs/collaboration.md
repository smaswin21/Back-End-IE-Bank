# Collaboration Tools and Integration

## Tools Overview

The IE Bank system utilizes a range of tools to streamline collaboration, communication, and project management:

1. **Azure DevOps**:
   - Manages the backlog, sprint planning, and task assignments.
   - Provides visibility into project progress and team contributions.
   - Integrates with GitHub for linking code to user stories and tasks.

2. **GitHub**:
   - Central repository for version control, code collaboration, and CI/CD workflows.
   - Hosts Infrastructure as Code (IaC) templates and project documentation via GitHub Pages.
   - Enables peer reviews and ensures code quality through pull requests.

3. **Slack**:
   - Primary communication tool for real-time messaging and updates.
   - Integrated with GitHub Actions for notifications about CI/CD pipeline status and code changes.

4. **Application Insights and Log Analytics**:
   - Monitors application performance and system health.
   - Aggregates logs for centralized troubleshooting and analysis.

---

## Tool Integrations

### GitHub
- **Code Repository**:
  - Enables version control for application and infrastructure code.
  - Maintains modular Bicep templates for IaC.
- **GitHub Actions**:
  - Automates CI/CD workflows:
    - Pushes to feature branches trigger deployments to DEV.
    - Pull requests trigger UAT deployments.
    - Merges to the main branch deploy to Production.
- **Documentation Hosting**:
  - GitHub Pages serves as a platform for sharing system design, API documentation, and architecture diagrams.

### Slack
- **Real-Time Updates**:
  - Sends automated notifications for CI/CD events, such as build successes or failures, and pull request reviews.
- **Incident Alerts**:
  - Integrated with Application Insights and Logic Apps to notify the team of critical issues in real-time.

### Azure DevOps
- **Backlog Management**:
  - Tracks epics, features, and user stories with associated tests.
- **Sprint Planning**:
  - Enables efficient planning with task assignments and progress tracking.
- **Linking Code to Stories**:
  - Ensures every code change maps back to a user story or requirement in the backlog.

---

## Documentation Hosting

- **GitHub Pages**:
The collaboration strategy used for the documentation consisted in each role having a personal .md file inside a separate branch created for this purpose. This was done to have a smooth workflow where different roles were not modifying each other's content.

When all the documentation was completed by all the different roles, the cloud architect created a structure and put each role's documentation in the right place maintaining whole sections.

