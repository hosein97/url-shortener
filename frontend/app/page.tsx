"use client";


import {
    useState,
} from "react";


import {
    useAuth,
} from "@/hooks/useAuth";


import {
    shortenURL,
} from "@/lib/api";



export default function Home(){


    const {

        initialized,

        authenticated,

        login,

        logout,

        register,

        getAccessToken,

        user,

    } = useAuth();



    const [url,setUrl]=useState("");

    const [result,setResult]=useState("");

    const [loading,setLoading]=useState(false);




    async function handleShorten(){


        try{

            setLoading(true);


            const data =
                await shortenURL(
                    url,
                    getAccessToken(),
                );


            setResult(
                data.short_code
            );


        }
        catch(e){

            console.error(e);

            alert(
                "Failed to shorten URL"
            );

        }
        finally{

            setLoading(false);

        }

    }




    return (

        <main className="min-h-screen bg-white">


            <nav className="border-b">

                <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">


                    <h1 className="text-2xl font-bold">
                        Shortly
                    </h1>



                    <div className="flex gap-3">


                        {!initialized ? (

                            <button
                                disabled
                                className="rounded-md border px-4 py-2 text-gray-400"
                            >
                                Loading...
                            </button>


                        ) : authenticated ? (

                            <>

                                <span className="py-2 text-sm">
                                    {user?.username}
                                </span>


                                <button
                                    onClick={logout}
                                    className="rounded-md border px-4 py-2"
                                >
                                    Logout
                                </button>

                            </>


                        ) : (

                            <>

                                <button
                                    onClick={login}
                                    className="rounded-md border px-4 py-2"
                                >
                                    Login
                                </button>


                                <button
                                    onClick={register}
                                    className="rounded-md bg-black px-4 py-2 text-white"
                                >
                                    Register
                                </button>

                            </>

                        )}


                    </div>

                </div>

            </nav>



            <section className="mx-auto mt-32 max-w-3xl px-6">


                <h2 className="mb-3 text-center text-5xl font-bold">
                    Shorten your URLs
                </h2>


                <p className="mb-10 text-center text-gray-600">
                    Fast, simple and secure URL shortening.
                </p>



                <div className="flex gap-4">


                    <input

                        value={url}

                        onChange={
                            e=>setUrl(e.target.value)
                        }

                        placeholder="https://example.com"

                        className="flex-1 rounded-lg border px-4 py-3"

                    />



                    <button

                        onClick={handleShorten}

                        disabled={loading}

                        className="rounded-lg bg-black px-8 py-3 text-white"

                    >

                        {
                            loading
                            ?
                            "..."
                            :
                            "Shorten"
                        }

                    </button>


                </div>



                {
                    result &&
                    <p className="mt-6 text-center">

                        Short code:
                        {" "}
                        {result}

                    </p>
                }


            </section>


        </main>

    );

}