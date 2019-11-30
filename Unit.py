import Global as Globe
import Popup


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

    def move(self, quantity, direction, units):
        # direction is a tuple of 2 numbers +1/-1, +1/-1
        # Units is a list that will be appended to
        # Quantity is the split quantity

        # Saves the position that this unit will be for popup
        saved_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])

        # This is called only if there is a unit combination of moved and not moved units. This will split the unit
        # according to the sidebar
        if quantity < self.quantity:
            units.append(Unit([self.pos[0] + direction[0], self.pos[1] + direction[1]], quantity, self.owner))
            self.quantity -= quantity
            self.quantity_not_moved -= quantity
            # The new unit has moved so it must be set to moved
            units[-1].quantity_not_moved = 0
            units[-1].quantity_moved = quantity
        else:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]

            self.set_moved()

        # Calculates units that are in the way of the movement and in opposite team
        attacking_units = [unit for unit in units if (unit.pos[0] == saved_pos[0]) and (unit.pos[1] == saved_pos[1])]
        if len(attacking_units) > 1:
            if attacking_units[0].owner != attacking_units[1].owner:
                # Locks the layer
                Globe.layers[0].update_lock = True
                # Creates a popup
                Globe.layers.append(Popup.Popup(False, False, False, attacking_units))

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
