
def calculator():
    while True:
        print("\n Select an operation ")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")

        operation = input("Enter the number of the operation (1/2/3/4/5): ")

        if operation == "5":
            print("Exiting the calculator. Goodbye!")
            break

        if operation not in {"1", "2", "3", "4"}:
            print("Invalid operation. Please try again.")
            continue

        while True:
            try:
                
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                break  
            except ValueError:
                print("Invalid input. Please enter numeric values. Try again.")
        try:
            if operation == "1":
                print(f"The result of addition is: {num1 + num2}")
            elif operation == "2":
                print(f"The result of subtraction is: {num1 - num2}")
            elif operation == "3":
                print(f"The result of multiplication is: {num1 * num2}")
            elif operation == "4":
                if num2 == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                print(f"The result of division is: {num1 / num2}")
        except ZeroDivisionError as e:
            print(e)
            print("Try again with valid input.")
            continue

if __name__ == "__main__":
    calculator()
