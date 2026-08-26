const API_URL = "http://127.0.0.1:8000";


export async function analyzeLocation(data: any) {

    const response = await fetch(
        `${API_URL}/api/analyze`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(data),
        }
    );


    if (!response.ok) {
        throw new Error("API request failed");
    }


    return await response.json();
}