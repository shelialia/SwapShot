# Uniswap WETH-USDC Transactions

## Overview
This project is designed to showcase the transaction fees in USDT for all Uniswap WETH-USDC transactions. It includes real-time transaction monitoring with exchange rates and ensures up-to-date data on page reload. The architecture is designed for separation of concerns, maintainability, and scalability.

Please note that the data fetching on the frontend will take around 4-5 seconds when the website is first opened. Subsequent fetches will be faster. A delay will also occur for fetching information for a certain transaction and filtering.

### Use Cases
1. When no filter or search is applied, the page will fetch the 10,000 most recent transactions for display. User can click on each of the txn_ids in the table to see more information about the transaction (such as the date and time at which it took place, the fee in USDT and fee in ETH (calculated based on the historical exchange rate at the point of the time that the transaction occured, the exchange rate at that time, and the current exchange rate)
2. User can filter for transactions between start date and time, and end date and time.
3. User can search for a transaction based on the txn_id / txn_hash.
4. User can navigate to the next page by clicking on the page numbers.
5. User can change the number of rows seen on the page -- default set to 50 rows per page.
   
---

## Installation

### Prerequisites
- [Node.js](https://nodejs.org/en/) (version 16+)
- [Docker](https://www.docker.com/) (optional, if you're using Docker to run your application)
- [npm](https://www.npmjs.com/)

### Steps to Install
1. Clone the repository:
- cd into your desired workspace
- git clone https://github.com/shelialia/tokka_labs_engineering_challenge.git

2. Install dependencies:
- npm install

## Running the Application Locally (without Docker)
Once dependencies are installed, you can run the frontend using: npm run dev. This will start the frontend application at [http://localhost:5173](http://localhost:5173).
Then, run the backend using: 
1. cd backend
2. uvicorn app.main:app --reload
This will start the fastapi backend at [http://172.18.0.2:3000](http://127.0.0.1:8000).

## Using Docker (Optional -- Has Issues)
The frontend and the backend have been dockerized separately but there are some issues currently preventing full functionality.
Backend (FastAPI): The FastAPI container starts, but there is an issue related to the main module. This results in the following error:
ERROR:    Error loading ASGI app. Could not import module "main".
This indicates that the main.py file, which serves as the entry point for the ASGI app, could not be imported. Further investigation into the file structure and import paths is required.

Frontend (React): While the React container starts successfully and displays the server details, I am currently unable to access the frontend via localhost:3000 as expected. The frontend container outputs the following:
Serving!
- Local:    http://localhost:3000
- Network:  http://172.18.0.2:3000
Despite this, attempts to connect to the application on localhost:3000 result in a 404 error, and the frontend is not accessible. This suggests a potential issue with networking or port binding in the Docker configuration, which requires further debugging.

In a working scenario, we should be able to Build and Run the Docker containers: docker-compose up
Your backend will be running on: http://localhost:8000
Your frontend will be running on: http://localhost:3000
This command will build the images for both the backend and frontend, then start the containers.
If you only want to build the images without running them immediately, you can use: docker-compose build

## Testing
To run the test suite (made by Jest) for the frontend, use: npm run test. 
The test suite for the backend has been submitted in a separate folder due to issues with import errors resulting in the app not working. 

## Backend Architecture
The backend is designed with a clear separation of concerns to ensure maintainability and scalability.

### Backend:
- API Folder: All API endpoints are located here. This layer is responsible for setting up api endpoints and handling incoming requests.
- Services Folder: The business logic is decoupled from the API layer, ensuring a clean architecture where each service has its distinct responsibilities. The services layer is divided into four key areas:
1. Etherscan Service (etherscan.py): Handles interactions with the Etherscan API to fetch blockchain data.
2. Binance Service (exchange_services.py): Responsible for interacting with the Binance API to retrieve current exchange rates (e.g., ETH to USDT). Note that the Binance API is indeterministic (unable to return a float at certain times), therefore I have chosen to return 2000 in the event that it occurs. This prevents an error from being raised that could result in the backend service going down).
3. Helper Service (helpers.py): A utility folder that contains reusable functions used across services.
4. Transaction Service (transaction_services): Implements the core business logic by calling functions from the other services. This service coordinates how the data flows through the system. The functions here are used called directly in the API endpoint. 

### Caching (Not Implemented):
Initially, I considered implementing a caching mechanism for the backend with a time-to-live (TTL) of 2 seconds to reduce API requests and improve performance.
Reason for Not Using Cache: I decided against caching because the real-time nature of the data is critical. Even a short caching window could result in outdated or inconsistent transaction statuses and exchange rates, which would compromise the user experience. The priority was to ensure that users always see the most accurate and current data.

## Version Control:
I employed Git version control throughout the project. As I am the only one working on the project, I decided to work on main branch. However, in a team setting, it is important to use Git branching for version control to ensure isolation of features/changes, parallel development, and easy code review and collaboration. 
In this project, I made frequent commits after each key feature was completed to maintain a clear development history.

## Frontend Architecture:
The frontend is designed with a focus on reusability, scalability in mind, and efficient rendering. 
To ensure code reusaibility and simplification of maintenance, I used a component-based architecture, where each UI element is encapsulated into reusable, self-contained components.
To efficiently handle large datasets, I also implemented server-side pagination. Instead of fetching all data at once, we only retrieve a subset of the data on demand, optimizing both performance and user experience.
- API-Driven Pagination: The frontend passes the current page number and limit (number of items per page) as parameters to the API. Although there are 10,000 total items available, we only fetch a limited number of items (e.g., 50 items per page) to avoid overloading the client.
- Lazy Data Fetching: While all 200 available page numbers are displayed in the UI, the actual data for a specific page is only fetched when the user selects a page number. This approach minimizes the initial data load, making the application more responsive.
- Dynamic Data Fetching: When a user clicks on a page number, the application dynamically fetches the corresponding data from the API, ensuring that only the necessary data is loaded at any given time.
