# Product Owner Documentation

## Table of Contents

- [Product Vision and Mission](#product-vision-and-mission)
- [Product Vision Board](#product-vision-board)
- [Minimum Viable Product (MVP)](#minimum-viable-product-mvp)
- [Objective and Key Results (OKRs)](#objective-and-key-results-okrs)
- [Product Backlog](#product-backlog)
- [Product Roadmap](#product-roadmap)
- [Sprint Backlog](#sprint-backlog)
- [Sprint Planning Ceremony](#sprint-planning-ceremony)
- [Daily Scrum Meetings](#daily-scrum-meetings)
- [Scrum Methodology](#scrum-methodology)
- [Collaboration Strategy](#collaboration-strategy)

---

## Product Vision and Mission

### Product Vision

Empowering young adults with secure, user-friendly banking to achieve financial goals.


### Product Mission

IE Bank is a platform that aims to deliver accessible, reliable and secure banking experiences that prioritize simplicity and user empowerment for young adults who are finance beginners. Through innovation and commitment to continuous improvements, we aim to simplify personal finance management, prompt financial inclusion and set the new standard for digital banking for younger adults.  

---

## Product Vision Board

<img width="1129" alt="Screenshot 2024-12-07 at 14 20 16" src="https://github.com/user-attachments/assets/1a2562da-91b7-4aa0-b26d-2475f61d61e0">


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

The product backlog was organized into 6 sections, each epics representing the different roles in our team for this sprint. Planning and Strategy is for the product owner, Architecture Design and Planning for the cloud architect, Implement Core Banking Features For MVP is a focus for the full stack developers, Establish Robust Infrastructure for CI/CD and Hosting is for the full stack developers and the infrastructure developers, Implementing Advanced Strategies for the cyber security engineer and Implementing Monitoring Strategy and Reliability for the site reliability engineer. Each epic is broken down into features, user stories and tasks so that each member can achieve their roles efficiently.

---

## Product Roadmap

Link for [Product Roadmap](https://github.com/users/talineshawwaa/projects/3/views/4)

The product roadmap focuses on how our next 4 fiscal quarters are going to look like. The first quarter (the one we are in) focuses on getting the app up and running, setting up security and monitoring strategies and implementing CI/CD. The first and second quarters also focus on deploying to production and ensuring all features of the app are working. The third and fourth quarters focus on receiving feedback from the users, making the app better and more user friendly, and start marketing it to the users to compete with bigger competitors in the market and stand out to new potential users.

---

## Sprint Backlog

Link for [Sprint Backlog](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_sprints/backlog/Software-Development-and-Devops-Assignment%20Team/Software-Development-and-Devops-Assignment/Sprint%201) on Azure DevOps Boards

This link contains all the user stories and tasks for each feature based on the epics in the product backlog. These user stories were written from the perspective of the users and the developers, depending on the user story. It was associated with an acceptance criteria and list of tasks so that it meets user needs and the team can perform tasks efficiently.

---

## Sprint Planning Ceremony

Link for [Sprint Planning Ceremony](https://drive.google.com/drive/folders/1MIUTjas9CrbjAQA3bDOTuj3iRrXdAbb6?usp=drive_link) which is the first video in the file.

We had 3 recorded daily scrum meetings, as the rest were conducted in person which was a bit difficult. Each meeting focused on discussing what everyone has accomplished since our last meeting, what they are doing right now and what they are going to do next. Also in such meetings we tried to cover any concerns and ask each other questions because the success of this project relies on heavy collaboration. In the video Scrum meeting 1, we performed the sprint planning and backlog refinement to make sure that everyone fully understood the backlog and how to use it. Also, I continuously updated the backlog for refinements and when I receive feedback I update the backlog so it aligns as much as possible with our sprint.

---

## Daily Scrum Meetings

### Purpose
Link for [Daily Scrum Meetings](https://drive.google.com/drive/folders/1MIUTjas9CrbjAQA3bDOTuj3iRrXdAbb6?usp=drive_link) which is found in the Drive-

### Format
- **Duration**: 15-20 minutes.
- **Focus**:
  1. What have you achieved so far?
  2. What are you doing now?
  3. What are you doing next?
  4. Do you have any blockers?

---

## Scrum Methodology

Everything previously mentioned contributed to implementing the Scrum methodology in this sprint, these are the following methodologies that were used:
1.  I ensured we implemented all concepts and principles from the agile methodology for planning and collaborating. This sprint relied on the communication and efficient collaboration between different team members in order to get work down, especially between the infrastructure developer and all other team members to ensure efficient deployment to production.
2.  A backlog was prepared and continuously refined by me (product owner) throughout the sprint, so that the team members can have a sense of direction and we used the user stories to make sure we are satisfying customer needs and remain user-centric
3.  Daily scrum meetings were carried out as much as possible and as long as needed so that everyone is updated of the other’s progress, cover any doubts and to make sure everyone is on track at that point in the sprint
4.  A sprint review was conducted on 29/11 to show what we have completed in this sprint, each team member gave an update, we presented our demo in the UAT environment, discussed technical debt of the sprint and what we aim to complete next. The sprint review also reflected how team collaboration was essential in completing all tasks in this sprint.
5.  A sprint retrospective was conducted on 4/12 to show what each member believed was done well, what should be improved and shout outs. The general consensus showed that our strongest factor was the team dynamic and collaboration. Each team member however saw ways in which they can contribute improvements to the next sprint. As for the shout outs, it can be clearly seen how in a way each member was thankful for the help of almost everyone.

---

## Collaboration Strategy

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

_This document is maintained by the Product Owner and will be updated regularly to reflect the current project status._
