import random

from beverages import HotBeverage, Coffee, Tea, Chocolate, Cappuccino


class CoffeeMachine:
    def __init__(self):
        self.nbr_served = 0
        pass


    class EmptyCup(HotBeverage):
        def __init__(self):
            super().__init__()
            self.price = 0.90
            self.name = "empty cup"

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.nbr_served = 0

    def serv(self, param: HotBeverage):
        if self.nbr_served == 10:
            raise self.BrokenMachineException()
        if random.randint(1, 2) == 2:
            return self.EmptyCup()
        else:
            self.nbr_served += 1
            return param

if __name__ == '__main__':
    machine = CoffeeMachine()
    beverages = [Coffee(), Tea(), Chocolate(), Cappuccino()]

    for i in range(50):
        try:
            beverage = machine.serv(beverages[random.randint(0, len(beverages) - 1)])
            print(beverage)
        except CoffeeMachine.BrokenMachineException as e:
            print("\n",e,"\n")
            machine.repair()