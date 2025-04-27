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

