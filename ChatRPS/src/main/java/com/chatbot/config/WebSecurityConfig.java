package com.chatbot.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

@Configuration
public class WebSecurityConfig {

    @Bean
    SecurityFilterChain defaultSecurityFilterChain(HttpSecurity http) throws Exception {

        http
                .cors(cors -> cors.configurationSource(corsConfigurationSource())) // Abilita CORS usando la configurazione definita
                .csrf(CsrfConfigurer::disable) // Disabilita CSRF, consigliato per le API REST
                .authorizeHttpRequests(requests -> requests
                        .requestMatchers("/user/**").permitAll() // Permetti l'accesso senza autenticazione agli endpoint sotto /user/
                        .anyRequest().authenticated()) // Richiedi autenticazione per tutte le altre richieste
                .formLogin(AbstractHttpConfigurer::disable) // Disabilita il form di login standard di Spring
                .httpBasic(AbstractHttpConfigurer::disable); // Disabilita l'autenticazione HTTP Basic

        return http.build();
    }

    private CorsConfigurationSource corsConfigurationSource() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        config.addAllowedOrigin("http://localhost:5173");
        config.addAllowedHeader("*");
        config.addAllowedMethod("*");
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
