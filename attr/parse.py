import re
import json


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
