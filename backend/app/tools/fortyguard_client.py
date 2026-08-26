import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class FortyGuardClient:

    def __init__(self):

        self.base_url="https://api.fortyguard.com/v1"
        self.api_key = os.getenv(
            "FORTYGUARD_API_KEY"
        )


    def headers(self):

        return {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def submit_task(
        self,
        endpoint,
        payload
    ):

        response = requests.post(
            self.base_url + endpoint,
            headers=self.headers(),
            json=payload
        )


        if response.status_code >= 400:
            print("STATUS:", response.status_code)
            print("ERROR:", response.text)


        response.raise_for_status()

        return response.json()


    def get_status(
        self,
        activity_id
    ):

        response = requests.get(
            f"{self.base_url}/status/{activity_id}",
            headers={
                "api-key": self.api_key
            }
        )

        response.raise_for_status()

        return response.json()


    def wait_for_result(
        self,
        activity_id,
        timeout=120
    ):

        start = time.time()


        while time.time() - start < timeout:

            result = self.get_status(
                activity_id
            )

            data = result["data"]

            status = data["status"].lower()


            if status in [
                "completed",
                "succeeded"
            ]:
                return data


            if status in [
                "failed",
                "error"
            ]:
                raise Exception(
                    "FortyGuard task failed"
                )


            time.sleep(5)


        raise TimeoutError(
            "FortyGuard timeout"
        )