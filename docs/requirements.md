# Functional and Non-Functional Requirements

This section outlines the functional features and non-functional attributes of the system.

---

## Functional Requirements

### Admin Portal - Bank Users Management System

This allows bank administrators to access, manage, and control users’ accounts. Through this portal, the admins can view, create, update, and delete bank users’ accounts. This consists of the following main features:

1. Administrators' accounts will have a default username and password. Once these credentials are used and the login is successful, the admins can access the users’ management portal.
2. Once logged in to the users’ portal, the administrator can:
   - List all users
   - Create new users
   - Update existing user details
   - Delete users and their passwords.
[**User story**](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_workitems/edit/163/) 
### User Portal - Bank Account Management System

This allows users to access their account management portals and associate more than one bank account with their user profile. This consists of the following features:

1. New users can register on IE Bank by filling out a form containing their username, password, and confirmation of their password. When a new user is registered, a new account will be provided by default with a random account number.
[**User story:**](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_workitems/edit/170/) 

2. Users can log in to the application using their username and password. Once login is successful, they can only view their own:
   - Bank accounts
   - Transaction details
[**User story:**](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_workitems/edit/173/) 

3. Users can perform transactions, primarily transferring money to another account. This is done by entering the:
   - Recipient’s account number
   - Amount to be transferred
[**User story:** ](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_workitems/edit/176/)

4. Users will be able to create accounts to manage their funds.
[**User story:** ](https://dev.azure.com/tshawwa/Software-Development-and-Devops-Assignment/_workitems/edit/437/)
---

## Non-Functional Requirements

### Basic Authentication
1. The application must implement a basic user or admin authentication system requiring users to enter their username and password to log in and access their respective accounts.
2. Authentication needs to remain simple. The business analysts of IE Bank do not expect the usage of complex authentication methods, such as biometrics, tokens, or OAuth, at this time.

### Security Compliance
1. Apply encryption to user credentials and store these credentials securely in a database by hashing the passwords.
2. Ensure that users’ sensitive information is securely stored to protect privacy and data integrity.

### Simple User Interface
1. The user interface must focus on ensuring that all functionalities and requirements are satisfied and executed successfully.
2. Minimal emphasis will be placed on the aesthetic aspects of the frontend to prioritize usability and simplicity.

