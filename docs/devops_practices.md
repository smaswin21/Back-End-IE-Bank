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

### DTAP Environments
<!-- Description of the Development, Testing, Acceptance, and Production setup -->

### Infrastructure as Code (IaC)
<!-- Use of tools like Azure Bicep to automate infrastructure -->

---

## Collaboration and Tools

### Collaboration Tools
<!-- Tools used for team communication and task management -->

### Version Control Strategy
<!-- Branching strategy and GitHub workflow -->
