import { createContext } from "react";
import type { KeycloakProfile } from "keycloak-js";


export interface AuthContextType {

    authenticated: boolean;

    user: KeycloakProfile | null;

    login: () => Promise<void>;

    logout: () => Promise<void>;

    register: () => Promise<void>;

    getAccessToken: () => string | undefined;

}


export const AuthContext =
    createContext<AuthContextType | null>(null);