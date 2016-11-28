# -*- coding: utf-8 -*-

from dashboard import r_kv


def sender(obj, key, value="", meta=None, force=True):
    """
    发送object到存储单元（redis）中，key为对象名，value是序列化对象，如字典
    参数：
    obj: 需要存入redis中的原始对象（未序列化）
    key: 可选，存入redis的key
    value: 可选，存如redis的value
    meta: 可选，redis中key-value的meta信息，字典类型
    force: 可选，如果为True，覆盖已存在的同名key的value
    """
    suffix = '-meta'
    if (key in r_kv or key + suffix in r_kv) and not force:
        print('Collision: key: {}, or {} exists in storage'.format(key, key + suffix))
        return None

    value = value if value else obj.to_json()
    res = r_kv.set(key, value)

    if meta is not None:
        res = r_kv.set(key + suffix, meta)

    return res
