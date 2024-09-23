from flask import Blueprint, render_template, request, redirect, url_for
from collections import defaultdict

main = Blueprint('main', __name__)

# In-memory storage for income and expenses
entries = []

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/log', methods=['GET', 'POST'])
def log():
    type = request.args.get('type')  # Get the type from query parameters
    
    if request.method == 'POST':
        selected_type = request.form.get('type')
        description = request.form.get('description') if selected_type == 'expense' else None
        source = request.form.get('source') if selected_type == 'income' else None
        amount = request.form.get('amount')
        category = request.form.get('category') if selected_type == 'expense' else None
        date_str = request.form.get('date')

        # Server-side validation
        if not amount or not date_str:
            return render_template('log.html', type=selected_type, error='Amount and Date are required.')
        
        try:
            amount = float(amount)
        except ValueError:
            return render_template('log.html', type=selected_type, error='Amount must be a valid number.')

        entry = {
            'type': selected_type,
            'description': description,
            'source': source,
            'amount': amount,
            'category': category,
            'date': date_str
        }
        entries.append(entry)

        return redirect(url_for('main.profile'))

    return render_template('log.html', type=type)

@main.route('/visualizations')
def visualizations():
    total_income = sum(entry['amount'] for entry in entries if entry['type'] == 'income')
    total_expenses = sum(entry['amount'] for entry in entries if entry['type'] == 'expense')

    # Expense breakdown by category
    category_totals = defaultdict(float)
    for entry in entries:
        if entry['type'] == 'expense':
            category_totals[entry['category']] += entry['amount']
    
    categories = list(category_totals.keys())
    category_data = list(category_totals.values())
    
    return render_template(
        'visualizations.html',
        total_income=total_income,
        total_expenses=total_expenses,
        categories=categories,
        category_totals=category_data
    )


@main.route('/summary', methods=['GET', 'POST'])
def summary():
    date_range = request.args.get('date_range', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_entries = entries
    
    if date_range == 'last_week':
        # Filter entries for the last week
        from datetime import datetime, timedelta
        one_week_ago = datetime.now() - timedelta(weeks=1)
        filtered_entries = [entry for entry in entries if datetime.strptime(entry['date'], '%Y-%m-%d') >= one_week_ago]
    elif date_range == 'last_month':
        # Filter entries for the last month
        from datetime import datetime, timedelta
        one_month_ago = datetime.now() - timedelta(weeks=4)
        filtered_entries = [entry for entry in entries if datetime.strptime(entry['date'], '%Y-%m-%d') >= one_month_ago]
    elif date_range == 'custom' and start_date and end_date:
        # Filter entries for a custom date range
        from datetime import datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_entries = [entry for entry in entries if start_date <= datetime.strptime(entry['date'], '%Y-%m-%d') <= end_date]
    
    total_income = sum(entry['amount'] for entry in filtered_entries if entry['type'] == 'income')
    total_expenses = sum(entry['amount'] for entry in filtered_entries if entry['type'] == 'expense')

    return render_template('summary.html', total_income=total_income, total_expenses=total_expenses)