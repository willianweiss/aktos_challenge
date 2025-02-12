
# Aktos Challenge

## Description
This project implements a system for ingesting and querying consumer account data for a collection agency. It includes functionality to upload data via a CSV file, list accounts, and filter them by specific parameters.

The project is already deployed on Heroku and can be accessed via the following URL:

**Base URL**: [https://aktoschallenge-158f9621818b.herokuapp.com/](https://aktoschallenge-158f9621818b.herokuapp.com/)

---

## Endpoints

### 1. **List Accounts**
   - **URL**: `GET /api/accounts/`
   - **Description**: Returns a list of accounts with optional filters.
   - **Query Parameters**:
     - `min_balance` (optional): Minimum balance amount.
     - `max_balance` (optional): Maximum balance amount.
     - `status` (optional): Account status (`INACTIVE`, `PAID_IN_FULL`, etc.).
     - `consumer_name` (optional): Consumer's name.
     - `offset` (optional): The starting position in the dataset (default: 0).
     - `limit` (optional): Number of results to return per page (default: 10).

   **Example Request**:
   ```bash
   curl -X GET "https://aktoschallenge-158f9621818b.herokuapp.com/api/accounts/?min_balance=50000&status=INACTIVE"
   ```

---

### 2. **Upload CSV**
   - **URL**: `POST /api/upload-csv/`
   - **Description**: Uploads a CSV file containing account, consumer, and client data.
   - **CSV Format**:
     The CSV must include the following mandatory fields:
     - `client reference no`
     - `balance`
     - `status`
     - `consumer name`

   **Example CSV File**:
   ```csv
   client reference no,balance,status,consumer name,consumer address,ssn
   ffeb5d88-e5af-45f0-9637-16ea469c58c0,59638.99,INACTIVE,Jessica Williams,"0233 Edwards Glens
   Allisonhaven, HI 91491",018-79-4253
   6155ee11-6eb5-4005-abc7-df2fe6c099ea,59464.79,PAID_IN_FULL,Christopher Harrison,"6791 Chang Mountain
   Port Jamiehaven, UT 24171",511-96-5364
   ```

   **Example Request with cURL**:
   ```bash
   curl -X POST https://aktoschallenge-158f9621818b.herokuapp.com/api/upload-csv/ \
   -F "file=@/path/to/consumers_balances.csv"
   ```

---

## Swagger Documentation
To access the API documentation, visit:

**URL**: [https://aktoschallenge-158f9621818b.herokuapp.com/swagger/](https://aktoschallenge-158f9621818b.herokuapp.com/swagger/)

This page provides a user-friendly interface to explore the API, view available endpoints, and test them.

---

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up the database**:
   Run migrations to create the required tables:
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser (optional)**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

---

## Testing

Run the test suite to validate functionality:
```bash
python manage.py test
```
