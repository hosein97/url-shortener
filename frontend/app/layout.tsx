import "./globals.css";

import Providers from "@/providers/Providers";

import Navbar from "@/components/Navbar";


export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {


    return (

        <html lang="en">

            <body>


                <Providers>


                    <Navbar />


                    {children}


                </Providers>


            </body>

        </html>

    );

}