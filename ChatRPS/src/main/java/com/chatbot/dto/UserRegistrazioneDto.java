package com.chatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class UserRegistrazioneDto {

    @NotNull
    @Pattern(regexp = "[a-zA-Z\\s']{5,50}", message = "nome non valido")
    private String name;

    @NotNull
    @Pattern(regexp = "[a-zA-Z\\s']{5,50}", message = "cognome non valido")
    private String lastname;

    @NotNull
    @Pattern(regexp = "^[A-Za-z][A-Za-z0-9_]{7,29}$", message = "username non valido")
    private String username;

    @NotNull
    @Pattern(regexp = "[A-Za-z0-9\\.\\+_-]+@[A-Za-z0-9\\._-]+\\.[A-Za-z]{2,24}", message = "email non valida")
    private String email;

    @NotNull
    private String password;
}
