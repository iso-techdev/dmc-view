import math

from PySide6.QtCore import QEvent, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
    QResizeEvent,
    QTransform,
)
from PySide6.QtWidgets import QWidget

from dmcview.accele_signal_manger import signal_manager


class Compass(QWidget):
    """
    Draw azimuth, declination, bank, and elevation class.

    Represent how to draw a circle, the 4 Directions (W, N, E, S), and how the user inputs as text,
    Draw the Elevation, Bank, and Azimuth inside the circle.

    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Digital Magnetic Compass")
        self.setMinimumSize(600, 420)
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.target_declination = 0.0
        self.current_declination = 0.0
        self.elevation = 0.0
        self.rotation = 0.0

        # acceleration vectors
        self.acc_x = 0.0
        self.acc_y = 0.0
        self.acc_z = 0.0

        self.signal_connected = (
            False  # So the first time the signal tries to disconnect it wont be able
        )

        self.start_animation_timer()

    def resizeEvent(self, event: QResizeEvent) -> None: # pylint: disable=invalid-name
        """
        triggers when the screen is resized.

        Args:
            event (QResizeEvent): The QT size event

        """


        self.create_static_pixmap()
        super().resizeEvent(event)

    def create_static_pixmap(self) -> None:
        """
        Create a black-outlined circle.

        (offset slightly to the left of center)using the QPainter class.


        Returns:
          Paints the circle on the left side of the widget.
        """

        self.static_pixmap = QPixmap(self.size())
        self.static_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(self.static_pixmap)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor("black")
        pen.setWidth(4)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Offset for the circle to be to the left
        x_offset = 70
        center = QPointF(self.rect().center().x() - x_offset, self.rect().center().y())
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 37

        # Drawing on the pixmap
        painter.drawEllipse(center, radius, radius)
        self.draw_cardinal_points(painter, center, radius)
        self.draw_lines(painter, center, radius)

        painter.end()

    def paintEvent(self, _: QEvent) -> None: # pylint: disable=invalid-name
        """
        Draws as text the user values.

        Type the azimuth, declination, bank angle, elevation, and acceleration on the right side of the circle.
        Args:
        event (QEvent): Class representing an event, such as a paint event.


        return:
        Displays as text the user values that have been input into the program.


        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.static_pixmap:
            painter.drawPixmap(0, 0, self.static_pixmap)

        x_offset = 70
        center = QPointF(self.rect().center().x() - x_offset, self.rect().center().y())
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 37
        self.draw_arrow(painter, center, radius)

        self.draw_red_line(painter, center, radius)

        font_size = max(12, self.width() // 80)
        line_spacing = font_size

        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.setFont(QFont("Arial", font_size))
        text_x = center.x() + radius + 47  # reduce the number to prevent capped text
        text_y = center.y() - radius

        test_pos = QPointF(text_x, text_y)
        azimuth_pos = QPointF(text_x, text_y + 4 * line_spacing)
        declination_pos = QPointF(text_x, text_y + 8 * line_spacing)
        rotation_pos = QPointF(text_x, text_y + 12 * line_spacing)
        inclination_pos = QPointF(text_x, text_y + 16 * line_spacing)
        acceleration_pos = QPointF(text_x, text_y + 20 * line_spacing)
        acceleration_vec_pos = QPointF(text_x, text_y + 22 * line_spacing)

        if self.signal_connected:
            signal_manager.data_signal.disconnect()  # Avoid duplicate connections
            self.signal_connected = True
        signal_manager.data_signal.connect(self.receive_acceleration)

        painter.drawText(test_pos, "Information: ")
        painter.drawText(azimuth_pos, f"Azimuth: {round(self.current_angle,2)} °")
        painter.drawText(
            declination_pos, f"Declination: {round(self.current_declination,2)} °"
        )
        painter.drawText(rotation_pos, f"Bank: {round(self.rotation,2)} °")
        painter.drawText(inclination_pos, f"Elevation: {round(self.elevation,2)} °")
        painter.drawText(acceleration_pos, "Acceleration:")
        painter.drawText(acceleration_vec_pos, f"{self.acc_x}, {self.acc_y}, {self.acc_z}")

    def receive_acceleration(self, x: float, y: float, z: float) -> None:
        self.acc_x = x
        self.acc_y = y
        self.acc_z = z
        self.update()

    def draw_cardinal_points(self, painter: QPainter, center: QPointF, radius: int) -> None:
        """
        Create cardinal direction markers (N, E, S, W).

        Radial lines from the center using the `draw_lines()` method.

        args:
            painter: QPainter object for drawing operations.
            center: Center point (QPointF) of the compass.
            radius: Radius of the compass circle.
        """
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)

        direction = {"N": 0, "E": 90, "S": 180, "W": 270}
        for label, angle in direction.items():
            rad_angle = math.radians(angle - 90)
            x = center.x() + (radius + 15) * math.cos(rad_angle)
            y = center.y() + (radius + 15) * math.sin(rad_angle)

            text_rect = painter.fontMetrics().boundingRect(label)
            text_x = x - text_rect.width() / 2
            text_y = y + text_rect.height() / 2

            painter.drawText(QPointF(text_x, text_y), label)

        for angle in range(0, 360, 30):
            rad_angle = math.radians(angle)
            outer_x = center.x() + radius * math.cos(rad_angle)
            outer_y = center.y() + radius * math.sin(rad_angle)
            inner_x = center.x() + (radius - 10) * math.cos(rad_angle)
            inner_y = center.y() + (radius - 10) * math.sin(rad_angle)

            painter.drawLine(QPointF(outer_x, outer_y), QPointF(inner_x, inner_y))

    def draw_lines(self, painter: QPainter, center: QPointF, radius: int) -> None:
        """ This method is for the inside lines around the circle from the inside. """

        painter.setPen(QPen(Qt.GlobalColor.black, 2))

        painter.drawLine(
            QPointF(center.x() - radius, center.y()), QPointF(center.x() + radius, center.y())
        )

        painter.drawLine(
            QPointF(center.x(), center.y() - radius), QPointF(center.x(), center.y() + radius)
        )

        split_length = 5
        num_splits = 12

        for i in range(num_splits):

            split_y = center.y() - (radius - 5) + i * (2 * (radius - 5) / (num_splits - 1))
            painter.drawLine(
                QPointF(center.x() - split_length, split_y),
                QPointF(center.x() + split_length, split_y),
            )

    def draw_arrow(self, painter: QPainter, center: QPointF, radius: int) -> None:
        """
        Creates an arrow that indicates the elevation angle.

        draws an arc to represent the elevation visually, and it uses trigonometric calculations to
        determine positions and transformations to ensure that the arrowhead is correctly oriented

        args:
        Radius: It determines how far the arrow will extend from its center.


        """

        painter.setBrush(QBrush(Qt.GlobalColor.red))
        painter.setPen(QPen(Qt.GlobalColor.red, 2))

        triangle_size = 20
        arrow_distance = radius * 0.8
        angle_rad = -math.radians(self.elevation)

        triangle_x: float = center.x() + arrow_distance * math.cos(angle_rad)
        triangle_y: float = center.y() + arrow_distance * math.sin(angle_rad)

        pen = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine)
        pen2 = QPen(QColor("DarkBlue"), 1, Qt.PenStyle.DashLine)

        painter.setPen(pen)

        painter.drawLine(int(center.x()), int(center.y()), int(triangle_x), int(triangle_y))

        floating_triangle = QPolygonF(
            [
                QPointF(-triangle_size / 2, triangle_size / 2),
                QPointF(triangle_size / 2, triangle_size / 2),
                QPointF(0, -triangle_size / 2),
            ]
        )

        transform = QTransform()
        transform.translate(triangle_x, triangle_y)
        transform.rotate(90 - self.elevation)

        rotated_triangle = transform.map(floating_triangle)
        painter.drawPolygon(rotated_triangle)

        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        arc2_radius = radius - 120
        rect2 = QRectF(
            center.x() - arc2_radius,
            center.y() - arc2_radius,
            2 * arc2_radius,
            2 * arc2_radius,
        )
        start_angle_incli = 0 * 16  # Inclination

        if self.elevation > 270:  # it is maxed at 90 but
            span_angle_incli = 90 * 16.00  # make it float
        elif self.elevation > 90:
            span_angle_incli = 0.00  # make it float
        else:
            span_angle_incli = (self.elevation) * 16  # float datatype (implicit)

        painter.resetTransform()

        mid_point_angel_incli = start_angle_incli + span_angle_incli / 2  # Inclination
        mid_angel_rad_incli = math.radians(mid_point_angel_incli / 16)

        midpoint_incli_x = center.x() + arc2_radius * math.cos(
            mid_angel_rad_incli
        )  # Inclination
        midpoint_incli_y = center.y() - arc2_radius * math.sin(mid_angel_rad_incli)

        label2 = "Elevation"

        painter.setPen(pen2)
        painter.drawArc(rect2, int(start_angle_incli), int(span_angle_incli))
        painter.drawText(
            QPointF(midpoint_incli_x + 11, midpoint_incli_y - 10), label2
        )  # Inclination

        self.draw_rotating_magnetic_north(
            painter, center, radius, self.current_declination
        )

        self.draw_azimuth(painter, center, radius, self.current_angle)

    def draw_rotating_magnetic_north(
        self,
        painter: QPainter,
        center: QPointF,
        radius: int,
        declination: float,
    ) -> None:
        """
        This method draws a magnetic north indicator along with a declination arc.

        args:
            declination (float): The magnetic declination in degrees.
        """

        dark_red = QColor(124, 10, 2)

        painter.setBrush(dark_red)
        painter.setPen(QPen(dark_red, 2))

        final_angle = declination % 360
        rad_angle = math.radians(final_angle - 90)  # -90 to align correctly

        marker_x = center.x() + (radius + 25) * math.cos(rad_angle)
        marker_y = center.y() + (radius + 25) * math.sin(rad_angle)

        marker_size = 10
        magnetic_marker = QPolygonF(
            [
                QPointF(marker_x - marker_size / 2, marker_y),
                QPointF(marker_x + marker_size / 2, marker_y),
                QPointF(marker_x, marker_y - marker_size),
            ]
        )

        painter.drawPolygon(magnetic_marker)

        painter.resetTransform()

        pen = QPen(dark_red, 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        arc_radius = radius + 25

        rect = QRectF(
            center.x() - arc_radius, center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius
        )

        start_angle = 90 * 16

        if self.current_declination > 180:
            span_angle = (360 - self.current_declination) * 16
        else:
            span_angle = -self.current_declination * 16  # angle in 1/16th degree expected by Qt

        painter.drawArc(rect, int(start_angle), int(span_angle))

        mid_point_angel = start_angle + span_angle / 2
        angel_rad = math.radians(mid_point_angel / 16)

        mid_point_x = center.x() + arc_radius * math.cos(angel_rad)
        mid_point_y = center.y() - arc_radius * math.sin(angel_rad)

        label = "Declination"

        if self.current_declination < 180:  # each side has different alignment
            painter.drawText(
                QPointF(mid_point_x + 50, mid_point_y + 1), label
            )  # +7 so it is not touching with the arc
        else:
            painter.drawText(
                QPointF(mid_point_x - 100, mid_point_y), label
            )  # -90 so it is not touching the circle

    def draw_azimuth(
        self,
        painter: QPainter,
        center: QPointF,
        radius: int,
        compass_angle: float,
    ) -> None:
        """
        Calculate the azimuth position based on the compass angle and draw it with specified properties.

        Args:
            painter: QPainter object for drawing operations.
            center: Center point (QPointF) of the compass.
            radius: Radius of the compass circle.
            compass_angle: Current compass angle in degrees.
        """

        dark_green = QColor(87, 108, 67)

        painter.setBrush(dark_green)
        painter.setPen(QPen(dark_green, 2))

        final_angle = compass_angle % 360
        rad_angle = math.radians(final_angle - 90)  # -90 to align correctly

        marker_x = center.x() + (radius - 20) * math.cos(rad_angle)
        marker_y = center.y() + (radius - 20) * math.sin(rad_angle)

        marker_size = 10
        magnetic_marker = QPolygonF(
            [
                QPointF(marker_x - marker_size / 2, marker_y),
                QPointF(marker_x + marker_size / 2, marker_y),
                QPointF(marker_x, marker_y - marker_size),
            ]
        )

        painter.drawPolygon(magnetic_marker)

        painter.resetTransform()

        pen = QPen(dark_green, 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        arc_radius = radius - 20

        rect = QRectF(
            center.x() - arc_radius, center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius
        )

        start_angle = 90 * 16

        if self.current_angle > 180:
            span_angle = (360 - self.current_angle) * 16
        else:
            span_angle = -self.current_angle * 16  # angle in 1/16th degree expected by Qt

        painter.drawArc(rect, int(start_angle), int(span_angle))

        mid_point_angel = start_angle + span_angle / 2
        angel_rad = math.radians(mid_point_angel / 16)

        mid_point_x = center.x() + arc_radius * math.cos(angel_rad)
        mid_point_y = center.y() - arc_radius * math.sin(angel_rad)

        label = "Azimuth"

        if self.current_angle == 0:  # each side has different alignment
            painter.drawText(QPointF(mid_point_x + 12, mid_point_y + 22), label)
        elif self.current_angle < 180:  # each side has different alignment
            painter.drawText(QPointF(mid_point_x - 25, mid_point_y + 25), label)
        else:
            painter.drawText(QPointF(mid_point_x - 10, mid_point_y + 25), label)

    def start_animation_timer(self) -> None:
        """ This method initializes and starts the timer.
        based animations for smoothly updating the azimuth (compass heading) and declination (magnetic deviation) angles
        """

        self.azimuth_timer = QTimer(self)
        self.azimuth_timer.timeout.connect(self.__rotate_angle)
        self.azimuth_timer.start(1)  # Adjust the speed of azimuth animation

        self.declination_timer = QTimer(self)
        self.declination_timer.timeout.connect(self.__animate_declination)
        self.declination_timer.start(2)  #  Adjust the speed of declination animation

    def __rotate_angle(self) -> None:
        if self.current_angle != self.target_angle:
            diff = round(self.target_angle - self.current_angle, 2)  # Here is for the azimuth
            step = 0.1 if diff > 0 else -0.1

            if abs(diff) > 180:
                step *= -1

            if abs(diff) < 0.2:
                self.current_angle = self.target_angle
            else:
                self.current_angle = (self.current_angle + step) % 360
            self.update()

    def update_angle(self, target_angle: float) -> None:
        self.target_angle = target_angle % 360

    def update_declination(self, target_declination: float) -> None:
        self.target_declination = target_declination % 360

    def __animate_declination(self) -> None:
        if self.current_declination != self.target_declination:
            diff = round(
                self.target_declination - self.current_declination, 2
            )  # Iso : float here stick to to decimal place as a diff result
            step = 0.1 if diff > 0 else -0.1

            if abs(diff) > 180:
                step *= -1

            if abs(diff) < 0.2:
                self.current_declination = self.target_declination
            else:
                self.current_declination = (self.current_declination + step) % 360
            self.update()

    def set_elevation(self, elevation: float) -> None:
        self.elevation = elevation
        self.update()

    def set_rotation(self, rotation: float) -> None:
        self.rotation = rotation
        self.update()

    def draw_red_line(self, painter: QPainter, center: QPointF, radius: int) -> None:
        """
        This method draws an arc to represent the bank visually.

        represent the magnetic north direction on a compass, it uses a QPainter to draw
        shapes and text on a graphical interface, typically in a Qt application.

        Args:
            painter (QPainter): An instance of QPainter used for drawing operations on the widget.
            center (QPointF): The center point of the compass, represented as a QPointF object.
            radius (int): The radius of the compass circle, determines the size and position of the drawn elements.

        """
        painter.setPen(QPen(Qt.GlobalColor.red, 2))

        line_length = radius * 2
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(-self.rotation)

        line_start = QPointF(-line_length / 2, 0)
        line_end = QPointF(line_length / 2, 0)
        transformed_line: QPolygonF = transform.map(QPolygonF([line_start, line_end]))

        painter.drawLine(transformed_line.first(), transformed_line.last())

        pen = QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.DashLine)
        painter.setPen(pen)

        arc_radius = radius - 40  # -40 so it is not touching the circle

        rect = QRectF(
            center.x() - arc_radius, center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius
        )

        start_angle = 16 * 180  # *180 so it is draw to the left of the circle
        span_angle = self.rotation * 16  # angle in 1/16th degree expected by Qt

        painter.drawArc(rect, int(start_angle), int(span_angle))

        mid_point_angel = start_angle + span_angle / 2
        mid_angel_rad = math.radians(
            mid_point_angel / 16
        )  # angle in 1/16th degree expected by Qt

        midpoint_x = (
            center.x() + arc_radius * math.cos(mid_angel_rad) + 10
        )  # offset to the right 10 so it is not touching the arc
        midpoint_y = center.y() - arc_radius * math.sin(mid_angel_rad)

        label = "Bank"
        painter.drawText(
            QPointF(midpoint_x, midpoint_y - 2), label
        )  # -2 so it is not touching line at 0 angle
