import { useState } from "react";
import { AuthContext } from "./AuthContext";
import { checkToken } from "../../components/services/config/RESTConfig";

export function AuthContextProvider({ children }) {

    const [tokenValid, setTokenValid] = useState(checkToken());

    const [user, setUser] = useState({
        name: "",
        lastname: "",
        username: "",
        email: "",
    });

    return (
        <AuthContext.Provider value={{ user, setUser, tokenValid, setTokenValid }}>
            {children}
        </AuthContext.Provider>
    );
}