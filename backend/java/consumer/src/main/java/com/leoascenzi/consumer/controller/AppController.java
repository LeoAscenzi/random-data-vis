package com.leoascenzi.consumer.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppController {

    @KafkaListener(topics={"trade-bids", "trade-asks"}, groupId ="my-group")
    public void tradeKafkaListener(String message)
    {
        System.out.println(message);
    }

    @GetMapping("/")
    public ResponseEntity<String> healthcheck()
    {
        return new ResponseEntity<String>("{\"status\": \"App is up!\"}", HttpStatus.OK);
    }

    @PostMapping("/prepare-stats")
    public ResponseEntity<String> prepareStats(@RequestParam int dataCount)
    {
        return new ResponseEntity<String>("{\"status\": \"ready\"}", HttpStatus.OK);
    }
    
}
