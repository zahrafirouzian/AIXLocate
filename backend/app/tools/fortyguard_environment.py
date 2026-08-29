from app.tools.fortyguard_client import FortyGuardClient


client = FortyGuardClient()


def get_environmental_data(
    lat,
    lon,
    temperature
):

    payload = {

        "latitude": lat,

        "longitude": lon,

        "temperature": temperature,

        "date_time": {

            "start_date": "2024-07-15",

            "start_time": "14:00",

            "filter_type": 1

        }

    }

    response = client.submit_task(
        "/env_params",
        payload
    )

    activity_id = response["data"]["activity_id"]

    result = client.wait_for_result(
        activity_id
    )

    return result
