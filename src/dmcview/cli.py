"""The command line interface (CLI) parser"""

from argparse import ArgumentParser, Namespace

from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from dmcview import __version__
from dmcview import __author__
from dmcview import __description__
from dmcview import __license__
from dmcview import __title__
from dmcview import __url__

from dmcview._help import bug_reporting
from dmcview.acceleration import Accelaration3D
from dmcview.compass import Compass
from dmcview.simulator import start_simulator


def get_float_input(prompt: str, default: float) -> float:
    """
    Gets the input from the user using the terminal.

    Prompts the user to enter the angle for azimuth, declination, rotation, elevation, and bank.

    Args:
        prompt (str) : The desired question for the user to indicate which angle is required.
        default (float) : The default value of the angle if the user does not enter a value.

    Return:
        float: the parsed string as float is returned

    Raises:
        ValueError: If the user's input is not a numerical value.
    """

    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ") or default
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_acceleration_input(
    prompt: str, x: float, y: float, z: float
) -> tuple[float, float, float]:
    """
    Get three acceleration values from the user, and provide default values.

    Args:
        prompt (str): contains the message to display to the user when asking for input.
        x (float): represent the default value for the x of acceleration.
        y (float): represent the default value for the y of acceleration.
        z (float): represent the default value for the z of acceleration.

    Return:
        tuple: the x,y and z values.

    Raises:
        ValueError: if (x, y, z) are not numeric values.
    """

    while True:
        try:
            user_input = input(f"{prompt} (default {x,y,z}): ").split()
            try:
                user_x = user_input[0]
            except IndexError:
                user_x = str(x)
            try:
                user_y = user_input[1]
            except IndexError:
                user_y = str(y)
            try:
                user_z = user_input[2]
            except IndexError:
                user_z = str(z)

            return float(user_x), float(user_y), float(user_z)

        except ValueError:
            print("Invalid input. Please enter a correct numeric value.")


def main() -> None:
    """
    This is the main function that executes the program.

    This function uses argparse to handle input from the command line.
    It creates an instance of the Compass class and sets its values using the inputs provided.

    Command-line arguments
    ----------------------
    -a : float
        Azimuth angle towards the desired location.
    -d : float
        Declination angle from the real north to the magnetic north.
    -b : float
        Bank angle at the longitudinal and horizontal axis.

    -ac: float float float
        X, Y and Z acceleration

    Examples:
        >>> dmcview -a 45.5 -d 5.6 -b 30.35 -e 15.23 -ac 14.21 12.3 13.5
        >>> dmcview -s Y
    """

    # https://docs.python.org/3/howto/argparse.html
    parser = ArgumentParser(
        prog="dmcview",
        usage="dmcview -a 45.5 -d 5.6 -b 30.35 -e 15.23 -ac 14.21 12.3 13.5  \n       dmcview -s Y",
        description="dmcview Command Line Interface",
    )

    parser.add_argument(
        "-s",
        help='Start simulator Y/N. If argument is not supplied or "N" is supplied, it will start input mode',
        type=str,
        default="N",
        nargs="?",
        metavar="simulation",
    )
    parser.add_argument(
        "-a",
        help="direction measured in degrees clockwise from north",
        type=float,
        default=None,
        nargs="?",
        metavar="azimuth",
    )
    parser.add_argument(
        "-d",
        help="difference between real north and magnetic north",
        type=float,
        nargs="?",
        default=None,
        metavar="declination",
    )
    parser.add_argument(
        "-b",
        help="Inclination angle at the longitudinal and horizontal axis",
        type=float,
        nargs="?",
        default=None,
        metavar="inclination",
    )
    parser.add_argument(
        "-e",
        help="angular height of a point of interest above or below the horizon, in degrees",
        type=float,
        nargs="?",
        default=None,
        metavar="bank",
    )
    parser.add_argument(
        "-ac",
        help="acceleration of the object, using 3 points vector",
        type=float,
        nargs="*",
        default=None,
        metavar="[x,y,z]",
    )
    parser.add_argument("--version", action="version", version=f"dmcview {__version__}") # this is build in parser to display the version of the package
    parser.add_argument("--author", action="store_true", help="Display author information")
    parser.add_argument("--report-bug", action="store_true", help="Library detail information to report a bug")
    parser.add_argument("--description", action="store_true", help="Display description of the package")
    parser.add_argument("--license", action="store_true", help="Display license information")
    parser.add_argument("--title", action="store_true", help="Display title of the package")
    parser.add_argument("--url", action="store_true", help="Display read the docs url of the package")

    args: Namespace = parser.parse_args()

    if args.author:
        print(f"Author: {__author__}")
        return

    if args.report_bug:
        bug_reporting()
        return

    if args.description:
        print(f"Description: {__description__}")
        return

    if args.license:
        print(f"License: {__license__}")
        return

    if args.title:
        print(f"Title: {__title__}")
        return

    if args.url:
        print(f"URL: {__url__}")
        return

    simulation: str = args.s
    print(simulation)
    if args.s is not None and args.s == "Y":
        start_simulator()
    else:
        start_input(args)

# pylint: disable=too-many-statements
def start_input(args: Namespace) -> None:
    azimuth: float = (
        args.a
        if args.a is not None
        else get_float_input("Enter the azimuth angle in degrees; for example 40.45", 45.5)
    )  # azimuth
    declination: float = (
        args.d
        if args.d is not None
        else get_float_input("Enter the declination angle in degrees; for example 30.0", 30.0)
    )  # declination
    bank: float = (
        args.b
        if args.b is not None
        else get_float_input("Enter the bank angle in degrees; for example -7.0", 5.0)
    )  # Inclination
    elevation: float = (
        args.e
        if args.e is not None
        else get_float_input("Enter the elevation in degrees; for example 25.21", 20.0)
    )  # elevation
    x, y, z = (
        args.ac
        if args.ac is not None
        else get_acceleration_input(
            "Enter the acceleration values(vectors: x,y,z); for example 12 12 13",
            0.0,
            0.0,
            0.0,
        )
    )

    app = QApplication()
    main_widget = QWidget()
    layout = QHBoxLayout(main_widget)
    compass = Compass()

    layout.addWidget(compass)

    canvas = Accelaration3D()
    canvas.setFixedSize(350, 350)
    layout.addWidget(canvas)

    # def on_resize(event):
    #    screen_size = main_widget.size()
    #    if screen_size.width()<1000 or screen_size.height()<500:
    #        canvas.setFixedSize(250,250)
    #    else:
    #        canvas.setFixedSize(350,350)
    #
    #    print(screen_size)

    # main_widget.resizeEvent = on_resize

    compass.update_declination(
        declination
    )  # This is Declination and can be float to two decimal places for example 35.55
    compass.update_angle(
        azimuth
    )  # This is Azimuth and can be float to two decimal places for example 35.55
    compass.set_rotation(
        bank
    )  # This is the Inclination can be floated to two decimal places for example 35.55
    compass.set_elevation(
        elevation
    )  # This is the Elevation can be floated to two decimal places for example 25.55

    canvas.update_acceleration(x, y, z)

    main_widget.show()
    app.exec()


if __name__ == "__main__":  # this is important so that it does not run from pytest
    main()
