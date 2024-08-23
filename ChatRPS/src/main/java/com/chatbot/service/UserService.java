package com.chatbot.service;

import com.chatbot.dto.UserDto;
import com.chatbot.dto.UserLoginRequestDto;
import com.chatbot.dto.UserRegistrazioneDto;
import com.chatbot.model.User;

public interface UserService {

    void registraUtente(UserRegistrazioneDto utente);

    boolean loginUtente(UserLoginRequestDto utente);

    boolean esisteUtenteMail(String email);

    User trovaUtenteMail(String email);

    UserDto getUserByEmail(String email);
}
