# app/__init__.py
"""
Nest of Books — Python OOP Implementation

This package includes:
- models: domain entities (Book, User, Cart, etc.)
- repositories: database CRUD + Singleton pattern
- controllers: logic mapping to use cases
- cli: text-based interface for demonstration
- utils: observer + session utilities
"""
__all__ = ["models", "repositories", "controllers", "cli", "utils"]
