import sys
from os.path import dirname
from kerykeion.astrocore import AstroData, Calculator, CalculatorPosition
from kerykeion.utilities import kr_settings as settings
from kerykeion.utilities.general import print_settings_path
from kerykeion.utilities.charts import (
  MakeSvgInstance as MakeSvgInstance,
  MakeSvgConfig
)

sys.path.append(dirname(__file__))
