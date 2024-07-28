from flask import Flask, request, jsonify, make_response
from models import db, User, Expense
import csv
from io import StringIO

# Initialize the Flask app
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db.init_app(application)

# Create database tables if they don't exist
with application.app_context():
    db.create_all()

@application.route('/user', methods=['POST'])
def register_user():
    """Endpoint to register a new user."""
    user_data = request.get_json()
    if not user_data or not user_data.get('email') or not user_data.get('name') or not user_data.get('phone'):
        return jsonify({'error': 'Invalid input'}), 400

    if User.query.filter_by(email=user_data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(email=user_data['email'], name=user_data['name'], phone=user_data['phone'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@application.route('/expense', methods=['POST'])
def create_expense():
    """Endpoint to create a new expense."""
    expense_data = request.get_json()
    if not expense_data or not expense_data.get('description') or not expense_data.get('amount') or not expense_data.get('user_id') or not expense_data.get('split_method') or not expense_data.get('split_details'):
        return jsonify({'error': 'Invalid input'}), 400

    if not User.query.get(expense_data['user_id']):
        return jsonify({'error': 'User not found'}), 404

    if expense_data['split_method'] == 'Percentage' and sum(expense_data['split_details'].values()) != 100:
        return jsonify({'error': 'Percentages must add up to 100'}), 400

    new_expense = Expense(
        description=expense_data['description'],
        amount=expense_data['amount'],
        user_id=expense_data['user_id'],
        split_method=expense_data['split_method'],
        split_details=expense_data['split_details']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense created successfully'}), 201

@application.route('/user/<int:user_id>', methods=['GET'])
def retrieve_user(user_id):
    """Endpoint to get user details."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'email': user.email, 'name': user.name, 'phone': user.phone}), 200

@application.route('/expense/user/<int:user_id>', methods=['GET'])
def retrieve_user_expenses(user_id):
    """Endpoint to get all expenses for a specific user."""
    user_expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'description': exp.description,
            'amount': exp.amount,
            'split_method': exp.split_method,
            'split_details': exp.split_details
        } for exp in user_expenses
    ]), 200

@application.route('/expenses', methods=['GET'])
def retrieve_all_expenses():
    """Endpoint to get all expenses."""
    all_expenses = Expense.query.all()
    return jsonify([
        {
            'description': exp.description,
            'amount': exp.amount,
            'user_id': exp.user_id,
            'split_method': exp.split_method,
            'split_details': exp.split_details
        } for exp in all_expenses
    ]), 200

@application.route('/balance_sheet', methods=['GET'])
def export_balance_sheet():
    """Endpoint to download balance sheet as CSV."""
    all_expenses = Expense.query.all()
    balance_sheet_data = []

    for exp in all_expenses:
        user = User.query.get(exp.user_id)
        balance_sheet_data.append({
            'user': user.name,
            'email': user.email,
            'description': exp.description,
            'amount': exp.amount,
            'split_method': exp.split_method,
            'split_details': exp.split_details
        })

    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)
    csv_writer.writerow(['User', 'Email', 'Description', 'Amount', 'Split Method', 'Split Details'])
    csv_writer.writerows([(row['user'], row['email'], row['description'], row['amount'], row['split_method'], row['split_details']) for row in balance_sheet_data])

    response = make_response(csv_output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=balance_sheet.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    application.run(debug=True)
