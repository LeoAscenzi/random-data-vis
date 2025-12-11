package com.leoascenzi.consumer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppController {

    @GetMapping("/")
    public ResponseEntity<String> healthcheck()
    {
        return new ResponseEntity<String>("{\"status\": \"App is up!\"}", HttpStatus.OK);
    }
    
}
