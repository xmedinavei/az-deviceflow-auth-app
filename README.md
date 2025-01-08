# 🔐 Azure AD Authentication with MSAL and Microsoft Graph in Python

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

- Cloud Architecture
- Azure Development
- Identity & Security
- Infrastructure as Code

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/xmedinavei)

> 💡 Feel free to reach out if you have questions about this project or want to discuss cloud infrastructure solutions!

For more details about MSAL, see [MSAL Python Documentation](https://github.com/AzureAD/microsoft-authentication-library-for-python)
