from decimal import ROUND_HALF_UP, Decimal

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import QTimer

from dmcview.accele_signal_manger import signal_manager


class Accelaration3D(FigureCanvas):
    """
    This class displays a 3D window.

    It depends on the acceleration value provided by the user in (x, y, z), and it uses the add_subplot()
    method to represent the entire canvas for the plot.


    """
    def __init__(self, figure: Figure | None = None) -> None:
        super().__init__(figure)

        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 0.0

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.value = 0.2  # 0.1 step is very slow

        self.figure = Figure()
        self.ax = self.figure.add_subplot(projection="3d")

        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([-15, 15])
        self.ax.set_title("3D Acceleration")

        self.quiver = self.ax.quiver(
            0, 0, 0, 0, 0, 0, color="red", linewidth=2, arrow_length_ratio=0.3
        ) #this is for the arrow

        self.ax.view_init(azim=-115, elev=20, roll=3)
        self.start_acceleration_timer()

    def update_acceleration_vector(self) -> None:
        """
        Draws the arrow that represents the acceleration value provided by the user.

        This method uses Decimal to round the floating-point number.


        """

        if self.target_x < self.x:
            self.target_x += self.value
        elif self.target_x > self.x:
            self.target_x -= self.value

        if self.target_y < self.y:
            self.target_y += self.value
        elif self.target_y > self.y:
            self.target_y -= self.value

        if self.target_z < self.z:
            self.target_z += self.value
        elif self.target_z > self.z:
            self.target_z -= self.value

        self.target_y = float(
            Decimal(self.target_y).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        )
        self.target_x = float(
            Decimal(self.target_x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        )
        self.target_z = float(
            Decimal(self.target_z).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        )

        signal_manager.data_signal.emit(self.target_x, self.target_y, self.target_z)

        accel = np.array([self.target_x, self.target_y, self.target_z])
        origin = np.array([0, 0, 0])

        self.quiver.remove()
        self.quiver = self.ax.quiver(
            *origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3
        )
        self.draw()

    def start_acceleration_timer(self) -> None:
        self.acceleration_timer = QTimer(self)
        self.acceleration_timer.timeout.connect(self.update_acceleration_vector)
        self.acceleration_timer.start(60)

    def update_acceleration(self, x: float, y: float, z: float) -> None:
        self.y = round(y, 1)
        self.x = round(x, 1)
        self.z = round(z, 1)

        last_x_digit = self.x * 10
        last_x_digit = last_x_digit % 10

        if last_x_digit % 2 != 0:
            self.x -= 0.1  # since the step is 0.2 we will make odd inputs into even.

        last_y_digit = self.y * 10
        last_y_digit = last_y_digit % 10

        if last_y_digit % 2 != 0:
            self.y -= 0.1  # since the step is 0.2 we will make odd inputs into even.

        last_z_digit = self.z * 10
        last_z_digit = last_z_digit % 10

        if last_z_digit % 2 != 0:
            self.z -= 0.1  # since the step is 0.2 we will make odd inputs into even.

        self.y = round(self.y, 1)
        self.x = round(self.x, 1)
        self.z = round(self.z, 1)
