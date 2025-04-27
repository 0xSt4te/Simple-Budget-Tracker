# 💰 Simple Budget Tracker

A command-line budget tracking tool to help you manage your income, expenses, and stay on budget.

## ✨ Features

- 💵 Track income and expenses
- 📊 Set budgets for different categories
- 📅 View transactions by date range
- 📈 Generate summary reports
- 🏷️ Categorize transactions
- 🔍 Filter transactions by type or category
- 📤 Export data to JSON or CSV formats
- 💾 Store data locally in JSON format

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xSt4te/budget-tracker.git
cd budget-tracker
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `add`: Add a new transaction
- `delete`: Delete a transaction
- `list`: List transactions
- `budget`: Set budget for a category
- `summary`: Show budget summary
- `export`: Export data to a file

## 📋 Command Options

### Add a transaction:
```bash
python main.py add <amount> <description> [options]
```

#### Options:

- `-c, --category`: Transaction category
- `-d, --date`: Transaction date (YYYY-MM-DD)

### Delete a transaction:
```bash
python main.py delete <id>
```

### List transactions:
```bash
python main.py list [options]
```

#### Options:

- `-s, --start`: Start date (YYYY-MM-DD)
- `-e, --end`: End date (YYYY-MM-DD)
- `-c, --category`: Filter by category
- `-l, --limit`: Limit number of transactions shown
- `-i, --income`: Show only income
- `-x, --expenses`: Show only expenses

### Set budget for a category:
```bash
python main.py budget <category> <amount>
```

### Show budget summary:
```bash
python main.py summary [options]
```

#### Options:

- `-m, --month`: Month (1-12)
- `-y, --year`: Year

### Export data:
```bash
python main.py export <output_file> [options]
```

#### Options:

- `-f, --format`: Export format (json, csv)

### Global options:

- `-d, --data`: Data file (default: ~/.budget_tracker.json)

## 📝 Examples

### Add transactions:
```bash
# Add an expense
python main.py add -50 "Grocery shopping" -c "Food"
```

```bash
# Add income
python main.py add 1000 "Salary" -c "Income" -d "2023-09-01"
```

```bash
# Add an expense with a specific date
python main.py add -25.50 "Restaurant" -c "Dining" -d "2023-09-15"
```

### List transactions:
```bash
# List all transactions
python main.py list
```

```bash
# List transactions for a specific month
python main.py list -s "2023-09-01" -e "2023-09-30"
```

```bash
# List only expenses
python main.py list -x
```

```bash
# List transactions for a specific category
python main.py list -c "Food"
```

```bash
# List the 5 most recent transactions
python main.py list -l 5
```

### Set budgets:
```bash
# Set a monthly budget for food expenses
python main.py budget "Food" -300
```

```bash
# Set a monthly budget for income
python main.py budget "Income" 3000
```

### View budget summary:
```bash
# View summary for the current month and year
python main.py summary
```

```bash
# View summary for a specific month
python main.py summary -m 9
```

```bash
# View summary for a specific year
python main.py summary -y 2023
```

```bash
# View summary for a specific month and year
python main.py summary -m 9 -y 2023
```

### Export data:
```bash
# Export to JSON
python main.py export budget_data.json
```

```bash
# Export to CSV
python main.py export budget_data.csv -f csv
```

## 💡 Budget Management Tips

1. **Track Everything**: Record all your income and expenses for an accurate view of your finances

2. **Use Categories Consistently**: Develop a consistent categorization system for easier analysis

3. **Set Realistic Budgets**: Start with realistic budget amounts based on your actual spending

4. **Regular Reviews**: Review your spending weekly to stay on track with your budget goals

5. **Distinguish Needs vs. Wants**: Categorize expenses as either necessities or discretionary spending

6. **Use the 50/30/20 Rule**: Allocate 50% to needs, 30% to wants, and 20% to savings

7. **Emergency Fund**: Build an emergency fund to cover unexpected expenses

8. **Export Regularly**: Export your data regularly as a backup

