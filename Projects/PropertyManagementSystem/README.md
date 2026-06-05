
Project Structure:
The directory structure of the Property Management System project is as follows:

PropertyManagementSystem/
├── node_modules/              # Installed dependencies
├── public/                    # Front-end assets (HTML, CSS, JS)
│   └── index.html             # Landing page or home page
│   └── owner-dashboard.html   # Dashboard for property owners
│   └── staff-dashboard.html   # Dashboard for property staff
├── server.js                  # Main server file (backend logic)
├── package.json               # Project metadata and dependencies
└── package-lock.json          # Exact versions of installed dependencies

node_modules/: This directory contains all the installed Node.js dependencies.
public/: Contains the front-end HTML files (landing page and dashboards).
server.js: The main server file where Express is set up, routes are defined, and session handling is implemented.
package.json: Stores metadata about the project and its dependencies.
package-lock.json: Contains a detailed description of the dependency tree, ensuring consistent installations across different environments.


Project Setup:
Prerequisites: Node.js: Ensure that Node.js and npm (Node Package Manager) are installed on your machine. You can download and install them from the official website: Node.js.

Steps to Set Up the Project:
1. Navigate to the Project Folder: Once you have cloned or downloaded the repository, navigate into the PropertyManagementSystem directory.
cd PropertyManagementSystem

2. Install Dependencies: Initialize the project and install all necessary dependencies by running:
npm init -y
npm install express body-parser express-session
npm install socket.io
npm install openai
npm install node-fetch
npm install formdata-node

3. Running the Application
Once the dependencies are installed, you can start the server using the following command:
node server.js

4. This will start the backend server, and the application will be accessible in your browser at:
http://localhost:3000/


Credentials:
To log in to the application, use the following credentials:
    Owner 1:
        Username: owner1
        Password: password1

    Staff 1:
        Username: staff1
        Password: password2

    Owner 2:
        Username: owner2
        Password: 123