#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime
import calendar
import sys

# Constants
DEFAULT_DATA_FILE = os.path.expanduser("~/.budget_tracker.json")

def load_data(data_file=DEFAULT_DATA_FILE):
    """Load budget data from file"""
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {data_file} is corrupted")
            return {"transactions": [], "categories": {}}
    return {"transactions": [], "categories": {}}

def save_data(data, data_file=DEFAULT_DATA_FILE):
    """Save budget data to file"""
    try:
        directory = os.path.dirname(data_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def add_transaction(amount, description, category=None, transaction_date=None, data_file=DEFAULT_DATA_FILE):
    """Add a new transaction"""
    data = load_data(data_file)
    
    # Validate amount
    try:
        amount = float(amount)
    except ValueError:
        print("Error: Amount must be a number")
        return False
    
    # Validate date
    if transaction_date:
        try:
            transaction_date = datetime.strptime(transaction_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format")
            return False
    else:
        transaction_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create transaction
    transaction = {
        "id": len(data["transactions"]) + 1,
        "amount": amount,
        "description": description,
        "category": category,
        "date": transaction_date,
        "created": datetime.now().isoformat()
    }
    
    # Add transaction
    data["transactions"].append(transaction)
    
    # Update category if provided
    if category and category not in data["categories"]:
        data["categories"][category] = {
            "budget": 0.0,
            "type": "expense" if amount < 0 else "income"
        }
    
    if save_data(data, data_file):
        print(f"Transaction added: ${abs(amount):.2f} - {description}")
        return True
    return False

def delete_transaction(transaction_id, data_file=DEFAULT_DATA_FILE):
    """Delete a transaction"""
    data = load_data(data_file)
    
    # Find transaction
    for i, transaction in enumerate(data["transactions"]):
        if transaction["id"] == transaction_id:
            del data["transactions"][i]
            if save_data(data, data_file):
                print(f"Transaction #{transaction_id} deleted")
                return True
            return False
    
    print(f"Transaction #{transaction_id} not found")
    return False

def list_transactions(start_date=None, end_date=None, category=None, 
                     limit=None, income_only=False, expense_only=False,
                     data_file=DEFAULT_DATA_FILE):
    """List transactions with optional filtering"""
    data = load_data(data_file)
    
    if not data["transactions"]:
        print("No transactions found")
        return
    
    # Apply filters
    filtered = data["transactions"]
    
    if start_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            filtered = [t for t in filtered if datetime.strptime(t["date"], "%Y-%m-%d") >= start]
        except ValueError:
            print("Error: Start date must be in YYYY-MM-DD format")
            return
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            filtered = [t for t in filtered if datetime.strptime(t["date"], "%Y-%m-%d") <= end]
        except ValueError:
            print("Error: End date must be in YYYY-MM-DD format")
            return
    
    if category:
        filtered = [t for t in filtered if t["category"] == category]
    
    if income_only:
        filtered = [t for t in filtered if t["amount"] > 0]
    
    if expense_only:
        filtered = [t for t in filtered if t["amount"] < 0]
    
    # Sort by date (newest first)
    filtered.sort(key=lambda x: x["date"], reverse=True)
    
    # Apply limit
    if limit and limit > 0:
        filtered = filtered[:limit]
    
    if not filtered:
        print("No transactions match the criteria")
        return
    
    # Calculate totals
    total_income = sum(t["amount"] for t in filtered if t["amount"] > 0)
    total_expenses = sum(t["amount"] for t in filtered if t["amount"] < 0)
    balance = total_income + total_expenses
    
    # Display transactions
    print("\nTransactions:")
    print("=" * 70)
    print(f"{'ID':<5} {'Date':<12} {'Amount':<10} {'Category':<15} {'Description':<30}")
    print("-" * 70)
    
    for t in filtered:
        amount_str = f"${t['amount']:.2f}" if t["amount"] > 0 else f"-${abs(t['amount']):.2f}"
        category = t["category"] or "Uncategorized"
        print(f"{t['id']:<5} {t['date']:<12} {amount_str:<10} {category:<15} {t['description'][:30]}")
    
    print("=" * 70)
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${abs(total_expenses):.2f}")
    print(f"Balance: ${balance:.2f}")
    print(f"Total Transactions: {len(filtered)}")

def set_category_budget(category, budget, data_file=DEFAULT_DATA_FILE):
    """Set a budget for a category"""
    data = load_data(data_file)
    
    # Validate budget
    try:
        budget = float(budget)
    except ValueError:
        print("Error: Budget must be a number")
        return False
    
    # Check if category exists
    if category in data["categories"]:
        data["categories"][category]["budget"] = budget
    else:
        # Create new category
        data["categories"][category] = {
            "budget": budget,
            "type": "expense" if budget > 0 else "income"
        }
    
    if save_data(data, data_file):
        print(f"Budget for '{category}' set to ${abs(budget):.2f}")
        return True
    return False

def show_budget_summary(month=None, year=None, data_file=DEFAULT_DATA_FILE):
    """Show budget summary for a specific month or all time"""
    data = load_data(data_file)
    
    if not data["transactions"]:
        print("No transactions found")
        return
    
    # Determine period
    current_date = datetime.now()
    if month and year:
        try:
            month = int(month)
            year = int(year)
            if month < 1 or month > 12:
                raise ValueError
            start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day).strftime("%Y-%m-%d")
            period = f"{calendar.month_name[month]} {year}"
        except ValueError:
            print("Error: Invalid month or year")
            return
    elif month:
        try:
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError
            year = current_date.year
            start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
            last_day = calendar.monthrange(year, month)[1]
            end_date = datetime(year, month, last_day).strftime("%Y-%m-%d")
            period = f"{calendar.month_name[month]} {year}"
        except ValueError:
            print("Error: Invalid month")
            return
    elif year:
        try:
            year = int(year)
            start_date = datetime(year, 1, 1).strftime("%Y-%m-%d")
            end_date = datetime(year, 12, 31).strftime("%Y-%m-%d")
            period = f"Year {year}"
        except ValueError:
            print("Error: Invalid year")
            return
    else:
        start_date = None
        end_date = None
        period = "All Time"
    
    # Filter transactions by date
    transactions = data["transactions"]
    
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        transactions = [t for t in transactions if datetime.strptime(t["date"], "%Y-%m-%d") >= start]
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        transactions = [t for t in transactions if datetime.strptime(t["date"], "%Y-%m-%d") <= end]
    
    if not transactions:
        print(f"No transactions found for {period}")
        return
    
    # Calculate category totals
    categories = {}
    for t in transactions:
        cat = t["category"] or "Uncategorized"
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += t["amount"]
    
    # Calculate totals
    total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
    total_expenses = sum(t["amount"] for t in transactions if t["amount"] < 0)
    balance = total_income + total_expenses
    
    # Display summary
    print(f"\nBudget Summary for {period}:")
    print("=" * 50)
    
    # Income categories
    print("Income:")
    print("-" * 50)
    if not any(amount > 0 for amount in categories.values()):
        print("No income found")
    else:
        for cat, amount in sorted(categories.items(), key=lambda x: -x[1]):
            if amount <= 0:
                continue
            
            budget = data["categories"].get(cat, {}).get("budget", 0)
            budget_str = f"(Budget: ${abs(budget):.2f})" if budget != 0 else ""
            
            print(f"{cat:<20} ${amount:.2f} {budget_str}")
    
    # Expense categories
    print("\nExpenses:")
    print("-" * 50)
    if not any(amount < 0 for amount in categories.values()):
        print("No expenses found")
    else:
        for cat, amount in sorted(categories.items(), key=lambda x: x[1]):
            if amount >= 0:
                continue
            
            budget = data["categories"].get(cat, {}).get("budget", 0)
            budget_str = f"(Budget: ${abs(budget):.2f})" if budget != 0 else ""
            
            # Calculate percentage of budget used
            if budget < 0:  # It's an expense budget
                percentage = (amount / budget) * 100
                budget_status = f"{percentage:.1f}% used" if percentage <= 100 else f"{percentage:.1f}% OVER BUDGET"
            else:
                budget_status = ""
            
            print(f"{cat:<20} ${abs(amount):.2f} {budget_str} {budget_status}")
    
    # Summary
    print("\nSummary:")
    print("-" * 50)
    print(f"Total Income:  ${total_income:.2f}")
    print(f"Total Expenses: ${abs(total_expenses):.2f}")
    print(f"Balance:       ${balance:.2f}")
    
    # Savings rate
    if total_income > 0:
        savings_rate = (balance / total_income) * 100
        print(f"Savings Rate:  {savings_rate:.1f}%")
    
    print(f"Transactions:   {len(transactions)}")

def export_data(output_file, format="json", data_file=DEFAULT_DATA_FILE):
    """Export budget data to a file"""
    data = load_data(data_file)
    
    if not data["transactions"]:
        print("No transactions to export")
        return False
    
    try:
        if format.lower() == "json":
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data exported to {output_file} in JSON format")
            return True
        
        elif format.lower() == "csv":
            import csv
            
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["ID", "Date", "Amount", "Category", "Description"])
                
                # Write transactions
                for t in data["transactions"]:
                    writer.writerow([
                        t["id"],
                        t["date"],
                        t["amount"],
                        t["category"] or "Uncategorized",
                        t["description"]
                    ])
            
            print(f"Data exported to {output_file} in CSV format")
            return True
        
        else:
            print(f"Unsupported format: {format}")
            return False
    
    except Exception as e:
        print(f"Error exporting data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Simple Budget Tracker")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add transaction command
    add_parser = subparsers.add_parser("add", help="Add a new transaction")
    add_parser.add_argument("amount", help="Transaction amount (negative for expenses)")
    add_parser.add_argument("description", help="Transaction description")
    add_parser.add_argument("-c", "--category", help="Transaction category")
    add_parser.add_argument("-d", "--date", help="Transaction date (YYYY-MM-DD)")
    
    # Delete transaction command
    delete_parser = subparsers.add_parser("delete", help="Delete a transaction")
    delete_parser.add_argument("id", type=int, help="Transaction ID")
    
    # List transactions command
    list_parser = subparsers.add_parser("list", help="List transactions")
    list_parser.add_argument("-s", "--start", help="Start date (YYYY-MM-DD)")
    list_parser.add_argument("-e", "--end", help="End date (YYYY-MM-DD)")
    list_parser.add_argument("-c", "--category", help="Filter by category")
    list_parser.add_argument("-l", "--limit", type=int, help="Limit number of transactions shown")
    list_parser.add_argument("-i", "--income", action="store_true", help="Show only income")
    list_parser.add_argument("-x", "--expenses", action="store_true", help="Show only expenses")
    
    # Set budget command
    budget_parser = subparsers.add_parser("budget", help="Set budget for a category")
    budget_parser.add_argument("category", help="Category name")
    budget_parser.add_argument("amount", help="Budget amount (positive for income, negative for expenses)")
    
    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show budget summary")
    summary_parser.add_argument("-m", "--month", help="Month (1-12)")
    summary_parser.add_argument("-y", "--year", help="Year")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export data to a file")
    export_parser.add_argument("output", help="Output file path")
    export_parser.add_argument("-f", "--format", choices=["json", "csv"], default="json", 
                             help="Export format (default: json)")
    
    # Global options
    parser.add_argument("-d", "--data", default=DEFAULT_DATA_FILE, 
                       help=f"Data file (default: {DEFAULT_DATA_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_transaction(args.amount, args.description, args.category, args.date, args.data)
    
    elif args.command == "delete":
        delete_transaction(args.id, args.data)
    
    elif args.command == "list":
        list_transactions(args.start, args.end, args.category, args.limit, 
                         args.income, args.expenses, args.data)
    
    elif args.command == "budget":
        set_category_budget(args.category, args.amount, args.data)
    
    elif args.command == "summary":
        show_budget_summary(args.month, args.year, args.data)
    
    elif args.command == "export":
        export_data(args.output, args.format, args.data)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
