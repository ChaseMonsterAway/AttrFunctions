import os
import re


def write_attr_to_file(parse_res, img_prefix, txt):
    """
    :param parse_res: [(img_name, attrs), (img_name, attrs)]
    :param img_prefix: str
    :param txt: file path
    :return:
        prefix/img_name attrs
        prefix/img_name attrs
    """
    with open(txt, 'w', encoding='utf-8') as f:
        for res in parse_res:
            img_name, r = res
            if r and r[0][1]:
                if len(r[0][1]) == 1 and re.match('v[0123456789]+.*', r[0][1][0]):
                    continue
                if len(r[0][1]) == 1 and r[0][1][0] == 'GeneralHumanAttribute':
                    continue
                attrs = ' '.join(r[0][1])
                f.writelines(f'{os.path.join(img_prefix, img_name)} {attrs}\n')
                f.flush()
