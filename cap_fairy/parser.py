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

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import logging
import re

from cap_fairy.data import AREAS, CITYS, PROVINCES

CONST_PROVINCE = 0
CONST_CITY = 1
CONST_AREA = 2


class Parser:
    exclude_keys = [
        "发件人",
        "收货地址",
        "收货人",
        "收件人",
        "收货",
        "手机号码",
        "邮编",
        "电话",
        "所在地区",
        "详细地址",
        "地址",
        "：",
        ":",
        "；",
        ";",
        "，",
        ",",
        "。",
        "、",
    ]

    province_keys = [
        "特别行政区",
        "古自治区",
        "维吾尔自治区",
        "壮族自治区",
        "回族自治区",
        "自治区",
        "省省直辖",
        "省",
        "市",
    ]

    city_keys = [
        "布依族苗族自治州",
        "苗族侗族自治州",
        "藏族羌族自治州",
        "哈尼族彝族自治州",
        "壮族苗族自治州",
        "傣族景颇族自治州",
        "蒙古族藏族自治州",
        "傣族自治州",
        "白族自治州",
        "藏族自治州",
        "彝族自治州",
        "回族自治州",
        "蒙古自治州",
        "朝鲜族自治州",
        "地区",
        "哈萨克自治州",
        "盟",
        "市",
    ]

    area_keys = [
        "满族自治县",
        "满族蒙古族自治县",
        "蒙古族自治县",
        "朝鲜族自治县",
        "回族彝族自治县",
        "彝族回族苗族自治县",
        "彝族苗族自治县",
        "土家族苗族自治县",
        "布依族苗族自治县",
        "苗族布依族自治县",
        "彝族傣族自治县",
        "傣族彝族自治县",
        "仡佬族苗族自治县",
        "黎族苗族自治县",
        "苗族侗族自治县",
        "哈尼族彝族傣族自治县",
        "哈尼族彝族自治县",
        "彝族哈尼族拉祜族自治县",
        "傣族拉祜族佤族自治县",
        "傣族佤族自治县",
        "拉祜族佤族布朗族傣族自治县",
        "苗族瑶族傣族自治县",
        "彝族回族自治县",
        "独龙族怒族自治县",
        "保安族东乡族撒拉族自治县",
        "回族土族自治县",
        "撒拉族自治县",
        "哈萨克自治县",
        "塔吉克自治县",
        "回族自治县",
        "畲族自治县",
        "土家族自治县",
        "布依族自治县",
        "苗族自治县",
        "瑶族自治县",
        "侗族自治县",
        "水族自治县",
        "傈僳族自治县",
        "仫佬族自治县",
        "毛南族自治县",
        "黎族自治县",
        "羌族自治县",
        "彝族自治县",
        "藏族自治县",
        "纳西族自治县",
        "裕固族自治县",
        "哈萨克族自治县",
        "哈尼族自治县",
        "拉祜族自治县",
        "佤族自治县",
        "左旗",
        "右旗",
        "中旗",
        "后旗",
        "联合旗",
        "自治旗",
        "旗",
        "自治县",
        "街道办事处",
        "新区",
        "区",
        "县",
        "市",
    ]

    reg: dict = {
        "mobile":
        re.compile("(86-[1][0-9]{10})|(86[1][0-9]{10})|([1][0-9]{10})"),
        "phone":
        re.compile(
            "(([0-9]{3,4}-)[0-9]{7,8})|([0-9]{12})|([0-9]{11})|([0-9]{10})|([0-9]{9})|([0-9]{8})|([0-9]{7})"
        ),
        "zip_code":
        re.compile("([0-9]{6})"),
    }
    # cache province short.
    # e.g: 北京市, 北京
    _province_short: dict = {}
    _city_short: dict = {}
    _area_short: dict = {}

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        for code in PROVINCES:
            province = PROVINCES[code]
            self._province_short[code] = self._get_short(
                self.province_keys, province)

        for code in CITYS:
            self._city_short[code] = self._get_short(self.city_keys,
                                                     CITYS[code])

        for code in AREAS:
            area = AREAS[code]
            if "雨花台区" == area:
                area = "雨花区"
            if "神农架林区" == area:
                area = "神农架"

            if len(area) > 2 and "高新区" != area:
                self._area_short[code] = self._get_short(self.area_keys, area)

    def _get_short(self, names: dict, name: str):
        for key in names:
            short_name = name.replace(key, "")
        return short_name

    def parse_by_name(self, short: dict, names: dict, address: str):
        _name = None
        _code = None
        for code in names:
            _name_tmp = names.get(code, None)
            _name_short_tmp = short.get(code, None)

            if _name_tmp == "县":
                continue

            if _name_tmp and address.find(_name_tmp) == 0:
                return code, _name_tmp, address.replace(_name_tmp, "")
            elif _name_short_tmp and address.find(_name_short_tmp) == 0:
                return (
                    code,
                    _name_tmp,
                    address.replace(_name_short_tmp, ""),
                )

        return _code, _name, address

    def parse(self, address: str):
        mobile = None
        phone = None
        zip_code = None
        address = address.replace("\r\n", " ").replace("\n", " ")
        for key in self.exclude_keys:
            address = address.replace(key, " ")

        mobile_match = self.reg["mobile"].search(address)
        if mobile_match:
            mobile = mobile_match.group(0)
            address = address.replace(mobile, " ")

        phone_match = self.reg["phone"].search(address)
        if phone_match:
            phone = phone_match.group(0)
            address = address.replace(phone, " ")

        zip_code_match = self.reg["zip_code"].search(address)
        if zip_code_match:
            zip_code = zip_code_match.group(0)
            address = address.replace(zip_code, "")
        address = re.sub(" {2,}", " ", address)

        # _address = address

        def parse_name(address: str):
            lst = address.split(" ")
            name = ""
            name_index = 0
            if 1 < len(lst):
                index = 0

                for v in lst:
                    if name and len(name) < len(v):
                        break
                    else:
                        if name and len(name) > len(v):
                            name = v
                            name_index = index
                            break
                        name = v
                        name_index = index

                    index += 1

                if name:
                    lst.pop(name_index)
                    address = " ".join(lst)

            return address, name

        province_code, province, address = self.parse_province(address)
        city_code, city, address = self.parse_city(address)
        area_code, area, address = self.parse_area(address)

        address, first_name = parse_name(address)
        # print(self.get_name_by_ref(CONST_CITY, province_code, CITYS))

        result = {
            "mobile": mobile,
            "phone": phone,
            "zip_code": zip_code,
            "name": first_name,
            "province": province,
            "province_code": province_code,
            "city": city,
            "city_code": city_code,
            "area": area,
            "area_code": area_code,
            "address": address.strip(),
        }

        return self._fix_address(result)

    def _fix_address(self, result: dict):
        if not result["province_code"] and result["city_code"]:
            province = self.get_name_by_ref(CONST_PROVINCE,
                                            result["city_code"], PROVINCES)
            if province:
                (result["province"], ) = province.values()
                (result["province_code"], ) = province.keys()
        if (not result["province_code"] and not result["city_code"]
                and result["area_code"]):
            city = self.get_name_by_ref(CONST_CITY, result["area_code"], CITYS)
            if city:
                (result["city"], ) = city.values()
                (result["city_code"], ) = city.keys()

            province = self.get_name_by_ref(CONST_PROVINCE,
                                            result["area_code"], PROVINCES)

            if province:
                (result["province"], ) = province.values()
                (result["province_code"], ) = province.keys()

        if not result["city_code"] and result["area_code"]:
            city = self.get_name_by_ref(CONST_CITY, result["area_code"], CITYS)
            if city:
                (result["city"], ) = city.values()
                (result["city_code"], ) = city.keys()
        if not result["area_code"]:
            area_code, area, address = self.parse_area(result["address"])
            result["area"] = area
            result["area_code"] = area_code
            result["address"] = address

            for key in self.area_keys:
                if key in result["address"]:
                    result["area"] = key
                    result["area_code"] = key
            self.logger.warning(f"{result} address need fix.")

        return result

    def parse_province(self, address: str):
        province_code, province, address = self.parse_by_name(
            self._province_short, PROVINCES, address)

        for key in self.province_keys:
            if address.find(key) == 0:
                address = address.replace(key, "")

        return province_code, province, address

    def parse_city(self, address: str):
        city_code, city, address = self.parse_by_name(self._city_short, CITYS,
                                                      address)
        for key in self.city_keys:
            if address.find(key) == 0:
                if key not in ["市北区", "市南区", "市中区", "市辖区"]:
                    address = address.replace(key, "")

        return city_code, city, address

    def parse_area(self, address: str):
        area_code, area, address = self.parse_by_name(self._area_short, AREAS,
                                                      address)

        for key in self.area_keys:
            if address.find(key) == 0:
                address = address.replace(key, "")

        return area_code, area, address

    def get_sub_set(self, code, names, zero=""):
        sub_set = {}
        for i in range(1, 100):
            _sub_code = ""
            if i < 10:
                _sub_code = f"0{i}"
            else:
                _sub_code = f"{i}"
            sub_code = f"{code}{_sub_code}{zero}"

            value = names.get(sub_code, None)
            if value:
                sub_set[sub_code] = value
        return sub_set

    def get_name_by_ref(self, flag: int, code: str, names: dict):
        def get_ref(flag, code, names):
            def _get_sub_ref(flag, parent, sub, names):
                if CONST_AREA == flag and sub != "00":
                    _code = f"{parent}{sub}"
                    return self.get_sub_set(_code, names)
                if CONST_CITY == flag:
                    # _code = f"{parent}"
                    _value = names.get(f"{parent}{sub}00", None)
                    if _value:
                        return {f"{parent}{sub}00": _value}
                if CONST_PROVINCE == flag:
                    _value = names.get(f"{parent}0000", None)

                    if _value:
                        return {f"{parent}0000": _value}

            parent = code[0:2]
            sub = code[2:4]
            return _get_sub_ref(flag, parent, sub, names)

        return get_ref(flag, code, names)
