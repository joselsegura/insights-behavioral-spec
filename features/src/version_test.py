#!/usr/bin/env python3
# vim: set fileencoding=utf-8

# Copyright © 2023  Pavel Tisnovsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Unit tests for functions defined in version.py source file."""

import pytest

from version import check


def test_empty_input():
    """Check how the version check function handles empty input."""
    with pytest.raises(Exception):
        check([])


def test_missing_version():
    """Check how the version check function handles input without version."""
    with pytest.raises(Exception):
        check(["this", "is", "not", "version"])
