from app.tools.fortyguard_client import FortyGuardClient


client = FortyGuardClient()



def create_heatmap(payload):


    response = client.submit_task(
        "/heatmap",
        payload
    )


    activity_id = response["data"]["activity_id"]


    return client.wait_for_result(
        activity_id
    )