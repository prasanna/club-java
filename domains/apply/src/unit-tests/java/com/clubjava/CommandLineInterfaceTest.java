package com.clubjava;

import org.junit.Test;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

public class CommandLineInterfaceTest {
    @Test
    public void runsTheApplication() {
        Application mockApplication = mock(Application.class);
        new CommandLineInterface(mockApplication).run();
        verify(mockApplication).run();
    }


}
