class Flight:
    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError("No airline code in {}".format(number))
        if not number[:2].isupper():
            raise ValueError("Invalid airline code in {}".format(number))
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number {}".format(number))
        self._number=number
        self._aircraft=aircraft
        rows, seats = self._aircraft.seating_plan()
        self._seating= [None] + [{letter: None for letter in seats} for _ in rows]
    def number(self):
        return self._number
    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger
        Args:
            seat: A seat deisgnator such as '12C' or '21F'
            passenger: The passenger Name
        Raises:
            ValueError: If the seat is unavialble
        """
        rows, seat_letters = self._aircraft.seating_plan()

        letter=seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalide seat letter {}".format(letter))

        row_text=seat[:1]
        try:
            row=int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in rows:
            raise ValueError("Invalid row number {}".format(row))

        if self._seating[row][letter] is not None:
            raise ValueError("seat {} is already occupied".format(seat))

        self._seating[row][letter] = passenger

    def _parse_seat(self, seat):
        """Parse a seat designator into a valid row and letter

        Args:
            seat: A seat designator such as 12F

        Returns:
            A tuple containing an integer and string for row and seat
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()

        letter=seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalide seat letter {}".format(letter))

        row_text=seat[:-1]
        try:
            row=int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))

        if row not in row_numbers:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter

    def allocate_seat(self, seat, passenger):
        """Allocate a seat to a passenger.
        Args:
            seat: A seat designator such as 12F
            passenger: The passenger name

        Raise:
            ValueError: If the seat in unavialble
        """
        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("seat {} is already occupied".format(seat))

        self._seating[row][letter] = passenger

    def relocate_passenger(self, from_seat, to_seat):
        """Relocate a passenger to a different seat

        Args:
            from_seat: The existing seat designator for
                       passenger to  be moved

            to_seat: The new seat designator
        """
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate in seat {}".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} already occupied".format(to_seat))

        self._seating[to_row][to_letter]=self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_avialble_seats(self):
        return sum( sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)
class AirCraft:
    def __init__(self,registration, model, num_rows, num_seats_per_row):
        self._registration=registration
        self._model=model
        self._num_rows=num_rows
        self._num_seats_per_row=num_seats_per_row
    def registration(self):
        return self._registration
    def model(self):
        return self._model
    def seating_plan(self):
        return (range(1, self._num_rows + 1), "ABCDEFGK"[:self._num_seats_per_row])

from pprint import pprint as pp
def make_flight():
    f= Flight("BA587", AirCraft("G_EUPT", "AirBus A319", num_rows=22, num_seats_per_row=6))
    f.allocate_seat('12A', 'Vijay')
    f.allocate_seat('15F', 'Vicky')
    f.allocate_seat('15E', 'Kumar')
    f.allocate_seat('1C', 'Jhon')
    f.allocate_seat('1D', 'Richard')
    return f
f = make_flight()
pp(f._seating)
f.relocate_passenger('12A', '15D')
pp(f._seating)
pp(f.num_avialble_seats())
