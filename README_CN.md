# CAP_FAIRY
*cap* 名字是`Chinese address parser`的意思，`CAP_FAIRY`大意就是，磨人的小妖精。 [英文文档](README.md)

# 介绍
中文地址解析，在`python`第三方包或库中没找到一个好用，并且能解决复杂文本及自动修正地址的库，找到的基本上是用`nodejs`实现的识别，但不能自动添加修正，所以参考相关开源项目，自己实现了一个。

## 安装
目前没有推送`pip`仓库，需要自行使用`python setuptools`进行源码安装。
安装命令：
```shell
python setup.py install
```

## 数据解析
实际数据解析，这里采用的是故宫地址。支持解析：“北京市东城区景山前街4号 故宫博物院010-1008611”等多种文本格式，常见的比如快递地址，收件人信息等。
```python
# example.py
from cap_fairy.parser import Parser
from loguru import logger

if __name__ == '__main__':
    address = Parser(logger=logger).parse("北京市东城区景山前街4号 故宫博物院")
    print(address)
```

运行样例脚本:
```shell
python example.py
```

结果如下:
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

## 自动修正数据
所有数据来源与 http://www.mca.gov.cn/article/sj/xzqh/ ，如果发现数据不是最新，请自行更新`data.py`数据。
由于数据每年都有变化，需要应对新的变化就需要对旧的数据进行识别，`cap_fairy.parser.Parser`类，提供了（`fix_areas`, `fix_citys`, `fix_provinces`）三个属性，它们都是`List[Dict]`类型，在未识别出相关数据时自动尝试修复，修复失败时会根据提供的数据进行修正。
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
## 测试
目前程序测试样本12W条地址数据，基本满足预期要求。

## 其他
如发现新的bug，或者畸形的文本无法解析时请在`[ISSUE](https://github.com/7ym0n/cap_fairy/issues)`中反馈，或提交`pr`。
