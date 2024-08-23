package com.chatbot.service;

import com.chatbot.dto.UserDto;
import com.chatbot.dto.UserRegistrazioneDto;
import com.chatbot.model.User;
import com.chatbot.repository.UserRepository;
import org.apache.commons.codec.digest.DigestUtils;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {

    ModelMapper modelMapper = new ModelMapper();

    @Autowired
    private UserRepository userRepository;

    @Override
    public void registraUtente(UserRegistrazioneDto utenteDto) {

        String password = DigestUtils.sha256Hex(utenteDto.getPassword());
        utenteDto.setPassword(password);

        User user = modelMapper.map(utenteDto, User.class);

        userRepository.save(user);
    }

    @Override
    public boolean loginUtente(UserRegistrazioneDto utente) {
        User user = new User();

        user.setEmail(utente.getEmail());
        user.setPassword(utente.getPassword());

        String passwordHash = DigestUtils.sha256Hex(user.getPassword());

        User credenzialiUser = userRepository.findByEmailAndPassword(user.getEmail(), user.getPassword());

        return credenzialiUser != null ? true : false;
    }

    @Override
    public boolean esisteUtenteMail(String email) {
        return userRepository.existsByEmail(email);
    }

    @Override
    public User trovaUtenteMail(String email) {
        return userRepository.findByEmail(email);
    }

    @Override
    public UserDto getUserByEmail(String email) {

        User user = userRepository.findByEmail(email);

        UserDto userDto = modelMapper.map(user, UserDto.class);

        return userDto;
    }
}
