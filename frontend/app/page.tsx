"use client";

import { useAuth } from "@/hooks/useAuth";

export default function Home() {
    const {
        initialized,
        authenticated,
        login,
        logout,
    } = useAuth();

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

                            <button
                                onClick={logout}
                                className="rounded-md border px-4 py-2 hover:bg-gray-100"
                            >
                                Logout
                            </button>

                        ) : (

                            <>
                                <button
                                    onClick={login}
                                    className="rounded-md border px-4 py-2 hover:bg-gray-100"
                                >
                                    Login
                                </button>

                                <button
                                    onClick={login}
                                    className="rounded-md bg-black px-4 py-2 text-white hover:bg-gray-800"
                                >
                                    Register
                                </button>
                            </>

                        )}

                    </div>
                </div>
            </nav>

            <section className="mx-auto mt-32 flex max-w-3xl flex-col items-center px-6">

                <h2 className="mb-3 text-5xl font-bold">
                    Shorten your URLs
                </h2>

                <p className="mb-10 text-center text-gray-600">
                    Fast, simple and secure URL shortening.
                </p>

                <div className="flex w-full gap-4">

                    <input
                        type="url"
                        placeholder="https://example.com/very/long/url"
                        className="flex-1 rounded-lg border px-4 py-3 outline-none focus:border-black"
                    />

                    <button
                        className="rounded-lg bg-black px-8 py-3 font-medium text-white hover:bg-gray-800"
                    >
                        Shorten
                    </button>

                </div>

            </section>

        </main>
    );
}