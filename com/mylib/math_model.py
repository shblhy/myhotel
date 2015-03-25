#-*- coding:utf-8 -*-
def stat(attrs,datalist,method='avg',nonealowed=True):
    '''
       按属性数组返回统计后的结果字典；最终结果以method为准进行提供。
       依据attrs中的方法进行取值运算，依据method中的方法进行统计运1算
    允许datalist中的None，None不会参与计算。
    '''
    if type(attrs).__name__ == 'list':
        attrs = dict([(attr,lambda x:getattr(x,attr)) for attr in attrs]) 
    res = {}
    for item in datalist:
        if not item:
            if nonealowed:continue
            else:raise Exception('None in data')
        for attr in attrs:
            if not res.has_key(attr):
                res[attr] = []
            res[attr].append(attrs[attr](item))
    try:
        if type(method).__name__ == 'dict':
            if res:
                outputKeys = []
                for key in method:
                    res[key] = get_method(method[key])(res[key] if key in res else res)
                    outputKeys.append(key)
                for key in res.keys():
                    if not key in outputKeys:
                        del res[key]
        else:
            for key in res:
                res[key] = get_method(method)(res[key])
    except Exception,e0:
        print e0
    return res

def get_method(method):
    if method == 'avg': 
        baseFunc = lambda x:sum(x)/len(x)
    elif method == 'sum':
        baseFunc = sum
    elif method ==  'first':
        baseFunc = lambda x:x[0]
    elif type(method).__name__ == 'function':
        baseFunc = method
    return baseFunc

