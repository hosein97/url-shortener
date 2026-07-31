import { createContext } from "react";

export interface AuthContextType {
    initialized: boolean;
    authenticated: boolean;

    login: () => Promise<void>;
    logout: () => Promise<void>;

    getAccessToken: () => string | undefined;
}

export const AuthContext = createContext<AuthContextType | null>(null);