# split

`self_sorted`:

提供给排序函数`sorted`的基础函数

```python
from HAttr import self_sorted

a = [('1.jpg', '1.json'), ('10.jpg', '10.json'), ('2.jpg', '2.json')]

a = sorted(a, key=self_sorted)
# a = [('1.jpg', '1.json'), ('2.jpg', '2.json'), ('10.jpg', '10.json')]
```

---

---

`train_val_split`:

根据给定的`list`按照给定的`ratio`进行划分

- `name_list`：带划分列表
- `train_ratio`：训练集占的比例
- `sort_func`: 对文件名排序时传入`sorted`的函数

---

---

`train_val_split_write`:

根据给定的`list`按照给定的`ratio`进行划分，**并分别写入到对应的文件中**

- `name_list`: 待划分列表
- `train_ratio`：训练集占的比例
- `train_file`：将划分的训练集内容写入的文件名
- `val_file`: 将划分的验证集内容写入文件名
- `tmode`: 训练集文件写入模式, `('w', 'w+', 'a', 'a+')`
- `vmode`: 验证集文件写入模式，`('w', 'w+', 'a', 'a+')`
- `line_split_tag`: 如果每一行内容是由`list`组成的，用此符号进行分隔
- `sort_func`: 对文件名进行排序时传入`sorted`的函数

```python
from HAttr import train_val_split_write


def _sort(x):
    return int(x[0][:-4])


name_list = [
    ['1.jpg', '1.json'],
    ['2.jpg', '2.json'],
]

train_f = 'train.txt'
val_f = 'val.txt'
mode = 'w'
train_ratio = 0.5

train_val_split_write(name_list, train_ratio, train_f, val_f, mode, mode, sort_func=_sort)
```





# parse

`_load`:

读取json文件内容

- `jpath`: json文件路径
- `encoding`: 编码格式

---

---

`_cls_step_parse`:

分类步骤内容解析, 返回 `list(tuple(sourceID, list(attr)), .....)`

- `content`: `labelbee`标注文件中分类对应的`step`的内容
- `skip_version`：返回属性中跳过版本号

```python
from HAttr import cls_step_parse

content = {'toolName': 'tagTool',
           'result': [
               {'id': '49op0v5Q',
                'sourceID': '',
                'result': {
                    'class-1': 'Male',
                    'class-2': 'UpperBodyLongSleeve',
                    'class-3': 'LowerBodyTrousers',
                    'class-4': 'NoHats',
                    'class-5': 'NoMask',
                    'class-6': 'NoMuffler',
                    'class-8': 'OtherShoes',
                    'class-9': 'UpRight',
                    'class-10': 'Front',
                    'class-11': 'NoUpperTrunc',
                    'class-12': 'NoLowerTrunc',
                    'class-13': 'NoOcclusion',
                    'class-14': 'NoSmoke',
                    'class-15': 'NoPhone',
                    'class-16': 'HandHoldNothing',
                    'class-7': 'NoGloves',
                    'class-version': 'v1.1'}}]
           }  # 从labelbee的标注文件中获取的基于分类的step_1的内容
res = cls_step_parse(content, skip_version=True)
"""
[ ('', ['Male', 'UpperBodyLongSleeve', 'LowerBodyTrousers', 'NoHats', 'NoMask', 'NoMuffler', 'OtherShoes', 'UpRight', 'Front', 'NoUpperTrunc', 'NoLowerTrunc', 'NoOcclusion', 'NoSmoke', 'NoPhone', 'HandHoldNothing', 'NoGloves']),
]
"""

res = cls_step_parse(content)
"""
[ ('', ['Male', 'UpperBodyLongSleeve', 'LowerBodyTrousers', 'NoHats', 'NoMask', 'NoMuffler', 'OtherShoes', 'UpRight', 'Front', 'NoUpperTrunc', 'NoLowerTrunc', 'NoOcclusion', 'NoSmoke', 'NoPhone', 'HandHoldNothing', 'NoGloves', 'v1.1']),
]
"""

```

