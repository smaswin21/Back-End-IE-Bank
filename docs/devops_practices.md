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

### Environment Deployment Process (DTAP)

#### Development (Dev)

The **Development (Dev)** environment serves as a **sandbox** where developers can **experiment**, **learn**, and **validate** infrastructure updates. It features **automated provisioning**, ensuring infrastructure is deployed seamlessly upon code commits to **feature branches**. Through **resource management**, it optimizes expenses by utilizing **cost-effective SKUs**. Additionally, the environment provides **wider access** to developers, enabling **rapid iteration** and fostering innovation.

#### User Acceptance Testing (UAT)

The **User Acceptance Testing (UAT)** environment serves as a **pre-production** stage where **stakeholders** can **test** and **validate** new features and infrastructure changes. It is designed with **production parity**, ensuring it mirrors the **production environment** in both configurations and resources for **accurate testing**. Deployments are **controlled**, initiated via **pull requests** to maintain **code quality**. Additionally, **limited access** is granted to **business users**, enabling them to perform **acceptance testing** and confirm that changes meet their requirements before moving to production.

#### Production (Prod)

The **Production (Prod)** environment is the **live environment** dedicated to serving **end-users** with **stable** and **thoroughly tested** infrastructure and application updates. It is designed with **high availability**, leveraging **redundant resources** to ensure **maximum uptime**. **Strict access control** is implemented and carefully monitored to maintain **security**. Additionally, the environment features **performance monitoring**, ensuring **optimal performance** and an exceptional **user experience** at all times. It is important to note that currently the resources are replicated consistently across stages.


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


