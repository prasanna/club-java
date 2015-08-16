package com.clubjava.hello;

import org.junit.Test;

import static org.junit.Assert.assertThat;
import static org.hamcrest.CoreMatchers.is;

public class HelloTest {
    @Test
    public void passes() {
        Hello hello = new Hello();
        assertThat(hello, is(hello));
    }
}
