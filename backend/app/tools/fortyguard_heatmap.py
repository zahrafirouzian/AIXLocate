from pprint import pprint

from app.tools.fortyguard_client import FortyGuardClient


client = FortyGuardClient()


def create_heatmap(payload):

    print("\n===== HEATMAP PAYLOAD =====")
    pprint(payload)
    print("===========================\n")

    response = client.submit_task(
        "/heatmap",
        payload
    )

    print(
        "HEATMAP SUBMIT:",
        response
    )

    activity_id = response["data"]["activity_id"]

    result = client.wait_for_result(
        activity_id
    )

    print(
        "HEATMAP COMPLETED"
    )

    return result