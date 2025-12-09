import json
import os

class RouteTools:
    """
    地铁线路工具类，用于处理线路和站台数据
    """
    
    def __init__(self, route_file_path=None, station_file_path=None, trans_file_path=None, color_file_path=None):
        """
        初始化工具类
        
        Args:
            route_file_path: 线路数据文件路径，默认为data/route.json
            station_file_path: 站台数据文件路径，默认为data/station.json
            trans_file_path: 站点英文名映射文件路径，默认为data/trans_name.json
            color_file_path: 线路主题色文件路径，默认为data/color.json
        """
        if route_file_path is None:
            route_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'route.json')
        if station_file_path is None:
            station_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'station.json')
        if trans_file_path is None:
            trans_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'trans_name.json')
        if color_file_path is None:
            color_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'color.json')
        
        self.route_file_path = route_file_path
        self.station_file_path = station_file_path
        self.trans_file_path = trans_file_path
        self.color_file_path = color_file_path
        self.route_data = None
        self.station_data = None
        self.trans_data = None
        self.color_data = None
        
        self._load_data()
    
    def _load_data(self):
        """加载线路、站台、英文名与主题色数据"""
        try:
            with open(self.route_file_path, 'r', encoding='utf-8') as f:
                self.route_data = json.load(f)
            
            with open(self.station_file_path, 'r', encoding='utf-8') as f:
                self.station_data = json.load(f)
            
            # 加载英文名映射
            if os.path.exists(self.trans_file_path):
                with open(self.trans_file_path, 'r', encoding='utf-8') as f:
                    self.trans_data = json.load(f)
            else:
                self.trans_data = {}
            
            # 加载线路主题色
            if os.path.exists(self.color_file_path):
                with open(self.color_file_path, 'r', encoding='utf-8') as f:
                    self.color_data = json.load(f)
            else:
                self.color_data = {}
        except FileNotFoundError as e:
            raise FileNotFoundError(f"数据文件未找到: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"数据文件格式错误: {e}")
    
    def get_station_info(self, line_name, route_name):
        """
        获取指定线路和路线的站台信息
        
        Args:
            line_name: 线路名称，如 "line1", "line2"
            route_name: 路线名称，如 "route1", "route2"
            
        Returns:
            list: 包含字典的列表，每个字典格式为 {"station_name": str, "station_index": list}
            
        Raises:
            ValueError: 当线路或路线不存在时
        """
        if self.route_data is None or self.station_data is None:
            self._load_data()
        
        # 检查线路是否存在
        if line_name not in self.route_data:
            raise ValueError(f"线路 '{line_name}' 不存在")
        
        line_info = self.route_data[line_name]
        
        # 查找对应的路线
        route_found = None
        for service in line_info.get('services', []):
            # 处理不同的路线名称字段
            if 'type' in service and service['type'] == route_name:
                route_found = service
                break
            elif 'service_name' in service and service['service_name'] == route_name:
                route_found = service
                break
        
        if route_found is None:
            raise ValueError(f"路线 '{route_name}' 在线路 '{line_name}' 中不存在")
        
        # 获取站台列表
        stations = route_found.get('stations', [])
        
        # 构建结果列表
        result = []
        for station_name in stations:
            # 获取站台索引信息
            station_index = self.station_data.get(station_name, [])
            result.append({
                "station_name": station_name,
                "station_index": station_index
            })
        
        return result
    
    def get_all_lines(self):
        """获取所有线路名称"""
        if self.route_data is None:
            self._load_data()
        return list(self.route_data.keys())
    
    def get_routes_for_line(self, line_name):
        """获取指定线路的所有路线名称"""
        if self.route_data is None:
            self._load_data()
        
        if line_name not in self.route_data:
            raise ValueError(f"线路 '{line_name}' 不存在")
        
        line_info = self.route_data[line_name]
        routes = []
        for service in line_info.get('services', []):
            if 'type' in service:
                routes.append(service['type'])
            elif 'service_name' in service:
                routes.append(service['service_name'])
        
        return routes
    
    def get_line_display_name(self, line_key):
        """获取线路显示名称，比如 'line_5' -> '5号线'"""
        if self.route_data is None:
            self._load_data()
        info = self.route_data.get(line_key, {})
        full_name = info.get('line_name', line_key)
        if '-' in full_name:
            return full_name.split('-')[0]
        return full_name

    def get_line_en_name(self, line_key):
        """获取线路英文名称"""
        if self.route_data is None:
            self._load_data()
        info = self.route_data.get(line_key, {})
        full_name = info.get('line_name', line_key)
        if '-' in full_name:
            return full_name.split('-')[1]
        
        # 默认回退逻辑
        if line_key.startswith('line_'):
            part = line_key[5:]
            if part.isdigit():
                return f"Line {part}"
            return f"Line {part}"
        return line_key
    
    def _line_code_from_key(self, line_key):
        """从'line_5'或'line_S3'解析出站点索引里的线路代码（数字两位、字母数字原样）"""
        try:
            part = line_key.split('_')[1]
        except Exception:
            return ''
        s = str(part).strip()
        if s.isdigit():
            return f"{int(s):02d}"
        else:
            return s
    
    def get_station_en_name(self, station_name):
        """获取站点英文名，如果不存在，返回原名"""
        if self.trans_data is None:
            self._load_data()
        return self.trans_data.get(station_name, station_name)
    
    def get_transfer_lines(self, station_name):
        """返回站点涉及的线路代码列表，例如 ['05','06']"""
        if self.station_data is None:
            self._load_data()
        entries = self.station_data.get(station_name, [])
        lines = []
        for item in entries:
            if isinstance(item, list) and len(item) >= 1:
                lines.append(item[0])
        return sorted(list(set(lines)))
    
    def get_line_map_info(self, line_name, route_name):
        """
        获取用于线路图展示的站点信息（含英文名与换乘标识）
        返回: [{'station_name','station_name_en','station_index','is_transfer','transfer_lines','transfer_count_excl_current','transfer_badges'}]
        transfer_badges: [{'code': '4', 'color': '#XXXXXX'}]
        """
        if self.route_data is None or self.station_data is None:
            self._load_data()
        
        # 复用已有逻辑获取站序
        base_list = self.get_station_info(line_name, route_name)
        current_code = self._line_code_from_key(line_name)
        enriched = []
        for item in base_list:
            name = item['station_name']
            en = self.get_station_en_name(name)
            transfer_lines = self.get_transfer_lines(name)
            is_transfer = len(transfer_lines) > 1
            # 提取当前线路的索引号
            station_index = None
            for idx in item['station_index']:
                if isinstance(idx, list) and len(idx) >= 2 and idx[0] == current_code:
                    station_index = idx[1]
                    break
            transfer_count_excl_current = len([c for c in transfer_lines if c != current_code])
            # 构造换乘徽章（编号与颜色），排除当前线路
            badges = []
            for code in transfer_lines:
                if code == current_code:
                    continue
                code_str = str(code).strip()
                if code_str.isdigit():
                    line_key = f"line_{int(code_str)}"
                    code_disp = str(int(code_str))
                else:
                    line_key = f"line_{code_str}"
                    code_disp = code_str
                badges.append({
                    'code': code_disp,
                    'color': self.get_line_color(line_key)
                })
            enriched.append({
                'station_name': name,
                'station_name_en': en,
                'station_index': station_index,
                'is_transfer': is_transfer,
                'transfer_lines': transfer_lines,
                'transfer_count_excl_current': transfer_count_excl_current,
                'transfer_badges': badges
            })
        return enriched
    
    def get_terminal_station(self, line_name, route_name):
        """获取终点站（线性：列表末尾；环线：优先使用terminal_station字段）"""
        if self.route_data is None:
            self._load_data()
        line_info = self.route_data.get(line_name, {})
        target = None
        for service in line_info.get('services', []):
            if service.get('type') == route_name or service.get('service_name') == route_name:
                target = service
                break
        if not target:
            raise ValueError(f"路线 '{route_name}' 在线路 '{line_name}' 中不存在")
        if 'terminal_station' in target and target['terminal_station']:
            return target['terminal_station']
        stations = target.get('stations', [])
        return stations[-1] if stations else None
    
    def get_next_station(self, line_name, route_name, current_station):
        """获取下一站名称"""
        if self.route_data is None:
            self._load_data()
        line_info = self.route_data.get(line_name, {})
        target = None
        for service in line_info.get('services', []):
            if service.get('type') == route_name or service.get('service_name') == route_name:
                target = service
                break
        if not target:
            raise ValueError(f"路线 '{route_name}' 在线路 '{line_name}' 中不存在")
        stations = target.get('stations', [])
        for i, name in enumerate(stations):
            if name == current_station:
                if i + 1 < len(stations):
                    return stations[i+1]
                else:
                    return None
        return None
    
    def get_line_color(self, line_key):
        """根据'line_5'返回主题色，默认'#9b5de5'"""
        if self.color_data is None:
            self._load_data()
        # 优先data文件，其次route.json里可能存在主题色字段
        color = None
        if isinstance(self.color_data, dict):
            color = self.color_data.get(line_key)
        if not color:
            info = self.route_data.get(line_key, {}) if self.route_data else {}
            color = info.get('color')
        return color or '#9b5de5'
    
    def get_line_color_by_code(self, code):
        """根据线路代码返回主题色，支持数字与字母数字（如 S3）"""
        code_str = str(code).strip()
        if code_str.isdigit():
            key = f"line_{int(code_str)}"
        else:
            key = f"line_{code_str}"
        return self.get_line_color(key)