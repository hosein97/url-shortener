"use client";

import {
    useEffect,
    useMemo,
    useState,
} from "react";

import keycloak from "@/lib/keycloak";

import {
    AuthContext,
} from "@/contexts/AuthContext";

import type {
    KeycloakProfile,
} from "keycloak-js";

export default function AuthProvider({
    children,
}: {
    children: React.ReactNode;
}) {

    const [initialized, setInitialized] = useState(false);

    const [authenticated, setAuthenticated] =
        useState(false);

    const [user, setUser] =
        useState<KeycloakProfile | null>(null);

    useEffect(() => {

        async function initialize() {

            try {
                keycloak.onAuthLogout = () => {
                    setAuthenticated(false);
                    setUser(null);
                };


                const authenticated = await keycloak.init({

                    onLoad: "check-sso",
                
                    pkceMethod: "S256",
                
                    silentCheckSsoRedirectUri:
                        window.location.origin +
                        "/silent-check-sso.html",
                
                });
                
                setAuthenticated(authenticated);

                if (authenticated) {

                    const profile =
                        await keycloak.loadUserProfile();

                    setUser(profile);
                }

            } catch (error) {

                console.error(
                    "Keycloak initialization failed",
                    error
                );

            } finally {

                setInitialized(true);

            }

        }

        initialize();

    }, []);

    const login = async () => {
        await keycloak.login();
    };

    const logout = async () => {
        await keycloak.logout();
    };

    const getAccessToken = () => {
        return keycloak.token;
    };

    const value = useMemo(
        () => ({
            initialized,
            authenticated,
            user,
            login,
            logout,
            getAccessToken,
        }),
        [
            initialized,
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