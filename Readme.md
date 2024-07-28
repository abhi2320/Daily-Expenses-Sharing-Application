Daily Expenses Sharing Application

Overview
This application is a backend service designed to manage and share daily expenses among users. It allows users to add expenses and split them based on three different methods: exact amounts, percentages, and equal splits. The application handles user details, validates inputs, and generates downloadable balance sheets.

Features:
    User Management:
        Create user with email, name, and mobile number.
        Retrieve user details.
    Expense Management:
        Add expenses with descriptions, amounts, and user ID.
    Split expenses using three methods: Equal, Exact, and Percentage.
        Retrieve individual user expenses.
        Retrieve all expenses.
        Download balance sheet as a CSV file.

Setup Instructions:

1. Clone the Repository:
    git clone <repository-url>
    cd <repository-directory>
2. Create a Virtual Environment:
    python -m venv venv
    venv\Scripts\activate
3. Install Dependencies:
    pip install -r requirements.txt
4. Run the Application:
    python app.py

Prerequisites
    Python 3.x
    Flask
    Flask-SQLAlchemy

API Endpoints
Create User

URL: POST /user
Headers: Content-Type: application/json
Body (raw JSON):
    {
    "email": "test@example.com",
    "name": "Test User",
    "mobile": "1234567890"
    }

Add Expense

URL: POST /expense
Headers: Content-Type: application/json
Body (raw JSON):
    {
    "description": "Lunch",
    "amount": 25,
    "user_id": 1,
    "split_method": "Equal",
    "split_details": {"user1": 50, "user2": 50}
    }

Get User:

URL: GET '/user/<user_id>'

Get User Expenses:

URL: GET '/expense/user/<user_id>'

Get All Expenses:

URL: GET '/expenses'

Download Balance Sheet:

URL: GET '/balance_sheet'


Data Validation
User Inputs:

Ensure email, name, and mobile number are provided when creating a user.
Ensure description, amount, user ID, split method, and split details are provided when adding an expense.
Percentage Split Validation:
Ensure percentages add up to 100%.


Code Quality
    The code is clean, readable, and maintainable.
    Clear comments are provided for each function and important sections.
    Bonus Features
Error Handling:
    Proper error messages are returned for invalid inputs and non-existing users.
    Input Validation:
    Inputs are validated to ensure data integrity.


Repository Structure
.
├── app.py               # Main application file
├── models.py            # Database models
├── README.md            # This file
└── requirements.txt     # List of dependencies
