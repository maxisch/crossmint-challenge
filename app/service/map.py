import json
import logging
from collections import deque

import requests
import tenacity

from app.model.planets import PlanetFactory, Polyanet
from app.service.planet import PlanetService
from app.utils.constants import API_BASE, CANDIDATE_ID


class MapService:
    @tenacity.retry(
        stop=tenacity.stop.stop_after_delay(20),
        wait=tenacity.wait.wait_fixed(2),
        retry=tenacity.retry_if_exception_type(requests.exceptions.ConnectionError),
    )
    def fetch_target_map(self):
        try:
            response = requests.get(f"{API_BASE}/map/{CANDIDATE_ID}/goal")
            response.raise_for_status()
            goal_matrix = json.loads(response.text)["goal"]
            return self._parse_matrix(goal_matrix)
        except requests.exceptions.HTTPError as e:
            logging.exception("Error fetching target map", e)
            raise e

    def fill_map(self):
        target_map = self.fetch_target_map()
        self._validate_map(target_map)
        sorted_planets = self._sort_planets(target_map)
        planet_service = PlanetService()
        for planet in sorted_planets:
            planet_service.create_planet(planet)
        pass

    def reset_map(self):
        target_map = self.fetch_target_map()
        sorted_planets = self._sort_planets(target_map)
        planet_service = PlanetService()
        for planet in sorted_planets:
            planet_service.delete_planet(planet)
        pass

    def _sort_planets(self, map):
        """
        We flatten our matrix into a list, implementing a naive topological sort as our SOLoons have a positional
        dependency with the POLYanet. By doing this we avoid any temporal inconsistencies that could have happened if
        we created SOLoons first and POLYanet later, which would have been the case if we simply traversed the matrix
        and created each planet as we go.
        We also filter out empty cells in the process. ("SPACE" cells)

        The sort is straightforward: We start with an emtpy list and prepend POLYanet and append anything else.
        The overall complexity will be O(ROWS * COLUMNS)
        """

        planets = deque([])
        for row in map:
            for cell in row:
                if cell:
                    if isinstance(cell, Polyanet):
                        planets.appendleft(cell)
                    else:
                        planets.append(cell)
        return planets

    def _validate_map(self, map):
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell and not cell.valid_position(map):
                    raise Exception(f"Not valid position for planet at: [{i}][{j}]")

    def _parse_matrix(self, goal_matrix):
        row_count = len(goal_matrix)
        column_count = len(goal_matrix[0])
        matrix = [[None] * column_count for _ in range(row_count)]

        for i, row in enumerate(goal_matrix):
            for j, cell in enumerate(row):
                matrix[i][j] = PlanetFactory.get_planet(cell, i, j)
        return matrix
