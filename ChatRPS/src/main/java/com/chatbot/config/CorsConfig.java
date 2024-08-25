package com.chatbot.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {

    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true); // Permetti l'invio di credenziali (cookie, autenticazione HTTP)
        config.addAllowedOrigin("http://localhost:5173"); // Permetti richieste dall'origine del front-end React
        config.addAllowedHeader("*"); // Permetti tutti gli header
        config.addAllowedMethod("*"); // Permetti tutti i metodi HTTP (GET, POST, PUT, DELETE, ecc.)
        source.registerCorsConfiguration("/**", config); // Applica questa configurazione a tutte le rotte
        return new CorsFilter(source);
    }
}


