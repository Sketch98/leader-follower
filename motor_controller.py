from current_sensor import CurrentSensor
from motor import Motor
from pid import PIDController
from rotary_encoder import RotaryEncoder


accel_limit = 0.01


def doopadee(val, last_val):
    # stops val from exceeding set limits
    if val >= 0:
        return max(min(val, last_val + accel_limit), last_val - 20*accel_limit)
    return min(max(val, last_val - accel_limit), last_val + 20*accel_limit)


class MotorController:
    def __init__(self, pi, mcp, channel, pins, pid_constants, forward=1):
        self.current_sensor = CurrentSensor(mcp, channel)
        self.motor = Motor(pi, pins['pwm'], pins['dir'], forward=forward)
        self.encoder = RotaryEncoder(pi, pins['a'], pins['b'])
        self.pid = PIDController(pid_constants['kp'], pid_constants['ki'], pid_constants['kd'])
        self.last_speed = 0.0
    
    def adjust_motor_speed(self, target_vel, vel, max_edges_per_second):
        error = (target_vel - vel) / max_edges_per_second
        speed = min(max(self.pid.calc(error), -1.0), 1.0)
        speed = doopadee(speed, self.last_speed)
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
