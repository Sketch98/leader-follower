class Servo:
    """
    controls pigpio interface for a servo
    """
    
    def __init__(self, raspi, pin):
        self.raspi = raspi
        raspi.set_mode(pin, pigpio.OUTPUT)
        self.pin = pin
    
    def move_to(self, angle):
        # angle ranges from 0 to 1
        assert 0 <= angle <= 1, 'angle {} not in [0, 1]'.format(angle)
        pulse_width = 500 + 2000*angle
        self.raspi.set_servo_pulsewidth(self.pin, pulse_width)
    
    def stop(self):
        self.move_to(0.5)


if __name__ == "__main__":
    import pigpio
    import time
    
    pi = pigpio.pi()
    servo = Servo(pi, 18)
    time.sleep(1)
    for angle in range(0, 50):
        servo.move_to(angle/50.0)
        time.sleep(0.05)
    
    servo.stop()
    pi.stop()
