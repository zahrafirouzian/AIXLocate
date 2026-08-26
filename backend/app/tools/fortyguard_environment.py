from datetime import datetime

from app.tools.fortyguard_client import FortyGuardClient


client = FortyGuardClient()



def get_environmental_data(
    lat,
    lon,
    temperature
):

    now = datetime.now()


    payload = {

        "latitude": lat,

        "longitude": lon,

        "temperature": temperature,

        "date_time": {

            "start_date": now.strftime("%Y-%m-%d"),

            "start_time": now.strftime("%H:%M"),

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