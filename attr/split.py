import os
import random


def _sorted(x):
    return int(x[0][:-4].split('_')[-1])


def train_val_split(name_list, train_ratio=0.8, sort_func=None):
    assert isinstance(name_list, (list, tuple))
    random.shuffle(name_list)
    train_end = int(len(name_list) * train_ratio)
    train_name_list = name_list[:train_end]
    val_name_list = name_list[train_end:]
    if sort_func is not None:
        train_name_list = sorted(train_name_list, key=_sorted)
        val_name_list = sorted(val_name_list, key=_sorted)
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
        name_list, 0.8, train_file, val_file, tmode, vmode, _sorted
    )


if __name__ == '__main__':
    main()
