# Infrastructure Developer Documentation

## Overview

This document provides a comprehensive overview of our infrastructure setup for the **MONEY404-Bank** web application. It details our **Infrastructure as Code (IaC)** practices, resource configurations, deployment strategies, and the modularization approach adopted using **Azure Bicep** templates. The goal is to ensure clarity, maintainability, and scalability across Development (Dev), User Acceptance Testing (UAT), and Production (Prod) environments.

### Table of Contents

- [Infrastructure as Code (IaC) Strategy](#infrastructure-as-code-iac-strategy)
  - [Modularization Strategy](#modularization-strategy)
  - [Resource Dependency Graph](#resource-dependency-graph)
- [Environment Configurations](#environment-configurations)
  - [Parameter Files](#parameter-files)
  - [Key Configurations](#key-configurations)
- [Resource Modules and Bicep Files](#resource-modules-and-bicep-files)
  - [Applications Modules](#applications-modules)
  - [Databases Modules](#databases-modules)
  - [Infrastructure Modules](#infrastructure-modules)
  - [Orchestrators](#orchestrators)
- [Implementing Container Hosting](#implementing-container-hosting)
- [Continuous Integration and Continuous Deployment (CI/CD)](#continuous-integration-and-continuous-deployment-cicd)
  - [Workflow Configuration](#workflow-configuration)
  - [Secrets Management](#secrets-management)
  - [Rollback Strategy](#rollback-strategy)
  - [Security and Compliance](#security-and-compliance)
- [Static Web App Deployment](#static-web-app-deployment)
- [Deployment Process](#deployment-process)
- [Links to Code Repositories](#links-to-code-repositories)

---

## Infrastructure as Code (IaC) Strategy

Our infrastructure is defined and managed using **Infrastructure as Code (IaC)** principles, leveraging **Azure Bicep** templates for declarative resource provisioning. We have adopted a modularization strategy to enhance reusability, maintainability, and clarity.

### Modularization Strategy

**Modularity** is about designing our code in such a way that it's composed of smaller, interchangeable components. Each module represents an Azure service, encapsulating its configuration and deployment logic. Our main goals with modularization are:

- **Maintainability**: Isolating components to make updates and debugging more manageable.
- **Reusability**: Enabling modules to be reused across different environments and projects.
- **Scalability**: Facilitating the addition of new modules without impacting existing ones.
- **Testability**: Simplifying testing by dealing with smaller, isolated modules.
- **Flexibility**: Allowing easy swapping of modules with the same interface.

#### Directory Structure

The infrastructure is broken down into logical components, each encapsulated within its own module. These modules are organized into directories based on their functionality:

- **`modules/`**: The root directory for all modular templates.
  - **`applications/`**: Contains modules related to application services, such as App Service Plans and App Services for the frontend and backend.
  - **`databases/`**: Contains modules for deploying database resources, including PostgreSQL Flexible Server and databases.
  - **`infrastructure/`**: Contains shared infrastructure modules, such as Key Vault, Log Analytics Workspace, Application Insights, and Azure Container Registry.
- **`main.bicep`**: Orchestrates the deployment of all modules based on input parameters.

#### Benefits of Modularization

- **Maintainability**: Changes to a specific component can be made in one place without affecting other parts of the infrastructure.
- **Reusability**: Modules can be reused across different environments with varying configurations.
- **Scalability**: Supports the evolving needs of our application and organization by allowing for easy addition of new modules or services.
- **Testability**: Smaller, isolated modules are simpler to test for correctness.
- **Flexibility**: Swapping out one module for another with the same interface becomes straightforward.

### Resource Dependency Graph

The following diagram illustrates the dependencies between modules:

![image(5)](https://github.com/user-attachments/assets/92a9b070-910e-45c5-9441-1105de680d01)


---

## Environment Configurations

We have defined separate configurations for each environment—**Development (Dev)**, **User Acceptance Testing (UAT)**, and **Production (Prod)**—using JSON parameter files. This approach allows us to customize resource names, locations, and settings per environment while maintaining a single codebase for our Bicep templates.

### Parameter Files

- **Development**: [dev.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/dev.parameters.json)
- **UAT**: [uat.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/uat.parameters.json)
- **Production**: [prod.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/prod.parameters.json)

#### Key Configurations

- **Resource Names**: Prefixed with the environment identifier (e.g., `money404-asp-dev` for Dev).
- **Locations**: Azure regions are chosen based on proximity and compliance requirements.
- **SKUs and Tiers**: Adjusted based on the environment to optimize cost and performance.
- **Access and Security**:
  - **Key Vault Role Assignments**: Assigns appropriate roles to service principals and groups.
  - **Secrets Management**: Credentials and keys are stored securely in Azure Key Vault.
- **Monitoring and Diagnostics**:
  - **Application Insights and Log Analytics**: Configured for comprehensive monitoring.
  - **Diagnostic Settings**: Enabled for services like Key Vault, ACR, and PostgreSQL.

#### Rationale for Using JSON Parameter Files

We chose to use JSON files for parameterization to ensure:

- **Ease of Migration**: JSON is widely supported and facilitates easier migration to other IaC tools if needed.
- **Interoperability**: Enhances compatibility with various tools and services that consume JSON.
- **Separation of Concerns**: Keeps environment-specific configurations separate from the main templates, promoting cleaner code and easier management.

---

## Resource Modules and Bicep Files

Our infrastructure modules are designed to be reusable and environment-agnostic, relying on parameterization for customization. Below is a detailed overview of each module and its purpose.

### Applications Modules

#### 1. **app-service-plan.bicep**

- **Purpose**: Deploys an Azure App Service Plan.
- **File**: [app-service-plan.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/app-service-plan.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `appServicePlanName`: Name of the App Service Plan.
  - `skuName`: SKU tier (`B1`, `F1`, etc.).
- **Outputs**:
  - `id`: Resource ID of the App Service Plan.
- **Environment-Specific Configurations**:
  - `appServicePlanName`
  - `skuName`

#### 2. **backend-app-service.bicep**

- **Purpose**: Deploys the backend service using a Docker container.
- **File**: [backend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/backend-app-service.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `appServiceAPIAppName`: Name of the backend App Service.
  - `appServicePlanId`: ID of the associated App Service Plan.
  - `containerRegistryName`: Name of the Azure Container Registry.
  - `dockerRegistryUserName`, `dockerRegistryPassword`: Credentials for the container registry.
  - `dockerRegistryImageName`, `dockerRegistryImageTag`: Docker image details.
  - `appSettings`: Array of custom environment variables for the backend service.
  - `appInsightsInstrumentationKey`, `appInsightsConnectionString`: Monitoring configurations.
- **Outputs**:
  - `appServiceAppHostName`: Hostname of the App Service.
  - `systemAssignedIdentityPrincipalId`: Principal ID of the managed identity.
- **Environment-Specific Configurations**:
  - `appServiceAPIAppName`
  - `dockerRegistryImageTag`
  - `appSettings`

#### 3. **frontend-app-service.bicep**

- **Purpose**: Deploys the frontend service for the website.
- **File**: [frontend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/frontend-app-service.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `appServiceAppName`: Name of the frontend App Service.
  - `appServicePlanId`: ID of the associated App Service Plan.
  - `appCommandLine`: Command line to run for the App Service.
  - `appInsightsInstrumentationKey`, `appInsightsConnectionString`: Monitoring configurations.
  - `name`: Name of the Static Web App.
  - `locationswa`: Deployment location for the Static Web App.
  - `sku`: SKU tier for the Static Web App (`Free`, `Standard`).
- **Outputs**:
  - `appServiceAppHostName`: Hostname of the App Service.
  - `staticWebAppUrl`: URL of the Static Web App.
  - `staticWebAppEndpoint`: Endpoint of the Static Web App.
  - `staticWebAppResourceName`: Resource name of the Static Web App.
- **Environment-Specific Configurations**:
  - `appServiceAppName`
  - `name`
  - `sku`

### Databases Modules

#### 1. **postgres-sql-server.bicep**

- **Purpose**: Deploys a PostgreSQL Flexible Server.
- **File**: [postgres-sql-server.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/databases/postgres-sql-server.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `environmentType`: Environment type (`nonprod`, `prod`).
  - `postgresSQLServerName`: Name of the PostgreSQL server.
  - `postgreSQLAdminServicePrincipalObjectId`: Object ID for Active Directory authentication.
  - `postgreSQLAdminServicePrincipalName`: Name for the service principal.
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace for diagnostics.
- **Outputs**:
  - `postgresSQLServerName`: Name of the PostgreSQL server.
- **Environment-Specific Configurations**:
  - `postgresSQLServerName`
  - `environmentType`

#### 2. **postgres-sql-database.bicep**

- **Purpose**: Deploys a database within an existing PostgreSQL server.
- **File**: [postgres-sql-database.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/databases/postgres-sql-database.bicep)
- **Parameters**:
  - `postgresSQLServerName`: Name of the existing PostgreSQL server.
  - `postgresSQLDatabaseName`: Name of the database to create.
- **Outputs**:
  - `postgresSQLDatabaseName`: Name of the PostgreSQL database.
- **Environment-Specific Configurations**:
  - `postgresSQLDatabaseName`

### Infrastructure Modules

#### 1. **keyvault.bicep**

- **Purpose**: Deploys an Azure Key Vault.
- **File**: [keyvault.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/keyvault.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `keyVaultName`: Name of the Key Vault.
  - `roleAssignments`: Array of role assignments for the Key Vault.
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace for diagnostics.
- **Outputs**:
  - `keyVaultName`: Name of the Key Vault.
  - `keyVaultResourceId`: Resource ID of the Key Vault.
- **Environment-Specific Configurations**:
  - `keyVaultName`
  - `roleAssignments`

#### 2. **log-analytics.bicep**

- **Purpose**: Deploys a Log Analytics Workspace.
- **File**: [log-analytics.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/log-analytics.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `name`: Name of the Log Analytics Workspace.
- **Outputs**:
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace.
  - `logAnalyticsWorkspaceName`: Name of the Log Analytics Workspace.
- **Environment-Specific Configurations**:
  - `name`

#### 3. **app-insights.bicep**

- **Purpose**: Deploys an Application Insights resource.
- **File**: [app-insights.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/app-insights.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `appInsightsName`: Name of the Application Insights resource.
  - `logAnalyticsWorkspaceId`: ID of the associated Log Analytics Workspace.
  - `keyVaultResourceId`: Resource ID of the Key Vault for storing secrets.
- **Outputs**:
  - `appInsightsInstrumentationKey`: Instrumentation Key for Application Insights.
  - `appInsightsConnectionString`: Connection String for Application Insights.
- **Environment-Specific Configurations**:
  - `appInsightsName`

#### 4. **container-registry.bicep**

- **Purpose**: Deploys an Azure Container Registry (ACR).
- **File**: [container-registry.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/container-registry.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `registryName`: Name of the container registry.
  - `sku`: SKU tier (`Basic`, `Standard`, `Premium`).
  - `keyVaultResourceId`: Resource ID of the Key Vault for storing secrets.
  - `keyVaultSecretNameAdminUsername`, `keyVaultSecretNameAdminPassword0`, `keyVaultSecretNameAdminPassword1`: Names for storing ACR credentials.
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace for diagnostics.
- **Environment-Specific Configurations**:
  - `registryName`
  - `sku`

### Orchestrators

#### 1. **database.bicep**

- **Purpose**: Orchestrates the deployment of the PostgreSQL server and database.
- **File**: [database.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/database.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `environmentType`: Environment type (`nonprod`, `prod`).
  - `postgresSQLServerName`: Name of the PostgreSQL server.
  - `postgresSQLDatabaseName`: Name of the database.
  - `postgreSQLAdminServicePrincipalObjectId`, `postgreSQLAdminServicePrincipalName`: AD authentication details.
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace.
- **Environment-Specific Configurations**:
  - `postgresSQLServerName`
  - `postgresSQLDatabaseName`

#### 2. **website.bicep**

- **Purpose**: Orchestrates the deployment of the entire website, including both frontend and backend applications.
- **File**: [website.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/website.bicep)
- **Parameters**:
  - `location`: Deployment location.
  - `appServicePlanName`: Name of the App Service Plan.
  - `appServiceAppName`, `appServiceAPIAppName`: Names of the frontend and backend services.
  - `staticappServiceAppName`: Name of the Static Web App.
  - `appInsightsName`: Name of the Application Insights resource.
  - `environmentType`: Environment type (`nonprod`, `prod`).
  - `containerRegistryName`: Name of the Azure Container Registry.
  - `dockerRegistryImageName`, `dockerRegistryImageTag`: Docker image details.
  - `keyVaultResourceId`: Resource ID of the Key Vault.
  - `logAnalyticsWorkspaceId`: ID of the Log Analytics Workspace.
- **Outputs**:
  - `appServiceAppHostName`: Hostname of the frontend App Service.
  - `staticWebAppEndpoint`: Endpoint of the Static Web App.
  - `staticWebAppResourceName`: Resource name of the Static Web App.
- **Environment-Specific Configurations**:
  - `appServicePlanName`
  - `appServiceAppName`
  - `appServiceAPIAppName`
  - `staticappServiceAppName`

#### 3. **main.bicep**

- **Purpose**: Orchestrates the deployment of all modules based on input parameters.
- **File**: [main.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/main.bicep)
- **Functionality**:
  - Calls the orchestrators `database.bicep` and `website.bicep`.
  - Passes environment-specific parameters to each module.
  - Ensures that dependencies are correctly managed.

---

## Implementing Container Hosting

### Transition to Containerization

As our application evolved, we recognized the need to containerize our backend services for better scalability and portability. We implemented container hosting using **Azure App Services for Linux Containers** and **Azure Container Registry (ACR)**.

### Azure Container Registry (ACR)

- **Purpose**: Stores Docker images for the backend application.
- **Configuration**:
  - **Name**: Environment-specific (e.g., `money404acrdev`).
  - **SKU**: Selected based on the environment (`Basic` for Dev/UAT, `Standard` or `Premium` for Prod).
  - **Admin User**: Enabled, and credentials are stored securely in Azure Key Vault.
  - **Diagnostics**: Configured to send logs and metrics to Log Analytics Workspace for monitoring.
- **Module File**: [container-registry.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/container-registry.bicep)

### Backend App Service Configuration

- **Runtime**: Configured to use Docker containers.
- **Image Source**: Pulls images from the ACR.
- **Authentication**: Uses admin credentials retrieved securely from Azure Key Vault.
- **Environment Variables**: Configured via `appSettings`, including database connection strings and other application settings.
- **Monitoring**: Integrated with Application Insights for performance monitoring and diagnostics.
- **Module File**: [backend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/backend-app-service.bicep)

### Security Enhancements

- **Managed Identity**: Enabled System-Assigned Managed Identity on the backend App Service to securely access Azure resources without embedding credentials.
- **Key Vault Integration**: Secrets and credentials are retrieved at runtime from Azure Key Vault, enhancing security posture.

---

## Continuous Integration and Continuous Deployment (CI/CD)

We have implemented a robust CI/CD pipeline using **GitHub Actions** to automate the deployment process across all environments. This ensures consistent and reliable deployments, reduces manual effort, and minimizes the risk of errors.

### Workflow Configuration

Our workflows are defined in [`.github/workflows/ie-bank-infra.yml`](https://github.com/smaswin21/Banking_Infra/blob/main/.github/workflows/ie-bank-infra.yml) and are consistent across repositories (backend, frontend, infra).

#### Triggers

1. **Development Deployment**:
   - **Trigger**: Push to any branch that is not `main`.
   - **Action**: Deploys to the `Development` environment.
   - **Condition**:
     ```yaml
     if: github.event_name == 'push' || github.event_name == 'workflow_dispatch'
     ```

2. **UAT Deployment**:
   - **Trigger**: Pull request targeting the `main` branch.
   - **Action**: Deploys to the `UAT` environment.
   - **Condition**:
     ```yaml
     if: github.event.pull_request.base.ref == 'main' || github.event_name == 'workflow_dispatch'
     ```

3. **Production Deployment**:
   - **Trigger**: Merge into the `main` branch.
   - **Action**: Deploys to the `Production` environment.
   - **Condition**:
     ```yaml
     if: github.event_name == 'push' && github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
     ```

4. **Manual Deployment**:
   - **Trigger**: Manual initiation via GitHub Actions.
   - **Action**: Allows deployment to any environment.
   - **Condition**:
     ```yaml
     github.event_name == 'workflow_dispatch'
     ```

### Jobs and Dependencies

- **Validation Jobs**: `validate_dev`, `validate_uat`, `validate_prod`—validate Bicep templates for syntax and schema correctness using `az bicep` commands.
- **Linting Job**: `lint`—runs the Bicep linter to enforce code quality.
- **Security Scanning**: `build`—uses **Checkov** for static code analysis to detect security vulnerabilities.
- **Deployment Jobs**:
  - **`deploy-dev`**:
    - **Needs**: `build`, `lint`, `validate_dev`.
    - **Environment**: `Development`.
    - **File**: [`.github/workflows/ie-bank-infra.yml`](https://github.com/smaswin21/Banking_Infra/blob/main/.github/workflows/ie-bank-infra.yml)
  - **`deploy-uat`**:
    - **Needs**: `build`, `lint`, `validate_uat`.
    - **Environment**: `UAT`.
    - **File**: [`.github/workflows/ie-bank-infra.yml`](https://github.com/smaswin21/banking_infra/blob/main/.github/workflows/ie-bank-infra.yml)
  - **`deploy-prod`**:
    - **Needs**: `build`, `lint`, `validate_prod`, `deploy-uat`.
    - **Environment**: `Production`.
    - **File**: [`.github/workflows/ie-bank-infra.yml`](https://github.com/smaswin21/banking_infra/blob/main/.github/workflows/ie-bank-infra.yml)

### Secrets Management

- **GitHub Secrets**: Used to store sensitive information required by GitHub Actions (e.g., Azure credentials).
- **Azure Key Vault**: Stores secrets like ACR credentials and Application Insights keys, accessed securely using managed identities.

### Rollback Strategy

- **Version Control**: All infrastructure code is tracked in Git, enabling easy rollback to previous stable versions.
- **IaC**: Allows us to redeploy previous configurations consistently.
- **Automated Testing**: Validation and linting steps catch issues before deployment.

### Security and Compliance

- **Access Controls**: Implemented Role-Based Access Control (RBAC) for resources.
- **Compliance Checks**: Infrastructure code is scanned for compliance with organizational policies using **Checkov**.
- **Secure Secrets Management**: All secrets are stored in Azure Key Vault and accessed via managed identities.

---

## Static Web App Deployment

### Rationale for Static Web Apps

**Azure Static Web Apps** provide an efficient and cost-effective way to host frontend applications with static content, offering global distribution and integrated CI/CD capabilities.

### Implementation Approach

We created a custom Bicep module, `frontend-app-service.bicep`, to deploy our Static Web App.

- **Benefits**:
  - **Full Control**: Allows customization to meet our specific requirements.
  - **Simplified Integration**: Seamlessly fits into our existing Bicep structure.
  - **Maintainability**: Easier to update and manage over time.

### Configuration Details

- **Parameters**:
  - `name`: Environment-specific Static Web App name (e.g., `money404-swa-dev`).
  - `sku`: Defined per environment (`Free` for Dev/UAT, `Standard` for Prod).
  - `locationswa`: Deployment location (e.g., `West Europe`).
- **Deployment**:
  - Integrated into the `website.bicep` orchestrator.
  - Utilizes environment-specific parameter files for customization.
- **Output Variables**:
  - `staticWebAppEndpoint`: Used to configure the frontend application deployment.
- **Module File**: [frontend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/frontend-app-service.bicep)

---

## Deployment Process

### Step-by-Step Deployment

1. **Code Commit and Push**:
   - Developers commit changes to their feature branches.
   - Upon push, the `deploy-dev` job is triggered for the Development environment.

2. **Validation and Linting**:
   - Bicep templates are validated for syntax errors using `az bicep`.
   - Linting ensures adherence to coding standards.

3. **Security Scanning**:
   - **Checkov** scans the infrastructure code for security vulnerabilities.

4. **Deployment to Development**:
   - Resources are deployed to the Development resource group.
   - Environment-specific parameters are applied.

5. **Pull Request and Merge**:
   - Developers create a pull request targeting the `main` branch.
   - The `deploy-uat` job is triggered upon pull request creation.

6. **Deployment to UAT**:
   - Resources are deployed to the UAT environment.
   - QA teams perform testing and validation.

7. **Approval and Production Deployment**:
   - Upon merge into `main`, the `deploy-prod` job can be manually triggered.
   - Requires prior successful deployment to UAT.

8. **Monitoring and Verification**:
   - Post-deployment, Application Insights and Log Analytics monitor the application.
   - Any issues are addressed promptly.

### Continuous Improvement

- **Feedback Loop**: Monitoring data informs infrastructure improvements.
- **Scalability**: Infrastructure can be scaled based on performance metrics.
- **Updates**: Modules can be updated independently to introduce new features or optimizations.

---

## Links to Code Repositories

- **Main Bicep File**: [main.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/main.bicep)
- **Modules Directory**: [modules/](https://github.com/smaswin21/Banking_Infra/tree/main/modules)
  - **Applications Modules**:
    - [app-service-plan.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/app-service-plan.bicep)
    - [backend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/backend-app-service.bicep)
    - [frontend-app-service.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/applications/frontend-app-service.bicep)
  - **Databases Modules**:
    - [postgres-sql-server.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/databases/postgres-sql-server.bicep)
    - [postgres-sql-database.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/databases/postgres-sql-database.bicep)
  - **Infrastructure Modules**:
    - [keyvault.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/keyvault.bicep)
    - [log-analytics.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/log-analytics.bicep)
    - [app-insights.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/app-insights.bicep)
    - [container-registry.bicep](https://github.com/smaswin21/Banking_Infra/blob/main/modules/infrastructure/container-registry.bicep)
- **Parameter Files**:
  - **Development**: [dev.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/dev.parameters.json)
  - **UAT**: [uat.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/uat.parameters.json)
  - **Production**: [prod.parameters.json](https://github.com/smaswin21/Banking_Infra/blob/main/parameters/prod.parameters.json)
- **CI/CD Workflows**:
  - **Infrastructure Build Workflow (CI)**: [ie-bank-infra.yml](https://github.com/smaswin21/Banking_Infra/blob/main/.github/workflows/ie-bank-infra.yml)
- **GitHub Actions Portal**: [Actions](https://github.com/smaswin21/Banking_Infra/actions)

---

By adopting this modular and automated approach to infrastructure deployment, we ensure consistency, security, and efficiency across all environments. The use of Azure Bicep and GitHub Actions enables us to maintain high standards of quality while supporting the evolving needs of the **MONEY404-Bank** web application.

---

> [!NOTE]
> For more detailed information on our infrastructure release strategy, please refer to the [Infrastructure Release Strategy](https://smaswin21.github.io/Banking_Infra/docs/infrastructure-release-strategy) section in our Design Document on GitHub Pages.
