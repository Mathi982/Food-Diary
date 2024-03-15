import csv
import os
import itertools

CSV_FILE = 'food_items.csv'
CATEGORY_FILE = 'categories.csv'
DEFAULT_CATEGORIES = ["Main", "Snack"]

def create_csv_file():
    """ Create the CSV file with headers if it doesn't exist. """
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Category", "Subcategory", "Name", "Weight", "Calories", "Protein", "Price"])
            writer.writeheader()

def load_categories():
    """ Load categories from a file. """
    if os.path.exists(CATEGORY_FILE):
        with open(CATEGORY_FILE, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    else:
        return DEFAULT_CATEGORIES[:]

def save_categories(categories):
    """ Save the current categories to a file. """
    with open(CATEGORY_FILE, 'w', newline='') as file:
        for category in categories:
            file.write(category + '\n')

def save_to_csv(food_item):
    """ Append a food item to the CSV file. """
    try:
        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=food_item.keys())
            writer.writerow(food_item)
            print("Food item added successfully.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def input_with_validation(prompt, valid_options=None, input_type=str):
    """ Get user input and ensure it is of the correct type and value. """
    while True:
        try:
            user_input = input_type(input(prompt))
            if valid_options and user_input not in valid_options:
                raise ValueError("Invalid option selected.")
            return user_input
        except ValueError as e:
            print(e)

def add_or_get_category(categories):
    print("Current categories:", ", ".join(categories))
    new_category = input("Enter a category (or create a new one): ")
    if new_category in categories:
        print("This category already exists.")
        return None
    elif new_category != '0':
        categories.append(new_category)
        save_categories(categories)
        return new_category
    return None

def display_categories(categories):
    """ Display the current categories with an option to add a new one using 'n'. """
    for idx, category in enumerate(categories, start=1):
        print(f"{idx}. {category}")
    print("n. Add your own category")
    print("0. Go Back")

def add_food_item(categories):
    """ Add a new food item, including the option to add a new category. """
    while True:
        print("\nAdding New Food Item:")
        display_categories(categories)

        category_choice = input("Choose a category, 'n' for new category, or '0' to go back: ").lower()

        if category_choice == '0':
            return None  # Go back to the main menu
        elif category_choice == 'n':
            category = add_or_get_category(categories)
            if category == '0' or category is None:
                continue  # Redisplay category options
            sub_category = ""
        elif category_choice.isdigit() and 1 <= int(category_choice) <= len(categories):
            category = categories[int(category_choice) - 1]
            sub_category = ""
        else:
            print("Invalid option. Please try again.")
            continue

        # Sub-category logic
        if category == "Main":
            sub_category_choice = input_with_validation(
                "Enter 1 for Main Protein Source (Chicken, Beef, etc.) or 2 for Staple/Side (Rice, Noodles, etc.): ",
                valid_options=[1, 2],
                input_type=int
            )
            sub_category = "Main Protein Source" if sub_category_choice == 1 else "Staple/Side"

        # Checking for duplicate food item
        existing_food_items = read_food_items()
        name = input_with_validation("Enter the name of the food: ")
        if any(item['Name'].lower() == name.lower() and item['Category'].lower() == category.lower() for item in existing_food_items):
            print(f"A food item with the name '{name}' in category '{category}' already exists.")
            continue  # Prompt the user to enter the details again

        weight = input_with_validation("Enter the weight of the food (in grams): ", input_type=float)
        calories = input_with_validation("Enter the calorie content: ", input_type=int)
        protein = input_with_validation("Enter the protein content (in grams): ", input_type=float)
        price = input_with_validation("Enter the price in £: ", input_type=float)

        return {
            "Category": category,
            "Subcategory": sub_category,
            "Name": name,
            "Weight": weight,
            "Calories": calories,
            "Protein": protein,
            "Price": price
        }



def read_food_items():
    """ Read and return food items from the CSV file. """
    food_items = []
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food_items.append(row)
    except IOError as e:
        print(f"Error reading file: {e}")
    return food_items

def display_food_items(food_items):
    """ Display the list of food items with an index for selection. """
    for idx, item in enumerate(food_items, start=1):
        print(f"{idx}. {item['Name']} - {item['Category']} ({item['Subcategory']}) - {item['Calories']} calories - {item['Protein']}g protein - £{item['Price']}")

def edit_food_item(food_items, index):
    """ Edit a selected food item. """
    item = food_items[index]
    print(f"Editing '{item['Name']}'")
    for field in ['Name', 'Calories', 'Protein', 'Price']:
        new_value = input(f"Enter new {field} (leave blank to keep current value): ")
        if new_value:
            item[field] = new_value
    new_category = input("Enter new Category (leave blank to keep current value): ")
    if new_category:
        item['Category'] = new_category
    save_all_food_items(food_items)  # Save changes back to CSV
    print("Item updated successfully.")

def delete_food_item(food_items, index):
    """ Delete a selected food item after confirmation. """
    item = food_items.pop(index)
    if input(f"Are you sure you want to delete '{item['Name']}'? (y/n): ").lower() == 'y':
        save_all_food_items(food_items)  # Save changes back to CSV
        print("Item deleted successfully.")
    else:
        print("Deletion cancelled.")

def save_all_food_items(food_items):
    """ Save the entire list of food items back to the CSV file. """
    try:
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=food_items[0].keys())
            writer.writeheader()
            for item in food_items:
                writer.writerow(item)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def show_items():
    """ Show food items and handle edit/delete actions. """
    food_items = read_food_items()
    if not food_items:
        print("No food items found.")
        return

    while True:
        print("\nFood Items:")
        display_food_items(food_items)
        print("0. Go Back")
        choice = input("Enter the number of the item to edit/delete, or 0 to go back: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                break
            elif 1 <= choice <= len(food_items):
                action = input("Enter 'e' to edit or 'd' to delete: ").lower()
                if action == 'e':
                    edit_food_item(food_items, choice - 1)
                elif action == 'd':
                    delete_food_item(food_items, choice - 1)
                else:
                    print("Invalid action.")
            else:
                print("Invalid selection. Please choose a valid item number.")
        else:
            print("Please enter a number.")


def search_food_items():
    """ Search for food items by name or category. """
    search_query = input("Enter food name or category to search for: ").lower()
    food_items = read_food_items()
    found_items = [item for item in food_items if
                   search_query in item['Name'].lower() or search_query in item['Category'].lower()]

    if found_items:
        print("Found the following items:")
        display_food_items(found_items)
    else:
        print("No items found matching the search criteria.")

def generate_meal_plan(food_items, criteria):
    """ Generate meal plans based on specified criteria. """
    def meets_criteria(combination):
        total_calories = sum(float(item['Calories']) for item in combination)
        total_protein = sum(float(item['Protein']) for item in combination)
        total_price = sum(float(item['Price']) for item in combination)

        return ((criteria['calories_lower'] <= total_calories <= criteria['calories_upper']) if criteria['calories_lower'] is not None else True) and \
               ((criteria['protein_lower'] <= total_protein <= criteria['protein_upper']) if criteria['protein_lower'] is not None else True) and \
               ((criteria['price_lower'] <= total_price <= criteria['price_upper']) if criteria['price_lower'] is not None else True)

    # Adjust 'r' as needed for combination size
    for r in range(1, len(food_items) + 1):
        for combination in itertools.combinations(food_items, r):
            if meets_criteria(combination):
                yield combination

def get_user_criteria():
    """ Get meal plan criteria from the user. """
    print("Enter your meal plan criteria (leave blank if no preference):")
    criteria = {
        'calories_lower': None, 'calories_upper': None,
        'protein_lower': None, 'protein_upper': None,
        'price_lower': None, 'price_upper': None
    }
    for key in criteria:
        value = input(f"{key.replace('_', ' ').title()}: ")
        criteria[key] = float(value) if value else None
    return criteria


def display_and_save_meal_plans(meal_plans, user_criteria, file_path):
    """ Display generated meal plans in a table and save them to a CSV file. """
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Meal Plan', 'User Criteria', 'Total Calories', 'Total Protein', 'Total Price'])

        for idx, plan in enumerate(meal_plans, start=1):
            total_calories = sum(float(item['Calories']) for item in plan)
            total_protein = sum(float(item['Protein']) for item in plan)
            total_price = sum(float(item['Price']) for item in plan)
            plan_details = [f"{item['Name']} ({item['Calories']} cal, {item['Protein']}g prot, £{item['Price']})" for item in plan]

            print(f"Meal Plan {idx}:")
            for detail in plan_details:
                print(f" - {detail}")
            print(f"Totals: {total_calories} calories, {total_protein}g protein, £{total_price}\n")

            criteria_details = ', '.join([f"{k}: {v}" for k, v in user_criteria.items() if v is not None])
            writer.writerow([f"Plan {idx}", criteria_details, total_calories, total_protein, total_price] + plan_details)


def main():
    categories = load_categories()
    create_csv_file()
    food_items = read_food_items()

    while True:
        print("\nMenu Options")
        print("1. Add Food Item")
        print("2. Show Items")
        print("3. Generate Meal Plan")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            food_item = add_food_item(categories)
            if food_item:
                save_to_csv(food_item)
        elif choice == '2':
            show_items()
        elif choice == '3':
            criteria = get_user_criteria()
            meal_plans = list(generate_meal_plan(food_items, criteria))
            if meal_plans:
                display_and_save_meal_plans(meal_plans, criteria, 'meal_plans.csv')
            else:
                print("No meal plans found that match the criteria.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == '__main__':
    main()
