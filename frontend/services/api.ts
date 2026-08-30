const API_URL = "";

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
        let message = "API request failed";

        try {
            const errorData = await response.json();

            if (errorData?.detail) {
                message = errorData.detail;
            }
        } catch {
            // Ignore JSON parsing errors
        }

        throw new Error(message);
    }

    return await response.json();
}