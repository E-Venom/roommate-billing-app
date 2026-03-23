class Bill:
    """
    Object that contains data about a bill one must pay.
    Data includes:
        - amount
        - period
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Roommate:
    """
    Creates a roommate person who lives in the apartment
    and pays a share of the bill.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill, other_roommate):
        """
        Calculates this roommate's share of the bill based on time spent in the house.
        Args:
            bill (Bill): The bill to be split.
            other_roommate (Roommate): The other roommate sharing the bill.
        Returns:
            float: The amount this roommate needs to pay.
        Notes:
            The bill is split proportionally based on the number of days
            each roommate stayed in the house.
        Raises:
            ZeroDivisionError: If both roommates have zero days in the house.
        """
        if self.days_in_house == 0 and other_roommate.days_in_house == 0:
            raise ZeroDivisionError("Both roommate have zero days in the house.")

        weight = self.days_in_house / (self.days_in_house + other_roommate.days_in_house)
        amount_to_pay = weight * bill.amount
        return amount_to_pay
