# Bomb Bridge API

## Overview

The Bridge API is designed to handle transaction information and update transaction statuses. It serves as an intermediary service for managing transaction workflows, providing endpoints to create, retrieve and update transaction records.

## Features

-   Retrieve transaction details
-   Update transaction status
-   List all transactions

## Installation

To get started with the Bridge API, follow these steps:
Requirement: Python 3.11.x, Docker compose

1. **Install dependencies:**

    ```bash
    python3 install -r requirements.txt
    ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory and add the necessary environment variables:
3. **Run the server with docker compose:**
    ```bash
    docker compose up -d --build
    ```
