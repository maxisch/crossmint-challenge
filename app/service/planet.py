import logging

import requests
import tenacity

from app.utils.constants import API_BASE, CANDIDATE_ID


class PlanetService:
    @tenacity.retry(
        stop=tenacity.stop.stop_after_delay(30),
        wait=tenacity.wait.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(requests.exceptions.ConnectionError)
        | tenacity.retry_if_exception_type(requests.exceptions.HTTPError),
    )
    def create_planet(self, planet):
        body = planet.json_representation()
        body["candidateId"] = CANDIDATE_ID
        try:
            response = requests.post(f"{API_BASE}/{planet.api_path()}", json=body)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.exception("Error creating planet", e)
            raise e

    @tenacity.retry(
        stop=tenacity.stop.stop_after_delay(30),
        wait=tenacity.wait.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(requests.exceptions.ConnectionError)
        | tenacity.retry_if_exception_type(requests.exceptions.HTTPError),
    )
    def delete_planet(self, planet):
        body = planet.json_representation()
        body["candidateId"] = CANDIDATE_ID
        try:
            response = requests.delete(f"{API_BASE}/{planet.api_path()}", json=body)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.exception("Error deleting planet", e)
            raise e
