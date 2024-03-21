import tkinter as tk
import sqlite3

# Create SQLite database connection
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

# Create Employee table
cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                salary REAL NOT NULL);''')
conn.commit()

# Function to add employee to the database
def add_employee():
    name = name_entry.get()
    age = int(age_entry.get())
    salary = float(salary_entry.get())
    cursor.execute("INSERT INTO employees (name, age, salary) VALUES (?, ?, ?)",
                   (name, age, salary))
    conn.commit()
    status_label.config(text="Employee added successfully!")
    populate_employees_listbox()

# Function to delete employee from the database
def delete_employee():
    selected_employee = employees_listbox.curselection()
    if not selected_employee:
        status_label.config(text="Please select an employee to delete.")
        return
    employee_id = employees_listbox.get(selected_employee).split(" - ")[0]
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    conn.commit()
    status_label.config(text="Employee deleted successfully!")
    populate_employees_listbox()
# Function to print employee from the database
def print_emp():
    selected_employee = employees_listbox.curselection()
    if not selected_employee:
        status_label.config(text="Please select an employee to print details.")
        return
    employee_id = employees_listbox.get(selected_employee).split(" - ")[0]
    cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
    row = cursor.fetchone()
    if row:
        status_label.config(text=f"Employee ID: {row[0]}\nName: {row[1]}\nAge: {row[2]}\nSalary: {row[3]}")
    else:
        status_label.config(text="Error: Employee not found")

# Create main window
root = tk.Tk()
root.title("Employee Management System")

# Create form elements using grid layout
name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

age_label = tk.Label(root, text="Age:")
age_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

salary_label = tk.Label(root, text="Salary:")
salary_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
salary_entry = tk.Entry(root)
salary_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

add_button = tk.Button(root, text="Add Employee", command=add_employee)
add_button.grid(row=3, columnspan=2, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Employee", command=delete_employee)
delete_button.grid(row=4, columnspan=2, padx=5, pady=5)

print_button = tk.Button(root, text="Print Employee", command=print_emp)
print_button.grid(row=5, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=6, columnspan=2, padx=5, pady=5)

# Create employees listbox
employees_label = tk.Label(root, text="Employees:")
employees_label.grid(row=0, column=2, padx=5, pady=5)
employees_listbox = tk.Listbox(root)
employees_listbox.grid(row=1, rowspan=5, column=2, padx=5, pady=5, sticky=tk.N+tk.S)

# Function to populate employees listbox
def populate_employees_listbox():
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    employees_listbox.delete(0, tk.END)
    for row in rows:
        employees_listbox.insert(tk.END, f"{row[0]} - {row[1]}")

populate_employees_listbox()

root.mainloop()
