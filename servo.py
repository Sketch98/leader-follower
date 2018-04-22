from globals import raspi
import pigpio


class Servo:
    """
    controls pigpio interface for a servo
    """
    
    def __init__(self, pin):
        raspi.set_mode(pin, pigpio.OUTPUT)
        self.pin = pin
    
    def move_to(self, angle):
        # angle ranges from 0 to 1
        assert 0 <= angle <= 1, 'angle {} not in [0, 1]'.format(angle)
        
        pulse_width = 500 + 2000*angle
        raspi.set_servo_pulsewidth(self.pin, pulse_width)


if __name__ == "__main__":
    from time import sleep
    from parameters import servo_pin
    
    servo = Servo(servo_pin)
    sleep(2)
    for angle in range(51):
        servo.move_to(angle/50.0)
        sleep(0.05)
    
    raspi.stop()
