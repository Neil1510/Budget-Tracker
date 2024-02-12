import sqlite3

"""conn = sqlite3.connect('budget_tracker.db') """
def connect_to_database():
    try:
        return sqlite3.connect("budget_tracker.db")
    except sqlite3.Error as e:

        print(f"Error connecting to the database: {e}")
        raise # raise error

""" this function creates tables"""
def create_tables():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_categories (
                id INTEGER PRIMARY KEY,
                category TEXT UNIQUE
            )
        ''') 

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                category_id INTEGER,
                amount REAL,
                FOREIGN KEY (category_id) REFERENCES expense_categories(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income_categories (
                id INTEGER PRIMARY KEY,
                category TEXT UNIQUE
            )
        ''') 

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY,
                category_id INTEGER,
                amount REAL,
                FOREIGN KEY (category_id) REFERENCES income_categories(id)
            )
        ''') 

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY,
                category_id INTEGER,
                budget_amount REAL,
                FOREIGN KEY (category_id) REFERENCES expense_categories(id)
            )
        ''') 

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_goals (
                id INTEGER PRIMARY KEY,
                total_income REAL,
                total_expenses_goal REAL,
                savings_goal REAL
            ); 
        ''') #create tables if they do not exist

    except sqlite3.Error as e: 
        print(f"Error creating tables: {e}") #print error message 
        raise

    """conn.close()"""
    conn.commit() #commit changes
    conn.close() #close connection

""" this function adds an expense category to the database"""
def add_expense_category(category):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check if the category already exists
        cursor.execute('SELECT id FROM expense_categories WHERE category = ?', (category,))
        existing_category = cursor.fetchone()

        if existing_category:
            print(f"Error: Expense category '{category}' already exists. Please choose a different category.")
        else:
            # Insert the new category
            cursor.execute('INSERT INTO expense_categories (category) VALUES (?)', (category,))
            conn.commit()
            print(f"Expense category '{category}' added successfully.")

    except sqlite3.Error as e:
        print(f"Error adding expense category: {e}")
        raise

    conn.commit() 
    conn.close() 

"""This function will add expenses to categories already in the database""" 
def add_expense():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Fetch all expense categories
        cursor.execute('SELECT * FROM expense_categories')
        categories = cursor.fetchall()

        if categories:
            print("\nExpense Categories:")
            for category in categories:
                print(f"{category[0]} - {category[1]}")

            # Prompt the user to select a category
            category_id = int(input("Enter the ID of the expense category: "))

            # Check if the selected category exists
            cursor.execute('SELECT id FROM expense_categories WHERE id = ?', (category_id,))
            category_exists = cursor.fetchone()

            if category_exists:
                # Insert the expense with the selected category
                amount = float(input("Enter expense amount: "))
                cursor.execute('INSERT INTO expenses (category_id, amount) VALUES (?, ?)', (category_id, amount))
                conn.commit()
                print(f"Expense of R{amount} added successfully for the selected category.")
            else:
                print("Invalid expense category ID. Please select a valid category.")
        else:
            print("No expense categories available. Please add expense categories first.")

    except ValueError:
        print("Error: Please enter a valid number for the category ID or the expense amount.")
    except sqlite3.Error as e:
        print(f"Error adding expense: {e}")

    conn.close() 

"""This function allows the user to update expenses for categories already in the database"""
def update_expense():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Fetch all expense categories
        cursor.execute('SELECT * FROM expense_categories')
        categories = cursor.fetchall()

        if categories:
            print("\nExpense Categories:")
            for category in categories:
                print(f"{category[0]} - {category[1]}")

            # Prompt the user to select a category
            category_id = int(input("Enter the ID of the expense category: "))

            # Check if the selected category exists
            cursor.execute('SELECT id FROM expense_categories WHERE id = ?', (category_id,))
            category_exists = cursor.fetchone()

            if category_exists:
                # Update the expense amount for the selected category
                amount = float(input("Enter new expense amount: "))
                cursor.execute('UPDATE expenses SET amount = ? WHERE category_id = ?', (amount, category_id))
                conn.commit()
                print(f"Expense amount updated successfully for the selected category.")
            else:
                print("Invalid expense category ID. Please select a valid category.")
        else:
            print("No expense categories available. Please add expense categories first.")

    except ValueError:
        print("Error: Please enter a valid number for the category ID or for the expense amount.")
    except sqlite3.Error as e:
        print(f"Error updating expense: {e}")

    conn.close() 

"""This function deletes an expense category in the database"""
def delete_expense_category(): 
    try:
        conn = sqlite3.connect('budget_tracker.db') 
        cursor = conn.cursor() 

        cursor.execute('SELECT * FROM expense_categories') 
        categories = cursor.fetchall() 

        if categories: 
            print("\nExpense Categories:") 
            for category in categories: 
                print(f"{category[0]} - {category[1]}") 

            category_id = int(input("Enter the ID of the expense category to delete, from the listed categories: ")) 

            cursor.execute('SELECT id FROM expense_categories WHERE id = ?', (category_id,)) #select id from table
            category_exists = cursor.fetchone() 

            if category_exists: 
                cursor.execute('DELETE FROM expenses WHERE category_id = ?', (category_id,)) 
                cursor.execute('DELETE FROM expense_categories WHERE id = ?', (category_id,)) 
                conn.commit() 
                print(f"Expense category with ID {category_id} deleted successfully.") 
            else:
                print("Invalid expense category ID. Please select a valid category to delete.") 
        else:
            print("No expense categories available. Please add expense categories first.") 

    except sqlite3.Error as e: 
        print(f"Error deleting expense category: {e}") 

    conn.close() 

"""This function allows the user to view all expenses in the database"""
def view_expenses(): 
    try:
        conn = sqlite3.connect('budget_tracker.db') 
        cursor = conn.cursor() 
        cursor.execute('SELECT expenses.id, expense_categories.category, expenses.amount FROM expenses INNER JOIN expense_categories ON expenses.category_id = expense_categories.id') 
        expenses = cursor.fetchall() 
        if expenses: 
            print("Expenses:")  
            for expense in expenses: #for each expense
                print(f"{expense[0]} - {expense[1]}: R{expense[2]}") 
        else:
            print("No expenses found") 

    except sqlite3.Error as e: 
        print(f"Error viewing expenses: {e}") 
        raise 

    conn.close() 

"""this function allows the user to view expenses in the database per category"""
def view_expenses_by_cat(category): 
    try:
        conn = sqlite3.connect('budget_tracker.db') 
        cursor = conn.cursor() 
        cursor.execute('SELECT expenses.id, expense_categories.category, expenses.amount FROM expenses INNER JOIN expense_categories ON expenses.category_id = expense_categories.id WHERE expense_categories.category = ?', (category,)) #select all from table
        expenses = cursor.fetchall() 
        if expenses: 
            print(f"Expenses for {category}:") 
            for expense in expenses: 
                print(f"{expense[0]} - {expense[1]}: R{expense[2]}") 
        else:
            print("No expenses found") 

    except sqlite3.Error as e: 
        print(f"Error viewing expenses: {e}") 
        raise 

    conn.close() 

"""This function allows the user to track spending based on the expenses"""
def track_spending(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 
        cursor.execute('SELECT ec.category, COALESCE(SUM(e.amount), 0) AS total_spent ' 
                    'FROM expense_categories ec ' 
                    'LEFT JOIN expenses e ON ec.id = e.category_id '
                    'GROUP BY ec.id') 
        spending_data = cursor.fetchall() 

        if spending_data: 
            print("\nSpending Summary:") 
            for category, total_spent in spending_data: #for each category and total spent
                print(f"Category: {category}, Total Spent: R{total_spent}") 
        else:
            print("No spending recorded.") 

    except sqlite3.Error as e: 
        print(f"Error tracking spending: {e}") 
        raise 

    conn.close() 

"""This function adds an income category to the database"""
def add_income_category(category):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Check if the category already exists
        cursor.execute('SELECT id FROM income_categories WHERE category = ?', (category,))
        existing_category = cursor.fetchone()

        if existing_category:
            print(f"Error: Income category '{category}' already exists. Please choose a different category.")
        else:
            # Insert the new category
            cursor.execute('INSERT INTO income_categories (category) VALUES (?)', (category,))
            conn.commit()
            print(f"Income category '{category}' added successfully.")

    except sqlite3.Error as e:
        print(f"Error adding income category: {e}")
        raise

    conn.commit() 
    conn.close() 

"""function to add income to the categories already stored in the database"""
def add_income():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Fetch all income categories
        cursor.execute('SELECT * FROM income_categories')
        categories = cursor.fetchall()

        if categories:
            print("\nIncome Categories:")
            for category in categories:
                print(f"{category[0]} - {category[1]}")

            # Prompt the user to select an income category
            category_id = int(input("Enter the ID of the income category, from the listed categories: "))

            # Check if the selected category exists
            cursor.execute('SELECT id FROM income_categories WHERE id = ?', (category_id,))
            category_exists = cursor.fetchone()

            if category_exists:
                # Insert the income with the selected category
                amount = float(input("Enter income amount: "))
                cursor.execute('INSERT INTO income (category_id, amount) VALUES (?, ?)', (category_id, amount))
                conn.commit()
                print(f"Income of R{amount} added successfully for the selected category.")
            else:
                print("Invalid income category ID. Please select a valid category.")
        else:
            print("No income categories available. Please add income categories first.")

    except ValueError:
        print("Error: Please enter a valid number for the category ID or for the income amount.")
    except sqlite3.Error as e:
        print(f"Error adding income: {e}") 

    conn.close() 

"""this function is to view all incomes in the database"""
def view_income(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 
        cursor.execute('''
            SELECT i.id, ic.category, i.amount
            FROM income i
            INNER JOIN income_categories ic ON i.category_id = ic.id
        ''')  
        income = cursor.fetchall() 

        if income: 
            print("\nIncome:")  
            for entry in income: 
                print(f"ID: {entry[0]}, Category: {entry[1]}, Amount: R{entry[2]}") 
        else:
            print("No income recorded.") #print error message if no income recorded
    
    except sqlite3.Error as e: 
        print(f"Error viewing income: {e}") 
        raise 

    conn.close() 

"""this function allows the user to view income in the database per category"""
def view_income_by_category(category): 
    try:   
        conn = connect_to_database() 
        cursor = conn.cursor() 
        cursor.execute('''
            SELECT i.id, ic.category, i.amount
            FROM income i
            INNER JOIN income_categories ic ON i.category_id = ic.id
            WHERE ic.category = ?
        ''', (category,)) 
        income = cursor.fetchall() 

        if income: 
            print(f"\nIncome for {category}:") 
            for entry in income: 
                print(f"ID: {entry[0]}, Amount: R{entry[2]}") 
        else:
            print(f"No income recorded for {category}.") 

    except sqlite3.Error as e: 
        print(f"Error viewing income: {e}") 
        raise 
    
    conn.close() 

"""This function deletes an income category in the database"""
def delete_income_category(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 

        cursor.execute('SELECT * FROM income_categories') 
        categories = cursor.fetchall() 

        if categories: 
            print("\nIncome Categories:") 
            for category in categories: 
                print(f"{category[0]} - {category[1]}") 
 
            category_id = int(input("Enter the ID of the income category to delete, from the listed categories: ")) 

            cursor.execute('SELECT id FROM income_categories WHERE id = ?', (category_id,)) 
            category_exists = cursor.fetchone() 

            if category_exists: 
                cursor.execute('DELETE FROM income WHERE category_id = ?', (category_id,)) 
                cursor.execute('DELETE FROM income_categories WHERE id = ?', (category_id,)) 
                conn.commit() #
                print(f"Income category with ID {category_id} deleted successfully.") 
            else: 
                print("Invalid income category ID. Please select a valid category.") 
        else:
            print("No income categories available. Please add income categories first.") 

    except sqlite3.Error as e: 
        print(f"Error deleting income category: {e}")

    conn.close() 

"""This function tracks income per category"""
def track_income(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 
        cursor.execute('SELECT ic.category, COALESCE(SUM(i.amount), 0) AS total_income '
                    'FROM income_categories ic '
                    'LEFT JOIN income i ON ic.id = i.category_id '
                    'GROUP BY ic.id') 
        income_data = cursor.fetchall() 

        if income_data: 
            print("\nIncome Summary:") 
            for category, total_income in income_data: 
                print(f"Category: {category}, Total Income: R{total_income}") 
        else:
            print("No income recorded.") 

    except sqlite3.Error as e: 
        print(f"Error tracking income: {e}") 
        raise 

    conn.close() 

"""This function views either the income or expense categories in the database"""
def view_categories(table_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        if table_name in ['expense', 'income']:
            cursor.execute(f'SELECT * FROM {table_name}_categories')
            categories = cursor.fetchall()

            if categories:
                print(f"\n{table_name.capitalize()} Categories:")
                for category in categories:
                    print(category[1])
            else:
                print(f"No {table_name} categories recorded.")
        else:
            raise ValueError(f"Invalid table name: {table_name}")

    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

    conn.close() 

"""This function allows the user to set the budget per expense category in the database"""
def set_budget(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 

        cursor.execute('SELECT * FROM expense_categories') 
        categories = cursor.fetchall() 

        if categories: 
            print("\nExpense Categories:") 
            for category in categories: 
                print(f"{category[0]} - {category[1]}") 

            category_id = int(input("Enter the ID of the expense category to set a budget: ")) 

            cursor.execute('SELECT id FROM expense_categories WHERE id = ?', (category_id,)) 
            category_exists = cursor.fetchone() 

            if category_exists: 
                budget_amount = float(input("Enter budget amount: ")) 
                cursor.execute('INSERT OR REPLACE INTO budget (category_id, budget_amount) VALUES (?, ?)', 
                               (category_id, budget_amount)) 
                conn.commit() 
                print(f"Budget set for expense category with ID {category_id}: R{budget_amount}") 
            else:
                print("Invalid expense category ID. Please select a valid category to set a budget.") 
        else:
            print("No expense categories available. Please add expense categories first.") 

    except ValueError:
        print("Error: Please enter a valid number for the category ID or for the income amount.")
    except sqlite3.Error as e: 
        print(f"Error setting budget: {e}") 

    conn.close() 

"""This function allows the user to view the budget set by the user per expense category in the database"""
def view_budget(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor() 

        cursor.execute('SELECT * FROM expense_categories') 
        categories = cursor.fetchall() 

        if categories: 
            print("\nExpense Categories:") 
            for category in categories: 
                print(f"{category[0]} - {category[1]}") 

            category_id = int(input("Enter the ID of the expense category to view budget: ")) 

            cursor.execute('SELECT budget_amount FROM budget WHERE category_id = ?', (category_id,)) 
            budget_amount = cursor.fetchone() 

            if budget_amount: 
                print(f"\nBudget for {categories[category_id-1][1]}: R{budget_amount[0]}") 
            else:
                print(f"No budget set for the selected expense category.") 
        else:
            print("No expense categories available. Please add expense categories first.") 

    except ValueError:
        print("Error: Please enter a valid number for the category ID or for the income amount.")
    except sqlite3.Error as e: 
        print(f"Error viewing budget: {e}") 

    conn.close()  

"""This function allows the user to set their own financial goals, such as expenses goal"""
def set_financial_goals():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Calculate total income
        cursor.execute('''
            SELECT COALESCE(SUM(i.amount), 0)
            FROM income i
            INNER JOIN income_categories ic ON i.category_id = ic.id
        ''')
        total_income = cursor.fetchone()[0]

        total_expenses_goal = float(input("Enter your total expenses goal: R"))
        
        # Allow the user to enter their own savings goal
        savings_goal = float(input("Enter your total savings goal: R"))

        print("\nCustom Financial Goals:")
        print(f"Total Income: R{total_income}")
        print(f"Total Expenses Goal: R{total_expenses_goal}")
        print(f"Savings Goal: R{savings_goal}")

        # Insert goals into the custom_goals table
        cursor.execute('INSERT INTO custom_goals (total_income, total_expenses_goal, savings_goal) VALUES (?, ?, ?)',
                       (total_income, total_expenses_goal, savings_goal))

        conn.commit()

    except ValueError:
        print("Invalid input. Please enter valid numeric values for your financial goals.")  # print error message

    conn.close()

"""This function allows the user to input current savings and view progress towards goals set in the set goals function"""
def view_progress_towards_goals():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM custom_goals ORDER BY id DESC LIMIT 1')
        goals = cursor.fetchone()

        if goals:
            total_income = goals[1]
            total_expenses_goal = goals[2]
            savings_goal = goals[3]

            cursor.execute('SELECT COALESCE(SUM(amount), 0) FROM expenses')
            total_expenses = cursor.fetchone()[0]

            if total_income is not None:
                remaining_budget = total_income - total_expenses if total_expenses is not None else total_income

                # Ask user for current savings
                current_savings = float(input("Enter your current savings: R"))

                # Set savings_goal to zero if it's None
                savings_goal = 0 if savings_goal is None else savings_goal

                # Calculate progress towards savings goal using user's input
                if savings_goal != 0:
                    progress_towards_savings_goal = current_savings / savings_goal * 100
                else:
                    progress_towards_savings_goal = 0

                # Calculate progress towards expense goal
                if total_expenses_goal != 0:
                    progress_towards_expense_goal = total_expenses / total_expenses_goal * 100
                else:
                    progress_towards_expense_goal = 0

                print("\nProgress Towards Custom Financial Goals:")
                print(f"Total Income: R{total_income}")
                print(f"Total Expenses: R{total_expenses}")
                print(f"Remaining Budget: R{remaining_budget}")
                print(f"Total Expenses Goal: R{total_expenses_goal}")
                print(f"Savings Goal: R{savings_goal}")
                print(f"Progress Towards Savings Goal: {progress_towards_savings_goal:.2f}%")
                print(f"Progress Towards Expense Goal: {progress_towards_expense_goal:.2f}%")

        else:
            print("No custom financial goals set. Use 'set_financial_goals' to set your goals.")

    except ValueError:
        print("Invalid input. Please enter valid numeric values for your current savings.")
    except (sqlite3.Error, ValueError) as e:
        print(f"Error viewing progress towards goals: {e}")

    conn.close()

"""This function allows the user to view the entire budget, including income and expenses per category"""
def view_income_and_expenses(): 
    try:
        conn = connect_to_database() 
        cursor = conn.cursor()

        """Fetch income data"""
        cursor.execute('SELECT ic.category, i.amount FROM income i INNER JOIN income_categories ic ON i.category_id = ic.id') #select all from table
        income_data = cursor.fetchall() 

        cursor.execute('SELECT ec.category, e.amount FROM expenses e INNER JOIN expense_categories ec ON e.category_id = ec.id') #select all from table
        expense_data = cursor.fetchall()

        print("\nBUDGET") 
        print("-" * 90) 

        print("Income\t\t\t\t\t\tExpenses") 
        print("-" * 90) 

        max_rows = max(len(income_data), len(expense_data)) #calculate max rows

        for i in range(max_rows): 
            income_row = income_data[i] if i < len(income_data) else ("", "") 
            expense_row = expense_data[i] if i < len(expense_data) else ("", "") #

            print(f"{income_row[0]:<20}\tR{income_row[1]:<20}\t|\t{expense_row[0]:<20}\tR{expense_row[1]:<20}") 
    
    except sqlite3.Error as e:
        print(f"Error viewing income and expenses: {e}")  
        raise 
    
    conn.close() 

"""This is the start of the menu section where each menu is printed and the user can choose what they want to do and the functions are called, the menu is divided into sub-menus to enhance the user experience and avoid 1 lengthy menu"""
def print_menu(): 
    print("\nBudget Tracker Menu:") 
    print("1. Expense Management") 
    print("2. Income Management")
    print("3. Budget Management") 
    print("4. Financial Goals") 
    print("5. Reports") 
    print("6. Quit") 

def print_expense_menu(): 
    print("\nExpense Management:") 
    print("1. Add Expense Category") 
    print("2. Add Expense") 
    print("3. Update Expense Amount")
    print("4. Delete Expense Category") 
    print("5. Track Spending") 
    print("6. View Expenses") 

def expense_menu_choice(choice): 
    try:
        if choice == "1": 
            category = input("Enter expense category: ") 
            add_expense_category(category)
        elif choice == "2": 
            add_expense() 
        elif choice == "3": 
            update_expense() 
        elif choice == "4": 
            delete_expense_category() 
        elif choice == "5": 
            track_spending() 
        elif choice == "6": 
            view_expenses() 
        else:
            print("Invalid choice. Please enter a number between 1 and 6.") #print error message not in range
    except Exception as e: 
        print(f"Error: {e}") 

def print_income_menu(): 
    print("\nIncome Management:") 
    print("1. Add Income Category") 
    print("2. Add Income") 
    print("3. Delete Income Category") 
    print("4. Track Income") 
    print("5. View Income")

def income_menu_choice(choice): 
    try:
        if choice == "1": 
            category = input("Enter income category: ") 
            add_income_category(category) 
        elif choice == "2": 
            add_income() 
        elif choice == "3": 
            delete_income_category()
        elif choice == "4": 
            track_income() 
        elif choice == "5": 
            view_income() 
        else: 
            print("Invalid choice. Please enter a number between 1 and 5.") 
    except Exception as e:
        print(f"Error: {e}")

def print_budget_menu():
    print("\nBudget Management:") 
    print("1. Set Budget for a Category") 
    print("2. View Budget for a Category") 
 
def budget_menu_choice(choice): 
    try:
        if choice == "1":
            set_budget() 
        elif choice == "2": 
            view_budget() 
        else: 
            print("Invalid choice. Please enter a number between 1 and 2.") 
    except Exception as e: 
        print(f"Error: {e}") 

def print_goals_menu(): 
    print("\nFinancial Goals:")
    print("1. Set Financial Goals") 
    print("2. View Progress Towards Financial Goals") 
def goals_menu_choice(choice): 
    try:
        if choice == "1": 
            set_financial_goals() #
        elif choice == "2":
            view_progress_towards_goals()
        else: 
            print("Invalid choice. Please enter a number between 1 and 2.") 
    except Exception as e: 
        print(f"Error: {e}") 

def print_reports_menu(): 
    print("\nReports:") 
    print("1. View Income and Expenses")
    print("2. View Income or Expenses Category")

def reports_menu_choice(choice): #
    try:
        if choice == "1": 
            view_income_and_expenses() 
        elif choice == "2":
            table_name = input("Enter table name (income/expense): ").lower() 
            view_categories(table_name)
        else: 
            print("Invalid choice. Please enter a number between 1 and 2.") #
    except Exception as e: 
        print(f"Error: {e}") 

"""main category"""
def main(): 
    create_tables() 

    while True: 
        try:  
            print_menu() 

            choice = input("Enter your choice (1-6): ") 

            if choice == "1": 
                print_expense_menu() 
                expense_choice = input("Enter your choice (1-6): ") 
                expense_menu_choice(expense_choice) 
            elif choice == "2":
                print_income_menu() 
                income_choice = input("Enter your choice (1-5): ")
                income_menu_choice(income_choice)
            elif choice == "3": 
                print_budget_menu() 
                budget_choice = input("Enter your choice (1-2): ")
                budget_menu_choice(budget_choice)
            elif choice == "4": 
                print_goals_menu() 
                goals_choice = input("Enter your choice (1-2): ")
                goals_menu_choice(goals_choice)
            elif choice == "5": 
                print_reports_menu()
                reports_choice = input("Enter your choice (1-2): ")
                reports_menu_choice(reports_choice)
            elif choice == "6":
                print("Exiting Budget Tracker. Goodbye!")
                break 
            else: 
                print("Invalid choice. Please enter a number between 1 and 6.") 
        except Exception as e: 
                print(f"Error: {e}") 

if __name__ == "__main__": 
    main() 