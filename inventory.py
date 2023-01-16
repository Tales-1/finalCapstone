#========The beginning of the class==========
class Shoe:
    # Constructor function
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method for getting cost
    def get_cost(self):
        return int(self.cost)
    # Method for getting quantity
    def get_quantity(self):
        return int(self.quantity)

    # get value of item in stock, not required by the task but I decided
    # to define this method anyway

    def get_value(self):
        value = int(self.quantity) * int(self.cost)
        print(f'{self.product} value: {value} ({int(self.quantity)} x {int(self.cost)})')

    def __str__(self):
       return f"Shoe:\nName: {self.product}\nCost: {self.cost} \nQuantity: {self.quantity}Country: {self.country} \nCode:{self.code}\n"


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []
#==========Functions outside the class==============
def read_shoes_data():
    # Initiate list for a new read of the inventory to avoid appending to an existing list
    updated_shoe_list = []
    # Try and open inventory.txt incase it doesn't exist
    try:
        with open("inventory.txt", "r") as f:
            # Get the lines in a list
            file = f.readlines()
            for index,line in enumerate(file, start = 0):
                # iterate through each line skipping index 0
                if index > 0:
                    # split the line into a list and assign each index to a readable variable
                    line = line.split(",")
                    country = line[0]
                    code = line[1]
                    product = line[2]
                    cost = line[3]
                    quantity = line[4]
                    # Create a new shoe object from these details and append it to a new list
                    updated_shoe_list.append(Shoe(country, code, product, cost, quantity))
        # return value of function is a list containing the newest reading of the inventory.txt file
        return updated_shoe_list

    # If file doesn't exist, create a new inventory.txt
    except FileNotFoundError as error:
        print(f"File not found.")
        print(error)
        # if file doesn't exist, initiate a new one
        with open("inventory.txt", "w") as f:
            f.write("Country,Code,Product,Cost,Quantity \n")

# function takes in arguments required for a new shoe object
def capture_shoes(country, code, product,cost,quantity):
    # Create new shoe object with details inputted by the user
    new_shoe = Shoe(country, code, product, cost, quantity)
    # append it to the shoe_list
    shoe_list.append(new_shoe)
    # Update inventory.txt with new shoe object
    # Assign easier to read variables
    country = new_shoe.country
    code = new_shoe.code
    product = new_shoe.product
    cost = new_shoe.cost
    quantity = new_shoe.quantity
    # If file exists, append new shoe item to the inventory.txt
    try:
        with open("inventory.txt", "a") as f:
            f.write(f"\n{country},{code},{product},{cost},{quantity}\n")
    # If file doesn't exist, create a new one.
    except FileNotFoundError:
        with open("inventory.txt", "w+") as f:
            f.write("Country,Code,Product,Cost,Quantity \n")
            f.write(f"{country},{code},{product},{cost},{quantity}\n")

def view_all():
    # Get the latest reading of inventory.txt
    shoe_list = read_shoes_data()
    # If there is nothing in stock let the user know
    if not shoe_list:
        print("No stock found. Please fill up on stock")
    # Else print the details of each shoe object
    else:
        for shoe in shoe_list:
            print(shoe)    

