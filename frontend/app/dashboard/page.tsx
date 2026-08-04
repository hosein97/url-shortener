"use client";


import {
    useEffect,
    useState,
} from "react";


import {
    apiFetch,
} from "@/lib/api";



interface Dashboard {

    total_links: number;

    total_clicks: number;

    clicks_today: number;

    clicks_last_7_days: number;

    unique_visitors: number;

}




interface TopLink {

    short_code: string;

    original_url: string;

    clicks: number;

    last_click: string;

}




export default function DashboardPage() {


    const [dashboard, setDashboard] =
        useState<Dashboard | null>(null);



    const [topLinks, setTopLinks] =
        useState<TopLink[]>([]);



    useEffect(() => {


        async function load() {


            const dashboardResponse =
                await apiFetch(
                    "/analytics/me/dashboard/"
                );


            const dashboardData =
                await dashboardResponse.json();



            const topResponse =
                await apiFetch(
                    "/analytics/me/top-links/"
                );


            const topData =
                await topResponse.json();



            setDashboard(
                dashboardData
            );


            setTopLinks(
                topData
            );

        }


        load();


    }, []);




    if (!dashboard) {

        return (

            <div className="p-10">
                Loading dashboard...
            </div>

        );

    }




    return (

        <main className="mx-auto max-w-6xl p-10">


            <h1 className="mb-8 text-3xl font-bold">

                Dashboard

            </h1>



            <div className="grid grid-cols-5 gap-4">


                <Card
                    title="Links"
                    value={dashboard.total_links}
                />


                <Card
                    title="Clicks"
                    value={dashboard.total_clicks}
                />


                <Card
                    title="Today"
                    value={dashboard.clicks_today}
                />


                <Card
                    title="Last 7 days"
                    value={dashboard.clicks_last_7_days}
                />


                <Card
                    title="Visitors"
                    value={dashboard.unique_visitors}
                />


            </div>




            <section className="mt-10">


                <h2 className="mb-4 text-xl font-bold">

                    Top Links

                </h2>



                <div className="space-y-4">


                    {topLinks.map((link) => (

                        <div

                            key={link.short_code}

                            className="rounded border p-4"

                        >

                            <p className="font-semibold">

                                {link.short_code}

                            </p>


                            <p className="text-gray-600">

                                {link.original_url}

                            </p>


                            <p>

                                Clicks:
                                {" "}
                                {link.clicks}

                            </p>


                        </div>

                    ))}


                </div>


            </section>



        </main>

    );

}





function Card({
    title,
    value,
}: {
    title:string;
    value:number;
}) {


    return (

        <div className="rounded-lg border p-5">

            <p className="text-gray-500">
                {title}
            </p>


            <p className="text-3xl font-bold">

                {value}

            </p>


        </div>

    );

}