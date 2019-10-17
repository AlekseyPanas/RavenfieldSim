class Unit:
    def __init__(self, pos, quantity, owner):
        # Grid position
        self.pos = pos

        # Amount of soldiers in this unit (in tens)
        self.quantity = quantity
        self.quantity_moved = 0
        self.quantity_not_moved = self.quantity

        # Is the unit being selected
        self.selected = False

        # "b" for eagles "r" for ravens
        self.owner = owner

    def set_moved(self):
        self.quantity_moved = self.quantity
        self.quantity_not_moved = 0

    @staticmethod
    def stack(unts):
        units = unts

        remove_list = []

        # Iterates through all units
        for unit in units:
            # If this unit wasn't already queued for removal
            if unit not in remove_list:
                quantity = 0
                quantity_moved = 0
                quantity_not_moved = 0
                # Scans all units to check for multiple units in same tile
                for unit2 in list(filter(lambda x: x.pos == unit.pos, units)):
                    # Adds quantities of units in same tile
                    quantity += unit2.quantity
                    quantity_moved += unit2.quantity_moved
                    quantity_not_moved += unit2.quantity_not_moved
                    # Queues removal of all units except one in that same tile
                    if not unit2 == unit:
                        remove_list.append(unit2)
                unit.quantity = quantity
                unit.quantity_moved = quantity_moved
                unit.quantity_not_moved = quantity_not_moved

        for unit in remove_list:
            units.remove(unit)

        return units
