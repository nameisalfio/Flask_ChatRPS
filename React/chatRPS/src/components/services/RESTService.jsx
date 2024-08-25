import { jwtDecode } from "jwt-decode";
import Cookies from "js-cookie";

export async function registrazione() {

    const nome = document.getElementById('nome').value;
    const cognome = document.getElementById('cognome').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8080/api/utente/registrazione', {
        method: 'POST', // Metodo HTTP per la richiesta POST
        headers: {
            'Content-Type': 'application/json', // Imposta l'intestazione del contenuto come JSON
        },
        body: JSON.stringify({
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "password": password
        }),
    })

    //console.log(response)

    if (!response.ok) {
        throw new Error('Errore durante la registrazione');
    }

    console.log(response);
    console.log(response.status);

    return response;

    // const user = await response.json();
    // console.log(user);
    // return user;
}

export async function login() {

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8080/api/utente/login', {
        method: 'POST', // Metodo HTTP per la richiesta POST
        headers: {
            'Content-Type': 'application/json', // Imposta l'intestazione del contenuto come JSON
        },
        body: JSON.stringify({
            "email": email,
            "password": password
        }),
    })

    if (!response.ok) {
        throw new Error('Errore durante la login');
    }

    // .then(async response => await response.json()) // Converte la risposta in JSON
    // .then(data => console.log(data)) // Gestisce i dati della risposta
    // .catch((error) => console.error('Errore:', error)); // Gestisce eventuali errori

    const userToken = await response.json();
    console.log(userToken);

    // const decodedToken = jwtDecode(userToken.token);
    // const idUtente = decodedToken.id;
    // console.log(idUtente);

    return userToken;

}

export async function getUser() {

    const token = Cookies.get("token");
    const decodedToken = jwtDecode(token);
    const email = decodedToken.email;

    try {

        const response = await fetch(`http://localhost:8080/api/utente/getUser/${email}`, {
            method: 'GET',
            // headers: {
            //     'Content-Type': 'Application/json',
            // },
        });

        if (!response.ok) {
            throw new Error('Errore durante la get dell\'utente');
        }

        const userData = await response.json();
        // console.log(newsData);
        return userData;


    } catch (error) {
        console.error('Errore: ', error);
        throw error;
    }
}