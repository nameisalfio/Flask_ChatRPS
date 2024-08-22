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
public class UserServiceImpl implements UserService{

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
        return false;
    }

    @Override
    public boolean esisteUtenteMail(String email) {
        return false;
    }

    @Override
    public User trovaUtenteMail(String email) {
        return null;
    }

    @Override
    public UserDto getUserByEmail(String email) {
        return null;
    }
}
