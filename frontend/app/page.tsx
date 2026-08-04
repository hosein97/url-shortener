"use client";

import {
    useState,
} from "react";

import {
    useAuth,
} from "@/hooks/useAuth";


export default function Home() {


    const {
        getAccessToken,
    } = useAuth();



    const [url, setUrl] =
        useState("");

    const [shortUrl, setShortUrl] =
        useState("");

    const [loading, setLoading] =
        useState(false);



    const shorten = async () => {


        if (!url) {
            return;
        }


        try {

            setLoading(true);


            const token =
                getAccessToken();



            const response =
                await fetch(
                    "http://localhost:8000/shorten/",
                    {

                        method: "POST",


                        headers: {

                            "Content-Type":
                                "application/json",


                            ...(token && {

                                Authorization:
                                    `Bearer ${token}`,

                            }),

                        },


                        body: JSON.stringify({

                            original_url: url,

                        }),

                    }
                );



            const data =
                await response.json();



            if (!response.ok) {

                console.error(data);

                return;

            }



            setShortUrl(
                data.short_code
            );



        } catch (error) {

            console.error(
                "Shorten failed",
                error
            );


        } finally {

            setLoading(false);

        }

    };




    return (

        <main className="min-h-screen bg-white">


            <section
                className="
                    mx-auto
                    mt-32
                    flex
                    max-w-3xl
                    flex-col
                    items-center
                    px-6
                "
            >


                <h2 className="mb-3 text-5xl font-bold">

                    Shorten your URLs

                </h2>



                <p className="mb-10 text-center text-gray-600">

                    Fast, simple and secure URL shortening.

                </p>



                <div className="flex w-full gap-4">


                    <input

                        type="url"

                        value={url}

                        onChange={(e) =>
                            setUrl(e.target.value)
                        }

                        placeholder="https://example.com/very/long/url"

                        className="
                            flex-1
                            rounded-lg
                            border
                            px-4
                            py-3
                            outline-none
                            focus:border-black
                        "

                    />



                    <button

                        onClick={shorten}

                        disabled={loading}

                        className="
                            rounded-lg
                            bg-black
                            px-8
                            py-3
                            font-medium
                            text-white
                            hover:bg-gray-800
                            disabled:opacity-50
                        "

                    >

                        {
                            loading
                                ? "Shortening..."
                                : "Shorten"
                        }


                    </button>


                </div>




                {
                shortUrl && (

                    <div className="mt-8 rounded-lg border p-4">


                        <p className="text-gray-600">

                            Your short URL:

                        </p>



                        <a

                            href={`http://localhost:8000/${shortUrl}/`}

                            target="_blank"

                            className="font-semibold text-blue-600"

                        >

                            http://localhost:8000/{shortUrl}/


                        </a>


                    </div>

                )
                }



            </section>


        </main>

    );

}