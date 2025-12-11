from functions.run_python_file import run_python_file

def test():
    result = run_python_file("calculator", "main.py")
    print("Result for current directory:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Should print the calculator's usage instructions")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Should run the calculator's tests successfully")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("This should return an error")
    print(result)
    print("")


    result = run_python_file("calculator", "nonexistent.py")
    print("This should return an error")
    print(result)
    print("")


    result = run_python_file("calculator", "lorem.txt")
    print("This should return an error")
    print(result)
    print("")


if __name__ == "__main__":
    test()