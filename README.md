# CAP_FAIRY
The *cap* is Chinese address parser. [中文文档](README_CN.md)

# Usage
## Install
using python setuptools install the package.

```shell
python setup.py install
```

## Parser
```python
# example.py
from cap_fairy.parser import Parser
from loguru import logger

if __name__ == '__main__':
    address = Parser(logger=logger).parse("北京市东城区景山前街4号 故宫博物院")
    print(address)
```

Run:
```shell
python example.py
```

Results:
```json
{
    'mobile': None,
    'phone': None,
    'zip_code': None,
    'name': '故宫博物院',
    'province': '北京',
    'province_code': '110000',
    'city': '北京市',
    'city_code': '110100',
    'area': '东城区',
    'area_code': '110101',
    'address': '景山前街4号'
}
```

## Auto Fix
All Data from http://www.mca.gov.cn/article/sj/xzqh/
Every year the data, there are changes, you can automatically correct the data for custom changes for the official latest.

The `cap_fairy.parser.Parser` Object has three properties method (`fix_areas`, `fix_citys`, `fix_provinces`) are provided, all of which are list types that automatically attempt to fix when the relevant data is not identified and are corrected based on the data provided when the repair fails.
E.g:
```python
# auto_fix_example.py
from cap_fairy.parser import Parser
from loguru import logger

parser = Parser(logger=logger)

parser.fix_areas = [
    {
        'old_name': '双流县',
        'new_name': '双流区'
    },
    {
        'old_name': '马龙县',
        'new_name': '马龙区',
    }
]

```
