# Product Owner Documentation

## Table of Contents

- [Product Vision and Mission](#product-vision-and-mission)
- [Product Vision Board](#product-vision-board)
- [Minimum Viable Product (MVP)](#minimum-viable-product-mvp)
- [Objective and Key Results (OKRs)](#objective-and-key-results-okrs)
- [Product Backlog](#product-backlog)
  - [User Stories and Acceptance Criteria](#user-stories-and-acceptance-criteria)
- [Product Roadmap](#product-roadmap)
- [Sprint Backlog](#sprint-backlog)
- [Sprint Planning Ceremony](#sprint-planning-ceremony)
- [Daily Scrum Meetings](#daily-scrum-meetings)
- [Scrum Methodology](#scrum-methodology)
- [Collaboration Strategy](#collaboration-strategy)

---

## Product Vision and Mission

### Product Vision

To revolutionize personal banking by providing a secure and user-centric digital platform that empowers young adults or students to manage their finances and helps achieve their financial goals


### Product Mission

IE Bank is a platform that aims to deliver accessible, reliable and secure banking experiences that prioritize simplicity and user empowerment for young adults who are finance beginners. Through innovation and commitment to continuous improvements, we aim to simplify personal finance management, prompt financial inclusion and set the new standard for digital banking for younger adults.  

---

## Product Vision Board

![Product Vision Board](images/Product-Vision-Board-Extended%20(dragged).png)

---

## Minimum Viable Product (MVP)

Our MVP setup consists of the functional requirements, primarily the admin portal and the user portal, non-functional requirements, including the authentication, user interface and security compliance, as well as all the development practices that will be implemented in our journey.

In general, IE bank is a fin-tech startup that is working on a bank management app for young adults who are looking for an easy and user-friendly app that allows them to manage their financial needs. IE bank provides a new digital experience for its customers due to its convenience and secure ways for users to manage their bank accounts, transfer money, pay bills and view all transactions. 

The following are the features that the business analysts wants to implement in the next phase of the app development.

## FUNCTIONAL REQUIREMENTS
### Admin Portal - Bank users management system

This allows bank administrators to access, manage and control users’ accounts. Through this portal, the admins can view, create, update and delete bank users’ accounts. This consist of the following main features
1. Administrators accounts will have a default username and password. Once these credentials are used and login is successful, the admins can access users’ management portals.
2. Once logged in to a users’ portal, the administrator can list, create, update and delete bank users and their passwords.

### User Portal - Bank account management system

This allows users to access their account management portals, and allows them to have more than one bank account to be associated with their user profile. This consists of the following features:
1. New users can register on IE back by filling out a form containing their username, password and confirming their password. When a new user is registered, a new account will be provided by default, with a random account number
2. Users can log in to the application using their username and password, and once login is successful, they can only view their own bank accounts and transactions (the information related to their account only)
3. Users can perform transactions, primarily transferring money to their existing account, which can be found in the account management portal. This is done by entering the recipient’s account number and amount to be transferred. 
4. Amount transferred by the sender should not be more than the amount available in their account at the time.

## NON-FUNCTIONAL REQUIREMENTS 
### Basic authentication
1. The application must implement a basic user or admin authentication system that requires the user or admin to enter their username and password to log in and access their respective accounts successfully
2. Authentication needs to remain simple, as the business analysts of IE bank do not expect the usage of complex authentication methods, such as biometrics, tokens or OAuth, at this time

### Security compliance 
1. Apply encryption to user credentials and store these credentials securely in a database by hashing the passwords.
2. Ensures users’ sensitive information is stored securely


### Simple user interface 
1. The user interface must focus on ensuring that all functionalities and requirements are satisfied and executed successfully, with minimal focus on the aesthetic aspects of the frontend 

## DEVOPS PRACTICES
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

## Objective and Key Results (OKRs)

**Objective 1:** Deliver a functioning Minimum Viable Product 

**Key results:**
1. Develop and deploy admin portal by using the CRUD functionalities, so that it can be used for user management
2. Implement a secure user registration system which generates random account numbers for each user
3. Allows transferring funds between accounts and ensures that transfer does not exceed amount in account
4. Ensure 100% completion of functional and unit testing for all the features
5. Conduct 2 rounds of UAT deployments and ensure both rounds have a 100% success rate and has zero defects

**Objective 2:** Implement a CI/CD pipeline 

**Key results:**
1. Automate deployments to Development, UAT and Production environments with 0 manual intervention by 4/12/2024
2. Setup GitHub Actions workflow by adding the necessary branching strategies to enable the automatic triggers for tests and deployments within one sprint
3. The average build time across all three environments should not exceed 5 minutes
4. Ensure a success rate of 90% for all deployments and necessary automation tests across all environments by the end of the sprint
5. Implement Azure monitoring tools to ensure that deployments are continuously successful and occur within approximately 10 minutes of initiation.

**Objective 3:** Improve System Security

**Key results:**
1. Implement secure password hashing for 100% of admin and user credentials 
2. Deploy Azure Key Vault to securely manage environment secrets for all three environments (Dev, UAT, Prod) by 4/12/2024
3. Ensure that Advanced Security features cover 100% of the GitHub repositories (frontend, backend, infra) through using CodeQL scanning and Dependabot alerts
4. Configure and validate push protection on all 3 repositories to block any accidental exposures to secrets 
5. Conduct 2 iterations of security framework implementations, choosing 5 guides from OpenSSF and 5 practices from SAFECode, ensuring all the controls are integrated into the application by 4/12/2024 

**Objective 4:** Improve Performance and Reliability 

**Key results:**
1. Achieve up to 99% availability of the application in the production environment by 4/12/2024
2. Define and monitor 5 Service Level Indicators (SLIs) to measure system health so that 100% of the SLIs are tracked on Azure Monitor
3. Scale the capacity of the system to handle 1500 users at the same time without any effects on system performance by 4/12/2024
4. Implement diagnostic and logging strategies with Azure Monitor and Application insights, achieving full integration across all services by the end of the sprint.
5. Optimize the database queries such that the average response time is reduced 20% across all endpoints by the end of the sprint.

**Objective 5:** Adopt and Foster an Agile and Collaborative Team Practice

**Key Results:**
1. Host Scrum meetings at least twice a week to focus on tracking each team member’s progress, roadblocks and future tasks
2. Document 15 user stores with the appropriate acceptance criteria for each member
3. Complete two sprint retrospectives to gather feedback and improve workflows as needed
4. Maintain a rate of 90% task completion rate for every sprint backlog 
5. Ensure at least 3 peer reviews for every pull request before merging and to ensure all changes are contributing to the application


---

## Product Backlog

Link for [Product Backlog](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_backlogs/backlog/Software-Development-and-Devops-Assignment%20Team/Epics) on Azure DevOps Boards.

---

## Product Roadmap

The roadmap outlines the high-level timeline for delivering the product's major milestones:

1. **Phase 1**: Development of Admin Portal and User Portal core functionalities.
2. **Phase 2**: Integration of fund transfer features and admin dashboard enhancements.
3. **Phase 3**: Deployment to production and user acceptance testing.

---

## Sprint Backlog

The sprint backlog consists of the prioritized tasks planned for the current sprint.

### Sprint 1 Goals
- Develop CRUD functionalities for the Admin Portal.
- Implement user registration and login for the User Portal.
- Set up CI/CD pipelines for Dev and UAT environments.

### Sprint 2 Goals
- Add fund transfer functionality with validation checks.
- Enhance the admin dashboard with filtering options.
- Finalize production deployment.

---

## Sprint Planning Ceremony

### Objectives
- Define sprint goals and backlog items.
- Estimate effort and assign tasks to the team.
- Ensure alignment with the product vision and roadmap.

### Key Activities
1. Review prioritized backlog items.
2. Break down user stories into actionable tasks.
3. Confirm team capacity and commitment.

---

## Daily Scrum Meetings

### Purpose
To provide a quick update on progress, identify blockers, and ensure alignment toward sprint goals.

### Format
- **Duration**: 15 minutes.
- **Focus**:
  1. What did you accomplish yesterday?
  2. What will you do today?
  3. Are there any blockers?

---

## Scrum Methodology

Scrum provides an iterative and incremental approach to project management and product delivery. Key principles include:
- **Transparency**: All work is visible to stakeholders.
- **Inspection**: Regular reviews of progress ensure alignment.
- **Adaptation**: Changes are incorporated dynamically.

---

## Collaboration Strategy

Effective collaboration is crucial for project success. Our strategy includes:
1. **Regular Communication**: Daily scrums, Slack channels, and email updates.
2. **Feedback Loops**: Sprint reviews to gather stakeholder feedback.
3. **Tool Integration**: Azure DevOps for backlog and sprint management, GitHub for code collaboration.
4. **Cross-Functional Teamwork**: Encourage open discussions between developers, designers, and stakeholders.

---

_This document is maintained by the Product Owner and will be updated regularly to reflect the current project status._
