#include "pico/stdlib.h"

#define LED_PIN 15

class Led {
private:
    uint pin;

public:
    Led(uint gpio_pin) : pin(gpio_pin) {
        gpio_init(pin);
        gpio_set_dir(pin, GPIO_OUT);
    }

    void on() {
        gpio_put(pin, 1);
    }

    void off() {
        gpio_put(pin, 0);
    }

    void blink(int delay_ms) {
        on();
        sleep_ms(delay_ms);
        off();
        sleep_ms(delay_ms);
    }
};

int main() {
    Led led(LED_PIN);

    while (true) {
        led.blink(500);
    }

    return 0;
}
