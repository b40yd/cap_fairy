# CAP_FAIRY
The *cap* is Chinese address parser.

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

if __name__ == '__main__':
    address = Parser().parse("北京市东城区景山前街4号 故宫博物院")
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
