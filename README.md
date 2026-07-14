# SOLID-microservice-ecomerce

A full-stack, distributed microservices e-commerce application built to demonstrate **SOLID Principles**, the **Saga Pattern**, and the **Circuit Breaker Pattern**.

## Overview
This project simulates an e-commerce platform where users can log in, view products, add items to a shopping cart, and proceed to a mock checkout. The backend is split into independent microservices, orchestrating transactions safely even when external systems fail.

## Features
- **Modern Minimalist UI**: Built with React & Vite.
- **Microservices Architecture**: Separate Auth, Order, and Payment services using FastAPI (Python).
- **Shopping Cart & Checkout**: End-to-end purchasing flow with dummy credit card validation.
- **Saga Orchestrator**: The Order service orchestrates distributed transactions. If payment fails, the Saga compensates by updating the order status to `payment_failed`.
- **Circuit Breaker**: The Order service protects itself from cascading failures using a Circuit Breaker when communicating with the Payment service.

## SOLID Principles in Action
Our backend strictly adheres to SOLID:
- **Single Responsibility (SRP)**: Use Cases orchestrate business logic, cleanly separated from database writes and HTTP requests.
- **Open/Closed (OCP)**: Discount Strategies are implemented via an interface, allowing new discount types without modifying core logic.
- **Liskov Substitution (LSP)**: Repositories perfectly fulfill Interface contracts, allowing blind substitution (e.g., swapping InMemory for Postgres).
- **Interface Segregation (ISP)**: Massive database interfaces are broken down into specific `OrderReader` and `OrderWriter` contracts.
- **Dependency Inversion (DIP)**: High-level business logic relies on Abstractions. Concrete gateways and repositories are injected, making the core 100% unit-testable offline.

## How to Run
Prerequisites: Docker and Docker Compose.

1. Clone the repository.
2. Build and start the microservices:
   ```bash
   sudo docker-compose up --build -d
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```
4. *Test the Saga & Circuit Breaker*: Proceed to checkout and enter an invalid credit card number (anything other than 16 digits) to see the transaction fail and intelligently compensate!
