import pytest


@pytest.fixture(scope='function')
def motor1(motors, conversions):
    motor = motors.MotorParams(
        name="am9015", 
        stall_torque=0.428, 
        stall_current=63.8, 
        free_speed=conversions.rpm_to_radps(16000.))
    return motor
    

def test_motor_init1(motors):
    motor = motors.MotorParams(
        name="am9015", 
        stall_torque=0.428, 
        stall_current=63.8, 
        free_speed=(16000.))

    assert motor.name == "am9015"
    assert motor.stall_torque == 0.428
    assert motor.free_speed == 16000.
    assert motor.spec_voltage == 12.


def test_motor_init2(motors):
    motor = motors.MotorParams(
        name="am9015", 
        stall_torque=0.428, 
        stall_current=63.8, 
        voltage=18.,
        free_speed=(16000.))

    assert motor.name == "am9015"
    assert motor.stall_torque == 0.428
    assert motor.free_speed == 16000.
    assert motor.spec_voltage == 18.


def test_motor_ktorque(motor1):
    assert motor1.ktorque() == pytest.approx(0.006708, 0.01)


def test_motor_kspeed(motor1):
    assert motor1.free_speed == pytest.approx(1675.51, 0.01)
    assert motor1.kspeed() == pytest.approx(0.00716, 0.01)


def test_motor_resistance(motor1):
    assert motor1.stall_torque == 0.428
    assert motor1.spec_voltage == 12.
    assert motor1.resistance() == pytest.approx(0.188, 0.01)


@pytest.mark.parametrize("current, torque", [
    (0, 0), # todo: free current
    (31.9, 0.214),
    (63.8, 0.428),
    ])
def test_motor_torque_at_current(motor1, current, torque):
    expected_torque = pytest.approx(torque, 0.01)
    assert motor1.torque_at_current(current) == expected_torque


@pytest.mark.parametrize("current, torque", [
    (0, 0), # todo: free current
    (31.9, 0.214),
    (63.8, 0.428),
    ])
def test_motor_torque_at_current(motor1, torque, current):
    expected_current = pytest.approx(current, 0.01)
    assert motor1.current_at_torque(torque) == expected_current


@pytest.mark.parametrize("speed, voltage", [
    (0, 0), 
    (1675.5, 12.), # todo: free current
    ])
def test_motor_back_emf(motor1, speed, voltage):
    expected_voltage = pytest.approx(voltage, 0.01)
    assert motor1.back_emf(speed) == expected_voltage


def test_motorsystem_init(motors, motor1):
    motorsystem = motors.MotorSystem(
        motor=motor1, motor_count=2, gearing_ratio=73)

    assert motorsystem.motor == motor1
    assert motorsystem.motor_count == 2
    assert motorsystem.gearing_ratio == 73
    assert motorsystem.name == "am9015"
    stall_torque = pytest.approx(2 * 73 * 0.428, 0.01)
    assert motorsystem.stall_torque == stall_torque
    free_speed = pytest.approx(1675.5 / 73, 0.01)
    assert motorsystem.free_speed == free_speed
    

def test_motorsystem_back_emf(motors, motor1):
    motorsystem = motors.MotorSystem(
        motor=motor1, motor_count=2, gearing_ratio=73)

    voltage = motorsystem.motor_back_emf(15.)
    voltage1 = motor1.back_emf(15. * 73)

    assert voltage == pytest.approx(voltage1, 0.01)



@pytest.mark.parametrize("current, torque", [
    (0, 0), # todo: free current
    (31.9, 0.214 * 73 * 2),
    (63.8, 0.428 * 73 * 2),
    ])
def test_motorsystem_torque_at_motor_current(motors, motor1, current, torque):
    motorsystem = motors.MotorSystem(
        motor=motor1, motor_count=2, gearing_ratio=73)

    actual_torque = motorsystem.torque_at_motor_current(current)
    expected_torque = pytest.approx(torque, 0.01)
    assert actual_torque == expected_torque


@pytest.mark.parametrize("current, torque", [
    (0, 0), # todo: free current
    (31.9, 0.214 * 73 * 2),
    (63.8, 0.428 * 73 * 2),
    ])
def test_motorsystem_motor_current_at_torque(motors, motor1, current, torque):
    motorsystem = motors.MotorSystem(
        motor=motor1, motor_count=2, gearing_ratio=73)

    actual_current = motorsystem.motor_current_at_torque(torque)
    expected_current = pytest.approx(current, 0.01)
    assert actual_current == expected_current
