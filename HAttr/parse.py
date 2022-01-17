import json
import os
import re

import cv2
import numpy as np
from tqdm import tqdm


def load(jpath, encoding='utf-8'):
    """
    读取json文件内容

    - `jpath`: json文件路径
    - `encoding`: 编码格式
    """
    return json.load(open(jpath, 'r', encoding=encoding))


def one_step_single_parse(content, type='cls'):
    keys = list(content.keys())
    steps = [k for k in keys if 'step' in k]
    src_lists = dict()
    for step in steps:
        label_step = content[step]
        label_res = label_step['result']
        for lres in label_res:
            id = lres['id']
            source_id = lres['sourceID']


def extract_loc(info: dict):
    x, y, width, height = info['x'], info['y'], info['width'], info['height']
    return int(x), int(y), int(x + width), int(y + height)


def det_parse(content):
    # {"dataSourceStep": 0, "toolName": "rectTool", "result": [
    #     {"x": 106.38058062449784, "y": 3.3889521255943, "width": 359.13664014974256, "height": 401.6110478744057,
    #      "attribute": "person", "valid": true, "id": "eBt0HYeH", "sourceID": "", "textAttribute": "", "order": 1}]}
    total_results = content['result']
    det_res = []
    for result in total_results:
        x1, y1, x2, y2 = extract_loc(result)
        class_attr, valid, cid, source_id = result['attribute'], result['valid'], result['id'], result['sourceID']
        det_res.append(
            dict(
                valid=valid,
                attr=class_attr,
                id=cid,
                source_id=source_id,
                loc=(x1, y1, x2, y2)
            )
        )
    return det_res


def crop_det_img(img, contents, save_dir, save_name=None):
    os.makedirs(save_dir, exist_ok=True)
    if contents is None:
        assert save_name is not None
        cv2.imwrite(os.path.join(save_dir, save_name), img)
    assert isinstance(img, np.ndarray)
    det_res = det_parse(contents)
    name_dict = dict()
    for dres in det_res:
        if dres['valid']:
            save_name = dres['attr'] + '_' + dres['id'] + '.jpg'
            name_dict[dres['id']] = save_name
            x1, y1, x2, y2 = dres['loc']
            cpatch = img[y1:y2, x1:x2, :]
            assert cpatch is not None, f'Current patch is None where x1, y1, x2, y2 are ' \
                                       f'{x1}, {y1}, {x2}, {y2}, image shape are {img.shape}'
            assert not os.path.exists(os.path.join(save_dir, save_name)), \
                f'{os.path.join(save_dir, save_name)} has existed.'
            cv2.imwrite(os.path.join(save_dir, save_name), cpatch)
    return name_dict


def two_step_parse_with_crop(source_img_dir, source_json_dir, save_dir):
    parse_res = []
    for name in tqdm(os.listdir(source_json_dir)):
        img_name = name[:-5]  # remove .json in name
        img_path = os.path.join(source_img_dir, img_name)
        json_path = os.path.join(source_json_dir, name)
        assert os.path.exists(img_path), f"Image '{img_path}' not exists."
        jcontents = load(json_path)
        step1_contents = jcontents.get('step_1', None)

        if step1_contents is None:
            print(f'Step1 is blank in {json_path}, SKIP!')
            continue
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # crop the img based on the detection annotations
        name_dict = crop_det_img(img, step1_contents, save_dir)

        step2_contents = jcontents.get('step_2', None)
        if step2_contents is None:
            import warnings
            warnings.warn(f'Step 2 is None in {json_path}', RuntimeWarning)
            continue
        step2_res = cls_step_parse(step2_contents, skip_version=True)
        for s2res in step2_res:
            assert s2res[0] != ''
            step2_img_name = name_dict[s2res[0]]
            parse_res.append(
                (step2_img_name, s2res[1])
            )
    return parse_res


def cls_step_parse(content, skip_version=False):
    """
    分类步骤内容解析, 返回 `list(tuple(sourceID, list(attr)), .....)`

    - `content`: `labelbee`标注文件中分类对应的`step`的内容
    - `skip_version`：返回属性中跳过版本号
    Example:
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
         } # 从labelbee的标注文件中获取的基于分类的step_1的内容
        res = _cls_step_parse(content, skip_tag=True)
        # [
        #   ('', ['Male', 'UpperBodyLongSleeve', 'LowerBodyTrousers', 'NoHats',
        #          'NoMask', 'NoMuffler', 'OtherShoes', 'UpRight', 'Front',
        #          'NoUpperTrunc', 'NoLowerTrunc', 'NoOcclusion', 'NoSmoke',
        #          'NoPhone', 'HandHoldNothing', 'NoGloves']),
        #]
    """
    results = content['result']
    parse_res = []
    for result in results:
        id = result['id']
        source_id = result['sourceID']
        c_res = result['result']
        attrs = []
        for key, value in c_res.items():
            # skip version type
            if skip_version and re.match('v[0123456789]+.*', value):
                continue
            value = [v.strip() for v in value.split(';')]
            attrs.extend(value)
        parse_res.append(
            (source_id, attrs)
        )
    return parse_res


if __name__ == '__main__':
    jcontents = load(
        r'H:\dataset\public\human_related\attr\sefl-labeled\20211222\json\20211222_1.jpg.json'
    )
    res = cls_step_parse(jcontents['step_1'], skip_version=True)
    a = {'toolName': 'tagTool',
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
         }

    print('done')
