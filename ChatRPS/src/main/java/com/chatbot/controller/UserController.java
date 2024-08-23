package com.chatbot.controller;

import com.chatbot.dto.UserDto;
import com.chatbot.dto.UserLoginRequestDto;
import com.chatbot.dto.UserLoginResponseDto;
import com.chatbot.dto.UserRegistrazioneDto;
import com.chatbot.model.User;
import com.chatbot.service.BlackList;
import com.chatbot.service.UserService;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.Key;
import java.time.LocalDateTime;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private BlackList blackList;

    @PostMapping("/registrazione")
    public ResponseEntity<UserRegistrazioneDto> registraUtente(@Valid @RequestBody UserRegistrazioneDto utenteDto) {
        try {
            if (!Pattern.matches("(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{6,20}", utenteDto.getPassword())) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }

            if (userService.esisteUtenteMail(utenteDto.getEmail())) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
            }

            userService.registraUtente(utenteDto);
            return ResponseEntity.ok(utenteDto);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }

    @PostMapping("/login")
    public ResponseEntity<UserLoginResponseDto> loginUtente(@RequestBody UserLoginRequestDto utente) {
        try {
            if (userService.loginUtente(utente)) {
                return ResponseEntity.ok(issueToken(utente.getEmail()));
            }

            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }

    private UserLoginResponseDto issueToken(String email) {
        byte[] secretKey = "iajwdawiduhadkjwddssdsdfdf8792133004".getBytes();
        Key key = Keys.hmacShaKeyFor(secretKey);

        User informazioniUtente = userService.trovaUtenteMail(email);
        Map<String, Object> map = new HashMap<>();
        map.put("name", informazioniUtente.getName());
        map.put("lastname", informazioniUtente.getLastname());
        map.put("username", informazioniUtente.getUsername());
        map.put("email", informazioniUtente.getEmail());
        map.put("id", informazioniUtente.getId());

        Date creation = new Date();
        Date end = java.sql.Timestamp.valueOf(LocalDateTime.now().plusMinutes(15L));

        String jwtToken = Jwts.builder().setClaims(map).setIssuer("http://localhost:8080")
                .setIssuedAt(creation).setExpiration(end).signWith(key).compact();

        UserLoginResponseDto token = new UserLoginResponseDto();
        token.setToken(jwtToken);
        token.setTtl(end);
        token.setTokenCreationTime(creation);
        return token;
    }

    @GetMapping("/logout")
    public ResponseEntity<Void> logoutUtente(@RequestHeader(HttpHeaders.AUTHORIZATION) String authorizationHeader) {
        try {
            String token = authorizationHeader.substring("Bearer".length()).trim();
            blackList.invalidateToken(token);
            return ResponseEntity.ok().build();

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @GetMapping("/getUser/{email}")
    public ResponseEntity<UserDto> getUser(@PathVariable("email") String email) {
        try {
            if (email != null && !email.isEmpty()) {
                UserDto user = userService.getUserByEmail(email);
                return ResponseEntity.ok(user);
            }

            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }
    }
}
