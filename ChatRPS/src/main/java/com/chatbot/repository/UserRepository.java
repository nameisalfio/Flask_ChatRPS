package com.chatbot.repository;

import com.chatbot.model.User;
import org.springframework.data.repository.CrudRepository;

public interface UserRepository extends CrudRepository<User, Integer> {

    boolean existsByEmail(String email);

    User findByEmail(String email);

    User findByEmailAndPassword(String email, String password);
}
