"use client";

import Link from "next/link";

import {
    useAuth,
} from "@/hooks/useAuth";



export default function Navbar() {


    const {
        authenticated,
        user,
        login,
        logout,
        register,
    } = useAuth();



    return (

        <nav className="border-b">


            <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">


                <Link
                    href="/"
                    className="text-2xl font-bold"
                >
                    Shortly
                </Link>



                <div className="flex items-center gap-3">


                    {
                    authenticated ? (

                        <>


                            {
                            user && (

                                <span className="text-sm text-gray-600">

                                    {user.firstName}

                                </span>

                            )
                            }



                            <Link
                                href="/dashboard"
                                className="rounded-md border px-4 py-2 hover:bg-gray-100"
                            >
                                Dashboard
                            </Link>



                            <Link
                                href="/links"
                                className="rounded-md border px-4 py-2 hover:bg-gray-100"
                            >
                                My Links
                            </Link>



                            <button
                                onClick={logout}
                                className="rounded-md bg-black px-4 py-2 text-white hover:bg-gray-800"
                            >
                                Logout
                            </button>


                        </>


                    ) : (


                        <>

                            <button
                                onClick={login}
                                className="rounded-md border px-4 py-2 hover:bg-gray-100"
                            >
                                Login
                            </button>



                            <button
                                onClick={register}
                                className="rounded-md bg-black px-4 py-2 text-white hover:bg-gray-800"
                            >
                                Register
                            </button>


                        </>


                    )
                    }


                </div>


            </div>


        </nav>

    );

}