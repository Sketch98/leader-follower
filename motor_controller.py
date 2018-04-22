from current_sensor import CurrentSensor
from filter import IrregularDoubleExponentialFilter
from motor import Motor
from parameters import distance_ratio, max_wheel_vel, motor_vel_smoothing_factors
from pid import PID
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, mcp_channel, pins, pid_constants, forward):
        self.current_sensor = CurrentSensor(mcp_channel)
        self._motor = Motor(pins['pwm'], pins['dir'], forward)
        self._encoder = RotaryEncoder(pins['a'], pins['b'])
        self._pid = PID(pid_constants)
        self._vel_filter = IrregularDoubleExponentialFilter(*motor_vel_smoothing_factors)
        self._vel = 0
    
    def adjust_motor_speed(self, target_vel, time_elapsed):
        # use a pi controller to control the speed and limit the output to
        # [-1, 1] (-1 and 1 correspond to 100% pwm output)
        error = (target_vel - self._vel)/max_wheel_vel
        speed = min(max(self._pid.calc(error, time_elapsed), -1), 1)
        self._motor.set_speed(speed)
    
    def read_encoder(self, time_elapsed):
        # gets the amount the wheel has turned in the last interval and
        # calculates the wheel's speed with a filter added in
        dist_traveled = self._encoder.get_pos_dif()*distance_ratio
        self._vel = self._vel_filter.filter(dist_traveled/time_elapsed, time_elapsed)
        return dist_traveled
    
    def reset(self):
        self._motor.set_speed(0)
        self._pid.reset()
        self._encoder.reset()
    
    def stop(self):
        self._motor.stop()
        self._encoder.stop()
