package com.clubjava.hello;

import org.joda.time.DateTime;

public class Hello {
    public static void main(String[] args) {
        DateTime now = new DateTime();
        System.out.println("Hello! The time is " + now.toString());
    }
}
