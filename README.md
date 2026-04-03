# Database Table Creation with SQLite

A comprehensive Python project demonstrating database fundamentals, table creation, and CRUD operations using SQLite.

##  Database Introduction

### What is a Database?
A database is an organized collection of structured data stored and accessed electronically. Databases are essential for:
- **Data Persistence**: Store data that persists beyond program execution
- **Data Organization**: Organize data into structured tables with relationships
- **Efficient Queries**: Quickly retrieve and filter specific data
- **Data Integrity**: Maintain consistency and prevent duplicate/invalid data

### What is SQLite?
SQLite is a lightweight, file-based relational database management system that:
- Requires no server setup or configuration
- Stores data in a single `.db` file
- Supports full SQL functionality for small to medium-sized applications
- Is perfect for learning database fundamentals
- Is widely used in mobile apps and embedded systems

### Key Database Concepts

#### Tables
- Structured like Excel sheets with rows and columns
- Each column has a specific data type (INTEGER, TEXT, REAL, etc.)
- Each row represents a unique record

#### Primary Keys
- Unique identifier for each row
- Prevents duplicate records
- Auto-incremented for convenience

#### Data Types
- `INTEGER`: Whole numbers
- `TEXT`: String data
- `REAL`: Decimal numbers
- `BLOB`: Binary large objects
- `NULL`: Missing/undefined values

##  CRUD Operations

This project demonstrates the four fundamental database operations:

### CREATE
Insert new records into the database

### READ
Query and retrieve data from tables

### UPDATE
Modify existing records

### DELETE
Remove records from the database

##  Project Structure

```
src/
├── database.py      # Database initialization and table creation
├── crud.py          # CRUD operations
└── main.py          # Tutorial and example usage

requirements.txt     # Python dependencies
README.md           # This file
```

##  Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Example
```bash
python src/main.py
```

##  Usage Examples

See `src/main.py` for comprehensive examples of:
- Creating a database
- Creating tables with schemas
- Inserting records
- Querying data
- Updating records
- Deleting records

##  Learning Outcomes

After completing this project, you'll understand:
- ✅ Relational database fundamentals
- ✅ SQL syntax basics
- ✅ Data modeling and schema design
- ✅ CRUD operations in Python
- ✅ Database constraints and relationships
- ✅ File-based database management with SQLite

---

**Happy Learning!** 🎓
