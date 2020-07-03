"""Just capture how to get the motors running.
"""
import gpiod


with gpiod.Chip("pinctrl-bcm2835") as chip:
    sleep_line = chip.get_lines([17])
    sleep_line.request(consumer="me", type=gpiod.LINE_REQ_DIR_OUT)
    sleep_line.set_values([1])


    pwm_line = chip.get_lines([22, 25])
    pwm_line.request(consumer="me", type=gpiod.LINE_REQ_DIR_OUT)

    while True:
        pwm_line.set_values([1,1])
        time.sleep(0.004)
        #pwm_line.set_values([0, 0])
        time.sleep(0.001)

