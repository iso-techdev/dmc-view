from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPaintEvent

from dmcview.compass import Compass


@pytest.fixture
def compass():
    c = Compass()
    return c


def test_initial_state(compass):
    """Check that default values are initialized correctly."""
    assert compass.current_angle == 0.0
    assert compass.target_angle == 0.0
    assert compass.current_declination == 0.0
    assert compass.target_declination == 0.0
    assert compass.elevation == 0.0
    assert compass.rotation == 0.0
    assert not compass.signal_connected


def test_update_angle_and_declination(compass):
    compass.update_angle(90)
    assert compass.target_angle == 90
    compass.update_angle(450)
    # Should wrap around 360
    assert compass.target_angle == 90

    compass.update_declination(720)
    assert compass.target_declination == 0


def test_receive_acceleration_updates_values(compass):
    compass.receive_acceleration(1.0, 2.0, 3.0)
    assert (compass.acc_x, compass.acc_y, compass.acc_z) == (1.0, 2.0, 3.0)

def test_rotation_and_elevation(compass):
    compass.set_rotation(45)
    compass.set_elevation(15)
    assert compass.rotation == 45
    assert compass.elevation == 15

def test_angle_animation(compass):
    """Simulate a timer tick — rotation animation should change current_angle."""
    compass.target_angle = 10.0
    compass.current_angle = 0.0
    compass._Compass__rotate_angle()
    assert compass.current_angle != 0.0


def test_declination_animation(compass):
    """Simulate declination animation."""
    compass.target_declination = 10.0
    compass.current_declination = 0.0
    compass._Compass__animate_declination()
    assert compass.current_declination != 0.0

def test_create_static_pixmap_no_crash(compass):
    compass.resize(600, 420)
    compass.create_static_pixmap()
    assert compass.static_pixmap is not None


def test_draw_methods_run(compass):
    """
    Test all main draw methods using minimal mocks to avoid real GUI painting.
    This will increase coverage for most of the Compass code.
    """
    # Dummy event to trigger paintEvent

    compass.create_static_pixmap()

    event = QPaintEvent(compass.rect())

    # Patch GUI-heavy drawing methods inside paintEvent
    with patch.object(compass, "draw_rotating_magnetic_north") as mock_north, \
         patch.object(compass, "draw_azimuth") as mock_azimuth, \
         patch.object(compass, "draw_red_line") as mock_red_line:

        # Call paintEvent which internally calls draw_arrow
        compass.paintEvent(event)

        # Assertions (optional, ensures patching worked)
        mock_north.assert_called()
        mock_azimuth.assert_called()
        mock_red_line.assert_called()


def test_draw_arrow_called(compass):
    painter = MagicMock()
    center = QPointF(100, 100)
    radius = 50

    compass.draw_arrow(painter, center, radius)


    # assert that drawText and drawLine were called
    assert painter.drawText.call_count == 3
    assert painter.drawLine.call_count == 1
    assert painter.drawPolygon.call_count == 3
