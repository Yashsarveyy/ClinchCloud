def add(a, b):
    return a + b

def subtract(a, b):
    return a - b 
def multiply(a, b):
    return a * b 

def divide(a, b):
    if b == 0:
        return None 
    return a / b

while True:
    print("\nProgram for Simple Arithmetic Calculation")
    print("1 - Addition")
    print("2 - Subtraction")
    print("3 - Multiplication")
    print("4 - Division")
    print("5 - Exit")

    try:
        choice = int(input("Enter your choice (1-5): "))
    except ValueError:
        print("Invalid input! Please enter a number between 1 and 5.")
        continue 

    if choice == 5:
        print("Thank you for visiting. Bye!")
        break 

    if choice not in [1, 2, 3, 4]:
        print("Invalid choice! Please enter a number between 1 and 5.")
        continue 
  
    try:
        first_num = float(input("Enter first number: "))
        second_num = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        continue

    
    if choice == 1:
        print("Result:", add(first_num, second_num))
    elif choice == 2:
        print("Result:", subtract(first_num, second_num))
    elif choice == 3:
        print("Result:", multiply(first_num, second_num))
    elif choice == 4:
        result = divide(first_num, second_num)
        if result is None:
            print("Error! Division by zero is not allowed.")
        else:
            print("Result:", result)
