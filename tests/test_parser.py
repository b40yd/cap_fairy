#
# Copyright (C) 2021, 7ym0n.q6e
#
# Author: 7ym0n.q6e <bb.qnyd@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import logging

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from cap_fairy.parser import Parser

log = logging.getLogger(__name__)


def test_parser():
    address = Parser().parse("北京市海淀区西二旗后厂村010-1008611中国移动")
    log.debug(address)
    assert address["province_code"] == "110000"
    assert address["city_code"] == "110100"
    assert address["area_code"] == "110108"


def test_parser2():
    address = Parser().parse("海淀区西二旗后厂村010-1008611中国移动")
    assert (address["province_code"] == "110000"
            and address["city_code"] == "110100"
            and address["area_code"] == "110108")


def test_parser3():
    address = Parser().parse(" 010-1008611中国移动 北京市海淀区西二旗后厂村")
    assert address["province_code"] == "110000"
    assert address["city_code"] == "110100"
    assert address["area_code"] == "110108"


def test_parser4():
    address = Parser().parse("中国移动010-1008611 北京市海淀区西二旗后厂村")
    assert address["province_code"] == "110000"
    assert address["city_code"] == "110100"
    assert address["area_code"] == "110108"


def test_parser5():
    address = Parser().parse("中国移动010-1008611 海淀区西二旗后厂村")
    assert address["province_code"] == "110000"
    assert address["city_code"] == "110100"
    assert address["area_code"] == "110108"
