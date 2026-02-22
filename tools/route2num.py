import json

# 原始线路数据
subway_data = {
  "line_环": {
    "line_name": "环线-Loop Line",
    "layout": "two_line",
    "type": "loop",
    "carriage_count": 4,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "terminal_station": "",
        "stations": ["三清观", "乔家沟", "学府南路", "莲花东", "文家湾", "福利院", "莲花村西", "〇八一路口", "育才北路", "东坝", "石器路", "东安路", "八二一中学", "何家沟", "水柜村", "百草园东", "梁家沟", "李家沟"]
      },
      {
        "service_name": "route2",
        "group": "1",
        "terminal_station": "李家沟",
        "stations": ["三清观", "乔家沟", "学府南路", "莲花东", "文家湾", "福利院", "莲花村西", "〇八一路口", "育才北路", "东坝", "石器路", "东安路", "八二一中学", "何家沟", "水柜村", "百草园东", "梁家沟", "李家沟"]
      }
    ],
    "detail_style": "default",
    "run_style": "detail"
  },
  "line_1": {
    "line_name": "1号线-Line 1",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 4,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["泡石", "权家岭", "袁家口", "雪峰", "奥体中心", "五洲", "德缘路", "利州东路", "沙壕巷", "东城学校", "电子路", "广元中学", "〇八一路口", "莲花村", "解家沟", "长胜路", "乔家沟", "朱家沟", "泉水湾", "田坝子", "田湾", "千佛村", "张家湾", "蜀门北路", "栖凤路"]
      },
      {
        "service_name": "route2",
        "stations": ["泡石", "权家岭", "袁家口", "雪峰", "奥体中心", "五洲", "德缘路", "利州东路", "沙壕巷", "东城学校", "电子路", "广元中学", "〇八一路口", "莲花村", "解家沟", "长胜路", "乔家沟"]
      }
    ]
  },
  "line_2": {
    "line_name": "2号线-Line 2",
    "type": "linear",
    "run_style": "detail",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 6,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["园包岭", "缠龙", "曹家河", "李家湾", "快乐社区", "外国语学校", "滨河路", "奥体大桥", "芸香", "口袋公园", "妇幼保健院", "御锦湾", "市一医院", "教育考试院", "莒国广场", "石马坝北", "南河坝", "体育场", "南河客运站", "利州西路", "中心医院", "凤凰山公园", "北街小学", "蜀门北路", "黄家沟", "莲花池", "莲花东", "天立国际", "千佛崖"]
      },
      {
        "service_name": "route2",
        "stations": ["李家湾", "快乐社区", "外国语学校", "滨河路", "奥体大桥", "芸香", "口袋公园", "妇幼保健院", "御锦湾", "市一医院", "教育考试院", "莒国广场", "石马坝北", "南河坝", "体育场", "南河客运站", "利州西路", "中心医院", "凤凰山公园", "北街小学"]
      }
    ]
  },
  "line_4": {
    "line_name": "4号线-Line 4",
    "type": "linear",
    "run_style": "detail",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 6,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["焦家沟", "袁家口", "春华路", "八二一中学", "德缘路", "妇幼保健院", "莲花路北", "育才路", "城监支队", "博文街", "广元中学", "新民东街", "新民西街", "广元东站", "栖凤小学", "凤凰山公园", "嘉陵广场", "皇泽大桥", "火车站", "皇泽寺", "五佛寺", "下西坝", "盘龙", "盘龙机场", "宝轮", "鸭浮岩", "昭化中学", "白龙湾", "昭化汽车站"]
      },
      {
        "service_name": "route2",
        "stations": ["焦家沟", "袁家口", "春华路", "八二一中学", "德缘路", "妇幼保健院", "莲花路北", "育才路", "城监支队", "博文街", "广元中学", "新民东街", "新民西街", "广元东站", "栖凤小学", "凤凰山公园", "嘉陵广场", "皇泽大桥", "火车站", "皇泽寺", "五佛寺", "下西坝", "盘龙", "盘龙机场", "宝轮"]
      }
    ]
  },
  "line_5": {
    "line_name": "5号线-Line 5",
    "type": "linear",
    "run_style": "detail",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 6,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["徐家湾", "川北幼专东", "红星公园", "快乐社区", "高家山", "米仓东路", "剑门路", "胤国路", "鼓城北路", "万达中学北", "万源医院", "湿地公园", "南石器路", "绵谷路", "莲花路南", "滨河北路", "教育考试院", "东城学校", "东坝", "环城北路", "〇八一路口", "天龙寺", "广元东站", "瞻凤路", "市中医院", "北街小学", "蜀门北路", "烟波街", "火车站", "上西坝"]
      },
      {
        "service_name": "route2",
        "stations": ["剑门路", "胤国路", "鼓城北路", "万达中学北", "万源医院", "湿地公园", "南石器路", "绵谷路", "莲花路南", "滨河北路", "教育考试院", "东城学校", "东坝", "环城北路", "〇八一路口", "天龙寺", "广元东站", "瞻凤路", "市中医院", "北街小学", "蜀门北路", "烟波街", "火车站", "上西坝"]
      }
    ]
  },
  "line_6": {
    "line_name": "6号线-Line 6",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 6,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["昭化火车站", "水电路", "希望城", "宝轮", "盘龙机场", "盘龙", "姚家梁", "中心医院", "琴台广场", "水上公园", "莒国广场", "滨河北路", "育才路", "市一医院", "博物馆", "利州东路", "菌种场", "孙沟路", "树德小学", "科技大道", "李家沟", "乔家沟", "朱家沟", "泉水湾", "田坝子", "田湾", "千佛村"]
      },
      {
        "service_name": "route2",
        "stations": ["昭化火车站", "水电路", "希望城", "宝轮", "盘龙机场", "盘龙", "姚家梁", "中心医院", "琴台广场", "水上公园", "莒国广场", "滨河北路", "育才路", "市一医院", "博物馆", "利州东路", "菌种场", "孙沟路", "树德小学", "科技大道", "李家沟"]
      }
    ]
  },
  "line_8": {
    "line_name": "8号线-Line 8",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 4,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["下西村", "下西小学", "会展中心·商贸城", "四号桥", "接官亭", "蜀门南路南", "广州路", "石马坝南", "老鹰嘴大桥", "滨河南路", "利州中学", "凤台", "南河广场", "南河客运站", "南河客运站西", "天成广场", "蜀门大桥", "市二医院", "琴台广场", "人民路", "电子路", "东坝", "五桂街", "御锦湾", "如意湖", "马家坝", "剑门路", "万龙路", "鼓城南路", "万里", "万达中学南", "万缘"]
      },
      {
        "service_name": "route2",
        "stations": ["南河客运站", "南河客运站西", "天成广场", "蜀门大桥", "市二医院", "琴台广场", "人民路", "电子路", "东坝", "五桂街", "御锦湾", "如意湖", "马家坝", "剑门路"]
      }
    ]
  },
  "line_剑阁": {
    "line_name": "剑阁线-Line Jian'ge",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 2,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["剑门关站", "沙溪", "剑门大道", "张家沟", "石羊", "赤化", "石桥", "宝轮"]
      }
    ]
  },
  "line_元坝": {
    "line_name": "元坝线-Line Yuanba",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 2,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["李家湾", "大石", "荣山", "元坝"]
      }
    ]
  },
  "line_朝天": {
    "line_name": "朝天线-Line Chaotian",
    "type": "linear",
    "run_style": "default",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 2,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["千佛村", "沙河", "朝天客运站"]
      }
    ]
  },
  "line_快": {
    "line_name": "快线-Express",
    "type": "linear",
    "run_style": "detail",
    "layout": "one_line",
    "detail_style": "default",
    "carriage_count": 6,
    "station_spacing_multiplier": 1,
    "services": [
      {
        "service_name": "route1",
        "stations": ["盘龙机场", "火车站", "烟波街", "北街小学", "南河客运站", "莒国广场", "妇幼保健院", "快乐社区"]
      }
    ]
  }
}

