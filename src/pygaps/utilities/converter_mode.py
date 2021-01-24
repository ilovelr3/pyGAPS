"""Perform conversions between different variables used."""

from .converter_unit import _MASS_UNITS
from .converter_unit import _MOLAR_UNITS
from .converter_unit import _PRESSURE_UNITS
from .converter_unit import _VOLUME_UNITS
from .converter_unit import c_unit
from .exceptions import ParameterError

_PRESSURE_MODE = {
    "absolute": _PRESSURE_UNITS,
    "relative": None,
    "relative%": None,
}

_MATERIAL_MODE = {
    "mass": _MASS_UNITS,
    "volume": _VOLUME_UNITS,
    "molar": _MOLAR_UNITS,
    "percent": None,
    "fractional": None,
}


def c_pressure(
    value, mode_from, mode_to, unit_from, unit_to, adsorbate=None, temp=None
):
    """
    Convert pressure units and modes.

    Adsorbate name and temperature have to be
    specified when converting between modes.

    Parameters
    ----------
    value : float
        The value to convert.
    mode_from : str
        Whether to convert from a mode.
    mode_to: str
        Whether to convert to a mode.
    unit_from : str
        Unit from which to convert.
    unit_from : str
        Unit to which to convert.
    adsorbate : Adsorbate, optional
        Adsorbate on which the pressure is to be
        converted. Required for mode change.
    temp : float, optional
        Temperature at which the pressure is measured, in K.
        Required for mode changes to relative pressure.

    Returns
    -------
    float
        Pressure converted as requested.

    Raises
    ------
    ``ParameterError``
        If the mode selected is not an option.
    """
    if mode_from != mode_to:

        if mode_to not in _PRESSURE_MODE:
            raise ParameterError(
                f"Mode selected for pressure ({mode_to}) is not an option. "
                f"Viable modes are {list(_PRESSURE_MODE)}"
            )

        unit = None
        sign = 1
        factor = 1

        # Now go through various global options
        if "absolute" in [mode_to, mode_from]:
            if mode_to == "absolute":
                if not unit_to:
                    raise ParameterError("Specify unit to convert to.")
                if unit_to not in _PRESSURE_UNITS:
                    raise ParameterError(
                        f"Unit selected for pressure ({unit_to}) is not an option. "
                        f"Viable units are {list(_PRESSURE_UNITS)}"
                    )
                unit = unit_to
                sign = 1

            if mode_from == "absolute":
                if not unit_from:
                    raise ParameterError("Specify unit to convert from.")
                if unit_from not in _PRESSURE_UNITS:
                    raise ParameterError(
                        f"Unit selected for pressure ({unit_from}) is not an option. "
                        f"Viable units are {list(_PRESSURE_UNITS)}"
                    )
                unit = unit_from
                sign = -1

            if not temp:
                raise ParameterError(
                    "A temperature is required for this conversion."
                )

            factor = adsorbate.saturation_pressure(temp, unit=unit)

            if "relative%" in [mode_to, mode_from]:
                factor = factor / 100

        elif mode_to in ["relative", "relative%"]:
            factor = 100
            if mode_to == "relative%":
                sign = 1
            elif mode_to == "relative":
                sign = -1

        return value * factor**sign

    # convert just units in absolute mode
    elif unit_to and mode_from == 'absolute':
        return c_unit(_PRESSURE_MODE[mode_from], value, unit_from, unit_to)

    # otherwise no change
    return value


