import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Function to load the dataset from a CSV file
def load_dataset():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the dataset: {e}")
    return None

# Load the dataset
df = load_dataset()
if df is None:
    exit()

# Check if the required columns are present in the dataset
required_columns = ['Income', 'CreditScore', 'LoanAmount', 'LoanTerm', 'Eligibility']
if not all(column in df.columns for column in required_columns):
    messagebox.showerror("Error", f"The dataset must contain the following columns: {required_columns}")
    exit()

# Features and target variable
X = df.drop('Eligibility', axis=1)
y = df['Eligibility']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Function to predict loan eligibility
def predict_eligibility():
    try:
        # Get input values from the GUI
        income = float(income_entry.get())
        credit_score = float(credit_score_entry.get())
        loan_amount = float(loan_amount_entry.get())
        loan_term = float(loan_term_entry.get())

        # Create a DataFrame with the input values
        input_data = pd.DataFrame({
            'Income': [income],
            'CreditScore': [credit_score],
            'LoanAmount': [loan_amount],
            'LoanTerm': [loan_term]
        })

        # Make a prediction
        prediction = model.predict(input_data)

        # Display the result
        if prediction[0] == 1:
            messagebox.showinfo("Loan Eligibility", "Congratulations! You are eligible for the loan.")
        else:
            messagebox.showinfo("Loan Eligibility", "Sorry, you are not eligible for the loan.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create the main GUI window
root = tk.Tk()
root.title("Loan Eligibility Prediction")

# Create input fields
tk.Label(root, text="Income:").grid(row=0, column=0, padx=10, pady=10)
income_entry = tk.Entry(root)
income_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Credit Score:").grid(row=1, column=0, padx=10, pady=10)
credit_score_entry = tk.Entry(root)
credit_score_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Loan Amount:").grid(row=2, column=0, padx=10, pady=10)
loan_amount_entry = tk.Entry(root)
loan_amount_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Loan Term (months):").grid(row=3, column=0, padx=10, pady=10)
loan_term_entry = tk.Entry(root)
loan_term_entry.grid(row=3, column=1, padx=10, pady=10)

# Create a button to trigger the prediction
predict_button = tk.Button(root, text="Check Eligibility", command=predict_eligibility)
predict_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the GUI
root.mainloop()