export const API_URL =
    process.env.NEXT_PUBLIC_API_URL;


export async function shortenURL(
    original_url: string,
    token?: string,
) {

    const response = await fetch(
        `${API_URL}/shorten/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",

                ...(token
                    ? {
                        Authorization: `Bearer ${token}`,
                    }
                    : {}),
            },

            body: JSON.stringify({
                original_url,
            }),
        }
    );


    if (!response.ok) {

        const text = await response.text();

        throw new Error(text);
    }


    return response.json();
}