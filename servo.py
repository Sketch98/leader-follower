class Servo:
    """
    controls pigpio interface for a servo
    """
    
    def __init__(self, pin):
        global raspi
        raspi.set_mode(pin, pigpio.OUTPUT)
        self.pin = pin
    
    def move_to(self, angle):
        # angle ranges from 0 to 1
        assert 0 <= angle <= 1, 'angle {} not in [0, 1]'.format(angle)
        pulse_width = 2300 - 1800*angle
        # use 500 + 1800*angle if servo is right-side-up
        global raspi
        raspi.set_servo_pulsewidth(self.pin, pulse_width)
    
    def stop(self):
        self.move_to(0.5)


if __name__ == "__main__":
    import pigpio
    import time
    
    raspi = pigpio.pi()
    servo = Servo(25)
    time.sleep(0.5)
    for angle in range(0, 50):
        servo.move_to(angle/50.0)
        time.sleep(0.05)
    
    servo.stop()
    raspi.stop()
