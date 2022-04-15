# -*- coding: utf-8 -*-
# Copyright 2007-2022 The HyperSpy developers
#
# This file is part of HyperSpy.
#
# HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpy. If not, see <https://www.gnu.org/licenses/#GPL>.

import numpy as np
import pytest

from hyperspy import signals
from hyperspy.misc.utils import (
    is_hyperspy_signal,
    parse_quantity,
    slugify,
    strlist2enumeration,
    str2num,
    swapelem,
    fsdict,
    closest_power_of_two,
    shorten_name,
    is_binned,
)
from hyperspy.exceptions import VisibleDeprecationWarning


def test_slugify():
    assert slugify("a") == "a"
    assert slugify("1a") == "1a"
    assert slugify("1") == "1"
    assert slugify("a a") == "a_a"
    assert slugify(42) == "42"
    assert slugify(3.14159) == "314159"
    assert slugify("├── Node1") == "Node1"

    assert slugify("a", valid_variable_name=True) == "a"
    assert slugify("1a", valid_variable_name=True) == "Number_1a"
    assert slugify("1", valid_variable_name=True) == "Number_1"

    assert slugify("a", valid_variable_name=False) == "a"
    assert slugify("1a", valid_variable_name=False) == "1a"
    assert slugify("1", valid_variable_name=False) == "1"


def test_parse_quantity():
    # From the metadata specification, the quantity is defined as
    # "name (units)" without backets in the name of the quantity
    assert parse_quantity("a (b)") == ("a", "b")
    assert parse_quantity("a (b/(c))") == ("a", "b/(c)")
    assert parse_quantity("a (c) (b/(c))") == ("a (c)", "b/(c)")
    assert parse_quantity("a [b]") == ("a [b]", "")
    assert parse_quantity("a [b]", opening="[", closing="]") == ("a", "b")


def test_is_hyperspy_signal():
    s = signals.Signal1D(np.zeros((5, 5, 5)))
    p = object()
    assert is_hyperspy_signal(s) is True
    assert is_hyperspy_signal(p) is False


def test_strlist2enumeration():
    assert strlist2enumeration([]) == ""
    assert strlist2enumeration("a") == "a"
    assert strlist2enumeration(["a"]) == "a"
    assert strlist2enumeration(["a", "b"]) == "a and b"
    assert strlist2enumeration(["a", "b", "c"]) == "a, b and c"


def test_str2num():
    assert (
        str2num("2.17\t 3.14\t 42\n 1\t 2\t 3")
        == np.array([[2.17, 3.14, 42.0], [1.0, 2.0, 3.0]])
    ).all()


def test_swapelem():
    L = ["a", "b", "c"]
    swapelem(L, 1, 2)
    assert L == ["a", "c", "b"]


def test_fsdict():
    parrot = {}
    fsdict(
        ["This", "is", "a", "dead", "parrot"], "It has gone to meet its maker", parrot
    )
    fsdict(["This", "parrot", "is", "no", "more"], "It is an ex parrot", parrot)
    fsdict(
        ["This", "parrot", "has", "seized", "to", "be"],
        "It is pushing up the daisies",
        parrot,
    )
    fsdict([""], "I recognize a dead parrot when I see one", parrot)
    assert (
        parrot["This"]["is"]["a"]["dead"]["parrot"] == "It has gone to meet its maker"
    )
    assert parrot["This"]["parrot"]["is"]["no"]["more"] == "It is an ex parrot"
    assert (
        parrot["This"]["parrot"]["has"]["seized"]["to"]["be"]
        == "It is pushing up the daisies"
    )
    assert parrot[""] == "I recognize a dead parrot when I see one"


def test_closest_power_of_two():
    assert closest_power_of_two(5) == 8
    assert closest_power_of_two(13) == 16
    assert closest_power_of_two(120) == 128
    assert closest_power_of_two(973) == 1024


def test_shorten_name():
    assert (
        shorten_name("And now for soemthing completely different.", 16)
        == "And now for so.."
    )


# Can be removed in v2.0:
def test_is_binned():
    s = signals.Signal1D(np.zeros((5, 5)))
    assert is_binned(s) == s.axes_manager[-1].is_binned
    with pytest.warns(VisibleDeprecationWarning, match="Use of the `binned`"):
        s.metadata.set_item("Signal.binned", True)
    assert is_binned(s) == s.metadata.Signal.binned
