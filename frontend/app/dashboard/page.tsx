"use client";

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
} from "@/components/ui/card";

import {
    useEffect,
    useState,
} from "react";


import {
    apiFetch,
} from "@/lib/api";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
} from "recharts";

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


interface TimePoint {
    date: string;
    clicks: number;
}


export default function DashboardPage() {

    const [series, setSeries] =
    useState<TimePoint[]>([]);

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

            const seriesResponse =
            await apiFetch(
                "/analytics/me/clicks/timeseries/"
            );
        
            const seriesData =
            await seriesResponse.json();
        
            setSeries(seriesData);            

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

                <Card>

                    <CardHeader>

                        <CardTitle>
                            Links
                        </CardTitle>

                    </CardHeader>

                    <CardContent>

                        <p className="text-4xl font-bold">

                            {dashboard.total_links}

                        </p>

                    </CardContent>

                </Card>

                <Card>

                    <CardHeader>

                        <CardTitle>
                            Clicks
                        </CardTitle>

                    </CardHeader>

                    <CardContent>

                        <p className="text-4xl font-bold">

                            {dashboard.total_clicks}

                        </p>

                    </CardContent>

                </Card>


                <Card>

                    <CardHeader>

                        <CardTitle>
                            Today
                        </CardTitle>

                    </CardHeader>

                    <CardContent>

                        <p className="text-4xl font-bold">

                            {dashboard.clicks_today}

                        </p>

                    </CardContent>

                </Card>




                <Card>

                    <CardHeader>

                        <CardTitle>
                            Last 7 days
                        </CardTitle>

                    </CardHeader>

                    <CardContent>

                        <p className="text-4xl font-bold">

                            {dashboard.clicks_last_7_days}

                        </p>

                    </CardContent>

                </Card>


                <Card>

                    <CardHeader>

                        <CardTitle>
                            Visitors
                        </CardTitle>

                    </CardHeader>

                    <CardContent>

                        <p className="text-4xl font-bold">

                            {dashboard.unique_visitors}

                        </p>

                    </CardContent>

                </Card>


            </div>


            <Card className="mt-10">

                <CardHeader>

                    <CardTitle>
                        Clicks over time
                    </CardTitle>

                </CardHeader>

                <CardContent>

                    <div className="h-[350px]">

                        <ResponsiveContainer
                            width="100%"
                            height="100%"
                        >

                            <LineChart
                                data={series}
                            >

                                <CartesianGrid
                                    strokeDasharray="3 3"
                                />

                                <XAxis
                                    dataKey="date"
                                />

                                <YAxis />

                                <Tooltip />

                                <Line
                                    type="monotone"
                                    dataKey="clicks"
                                />

                            </LineChart>

                        </ResponsiveContainer>

                    </div>

                </CardContent>

                </Card>


            <section className="mt-10">


                <h2 className="mb-4 text-xl font-bold">

                    Top Links

                </h2>


                <Table>

                    <TableHeader>

                    <TableRow>

                    <TableHead>
                    Short URL
                    </TableHead>

                    <TableHead>
                    Destination
                    </TableHead>

                    <TableHead>
                    Clicks
                    </TableHead>

                    </TableRow>

                    </TableHeader>

                    <TableBody>

                    {topLinks.map(link => (

                    <TableRow key={link.short_code}>

                    <TableCell>

                    <a
                    href={`http://localhost:8000/${link.short_code}/`}
                    target="_blank"
                    className="text-blue-600"
                    >

                    {link.short_code}

                    </a>

                    </TableCell>

                    <TableCell>

                    {link.original_url}

                    </TableCell>

                    <TableCell>

                    {link.clicks}

                    </TableCell>

                    </TableRow>

                    ))}

                    </TableBody>

                    </Table>


            </section>



        </main>

    );

}




