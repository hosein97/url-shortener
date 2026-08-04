"use client";


import {
    useEffect,
    useState,
} from "react";

import {
    apiFetch,
} from "@/lib/api";


interface Link {

    id: number;

    original_url: string;

    short_code: string;

    created_at: string;

}



export default function LinksPage() {


    const [links, setLinks] =
        useState<Link[]>([]);


    const [loading, setLoading] =
        useState(true);



    useEffect(() => {

        async function load() {

            try {

                const response =
                    await apiFetch(
                        "/links/"
                    );


                const data =
                    await response.json();


                setLinks(data);


            } finally {

                setLoading(false);

            }

        }


        load();


    }, []);




    if (loading) {

        return (

            <div className="p-10">
                Loading links...
            </div>

        );

    }



    return (

        <main className="mx-auto max-w-5xl p-10">


            <h1 className="mb-8 text-3xl font-bold">

                My Links

            </h1>



            <div className="space-y-4">


            {links.map((link) => (

                <div

                    key={link.id}

                    className="rounded-lg border p-5"

                >

                    <div className="mb-3">

                        <p className="text-sm text-gray-500">
                            Short URL
                        </p>

                        <a

                            href={`http://localhost:8000/${link.short_code}/`}

                            target="_blank"

                            rel="noopener noreferrer"

                            className="font-semibold text-blue-600 hover:underline"

                        >

                            http://localhost:8000/{link.short_code}/

                        </a>

                    </div>


                    <div>

                        <p className="text-sm text-gray-500">
                            Original URL
                        </p>

                        <a

                            href={link.original_url}

                            target="_blank"

                            rel="noopener noreferrer"

                            className="text-blue-600 hover:underline"

                        >

                            {link.original_url}

                        </a>

                    </div>


                    <p className="mt-3 text-sm text-gray-500">

                        Created:
                        {" "}
                        {new Date(
                            link.created_at
                        ).toLocaleString()}

                    </p>

                </div>

                ))}
   

            </div>


        </main>

    );

}