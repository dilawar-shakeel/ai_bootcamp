class vending_machine_inventory_and_cash():
    def __init__(self):
        self.vending_machine_inventory = {
    "1": {
        "product_name": "Potato Chips",
        "quantity": 10,
        "price": 50.0
    },
    "2": {
        "product_name": "Chocolate Bar",
        "quantity": 7,
        "price": 40.0
    },
    "3": {
        "product_name": "Coca-Cola",
        "quantity": 15,
        "price": 100.0
    },
    "4": {
        "product_name": "Sparkling Water",
        "quantity": 1,
        "price": 30.0
    },
    "5": {
        "product_name": "Energy Drink",
        "quantity": 5,
        "price": 150.0
    }
}

    def get_min_order_value(self):
        x = [self.vending_machine_inventory[i]["price"] for i in self.vending_machine_inventory if self.is_available(i)]
        return min(x)
    
    def is_available(self,item):
        if self.vending_machine_inventory[item]["quantity"] > 0:
            return True
        else:
            return False
        
    def update_invenory(self,item,qty=1):
        self.vending_machine_inventory[item]["quantity"] -= qty
        return self.vending_machine_inventory[item]["quantity"]

    def menu(self):
        for x in self.vending_machine_inventory:
            if self.vending_machine_inventory[x]["quantity"] > 0:
                print(f"{x} -> {self.vending_machine_inventory[x]["product_name"]} | {self.vending_machine_inventory[x]["price"]} pkr")

    def get_total_items(self):
        return len(self.vending_machine_inventory)            




class Vending_machine_state_managment (vending_machine_inventory_and_cash):

    def __init__(self):
        super().__init__()
        self.inserted_cash=0.0
        self.order_value=0.0
        self.returning_cash=0.0
        self.product_selected=None

    
    def idle_state(self):
        while True:
            self.inserted_cash=float(input("Idle State -> (Max: 500 PKR)Please Insert Cash: "))
            if self.is_inserted_cash_valid():
                break
            else:
                continue
        self.selection_state()

    def selection_state(self):

        self.menu()
        while True:
            if self.product_selection():
                self.dispensing_state()
                if self.returning_cash>self.get_min_order_value():
                    choice=input(f"Your remainig cash is {self.returning_cash} Would you like to shop more? (y/n)")
                    if choice == "y":
                        self.inserted_cash=self.returning_cash
                        self.menu()
                        continue
                    elif choice == "n":
                        print(f"Dispensig {self.returning_cash} PKR")
                else:
                       print(f"Dispensig {self.returning_cash} PKR")
                    
                break   
            else:
                continue        




    # def selection_state(self):
    #     print("waiting for selection")
    #     pass

    def dispensing_state(self, only_cash=False):
        if only_cash:
            print(f"Dispensing {self.inserted_cash} PKR")
            return
        else:
            print(f"Dispensing  {self.vending_machine_inventory[self.product_selected]} -- Invertory Updated {self.vending_machine_inventory[self.product_selected]["quantity"]} -> {self.update_invenory(self.product_selected)}")

    
    def is_inserted_cash_valid(self):
        if self.inserted_cash>=self.get_min_order_value() and self.inserted_cash<=500.0:
            return True
        else:
            print("Invalid Insertion")
            return False
        

    def product_selection(self):
        self.product_selected=input("Select Your Product:")
        if int(self.product_selected) > self.get_total_items() and int(self.product_selected) > 0 :
            print("Invalid Insertion")
            return False
        elif not self.is_available(self.product_selected):
            print("Invalid Insertion")
            return False    
        elif self.vending_machine_inventory[self.product_selected]["price"] <= self.inserted_cash:        
                self.order_value = self.vending_machine_inventory[self.product_selected]["price"]
                print(f"Selected -> {self.vending_machine_inventory[self.product_selected]["product_name"]}     --- Remaining Cash: {self.get_remainig_cash()}")
                return True
        else:
            print("Invalid Insertion")
            return False                
            
    def get_remainig_cash(self):
        self.returning_cash= self.inserted_cash - self.order_value
        return self.returning_cash
    
    
        

One = Vending_machine_state_managment()
One.idle_state()
