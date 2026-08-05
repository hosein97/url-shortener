"use client";

import {
    useEffect,
    useMemo,
    useState,
} from "react";

import type {
    KeycloakProfile,
} from "keycloak-js";

import keycloak from "@/lib/keycloak";

import {
    AuthContext,
} from "@/contexts/AuthContext";


export default function AuthProvider({
    children,
}: {
    children: React.ReactNode;
}) {


    const [authenticated, setAuthenticated] =
        useState(false);


    const [user, setUser] =
        useState<KeycloakProfile | null>(null);



    useEffect(() => {


        keycloak.onAuthLogout = () => {

            setAuthenticated(false);

            setUser(null);

        };



        keycloak.init({

            onLoad: "check-sso",

            pkceMethod: "S256",

        })
        .then(async (auth) => {


            setAuthenticated(auth);



            if (auth) {

                const profile =
                    await keycloak.loadUserProfile();


                setUser(profile);

            }


        })
        .catch((error) => {

            console.error(
                "Keycloak initialization failed",
                error
            );

        });


    }, []);



    const login = async () => {

        await keycloak.login();

    };


    const logout = async () => {
        await keycloak.logout({
            redirectUri: window.location.origin,
        });
    };

    const register = async () => {

        await keycloak.register();

    };


    const getAccessToken = () => {

        return keycloak.token;

    };



    const value = useMemo(
        () => ({

            authenticated,

            user,

            login,

            logout,

            register,

            getAccessToken,

        }),
        [
            authenticated,
            user,
        ]
    );



    return (

        <AuthContext.Provider value={value}>

            {children}

        </AuthContext.Provider>

    );

}