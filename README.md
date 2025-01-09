# 🔐 Azure AD Authentication with MSAL and Microsoft Graph in Python

[![Python](https://img.shields.io/badge/python-3.11-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Azure AD](https://img.shields.io/badge/Azure%20AD-Authentication-0078D4?style=flat&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/services/active-directory/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![MSAL](https://img.shields.io/badge/MSAL-Microsoft%20Auth-5E5E5E?style=flat&logo=microsoft&logoColor=white)](https://github.com/AzureAD/microsoft-authentication-library-for-python)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 🐳 Fully containerized solution for secure Microsoft Graph integration

This project demonstrates Azure Active Directory (Azure AD) authentication using the Microsoft Authentication Library (MSAL) in a containerized Python console application. The app authenticates users, interacts with Microsoft Graph API to manage user data and calendar events.

## ✨ Features

1. 🔑 Secure device code authentication flow
2. 👤 User profile information retrieval
3. 📅 Calendar management (view & create events)
4. 🐳 Docker containerization for easy deployment

Example output:

```plaintext
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABCD-EFGH to authenticate.

Welcome, John Doe!

Your upcoming calendar events:
1. Subject: Weekly Team Meeting
   Organizer: Jane Smith
   Start: 2023-12-01T10:00:00
   End:   2023-12-01T11:00:00

2. Subject: Project Review
   Organizer: Bob Johnson
   Start: 2023-12-02T14:00:00
   End:   2023-12-02T15:00:00

Your meeting was created with the following details:
Subject: Study for the AZ-204 exam
Location: Wherever you are
Start: 2023-12-01T15:05:00
End: 2023-12-01T15:35:00
```

## 🏗️ Application Architecture

This application leverages **Microsoft Entra ID (Azure AD)** for secure user authentication and **Microsoft Graph API** for accessing Microsoft 365 resources. The app is containerized using Docker and uses the **Device Flow** authentication mechanism, allowing seamless communication between the user's device and Azure cloud services.

<p align="center">
   <img src="./assets/msalapp-cloud-achitecture.png" alt="Cloud Architecture Diagram" width="600"/>
</p>

<p align="center">
   <em>Figure 1: Cloud Architecture showing the interaction between the containerized application, Microsoft Entra ID, and Microsoft Graph API</em>
</p>

### Cloud Components

#### 1. Microsoft Entra ID (Azure AD)

- **Authentication and Token Issuance**:
  - Handles user authentication using the **Device Flow**
  - Issues:
    - **Access Token**: For Microsoft Graph API access
    - **ID Token**: For user identity validation
    - **Refresh Token**: For token renewal

#### 2. App Registration

- **Purpose**: Defines app identity and permissions
- **Key Configuration**:
  - Public Client Flow enabled
  - API Permissions:
    - `User.Read`: Profile access
    - `Calendars.ReadWrite`: Calendar management

#### 3. Microsoft Graph API

- **Data Access Layer**:
  - Profile data via `/me` endpoint
  - Calendar management via `/me/events` endpoint

### Application Flow

1. **Initial Request** 🔄

   ```plaintext
   App -> Azure AD: Request device code
   Azure AD -> App: Returns code + verification URL
   ```

2. **User Authentication** 🔐

   ```plaintext
   User -> Browser: Opens microsoft.com/devicelogin
   User -> Browser: Enters device code
   Browser -> Azure AD: Completes authentication
   ```

3. **Token Acquisition** 🎟️

   ```plaintext
   App -> Azure AD: Polls for tokens
   Azure AD -> App: Returns access & refresh tokens
   ```

4. **API Integration** 📡

   ```plaintext
   App + Access Token -> Microsoft Graph: API requests
   Microsoft Graph -> App: Returns requested data
   ```

## 🚀 Quick Start

1. **Clone and Setup**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set Up Environment**:

   > ⚠️ **Critical Step**: Create `.env` from template and add your Azure credentials!

   ```env
   CLIENT_ID=your-client-id-from-azure-portal
   TENANT_ID=your-tenant-id-from-azure-portal
   ```

3. **Run with Docker**:

   ```bash
   docker build -t azure-ad-auth-demo .
   docker run --rm -it --env-file .env azure-ad-auth-demo
   ```

## 📋 Prerequisites

### Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to Microsoft Entra ID > App registrations
3. Click "New registration"
4. Set a name for your application
5. Select "Accounts in this organizational directory only"
6. Click Register

After registration:

1. Note down the following values (you'll need them later):

   - **Application (client) ID** - Found on the app registration Overview page
   - **Directory (tenant) ID** - Also found on the Overview page

2. Configure the app for public client flow:

   - Go to Authentication
   - Scroll to "Advanced settings"
   - Under "Allow public client flows", toggle to "Yes"
   - Add a Mobile and desktop redirect URI (e.g., <http://localhost>)
   - Save changes

3. Set API Permissions:
   - Go to "API permissions"
   - Add "Microsoft Graph" permissions:
     - User.Read (for profile access)
     - Calendars.ReadWrite (for viewing and creating calendar events)
   - Click "Grant admin consent"

### Environment Setup

1. In the root directory of the project, you'll find a `.env.template` file
2. Create a new file named `.env` in the same directory
3. Copy the contents from `.env.template` to `.env`
4. Fill in your values from the Azure AD app registration:

   ```env
   CLIENT_ID=your-application-client-id
   TENANT_ID=your-directory-tenant-id
   ```

> ⚠️ **Important**: The `.env` file is required for the application to work. Without proper credentials, the authentication will fail.

## Authentication Flow

1. When you run the app, it will display a device code
2. Open a browser and go to <https://microsoft.com/devicelogin>
3. Enter the provided code
4. Sign in with your Azure AD credentials
5. Return to the console app to see your profile and calendar information

## Project Structure

```text
├── assets/           # Project assets and diagrams
│   └── msalapp-cloud-architecture.png
├── .env              # Environment variables (git and docker ignored)
├── .env.template     # Template for environment variables
├── auth_app.py       # Main application
├── requirements.txt  # Dependencies
├── Dockerfile        # Container configuration
└── README.md         # Documentation
```

## Microsoft Graph Features

The application demonstrates several Microsoft Graph API capabilities:

1. **User Profile Access**

   - Fetches user's display name and basic information
   - Uses Microsoft Graph `/me` endpoint

2. **Calendar Management**

   - Lists upcoming calendar events (up to 5)
   - Creates new calendar events automatically
   - Supports custom event duration
   - Uses Microsoft Graph `/me/events` endpoints

3. **Authentication**
   - Device code flow for headless authentication
   - Token management and caching
   - Secure scope handling

## Development Notes

- **Token Cache**: Located at `msal_token_cache.bin` (container-scoped)
- **Security**: Credentials passed as runtime parameters
- **Environment**: Copy `.env.template` to `.env` and fill in your values
- **Dependencies**: Update `requirements.txt` and rebuild container as needed

## 🔒 Security Notes

- Environment variables are used for sensitive configuration
- Token cache is container-scoped
- The .env file is excluded from Docker builds
- Public client flow is secured by Azure AD's device code flow

## 🤝 Let's Connect!

Are you passionate about Cloud Infrastructure and Azure solutions? Let's connect and discuss more about:

- Software Engineering
- Cloud Architecture
- Infrastructure as Code
- Generative AI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/xmedinavei)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/xmedinavei)
[![Blog](https://img.shields.io/badge/Tech%20Blog-Read%20More-3B82F6?style=for-the-badge&logo=hashnode&logoColor=white)](https://xaviermedina.hashnode.dev/)

> 💡 Feel free to reach out if you have questions about this project or want to discuss cloud infrastructure solutions!

For more details about MSAL, see [MSAL Python Documentation](https://github.com/AzureAD/microsoft-authentication-library-for-python)
