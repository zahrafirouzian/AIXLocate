import os
import requests
import time

from dotenv import load_dotenv

load_dotenv()


class FortyGuardClient:


    def __init__(self):

        self.base_url = "https://api.fortyguard.com/v1"

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
            json=payload,
            timeout=60
        )


        response.raise_for_status()


        data = response.json()

        print("SUBMIT:", data)


        return data



    def get_status(
        self,
        activity_id
    ):


        response = requests.get(
            f"{self.base_url}/status/{activity_id}",
            headers={
                "api-key": self.api_key
            },
            timeout=30
        )


        if response.status_code == 503:

            return None


        response.raise_for_status()


        return response.json()



    def wait_for_result(
        self,
        activity_id,
        timeout=300
    ):


        start = time.time()


        while True:


            if time.time()-start > timeout:

                raise TimeoutError(
                    f"FortyGuard timeout {activity_id}"
                )



            result = self.get_status(
                activity_id
            )


            if result is None:

                print(
                    "503 retry..."
                )

                time.sleep(10)

                continue



            data = result.get(
                "data",
                {}
            )


            status = data.get(
                "status",
                ""
            ).lower()


            print(
                "STATUS:",
                status
            )



            if status == "completed":

                return data



            if status in [
                "failed",
                "error"
            ]:

                raise Exception(
                    result
                )


            time.sleep(10)