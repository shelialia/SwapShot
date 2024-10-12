# Uniswap WETH-USDC Transactions

## Overview
This project is designed to showcase the transaction fees in USDT for all Uniswap WETH-USDC transactions. It includes real-time transaction monitoring with exchange rates and ensures up-to-date data on page reload. The architecture is designed for separation of concerns, maintainability, and scalability.

---

## Installation

### Prerequisites
- [Node.js](https://nodejs.org/en/) (version 16+)
- [Docker](https://www.docker.com/) (optional, if you're using Docker to run your application)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)

### Steps to Install
1. Clone the repository:
- git clone https://github.com/your-username/your-repo.git
- cd your-repo

2. Install dependencies:
- npm install

## Using Docker (Optional)
To Build and Run the Docker containers: docker-compose up
Your backend will be running on: http://localhost:8000
Your frontend will be running on: http://localhost:3000
This command will build the images for both the backend and frontend, then start the containers.

If you only want to build the images without running them immediately, you can use: docker-compose build

## Running the Application Locally (without Docker)
Once dependencies are installed, you can run the frontend using npm run dev. 
This will start the frontend application at [http://localhost:5173](http://localhost:5173).
Then, run the backend using fastapi dev main.py.
This will start the fastapi backend at [http://172.18.0.2:3000](http://127.0.0.1:8000).

## Testing
To run the test suite for the frontend, use: npm run test
This project uses Jest for unit and integration tests. The test cases check the various functions in the backend to ensure correctness.

### Backend Architecture
The backend is designed with a clear separation of concerns to ensure maintainability and scalability.

## API Layer:
- All API endpoints are located in the api folder. This layer is responsible for setting up the routes and handling incoming requests.
Services Layer: The business logic is decoupled from the API layer, ensuring a clean architecture where each service has its distinct responsibilities. The services layer is divided into four key areas:

### Etherscan Service: Handles interactions with the Etherscan API to fetch blockchain data.
### Binance Service: Responsible for interacting with the Binance API to retrieve current exchange rates (e.g., ETH to USDT).
Helper Functions: A utility folder that contains reusable functions used across services.
Transaction Service: Implements the core business logic by calling functions from the other services. This service coordinates how the data flows through the system.

## Dockerization:
The backend is fully Dockerized, running in a separate container from the frontend to isolate the two environments. This setup allows for easier scaling and ensures that the backend can be deployed independently of the frontend.

## Version Control:
I employed Git version control throughout the project. Frequent commits were made after each key feature was completed to maintain a clear development history, which makes tracking changes and collaboration easier.

## Frontend Architecture:
The frontend is built with reusability and state management in mind.

## Real-time Updates:
Each time the page is reloaded, the application fetches the latest transaction data and exchange rates, ensuring users always see up-to-date information.
Caching (Not Implemented):

Initially, I considered implementing a caching mechanism for the backend with a time-to-live (TTL) of 2 seconds to reduce API requests and improve performance.
Reason for Not Using Cache: I decided against caching because the real-time nature of the data is critical. Even a short caching window could result in outdated or inconsistent transaction statuses and exchange rates, which would compromise the user experience. The priority was to ensure that users always see the most accurate and current data.
