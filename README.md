# Project Setup and Server Start Instructions

## Starting the FastAPI Server

1. Open a terminal and navigate to the `lang-graph-service` directory:
   ```sh
   cd lang-graph-service
   ```
2. Install dependencies (if you haven't already):
   ```sh
   poetry install
   ```
3. Start the server:
   ```sh
   poetry run python server.py
   ```

The server will start on port 8000 by default. You can access it at `http://localhost:8000`.

---

## Running the Copilot Runtime Dev Server

1. Open a terminal and navigate to the `copilot-runtime-service` directory:
   ```sh
   cd copilot-runtime-service
   ```
2. Install dependencies (if you haven't already):
   ```sh
   pnpm install
   ```
3. Start the development server:
   ```sh
   pnpm run dev
   ```

The server will start on port 4000 by default. You can access it at `http://localhost:4000/copilotkit`.

---

## Running the React Client

1. Open a terminal and navigate to the `react-client` directory:
   ```sh
   cd react-client
   ```
2. Install dependencies (if you haven't already):
   ```sh
   pnpm install
   ```
3. Start the development server:
   ```sh
   pnpm run dev
   ```

---

Add any additional project-specific instructions below as needed.