# Import sys to explicitly exit the program
import sys

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        raise ZeroDivisionError("Error: Division by zero is not allowed.")
    return num1 / num2

def get_numeric_input(prompt):
    """Helper function to get validated numeric input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value. Try again.")

def calculator():
    # Map operation choices to functions
    operations = {
        "1": {"name": "Addition", "func": add},
        "2": {"name": "Subtraction", "func": subtract},
        "3": {"name": "Multiplication", "func": multiply},
        "4": {"name": "Division", "func": divide}
    }

    while True:
        print("\n--- Select an Operation ---")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")
        print("---------------------------")

        operation_choice = input("Enter the number of the operation (1/2/3/4/5): ")

        if operation_choice == "5":
            print("Exiting the calculator. Goodbye!")
            break # Exit the main calculator loop

        if operation_choice not in operations:
            print("Invalid operation choice. Please select 1, 2, 3, 4, or 5.")
            continue # Go back to the start of the main loop

        num1 = get_numeric_input("Enter the first number: ")
        num2 = get_numeric_input("Enter the second number: ")

        try:
            selected_operation = operations[operation_choice]["func"]
            result = selected_operation(num1, num2)
            print(f"The result of {operations[operation_choice]['name'].lower()} is: {result}")
        except ZeroDivisionError as e:
            print(e)
            print("Please try again with valid input.")
        except Exception as e: # Catch any other unexpected errors during calculation
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    calculator()
