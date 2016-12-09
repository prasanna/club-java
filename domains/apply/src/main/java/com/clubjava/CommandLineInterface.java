package com.clubjava;

public class CommandLineInterface {
    private final Application application;

    public CommandLineInterface(Application application) {
        this.application = application;
    }

    public static void main(String[] args) {
        new CommandLineInterface(new ClubJavaApplication()).run();
    }

    public void run() {
        application.run();
    }
}
