import re
import json


def _load(jpath, encoding='utf-8'):
    return json.load(open(jpath, 'r', encoding=encoding))


def _one_step_single_parse(content, type='cls'):
    keys = list(content.keys())
    steps = [k for k in keys if 'step' in k]
    src_lists = dict()
    for step in steps:
        label_step = content[step]
        label_res = label_step['result']
        for lres in label_res:
            id = lres['id']
            source_id = lres['sourceID']


def _cls_step_parse(content, skip_version=False):
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
            attrs.extend(value.split(';'))
        parse_res.append(
            (source_id, attrs)
        )
    return parse_res


if __name__ == '__main__':
    jcontents = _load(
        r'H:\dataset\public\human_related\attr\sefl-labeled\20211222\json\20211222_1.jpg.json'
    )
    res = _cls_step_parse(jcontents['step_1'], skip_version=True)
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
