# SOLID Principles in the Microservices Backend

This document explains in detail how each of the five SOLID principles was implemented in the `order_service`, where they are located, why they were used, and whether it was strictly necessary.

---

## 1. Single Responsibility Principle (SRP)
**Definition:** A class should have one, and only one, reason to change.

* **Where it is used:** `order_service/application/use_cases.py` -> `PlaceOrderUseCase` class.
* **How it is used:** The `PlaceOrderUseCase` acts solely as the **Saga Orchestrator** for the checkout business logic. It orchestrates the flow: calculate total -> apply discount -> save pending order -> process payment -> update order status. It does **not** know *how* to save an order to a database, nor does it know *how* to call the Stripe API. It delegates those responsibilities to the injected Repository and Gateway classes.
* **Why it is used:** If we decide to switch from an in-memory database to PostgreSQL, or if the Stripe API changes, this Use Case file does not need to change. The only reason this file will ever change is if the *business rules of placing an order* change.
* **Was it necessary?** Yes. Business logic is the core of your application. Mixing HTTP requests, database SQL queries, and business logic into one massive function makes code incredibly hard to debug and read.

## 2. Open/Closed Principle (OCP)
**Definition:** Software entities should be open for extension, but closed for modification.

* **Where it is used:** `order_service/application/strategies.py` -> `DiscountStrategy` and `PercentageDiscount`.
* **How it is used:** We defined an abstract `DiscountStrategy` class with an `apply_discount` method. The `PlaceOrderUseCase` uses this abstraction. We implemented a `PercentageDiscount(10.0)` for the current checkout. 
* **Why it is used:** If the marketing team asks you to add a new "Holiday Flat $20 Off" discount, you **do not need to modify existing code** (which risks breaking things). You simply create a new class `HolidayDiscount(DiscountStrategy)` and inject it. The Use Case remains untouched. 
* **Was it necessary?** Highly recommended. Discount rules change constantly in e-commerce. Building a strategy pattern here prevents `PlaceOrderUseCase` from becoming bloated with hundreds of `if/else` statements for different discount scenarios.

## 3. Liskov Substitution Principle (LSP)
**Definition:** Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application.

* **Where it is used:** `order_service/infrastructure/repositories.py` -> `InMemoryOrderRepository`.
* **How it is used:** The `InMemoryOrderRepository` inherits from the abstract `OrderWriter` and `OrderReader`. It perfectly fulfills the contract defined by those abstractions (accepting an `Order` and saving it, or returning an `Order` by ID). 
* **Why it is used:** Because the `InMemoryOrderRepository` behaves exactly as the interface promises, the `PlaceOrderUseCase` can substitute it blindly. If it threw unexpected exceptions or returned incorrect data types, it would violate LSP and crash the Use Case.
* **Was it necessary?** Absolutely. LSP is the foundational rule that makes interfaces and abstractions actually work. If subclasses don't honor the parent's contract, polymorphism breaks.

## 4. Interface Segregation Principle (ISP)
**Definition:** No client should be forced to depend on methods it does not use.

* **Where it is used:** `order_service/application/interfaces.py` -> `OrderWriter` and `OrderReader`.
* **How it is used:** Instead of creating one giant `IOrderRepository` interface with `save`, `delete`, `get_all`, `get_by_id`, we split it into smaller, specific interfaces (`OrderWriter` and `OrderReader`).
* **Why it is used:** The `PlaceOrderUseCase` only needs the ability to `save()` an order. By injecting *only* the `OrderWriter` type hint into its constructor, we guarantee that the Use Case cannot accidentally call `delete()` or `get_all()`. 
* **Was it necessary?** In a small app, a single Repository interface is often fine. However, in larger enterprise apps, strictly segregating interfaces prevents accidental misuse of powerful database methods by developers working on restricted use cases.

## 5. Dependency Inversion Principle (DIP)
**Definition:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

* **Where it is used:** `order_service/application/use_cases.py` (Constructor) & `order_service/presentation/routers.py` (Dependency Injection setup).
* **How it is used:** The high-level business logic (`PlaceOrderUseCase`) relies on abstract classes (`OrderWriter`, `PaymentGateway`). The low-level implementations (`InMemoryOrderRepository`, `StripePaymentGateway`) are instantiated far away in `routers.py` and passed in as arguments (Dependency Injection).
* **Why it is used:** It completely decouples your application core from external frameworks. More importantly, it makes your code **100% Unit Testable**. You can easily write a unit test for `PlaceOrderUseCase` by passing in a `MockPaymentGateway` and `MockOrderWriter` that don't actually hit the network.
* **Was it necessary?** Yes. This is arguably the most important principle for building Microservices. If your Use Case directly imported and called `requests.post()` to the payment service, you could never test your order logic without spinning up the entire payment microservice.

---

### Summary: Over-engineering vs. Scalability
For a simple "Hello World" app, applying all 5 SOLID principles can feel like over-engineering, resulting in more files and boilerplate. 

However, you requested a **proper backend** implementing **Saga** and **Circuit Breakers**. Complex architectural patterns like those demand a solid foundation. If we didn't use SOLID principles, implementing the Saga Orchestrator would have turned `routers.py` into a tangled mess of HTTP requests, state management, and database writes. Because we used SOLID, the architecture remains clean, testable, and ready to scale!
