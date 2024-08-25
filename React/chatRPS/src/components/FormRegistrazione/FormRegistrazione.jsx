import css from "./FormRegistrazione.module.css"
import { useState } from "react";
import { registrazione } from "../services/RESTService"
import { NavLink } from "react-router-dom";

export function FormRegistrazione() {

    const [formData, setFormData] = useState({
        name: "",
        lastname: "",
        username: "",
        email: "",
        password: ""
    });

    const [registrationMessage, setRegistrationMessage] = useState("");
    const [registrationMessageRegex, setRegistrationMessageRegex] = useState("");

    const [showPassword, setShowPassword] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;

        setFormData({ ...formData, [name]: value });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        const nomeRegex = /^[a-zA-Z\s']{5,50}$/;
        const cognomeRegex = /^[a-zA-Z\s']{5,50}$/;
        const usernameRegex = /^[A-Za-z][A-Za-z0-9_]{7,29}$/;
        const emailRegex = /^[A-Za-z0-9\.+\-_]+@[A-Za-z0-9\._-]+\.[A-Za-z]{2,24}$/;
        const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$/;

        // recupero delle credenziali di registrazione
        const { nome, cognome, email, password } = formData;

        // Controllo regex
        if (!nome.match(nomeRegex)) {
            setRegistrationMessageRegex("Nome non valido. Assicurati di inserire un nome valido (da 5 a 50 caratteri, solo lettere).");
            return;
        }

        if (!cognome.match(cognomeRegex)) {
            setRegistrationMessageRegex("Cognome non valido. Assicurati di inserire un cognome valido (da 5 a 50 caratteri, solo lettere).");
            return;
        }

        if (!email.match(usernameRegex)) {
            setRegistrationMessageRegex("Username non valido. Deve iniziare con una lettera, contenere solo lettere, numeri o underscore, e avere una lunghezza tra 8 e 30 caratteri.");
            return;
        }

        if (!email.match(emailRegex)) {
            setRegistrationMessageRegex("Email non valida. Assicurati di inserire un indirizzo email valido.");
            return;
        }

        if (!password.match(passwordRegex)) {
            setRegistrationMessageRegex("Password non valida. Assicurati che la password abbia almeno 6 caratteri, includa almeno una lettera minuscola, una lettera maiuscola, un numero e un carattere speciale.");
            return;
        }


        try {

            const response = await registrazione();

            if (response.ok) {
                setRegistrationMessage("Registrazione avvenuta con successo!");
            }

            else {
                setRegistrationMessage("Dati inseriti non validi!");
            }

        } catch (error) {
            console.error("Errore durante la registrazione:", error);
            setRegistrationMessage("Si è verificato un errore durante la registrazione.");
        }

        setFormData({
            name: "",
            lastname: "",
            username: "",
            email: "",
            password: ""
        });
    }

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    return (

        <form className={css.form_main} onSubmit={handleSubmit}>
            <p className={css.heading}>Registrazione</p>

            <div className={css.inputContainer}>

                <input placeholder="Nome" name="name" id="name" className={css.inputField} type="text" value={formData.name} onChange={handleChange} required />
            </div>

            <div className={css.inputContainer}>

                <input placeholder="Cognome" name="lastname" id="lastname" className={css.inputField} type="text" value={formData.lastname} onChange={handleChange} required />
            </div>

            <div className={css.inputContainer}>

                <input placeholder="Username" name="username" id="username" className={css.inputField} type="text" value={formData.username} onChange={handleChange} required />
            </div>

            <div className={css.inputContainer}>

                <input placeholder="Email" name="email" id="email" className={css.inputField} type="email" value={formData.email} onChange={handleChange} required />
            </div>

            <div className={css.inputContainer}>

                <input placeholder="Password" name="password" id="password" className={css.inputField} type={showPassword ? "text" : "password"} value={formData.password} onChange={handleChange} required />
            </div>

            <div class={css.flex__row}>
                <input type="checkbox" id="showPassword" onChange={togglePasswordVisibility} />
                <label htmlFor="showPassword">Mostra password</label>
            </div>

            {/* <button type="button" onClick={togglePasswordVisibility} style={{borderRadius:"2rem", border:"1px solid black"}}>Mostra/nascondi password</button> */}


            <button className={css.button}>Submit</button>

            <div className={css.signupContainer}>
                <p>Sei gia registrato?</p>
                <NavLink to="/" className={css.signupLink}>Sign in</NavLink>
            </div>

            <div className={css.message} style={{ textWrap: "balance" }}>{registrationMessage && <p>{registrationMessage}</p>}</div>
            <div className={css.message} style={{ textWrap: "balance" }}>{registrationMessageRegex && <p>{registrationMessageRegex}</p>}</div>


        </form>
    );
}