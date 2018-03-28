from current_sensor import CurrentSensor
from motor import Motor
from parameters import motor_acceleration_limit
from pid import PID
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, raspi, mcp, channel, pins, pid_constants, forward=1):
        self.current_sensor = CurrentSensor(mcp, channel)
        self.motor = Motor(raspi, pins['pwm'], pins['dir'], forward=forward)
        self.encoder = RotaryEncoder(raspi, pins['a'], pins['b'])
        self.pid = PID(pid_constants['kp'], pid_constants['ki'], pid_constants['kd'])
        self.last_speed = 0.0
    
    def adjust_motor_speed(self, target_vel, vel, max_wheel_speed):
        error = (target_vel - vel)/max_wheel_speed
        speed = min(max(self.pid.calc(error), -1.0), 1.0)
        if speed > 0:
            speed = min(speed, self.last_speed + motor_acceleration_limit)
        else:
            speed = max(speed, self.last_speed - motor_acceleration_limit)
        self.motor.set_speed(speed)
        self.last_speed = speed
    
    def stop(self):
        self.motor.stop()
        self.encoder.stop()
    
    def check_current(self):
        # TODO: the motor should temporarily stop while the current lowers
        # instead of shutting off permanently
        if self.current_sensor.check_current():
            self.motor.stop()
            raise Exception('motor current trip')
    
    def get_pos_dif(self):
        return self.encoder.get_pos_dif()
