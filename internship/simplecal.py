import sys
class Calculator :
    def add(self, num1, num2):
        return num1 + num2
    def subtract(self, num1, num2):
        return num1 - num2
    def multiply(self, num1, num2):
        return num1 * num2
    def divide(self, num1, num2):
        if num2 == 0:
            return "Error! Division by zero."
        return num1 / num2

print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")
choice = input("Enter choice(1/2/3/4): ")
if choice not in ["1","2","3","4"]:
    print("invalid input please try again")
    sys.exit()
try :    
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
except ValueError:
    print("Enter proper value . Enter numeric value only")
calc = Calculator()
if choice == '1':
    print(f"{num1} + {num2} = {calc.add(num1, num2)}")
elif choice =='2':
    print(f"{num1} - {num2} = {calc.subtract(num1,num2)}")
elif choice =="3":
    print(f"{num1} * {num2} = {calc.multiply(num1,num2)}")
elif choice =="4":
    print(f"{num1} / {num2} = {calc.divide(num1,num2)}")
else:
    print("Exit")
