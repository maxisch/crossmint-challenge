import logging
from enum import Enum


class Color(Enum):
    BLUE = 1
    RED = 2
    PURPLE = 3
    WHITE = 4


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class SpaceObject(Enum):
    SPACE = 1
    POLYANET = 2
    LEFT_COMETH = 3
    RIGHT_COMETH = 4
    UP_COMETH = 5
    DOWN_COMETH = 6
    BLUE_SOLOON = 7
    RED_SOLOON = 8
    PURPLE_SOLOON = 9
    WHITE_SOLOON = 10


class Planet:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def valid_position(self, map):
        return True

    def api_path(self):
        return ""

    def json_representation(self):
        return {"row": self.row, "column": self.column}


class Polyanet(Planet):
    def __init__(self, row, column):
        super().__init__(row, column)

    def api_path(self):
        return "/polyanets"


class Soloon(Planet):
    def __init__(self, row, column, color):
        super().__init__(row, column)
        self.color = color

    def api_path(self):
        return "/soloons"

    def json_representation(self):
        rep = super().json_representation()
        rep["color"] = self.color.name.lower()
        return rep

    def valid_position(self, map):
        max_y = len(map) - 1
        max_x = len(map[0]) - 1
        return (
            # Check neighbour to the right
            self._valid_neighbour(map, self.column + 1, self.row, max_x, max_y)
            # Check neighbour to the left
            or self._valid_neighbour(map, self.column - 1, self.row, max_x, max_y)
            # Check neighbour below
            or self._valid_neighbour(map, self.column, self.row + 1, max_x, max_y)
            # Check neighbour above
            or self._valid_neighbour(map, self.column, self.row - 1, max_x, max_y)
        )

    def _valid_neighbour(self, map, x, y, max_x, max_y):
        if x > max_x or y > max_y or x < 0 or y < 0:
            return False
        return isinstance(map[x][y], Polyanet)


class Cometh(Planet):
    def __init__(self, row, column, direction):
        super().__init__(row, column)
        self.direction = direction

    def api_path(self):
        return "/comeths"

    def json_representation(self):
        rep = super().json_representation()
        rep["direction"] = self.direction.name.lower()
        return rep


class PlanetFactory:
    @staticmethod
    def get_planet(space_object, row, column):
        try:
            space_object = SpaceObject[space_object]
            match space_object:
                case SpaceObject.SPACE:
                    return None
                case SpaceObject.POLYANET:
                    return Polyanet(row, column)
                case SpaceObject.LEFT_COMETH:
                    return Cometh(row, column, Direction.LEFT)
                case SpaceObject.RIGHT_COMETH:
                    return Cometh(row, column, Direction.RIGHT)
                case SpaceObject.UP_COMETH:
                    return Cometh(row, column, Direction.UP)
                case SpaceObject.DOWN_COMETH:
                    return Cometh(row, column, Direction.DOWN)
                case SpaceObject.BLUE_SOLOON:
                    return Soloon(row, column, Color.BLUE)
                case SpaceObject.RED_SOLOON:
                    return Soloon(row, column, Color.RED)
                case SpaceObject.PURPLE_SOLOON:
                    return Soloon(row, column, Color.PURPLE)
                case SpaceObject.WHITE_SOLOON:
                    return Soloon(row, column, Color.WHITE)
                case _:
                    return None

        except Exception:
            logging.error(f"Could not parse space object type: {space_object}")
            return None
