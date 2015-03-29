# -*- coding: utf-8 -*-
import json
'''
    重写Table提供给前端控件的json数据格式，依不同的数据类型，封装所需数据。
'''
from widget import Table
from collections import OrderedDict


class OurTable(Table):
    total_page = 10
    total_num = 100

    def get_rows(self):
        rows = []
        tmpl = OrderedDict(self.columns + self.visible_columns)
        for line in self.rows:
            oneline = []
            item = dict(zip(tmpl.keys(), line))
            for key, _v in self.visible_columns:
                oneline.append(item[key])
            for key, _v in self.columns:
                oneline.append(item[key])
            rows.append(oneline)
        res = {
               'iTotalDisplayRecords': self.total,
               'iTotalRecords':self.total,
               'aaData': rows
               }
        return json.dumps(res)
    
    def get_columns(self):
        #[{"bVisible": true, "sTitle": "ID", "bSortable": false}, {"bVisible": true, "sTitle": "\u540d\u79f0", "bSortable": false}, {"bVisible": true, "sTitle": "\u72b6\u6001", "bSortable": false}, {"bVisible": true, "sTitle": "\u8bf4\u660e", "bSortable": false}, {"bVisible": true, "sTitle": "\u4ef7\u683c", "bSortable": false}, {"bVisible": true, "sTitle": "\u64cd\u4f5c", "bSortable": false}],
        res = []
        for c in self.visible_columns:
            res.append({"bVisible": False, "sTitle": c[0], "bSortable": False, 'sTitle': c[1]})
        for c in self.columns:
            res.append({"bVisible": True, "sTitle": c[0], "bSortable": False, 'sTitle': c[1]})
        return json.dumps(res)