def c_loading(
    value,
    basis_from,
    basis_to,
    unit_from,
    unit_to,
    adsorbate=None,
    temp=None
):
    """
    Convert loading units and basis.

    Adsorbate name and temperature have to be
    specified when converting between basis.

    Parameters
    ----------
    value : float
        The value to convert.
    basis_from : str
        Whether to convert from a basis.
    basis_to: str
        Whether to convert to a basis.
    unit_from : str
        Unit from which to convert.
    unit_from : str
        Unit to which to convert.
    adsorbate : str
        Adsorbate for which the pressure is to be converted.
    temp : float
        Temperature at which the pressure is measured, in K.

    Returns
    -------
    float
        Loading converted as requested.

    Raises
    ------
    ``ParameterError``
        If the mode selected is not an option.
    """
    if basis_from != basis_to:

        if basis_to not in _MATERIAL_MODE:
            raise ParameterError(
                f"Basis selected for loading ({basis_to}) is not an option. "
                f"Viable basis for uptake are {list(_MATERIAL_MODE)}"
            )

        if _MATERIAL_MODE[basis_to] is not None and not unit_to:
            raise ParameterError(
                f"To convert to {basis_to} basis, units must be specified."
            )
        if _MATERIAL_MODE[basis_from] is not None and not unit_from:
            raise ParameterError(
                f"To convert from {basis_from} basis, units must be specified."
            )

        if unit_to not in _MATERIAL_MODE[basis_to]:
            raise ParameterError(
                f"Unit selected for loading unit_to ({unit_to}) is not an option. "
                f"Viable units are {list(_MATERIAL_MODE[basis_to])}"
            )

        if unit_from not in _MATERIAL_MODE[basis_from]:
            raise ParameterError(
                f"Unit selected for loading unit_from ({unit_from}) is not an option. "
                f"Viable units are {list(_MATERIAL_MODE[basis_from])}"
            )

        if basis_from == 'mass':
            if basis_to == 'volume':
                constant = adsorbate.gas_density(temp=temp)
                sign = -1
            elif basis_to == 'molar':
                constant = adsorbate.molar_mass()
                sign = -1
        elif basis_from == 'volume':
            if basis_to == 'mass':
                constant = adsorbate.gas_density(temp=temp)
                sign = 1
            elif basis_to == 'molar':
                constant = adsorbate.gas_density(temp=temp
                                                 ) / adsorbate.molar_mass()
                sign = -1
        elif basis_from == 'molar':
            if basis_to == 'mass':
                constant = adsorbate.molar_mass()
                sign = 1
            elif basis_to == 'volume':
                constant = adsorbate.gas_density(temp=temp
                                                 ) / adsorbate.molar_mass()
                sign = -1

        value = value * _MATERIAL_MODE[basis_from][unit_from] \
            * constant ** sign \
            / _MATERIAL_MODE[basis_to][unit_to]

    elif unit_to and unit_from != unit_to:
        return c_unit(_MATERIAL_MODE[basis_from], value, unit_from, unit_to)

    return value


def c_adsorbent(
    value, basis_from, basis_to, unit_from, unit_to, material=None
):
    """
    Convert adsorbent units and basis.

    The name of the material has to be
    specified when converting between basis.

    Parameters
    ----------
    value : float
        The value to convert.
    basis_from : str
        Whether to convert from a basis.
    basis_to: str
        Whether to convert to a basis.
    unit_from : str
        Unit from which to convert.
    unit_from : str
        Unit to which to convert.
    material : str
        Name of the material on which the value is based.

    Returns
    -------
    float
        Loading converted as requested.

    Raises
    ------
    ``ParameterError``
        If the mode selected is not an option.

    """
    if basis_from != basis_to:

        if basis_to not in _MATERIAL_MODE:
            raise ParameterError(
                f"Basis selected for adsorbent ({basis_to}) is not an option. "
                f"Viable bases are {list(_MATERIAL_MODE)}"
            )

        if not unit_to or not unit_from:
            raise ParameterError("Specify both from and to units")

        if unit_to not in _MATERIAL_MODE[basis_to]:
            raise ParameterError(
                f"Unit selected for adsorbent unit_to ({unit_to}) is not an option. "
                f"Viable units are {list(_MATERIAL_MODE[unit_to])}"
            )

        if unit_from not in _MATERIAL_MODE[basis_from]:
            raise ParameterError(
                f"Unit selected for adsorbent unit_from ({unit_from}) is not an option. "
                f"Viable units are {list(_MATERIAL_MODE[basis_from])}"
            )

        if basis_from == 'mass':
            if basis_to == 'volume':
                constant = material.get_prop('density')
                sign = -1
            elif basis_to == 'molar':
                constant = material.get_prop('molar_mass')
                sign = -1
        elif basis_from == 'volume':
            if basis_to == 'mass':
                constant = material.get_prop('density')
                sign = 1
            elif basis_to == 'molar':
                constant = material.get_prop('density') / material.get_prop(
                    'molar_mass'
                )
                sign = -1
        elif basis_from == 'molar':
            if basis_to == 'mass':
                constant = material.get_prop('molar_mass')
                sign = 1
            elif basis_to == 'volume':
                constant = material.get_prop('density') / material.get_prop(
                    'molar_mass'
                )
                sign = -1

        return value / _MATERIAL_MODE[basis_from][unit_from] \
            / constant ** sign \
            * _MATERIAL_MODE[basis_to][unit_to]

    elif unit_to and unit_from != unit_to:
        return c_unit(
            _MATERIAL_MODE[basis_from], value, unit_from, unit_to, sign=-1
        )

    return value