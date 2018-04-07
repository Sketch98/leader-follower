from globals import raspi
import pigpio

a = (0, 0.25, 0.5, 0.75, 1)
b = (0.08, 0.35, 0.6, 0.78, 0.98)


def servo_transform(angle):
    for i in range(len(a)):
        if angle == a[i]:
            return b[i]
        if angle < a[i]:
            k = angle - a[i - 1]
            m = (b[i] - b[i - 1])/(a[i] - a[i - 1])
            return m*k + b[i - 1]


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
        angle = servo_transform(angle)
        
        pulse_width = 2500 - 2000*angle
        raspi.set_servo_pulsewidth(self.pin, pulse_width)
    
    def stop(self):
        self.move_to(0.5)


if __name__ == "__main__":
    import pigpio
    import time
    
    servo = Servo(25)
    time.sleep(2)
    for angle in range(51):
        servo.move_to(angle/50.0)
        time.sleep(0.05)
    
    servo.stop()
    raspi.stop()