# 线路标识映射（关键：确保线路简称准确）
line_code_mapping = {
    "line_环": "环",
    "line_1": "01",
    "line_2": "02",
    "line_4": "04",
    "line_5": "05",
    "line_6": "06",
    "line_8": "08",
    "line_剑阁": "剑阁",
    "line_元坝": "元坝",
    "line_朝天": "朝天",
    "line_快": "快"
}

# 初始化站点编号字典
station_number_map = {}

# 遍历每条线路，生成站点编号
for line_key, line_info in subway_data.items():
    line_code = line_code_mapping[line_key]
    # 取route1的站点列表（完整线路）
    full_stations = line_info["services"][0]["stations"]
    
    # 为每个站点生成顺序编号（两位数，补0）
    for idx, station_name in enumerate(full_stations, 1):
        station_num = f"{idx:02d}"  # 格式化为两位数，如1→01，11→11
        
        # 初始化站点列表（若不存在）
        if station_name not in station_number_map:
            station_number_map[station_name] = []
        
        # 避免同一线路重复添加（防止route2重复）
        exists = False
        for item in station_number_map[station_name]:
            if item[0] == line_code:
                exists = True
                break
        if not exists:
            station_number_map[station_name].append([line_code, station_num])

# 按站名排序（可选，提升可读性）
station_number_map = dict(sorted(station_number_map.items()))

# 输出带缩进的JSON格式结果
with open("res.json", "w") as f:
    json.dump(station_number_map, f, ensure_ascii=False, indent=2)