from current_sensor import CurrentSensor
from motor import Motor
from pid import PIController
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, pi, mcp, channel, pins, pi_constants, forward=1):
        self.current_sensor = CurrentSensor(mcp, channel)
        self.motor = Motor(pi, pins['pwm'], pins['dir'], forward=forward)
        self.encoder = RotaryEncoder(pi, pins['a'], pins['b'])
        self.pid = PIController(pi_constants['kp'], pi_constants['ki'])
    
    def adjust_motor_speed(self, target_vel, vel, max_edges_per_second):
        error = (target_vel - vel) / max_edges_per_second
        self.motor.set_speed(min(1.0, max(-1.0, self.pid.calc(error))))
    
    def stop(self):
        self.motor.stop()
        self.encoder.stop()
    
    def check_current(self):
        # TODO: the motor should temporarily stop while the current lowers instead of shutting off permanently
        if self.current_sensor.check_current():
            self.motor.stop()
            raise Exception('motor current trip')
    
    def get_pos_dif(self):
        return self.encoder.get_pos_dif()
