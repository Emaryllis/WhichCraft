def calculator(operation, num1, num2):
    potion_result = None
    if operation == "add":
        potion_result = num1 + num2
    if operation == "subtract":
        potion_result = num1 - num2
    if operation == "multiply":
        potion_result = num1 * num2
    if operation == "divide":
        if num2 != 0:
            potion_result = num1 / num2
        else:
            raise ValueError("Error: Cannot divide by zero!")
    print(potion_result)


calculator("add", 5, 3)
calculator("subtract", 10, 2)
calculator("multiply", 4, 6)
calculator("divide", 15, 3)
