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

        if not self.api_key:
            raise ValueError(
                "FORTYGUARD_API_KEY is not set"
            )

    # --------------------------------------------------
    # Headers
    # --------------------------------------------------

    def headers(self):

        return {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

    # --------------------------------------------------
    # Submit task
    # --------------------------------------------------

    def submit_task(
        self,
        endpoint,
        payload,
    ):

        print(
            "\n===== FORTYGUARD SUBMIT ====="
        )

        print(
            "Endpoint:",
            endpoint
        )

        try:

            response = requests.post(
                self.base_url + endpoint,
                headers=self.headers(),
                json=payload,
                timeout=60,
            )

        except requests.exceptions.Timeout:

            print(
                "\nFORTYGUARD SUBMIT TIMEOUT"
            )

            raise

        except requests.exceptions.ConnectionError as e:

            print(
                "\nFORTYGUARD CONNECTION ERROR"
            )

            print(
                "Error:",
                e
            )

            raise

        # --------------------------------------------------
        # Detailed API error
        # --------------------------------------------------

        if not response.ok:

            print(
                "FORTYGUARD ERROR STATUS:",
                response.status_code
            )

            print(
                "FORTYGUARD ERROR BODY:",
                response.text
            )

        response.raise_for_status()

        try:

            data = response.json()

        except ValueError:

            print(
                "FORTYGUARD INVALID JSON RESPONSE:"
            )

            print(
                response.text
            )

            raise

        print(
            "SUBMIT:",
            data
        )

        print(
            "============================\n"
        )

        return data

    # --------------------------------------------------
    # Get task status
    # --------------------------------------------------

    def get_status(
        self,
        activity_id,
    ):

        url = (
            f"{self.base_url}/status/"
            f"{activity_id}"
        )

        try:

            response = requests.get(
                url,
                headers={
                    "api-key": self.api_key
                },
                timeout=60,
            )

        except requests.exceptions.ReadTimeout:

            print(
                "\nFORTYGUARD STATUS REQUEST TIMEOUT"
            )

            print(
                "Activity:",
                activity_id
            )

            return None

        except requests.exceptions.ConnectionError as e:

            print(
                "\nFORTYGUARD CONNECTION ERROR"
            )

            print(
                "Activity:",
                activity_id
            )

            print(
                "Error:",
                e
            )

            return None

        # --------------------------------------------------
        # Temporary HTTP errors
        # --------------------------------------------------

        if response.status_code in (
            502,
            503,
            504,
        ):

            print(
                "\n===== FORTYGUARD TEMPORARY ERROR ====="
            )

            print(
                "Status:",
                response.status_code
            )

            print(
                "Activity:",
                activity_id
            )

            print(
                "Response body:",
                response.text
            )

            print(
                "========================================"
            )

            return None

        # --------------------------------------------------
        # Other HTTP errors
        # --------------------------------------------------

        if not response.ok:

            print(
                "\n===== FORTYGUARD STATUS ERROR ====="
            )

            print(
                "Status:",
                response.status_code
            )

            print(
                "Activity:",
                activity_id
            )

            print(
                "Response body:",
                response.text
            )

            print(
                "===================================="
            )

            response.raise_for_status()

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            return response.json()

        except ValueError:

            print(
                "\nFORTYGUARD INVALID STATUS JSON"
            )

            print(
                "HTTP status:",
                response.status_code
            )

            print(
                "Response:",
                response.text
            )

            return None

    # --------------------------------------------------
    # Wait for task result
    # --------------------------------------------------

    def wait_for_result(
        self,
        activity_id,
        timeout=600,
        poll_interval=5,
    ):

        print(
            "\n===== WAITING FOR FORTYGUARD ====="
        )

        print(
            "Activity ID:",
            activity_id
        )

        print(
            "Maximum wait:",
            timeout,
            "seconds"
        )

        print(
            "Poll interval:",
            poll_interval,
            "seconds"
        )

        print(
            "==================================\n"
        )

        start = time.time()

        while True:

            elapsed = (
                time.time()
                - start
            )

            # --------------------------------------------------
            # Overall timeout
            # --------------------------------------------------

            if elapsed >= timeout:

                raise TimeoutError(
                    "FortyGuard task timeout: "
                    f"{activity_id}"
                )

            # --------------------------------------------------
            # Request status
            # --------------------------------------------------

            result = self.get_status(
                activity_id
            )

            # --------------------------------------------------
            # Temporary request failure
            # --------------------------------------------------

            if result is None:

                print(
                    "Status unavailable."
                )

                print(
                    f"Retrying in {poll_interval} seconds..."
                )

                time.sleep(
                    poll_interval
                )

                continue

            # --------------------------------------------------
            # API-level error
            # --------------------------------------------------

            if result.get("error"):

                print(
                    "\n===== FORTYGUARD API ERROR ====="
                )

                print(
                    result
                )

                print(
                    "=================================\n"
                )

                raise Exception(
                    "FortyGuard status API returned "
                    f"an error: {result}"
                )

            # --------------------------------------------------
            # Extract data
            # --------------------------------------------------

            data = result.get(
                "data",
                {}
            )

            status = str(
                data.get(
                    "status",
                    ""
                )
            ).lower()

            print(
                "STATUS:",
                status,
                "| ELAPSED:",
                round(elapsed),
                "seconds"
            )

            # --------------------------------------------------
            # Completed
            # --------------------------------------------------

            if status in (
                "completed",
                "succeeded",
                "success",
            ):

                print(
                    "\n===== FORTYGUARD COMPLETED ====="
                )

                print(
                    "Activity:",
                    activity_id
                )

                print(
                    "Elapsed:",
                    round(elapsed),
                    "seconds"
                )

                print(
                    "================================\n"
                )

                return data

            # --------------------------------------------------
            # Failed
            # --------------------------------------------------

            if status in (
                "failed",
                "error",
            ):

                print(
                    "\n===== FORTYGUARD TASK FAILED ====="
                )

                print(
                    "Activity:",
                    activity_id
                )

                print(
                    "Result:",
                    result
                )

                print(
                    "==================================\n"
                )

                raise Exception(
                    "FortyGuard task failed: "
                    f"{result}"
                )

            # --------------------------------------------------
            # Still processing
            # --------------------------------------------------

            print(
                "Task still processing..."
            )

            time.sleep(
                poll_interval
            )