def re_stock():
    # Get the latest reading of inventory.txt
    shoe_list = read_shoes_data()
    # Intiate empty value for the shoe to be re-stocked
    updated_shoe = None
    # If there are shoes in stock
    if shoe_list:
        # loop through list and for each shoe loop through the list again to compare 
        # The shoe with the lowest stock will be re-stocked
        for shoe in shoe_list:
            # Flag to check if the shoe with lowest qty has been found
            shoe_found = False
            for x in range(0, len(shoe_list)):
                compare_shoe = shoe_list[x]
                # If current shoe has a qty which greater than the shoe we're comparing it with
                # break out of the loop as current shoe doesn't need restocking
                if shoe.get_quantity() > compare_shoe.get_quantity():
                    break
                # If current shoe has less qty than every shoe in the list
                # Ask user for how many shoes they'd liek to restock
                elif x == len(shoe_list) - 1:
                    print(f"{shoe.product} low on stock (qty:{shoe.quantity})")
                    update_quantity = int(input("Add quantity of shoes to this stock: "))
                    # Cast shoe.quantity to int to avoid unexpected output
                    shoe.quantity = int(shoe.quantity) + update_quantity
                    # Cast back into string
                    shoe.quantity = str(shoe.quantity)
                    # store the object of the re-stocked shoe in updated_shoe
                    updated_shoe = shoe
                    # Change flag to true as the shoe has been found
                    shoe_found = True
            # break out of loop
            if shoe_found: break

        # Retrieve current inventory.txt
        data = None
        with open("inventory.txt", "r") as f:
            # Store lines in data variable
            data = f.readlines()
            for index, line in enumerate(data, start = 0):
                # find index of the re-stocked item and replace it with the updated stock
                code = line.split(",")[1]
                if updated_shoe.code == code:
                    data[index] = f"{updated_shoe.country},{updated_shoe.code},{updated_shoe.product},{updated_shoe.cost},{updated_shoe.quantity}\n"

        # Update new stock in inventory.txt with newly updated data variable
        with open("inventory.txt", "w+") as f:
            f.writelines(data)

        print(f"Restocked on {updated_shoe.product}. New quantity: {updated_shoe.quantity}")
    else:
        print("No shoes in stock.")

def search_shoe(code):
    # Get the latest reading of inventory.txt
    shoe_list = read_shoes_data()
    # If shoes are in stock then search for the shoe with the same code
    # the user has inputted and return it
    for shoe in shoe_list:
        if code.lower() == shoe.code.lower():
            return shoe

def value_per_item():
    # Get the latest reading of inventory.txt
    shoe_list = read_shoes_data()
    # If shoes are in stock call the get_value() method defined in each sheo object
    if shoe_list:
        for shoe in shoe_list:
            shoe.get_value()
    else:
        print("No shoes in stock.")

def highest_qty():
    # Get the latest reading of inventory.txt
    shoe_list = read_shoes_data()
    # Intiate empty variable which will store the shoe that is for sale
    for_sale = None
    if shoe_list:
        # loop through list and for each shoe loop through the list again to compare 
        # The shoe with the highest stock will be printed as 'for sale'
        for shoe in shoe_list:
            for x in range(0, len(shoe_list)):
                compare_shoe = shoe_list[x]
                # If current shoe has less stock than the compared shoe then break out of second loop
                if shoe.get_quantity() < compare_shoe.get_quantity():
                    break
                # If current shoe has higher stock than every shoe it has been compared to
                # Store the current shoe object in the for_sale variable
                elif x == len(shoe_list) - 1:
                    for_sale = shoe
        # Print the shoe that is for sale
        print(f"\n{for_sale.product} is for sale. {for_sale.get_quantity()} in stock.")
    else:
        print("No shoes in stock.")

#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''

while True:
    menu = input('''\nWelcome to the stock management program. Please select an option:
    1 - view details of each shoe in stock
    2 - add shoe to stock
    3 - re-stock shoes
    4 - search shoe
    5 - value of each product in stock
    6 - check which item is on for sale
    ''')

    if menu == "1":
        view_all()
       
    elif menu == "2":
        # Ask for user input on each parameter required to generate a shoe object
        country = input("Enter country where it was manufactured: ")
        code = input("Enter product code: ")
        product = input("Enter product name: ")
        cost = input("Enter product cost: ")
        quantity = input("Enter product quantity: ")
        capture_shoes(country,code,product,cost,quantity)
    
    elif menu == "3":
        re_stock()
    
    elif menu == "4":
        # Ask for user input for code of the shoe they would like to search
        code = input("\nEnter code of the shoe you would like to search: ")
        target_shoe = search_shoe(code)
        if target_shoe != None:
            print(f"\n{target_shoe}")
        else:
            print("Please enter a correct code.")
    
    elif menu == "5":
        value_per_item()

    elif menu == "6":
        highest_qty()

    elif menu == "-1":
        print("Exiting stock manager")
        exit()
        
    else:
        # Prompt user to select a correct option
        print("Please select a correct option.")