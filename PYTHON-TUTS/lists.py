fruits = ['apple', 'banana', 'cherry']

fruits.append('kiwi')

for fruit in fruits:
    print(f"I like to eat {fruit}.")
    
    uppercase_fruits = [fruit.upper() for fruit in fruits]
    print('Fruits in uppercase:', uppercase_fruits)
    