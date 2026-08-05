"use client";

import {
    useEffect,
} from "react";

import {
    useRouter,
} from "next/navigation";

import {
    useAuth,
} from "@/hooks/useAuth";


export default function AuthGuard({
    children,
}: {
    children: React.ReactNode;
}) {

    const {
        authenticated,
    } = useAuth();


    const router = useRouter();


    useEffect(() => {

        if (
            !authenticated
        ) {
            router.replace("/");
        }

    }, [
        authenticated,
        router,
    ]);



    if (!authenticated) {

        return null;

    }


    return children;
}