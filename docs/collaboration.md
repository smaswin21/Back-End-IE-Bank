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

## How Collaboration was Done
**Connect GitHub with Azure DevOps Boards**
This help synchronize the repositories with the Azure Boards, here are the steps to do it:
1. Go to project settings
2. Go to GitHub connections
3. Connect to the GitHub account with all the main repositories 
4. Select the repositories relevant to the Azure Boards (in our cases It was repositories for the backend, frontend and infrastructure)

Connection:
<img width="1147" alt="Screenshot 2024-12-07 at 14 18 07" src="https://github.com/user-attachments/assets/5f3450ce-f101-4e77-9c03-cd733624fa2c">


**Connect Slack with Azure DevOps Boards**
1. In the apps section on Slack, download Azure DevOps Boards
2. In the designated Slack channel, log in to the Azure DevOps account with the product backlog 
3. On setting in Azure Boards, go to Security → Policies → Application connection policies and enable Third-party application access via OAuth
4. Use /azboards link [Azure Boards Link] to connect the desired Azure Board

**Connect Slack with GitHub**
1. In the apps section on Slack, download GitHub
2. In the designated Slack channel, log into the GitHub account with all repositories 
3. Using this syntax /github subscribe owner/repo, link the repositories 
4. Validate through entering the code received by email
5. This helped us keep track of all pushes to main, deployments and changes made to all repositories

**Connect Slack with Zoom**
1. In the apps section on Slack, download Zoom
2. Authenticate zoom account by logging in

This was used to schedule and start all the scrum meetings through the command /zoom call.

**Connect Azure with Slack**
This was needed for sending all the alerts from Azure and the logs to our slack channel, and it was useful when we realized we did something wrong and unnecessary alerts about data leaks were being sent, this was how it was done:
1. Create logic app on Azure for the alerts
2. Once alerts are configured choose the option of integration with Slack
3. In the apps section on Slack, download Azure
4. Log into the Azure account with the logic app and alerts
5. Select the resource groups and alerts we want to monitor through Slack
6. Configure Slack channel to send notification for alerts

Example alerts:

<img width="518" alt="Screenshot 2024-12-07 at 14 19 22" src="https://github.com/user-attachments/assets/9fc5d86c-7918-4604-bac0-73fe6c23eac9">



All these integrations ensured everything was traced back to the Slack chat, contributing to efficient communication and tracking of all updates from all tools that were utilized. 

---

## Documentation Hosting

- **GitHub Pages**:
The collaboration strategy used for the documentation consisted in each role having a personal .md file inside a separate branch created for this purpose. This was done to have a smooth workflow where different roles were not modifying each other's content.

When all the documentation was completed by all the different roles, the cloud architect created a structure and put each role's documentation in the right place maintaining whole sections.

