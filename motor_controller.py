from motor import Motor
from rotary_encoder import RotaryEncoder
from pid import PID
from current_sensor import CurrentSensor


class MotorController:
    def __init__(self, pi, mcp, channel, pins, pid_constants, pwm_range=255, forward=1, interval=0.01):
        self.current_sensor = CurrentSensor(mcp, channel)
        self.motor = Motor(pi, pins['pwm'], pins['dir'], pwm_range=pwm_range, forward=forward)
        self.encoder = RotaryEncoder(pi, pins['a'], pins['b'])
        self.pid = PID(pid_constants['kp'], pid_constants['ki'], pid_constants['kd'])
        self.interval = interval
    
    def do_mo_shit(self, target_vel, vel):
        error = target_vel - vel
        # TODO: name that
        name_this = self.pid.calc(error)
        self.motor.set_speed(name_this)
    
    def stop(self):
        self.motor.stop()
        self.encoder.stop()
    
    def check_current(self):
        return self.current_sensor.check_current()
    
    def get_pos_dif(self):
        return self.encoder.get_pos_dif()
