# 1. Create a tuple
coordinates = (10, 20, 30)
print("Tuple:", coordinates)

# 2. Print elements in a tuple
print("Element at index 0:", coordinates[0])
print("Element at index 2:", coordinates[2])

# 3. Use tuple methods
# count() counts how many times a value appears
example_tuple = (1, 2, 3, 2, 4, 2)
print("Count of 2 in example_tuple:", example_tuple.count(2))

# index() finds the first occurrence of a value
print("Index of 3 in example_tuple:", example_tuple.index(3))

# 4. Check for the presence of an element
if 20 in coordinates:
    print("20 is in the coordinates tuple")
else:
    print("20 is not in the coordinates tuple")

# 5. Implement tuples in a function
def get_first_and_last(tup):
    """Returns the first and last elements of a tuple"""
    return (tup[0], tup[-1])

result = get_first_and_last(coordinates)
print("First and last elements:", result)
