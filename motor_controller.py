from current_sensor import CurrentSensor
from filter import DoubleExponentialFilter
from motor import Motor
from parameters import distance_ratio, max_wheel_vel, smoothing_factor, \
    trend_smoothing_factor
from pid import PID
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, mcp_channel, pins, pid_constants, forward):
        self.current_sensor = CurrentSensor(mcp_channel)
        self._motor = Motor(pins['pwm'], pins['dir'], forward)
        self._encoder = RotaryEncoder(pins['a'], pins['b'])
        self._pid = PID(pid_constants)
        self._vel_filter = DoubleExponentialFilter(smoothing_factor,
                                                   trend_smoothing_factor)
        self._vel = 0
    
    def adjust_motor_speed(self, target_vel, time_elapsed):
        error = (target_vel - self._vel)/max_wheel_vel
        speed = min(max(self._pid.calc(error, time_elapsed), -1.0), 1.0)
        self._motor.set_speed(speed)
    
    def read_encoder(self, time_elapsed):
        dist_traveled = self._encoder.get_pos_dif()*distance_ratio
        self._vel = self._vel_filter.filter(dist_traveled/time_elapsed)
        return dist_traveled
    
    def brake(self):
        self._motor.set_speed(0)
        self._pid.reset()
    
    def stop(self):
        self._motor.stop()
        self._encoder.stop()
