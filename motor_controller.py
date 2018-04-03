from current_sensor import CurrentSensor
from motor import Motor
from parameters import max_wheel_vel
from pid import PID
from rotary_encoder import RotaryEncoder


class MotorController:
    def __init__(self, mcp_channel, pins, pid_constants, forward):
        self._current_sensor = CurrentSensor(mcp_channel)
        self._motor = Motor(pins['pwm'], pins['dir'], forward)
        self._encoder = RotaryEncoder(pins['a'], pins['b'])
        self._pid = PID(pid_constants)
        self._last_speed = 0.0
    
    def adjust_motor_speed(self, target_vel, vel):
        error = (target_vel - vel)/max_wheel_vel
        speed = min(max(self._pid.calc(error), -1.0), 1.0)
        self._motor.set_speed(speed)
        self._last_speed = speed
    
    def stop(self):
        self._motor.stop()
        self._encoder.stop()
    
    def check_current(self):
        # TODO: the motor should temporarily stop while the current lowers
        # instead of shutting off permanently
        if self._current_sensor.check_current():
            self._motor.stop()
            # raise Exception('motor current trip')
    
    def get_pos_dif(self):
        return self._encoder.get_pos_dif()
