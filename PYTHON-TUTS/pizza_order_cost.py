# pizza_order_cost.py
# A script to calculate the total cost of a pizza order

def main():
    # --- User Input Section ---
    print("--- Welcome to the Pizza Order Calculator ---")
    size = input("Enter pizza size (small/large): ").strip().lower()
    try:
        toppings = int(input("Enter number of toppings: "))
        distance = float(input("Enter delivery distance in miles: "))
    except ValueError:
        print("Invalid input. Please enter numbers for toppings and distance.")
        return

    # --- Base Cost Calculation ---
    if size == "small":
        base_cost = 10.00
    elif size == "large":
        base_cost = 15.00
    else:
        print("Invalid size entered. Please restart and choose small or large.")
        return

    # --- Toppings Cost Calculation ---
    # Each topping costs $1.50
    topping_cost = toppings * 1.50

    # --- Delivery Fee Calculation ---
    # $2.00 base delivery fee for first 5 miles, $0.50 per mile after
    if distance == 0:
        delivery_fee = 0.00
    elif distance <= 5:
        delivery_fee = 2.00
    else:
        delivery_fee = 2.00 + ((distance - 5) * 0.50)

    # --- Total Cost Calculation ---
    total_cost = base_cost + topping_cost + delivery_fee

    # --- Display Result ---
    print(f"\n--- Order Summary ---")
    print(f"Base Pizza ({size}): ${base_cost:.2f}")
    print(f"Toppings ({toppings}): ${topping_cost:.2f}")
    print(f"Delivery Fee: ${delivery_fee:.2f}")
    print(f"Total Order Cost: ${total_cost:.2f}")

if __name__ == "__main__":
    main()
