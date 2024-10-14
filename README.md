# 🗳️ ElectEU - Online Election System

Welcome to **ElectEU**! 🎉 ElectEU is a secure, reliable, and user-friendly online voting system designed for European citizens to cast their votes easily from anywhere. This app incorporates **two-factor authentication (2FA)** using Google Authenticator to ensure that voting is both secure and trustworthy.

> **Note:** If you want the app to work with HTTPS, please request the necessary keys from the developers.

## 🌟 Features:

- 🛡️ **Two-Factor Authentication (2FA)** for added security
- 🔐 **Bearer Token** authentication for secure voting
- ✅ Easy-to-use API for registration, authentication, and voting

---

## 🚀 Quick Start Guide

### 📋 Prerequisites

- Install [Postman](https://www.postman.com/downloads/) for API testing.
- Ensure you have **Google Authenticator** installed on your phone:
  - **Android**: [Download Here](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
  - **iOS**: [Download Here](https://apps.apple.com/us/app/google-authenticator/id388497605)
- Install **Docker Desktop** to run the application with Docker Compose. You can download it [here](https://www.docker.com/products/docker-desktop).

### 🐳 Running the App with Docker Compose

To run the ElectEU application, you'll need to use Docker Compose. Follow these steps:

1. Open your terminal and navigate to the project directory.
2. If needed, run the following command to stop any currently running containers:

```bash
   docker-compose down
```

3. Build the Docker images with the following command:

```bash
   docker-compose down
```

4. Start the application:

```bash
   docker-compose up
```

Once the application is running, you can access the Voting App at http://localhost:5000 and the Authentication Service at http://localhost:5001.

## ⚙️ Functionality & API Workflow

### Step 1: Register a Citizen 📝

Send a `POST` request to **http://localhost:5000/register** to register a new user in the system.

#### Example Request Body:

```json
{
  "user_id": 123,
  "email": "ElectEU@gmail.com",
  "password": "123"
}
```

If the registration is successful, you will receive a confirmation message:

#### Example Response:

```json
{
  "message": "Citizen created succesfully"
}
```

### Step 2: Activate 2FA Authentication 🔐

Send a `POST` request to **http://localhost:5001/register** to activate 2FA with Google Authenticator. This will send a QR code to the user’s email for scanning with the Google Authenticator app.

#### Example Request Body:

```json
{
  "email": "ElectEU@gmail.com",
  "password": "123"
}
```

If the registration is successful, you will receive a confirmation message:

#### Example Response:

```json
{
  "message": "Registration successful, scan the QR code in Google Authenticator",
  "secret": "W3ZQMGCOYPUZEX34C4G2FU4DNWROADFZ"
}
```

If the email and password are correct, a QR code will be sent to the user’s email.
**Scan the QR code using the Google Authenticator app to get the 6-digit code.**

Here's how the app should look like:

<img src="images/auth_app.jpg" alt="Google Authenticator App" width="300"/>

### Step 3: Verify 2FA Code ✅

Send a `POST` request to **http://localhost:5001/verify-2fa** to verify the 6-digit code generated by the Google Authenticator app.

#### Example Request Body:

```json
{
  "user_id": 123,
  "email": "ElectEU@gmail.com",
  "code": 841165
}
```

If the code is valid, you will receive a **Bearer token** in the response. This token is needed to vote in the election.

#### Example Response:

```json
{
  "message": "2FA verification successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImVtYWlsIjoiY2FybG9zYXJib25lczAzQGdtYWlsLmNvbSIsImV4cCI6MTcyODkwMjA5N30.aMcx7R4gg7E0FlIK54evqe_j-744Ab34IgTyzl0j-vQ"
}
```

### Step 4: Submit Your Vote 🗳️

Send a `POST` request to **http://localhost:5000/vote** to cast your vote. You must include the Bearer token you received from the 2FA verification step.

#### Steps in Postman:

1. **Go to the "Authorization" tab** in Postman.
2. Select **"Bearer Token"** from the dropdown.
3. **Paste your token** into the token field.

Here's how it looks:

<img src="images/bearer_token.png" alt="Bearer token" width="800"/>

#### Example Request Body:

```json
{
  "user_id": 123,
  "vote_option_id": 2
}
```

Once the vote is submitted successfully, you will receive a confirmation message.

#### Example Response:

```json
{
  "message": "Vote submitted successfully"
}
```

## 🔧 Additional Features

In addition to the core functionalities, ElectEU offers several additional features for managing votes and users.

### 1. Get Votes 🗳️

To retrieve the list of votes, send a `GET` request to **http://localhost:5000/votes**.

#### Example Response:

```json
[
  {
    "user_id": 123,
    "vote_option_id": 2
  }
]
```

### 2. Get Users 👥

To retrieve the list of registered users, send a `GET` request to **http://localhost:5000/users**.

#### Example Response:

```json
[
  {
    "admin_rights": false,
    "email": "ElectEU@gmail.com",
    "password": "123",
    "user_id": 123
  }
]
```

### 3. Get Current Election 📅

To retrieve information about the current election, send a `GET` request to **http://localhost:5000/election**.

#### Example Response:

```json
{
  "date": "06-10-2024",
  "election_id": 1,
  "vote_options": [
    {
      "candidates": ["name0", "name1", "name2"],
      "party_name": "party1",
      "photo": "photo1",
      "vote_option_id": 1
    },
    {
      "candidates": ["name0", "name1", "name2"],
      "party_name": "party2",
      "photo": "photo2",
      "vote_option_id": 2
    },
    {
      "candidates": ["name0", "name1", "name2"],
      "party_name": "party3",
      "photo": "photo3",
      "vote_option_id": 3
    }
  ]
}
```

### 4. Delete User ❌

To delete a user, send a `DELETE` request to **http://localhost:5000/user** with the user ID in the request body.

#### Example Request Body:

```json
{
  "user_id": 123
}
```

If the deletion is successful, you will receive the following response:

#### Example Response:

```json
{
  "message": "User deleted successfully."
}
```

## 🎉 Congratulations! 🎉

You’ve successfully registered, authenticated, and voted in ElectEU! Keep your Bearer token safe, and ensure to follow the security measures during the voting process. 🛡️

You can also use the different functionalities of the system to explore more features, such as:

- **Viewing registered users**
- **Retrieving current election details**
- **Checking the votes cast**
- **Deleting users**

These functionalities enhance your interaction with the ElectEU system and provide you with more insights into the voting process. Enjoy using ElectEU! 🎊
