import os
import random


def self_sorted(x):
    """
    提供给排序函数`sorted`的基础函数
    Example:
    >>>> a = [('1.jpg', '1.json'), ('10.jpg', '10.json'), ('2.jpg', '2.json')]
    >>>> a = sorted(a, key=self_sorted) # a = [('1.jpg', '1.json'), ('2.jpg', '2.json'), ('10.jpg', '10.json')] # noqa 501
    """

    return int(x[0][:-4].split('_')[-1])


def train_val_split(name_list, train_ratio=0.8, sort_func=None):
    """
    根据给定的`list`按照给定的`ratio`进行划分
    - `name_list`：带划分列表
    - `train_ratio`：训练集占的比例
    - `sort_func`: 对文件名排序时传入`sorted`的函数
    """
    assert isinstance(name_list, (list, tuple))
    random.shuffle(name_list)
    train_end = int(len(name_list) * train_ratio)
    train_name_list = name_list[:train_end]
    val_name_list = name_list[train_end:]
    if sort_func is not None:
        train_name_list = sorted(train_name_list, key=self_sorted)
        val_name_list = sorted(val_name_list, key=self_sorted)
    return train_name_list, val_name_list


def write(contents, f_path, f_mode, line_split_tag):
    assert f_mode in ('w', 'w+', 'a', 'a+')
    with open(f_path, f_mode) as f:
        for line in contents:
            if isinstance(line, (list, tuple)):
                line = f'{line_split_tag}'.join(line)
            f.writelines(f'{line}\n')
            f.flush()
    return


def train_val_split_write(
        name_list, train_ratio, train_file, val_file,
        tmode='w', vmode='w', line_split_tag='\t',
        sort_func=None,
):
    """
    根据给定的`list`按照给定的`ratio`进行划分，**并分别写入到对应的文件中**

    - `name_list`: 待划分列表
    - `train_ratio`：训练集占的比例
    - `train_file`：将划分的训练集内容写入的文件名
    - `val_file`: 将划分的验证集内容写入文件名
    - `tmode`: 训练集文件写入模式, `('w', 'w+', 'a', 'a+')`
    - `vmode`: 验证集文件写入模式，`('w', 'w+', 'a', 'a+')`
    - `line_split_tag`: 如果每一行内容是由`list`组成的，用此符号进行分隔
    - `sort_func`: 对文件名进行排序时传入`sorted`的函数
    Example:
    >>>> def _sort(x):
    >>>>    return int(x[0][:-4])
    >>>> name_list = [
    >>>>    ['1.jpg', '1.json'],
    >>>>    ['2.jpg', '2.json'],
    >>>> ]
    >>>> train_f = 'train.txt'
    >>>> val_f = 'val.txt'
    >>>> mode='w'
    >>>> train_ratio=0.5
    >>>> train_val_split_write(name_list, train_ratio, train_f, val_f, mode, mode, sort_func=_sort)

    """
    train_names, val_names = \
        train_val_split(name_list, train_ratio=train_ratio, sort_func=sort_func)
    write(train_names, train_file, tmode, line_split_tag=line_split_tag)
    write(val_names, val_file, vmode, line_split_tag=line_split_tag)
    return


def main():
    src_img_path = r'./20211222/JPEGImages'
    src_ann_path = r'./20211222/json'
    train_file = './20211222/train_names.txt'
    tmode = 'w'
    val_file = './20211222/val_names.txt'
    vmode = 'w'

    def match(name):
        return name[:-5]

    name_list = []
    for name in os.listdir(src_ann_path):
        assert os.path.exists(os.path.join(src_img_path, match(name)))
        name_list.append([
            os.path.join(src_img_path, match(name)),
            os.path.join(src_ann_path, name)
        ])

    train_val_split_write(
        name_list, 0.8, train_file, val_file, tmode, vmode, self_sorted
    )


if __name__ == '__main__':
    main()
