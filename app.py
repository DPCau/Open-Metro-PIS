from flask import Flask, render_template, jsonify, request
import os
import sys
import json

# 将tools目录加入路径以便导入RouteTools
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools'))
try:
    from route_tools import RouteTools
    route_tools_available = True
except ImportError as e:
    print(f"警告: 无法导入RouteTools模块: {e}，将使用数据文件回退")
    route_tools_available = False

# 初始化Flask应用
app = Flask(__name__)

# 配置项
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化RouteTools
tools = None
try:
    if route_tools_available:
        tools = RouteTools()
        print("成功初始化RouteTools")
except Exception as e:
    print(f"初始化RouteTools失败: {e}")

# 模拟当前状态数据
current_state = {
    'line_name': 'line_17',
    'route_name': 'route1',
    'next_station': '二仙桥',
    'direction': 1, # 方向：0与数据文件顺序一致，1为反向（显示反转）
    'door_side': '本侧',  # 本侧或对侧
    'current_time': '22:19',
    'current_carriage': 3
}


@app.route('/')
def index():
    """首页 - 默认显示下一站信息（适配direction与终点展示）"""
    # 主题色
    line_color = None
    try:
        if tools is not None:
            line_color = tools.get_line_color(current_state['line_name'])
    except Exception:
        pass
    if line_color is None:
        line_color = fallback_get_line_color(current_state['line_name'])

    # 根据direction计算两端站名用于展示（右侧为终点站）
    terminal_station = None
    start_station = None
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        direction = current_state.get('direction', 0)
        line_info = None
        if tools is not None:
            try:
                line_info = tools.get_line_map_info(line_name, route_name)
            except Exception:
                pass
        if line_info is None:
            try:
                line_info = fallback_get_line_map_info(line_name, route_name)
            except Exception:
                pass
        if line_info:
            if direction == 1:
                terminal_station = line_info[0].get('station_name')
                start_station = line_info[-1].get('station_name')
            else:
                terminal_station = line_info[-1].get('station_name')
                start_station = line_info[0].get('station_name')
        else:
            # 回退：无line_info时，direction=0使用终点函数，direction=1取首站
            if direction == 0:
                try:
                    if tools is not None:
                        terminal_station = tools.get_terminal_station(line_name, route_name)
                except Exception:
                    pass
                if terminal_station is None:
                    terminal_station = fallback_get_terminal_station(line_name, route_name)
                # 起点站回退：取该路线的首站
                try:
                    route_data = _get_route_data()
                    services = route_data.get(line_name, {}).get('services', [])
                    for s in services:
                        name = s.get('type') or s.get('service_name')
                        if name == route_name:
                            stations = s.get('stations', [])
                            if stations:
                                start_station = stations[0]
                            break
                except Exception:
                    pass
            else:
                try:
                    route_data = _get_route_data()
                    services = route_data.get(line_name, {}).get('services', [])
                    for s in services:
                        name = s.get('type') or s.get('service_name')
                        if name == route_name:
                            stations = s.get('stations', [])
                            if stations:
                                terminal_station = stations[0]
                                start_station = stations[-1] if len(stations) > 0 else None
                            break
                except Exception:
                    pass
    except Exception:
        pass

    # 构建多运营线路数据：主线置顶，其他服务按数据文件加载（环线特殊显示）
    route_services = []
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        direction = current_state.get('direction', 0)
        # 线路类型与原始服务数据（用于环线识别与终点字段）
        route_data = _get_route_data()
        line_info_raw = route_data.get(line_name, {})
        line_type = line_info_raw.get('type', 'linear')
        raw_services = line_info_raw.get('services', [])
        def _raw_service_by_name(name):
            for s in raw_services:
                n = s.get('type') or s.get('service_name')
                if n == name:
                    return s
            return None
        # 环线文案：基于方向（数据为外环方向，direction=1 反向视为内环）
        def _ring_label_by_direction(dir_val):
            try:
                return '内环运行' if int(dir_val) == 1 else '外环运行'
            except Exception:
                return '外环运行'
        # 获取该线路下的所有服务名称
        routes = []
        if tools is not None:
            try:
                routes = tools.get_routes_for_line(line_name)
            except Exception:
                routes = []
        if not routes:
            try:
                routes = fallback_get_routes_for_line(line_name)
            except Exception:
                routes = []
        # 主线信息
        main_count = 0
        try:
            if tools is not None:
                info = tools.get_station_info(line_name, route_name)
                main_count = len(info)
            if main_count == 0:
                info = fallback_get_station_info(line_name, route_name)
                main_count = len(info)
        except Exception:
            main_count = 0
        # 主线完整站序（适配direction）
        main_stations = []
        try:
            main_info = []
            if tools is not None:
                try:
                    main_info = tools.get_station_info(line_name, route_name)
                except Exception:
                    main_info = []
            if not main_info:
                main_info = fallback_get_station_info(line_name, route_name)
            main_stations = [s.get('station_name') for s in main_info]
            if direction == 1:
                main_stations = list(reversed(main_stations))
        except Exception:
            main_stations = []
        # 环线特殊：左端显示“外/内环运行”，右端显示终点（若存在）
        def _ring_label_for_service(svc_name):
            # 简单映射：route1->外环运行，route2->内环运行
            try:
                if isinstance(svc_name, str) and svc_name.endswith('1'):
                    return '外环运行'
                elif isinstance(svc_name, str) and svc_name.endswith('2'):
                    return '内环运行'
            except Exception:
                pass
            return '环线运行'
        main_raw = _raw_service_by_name(route_name)
        main_terminal_field = (main_raw or {}).get('terminal_station')
        main_has_terminal = bool((main_terminal_field or '').strip())
        route_services.append({
            'name': route_name,
            'is_main': True,
            'is_loop': (line_type == 'loop'),
            'ring_label': _ring_label_by_direction(direction) if line_type == 'loop' else '',
            'has_terminal': main_has_terminal if line_type == 'loop' else True,
            'start': (_ring_label_by_direction(direction) if line_type == 'loop' else start_station),
            'end': (main_terminal_field if line_type == 'loop' else terminal_station),
            'count': max(2, min(6, main_count)),
            'total': main_count,
            'stations': main_stations
        })
        # 其他服务
        for r in routes:
            if r == route_name:
                continue
            try:
                other_info = []
                if tools is not None:
                    try:
                        other_info = tools.get_station_info(line_name, r)
                    except Exception:
                        other_info = []
                if not other_info:
                    other_info = fallback_get_station_info(line_name, r)
                other_names = [s.get('station_name') for s in other_info]
                if direction == 1:
                    other_names = list(reversed(other_names))
                    start_other = other_names[0] if len(other_names) > 0 else ''
                    end_other = other_names[-1] if len(other_names) > 0 else ''
                else:
                    start_other = other_names[0] if len(other_names) > 0 else ''
                    end_other = other_names[-1] if len(other_names) > 0 else ''
                raw = _raw_service_by_name(r)
                terminal_field = (raw or {}).get('terminal_station')
                has_terminal = bool((terminal_field or '').strip())
                route_services.append({
                    'name': r,
                    'is_main': False,
                    'is_loop': (line_type == 'loop'),
                    'ring_label': _ring_label_by_direction(direction) if line_type == 'loop' else '',
                    'has_terminal': has_terminal if line_type == 'loop' else True,
                    'start': (_ring_label_by_direction(direction) if line_type == 'loop' else start_other),
                    'end': (terminal_field if line_type == 'loop' else end_other),
                    'count': max(2, min(6, len(other_names))),
                    'total': len(other_names),
                    'stations': other_names
                })
            except Exception:
                # 忽略单个服务错误，继续
                pass
    except Exception:
        route_services = []

    # 按route后的数字排序（稳定排序，不改变非数字名的相对顺序）
    def _route_num(n):
        try:
            if isinstance(n, str) and n.startswith('route'):
                digits = ''.join([c for c in n[5:] if c.isdigit()])
                if digits:
                    return int(digits)
        except Exception:
            pass
        return 10**9
    route_services.sort(key=lambda s: _route_num(s.get('name', '')))

    # 首页底部“终点站”信息在环线时：仅基于主服务的 terminal_station；direction 仅影响文案
    loop_ring_label_main = ''
    loop_terminal_main = ''
    try:
        # 找到主服务（避免排序后取到非主服务）
        main_service = None
        for s in route_services:
            if s.get('is_main'):
                main_service = s
                break
        if main_service and main_service.get('is_loop'):
            loop_ring_label_main = main_service.get('ring_label', '')
            main_has = bool(main_service.get('has_terminal'))
            main_end = (main_service.get('end') or '').strip()
            if main_has and main_end:
                loop_terminal_main = main_end
            else:
                loop_terminal_main = ''
    except Exception:
        pass

    return render_template('next_station.html',
                           line_color=line_color,
                           terminal_station=terminal_station,
                           start_station=start_station,
                           route_services=route_services,
                           loop_ring_label_main=loop_ring_label_main,
                           loop_terminal_main=loop_terminal_main,
                           **current_state)

@app.route('/next_station')
def next_station():
    """下一站信息页面（适配direction与终点展示）"""
    # 主题色
    line_color = None
    try:
        if tools is not None:
            line_color = tools.get_line_color(current_state['line_name'])
    except Exception:
        pass
    if line_color is None:
        line_color = fallback_get_line_color(current_state['line_name'])

    # 根据direction计算两端站名用于展示（右侧为终点站）
    terminal_station = None
    start_station = None
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        direction = current_state.get('direction', 0)
        line_info = None
        if tools is not None:
            try:
                line_info = tools.get_line_map_info(line_name, route_name)
            except Exception:
                pass
        if line_info is None:
            try:
                line_info = fallback_get_line_map_info(line_name, route_name)
            except Exception:
                pass
        if line_info:
            if direction == 1:
                terminal_station = line_info[0].get('station_name')
                start_station = line_info[-1].get('station_name')
            else:
                terminal_station = line_info[-1].get('station_name')
                start_station = line_info[0].get('station_name')
        else:
            if direction == 0:
                try:
                    if tools is not None:
                        terminal_station = tools.get_terminal_station(line_name, route_name)
                except Exception:
                    pass
                if terminal_station is None:
                    terminal_station = fallback_get_terminal_station(line_name, route_name)
                # 起点站回退：取该路线的首站
                try:
                    route_data = _get_route_data()
                    services = route_data.get(line_name, {}).get('services', [])
                    for s in services:
                        name = s.get('type') or s.get('service_name')
                        if name == route_name:
                            stations = s.get('stations', [])
                            if stations:
                                start_station = stations[0]
                            break
                except Exception:
                    pass
            else:
                try:
                    route_data = _get_route_data()
                    services = route_data.get(line_name, {}).get('services', [])
                    for s in services:
                        name = s.get('type') or s.get('service_name')
                        if name == route_name:
                            stations = s.get('stations', [])
                            if stations:
                                terminal_station = stations[0]
                                start_station = stations[-1] if len(stations) > 0 else None
                            break
                except Exception:
                    pass
    except Exception:
        pass

    # 构建多运营线路数据（与首页一致，direction适配反向）
    route_services = []
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        direction = current_state.get('direction', 0)
        routes = []
        if tools is not None:
            try:
                routes = tools.get_routes_for_line(line_name)
            except Exception:
                routes = []
        if not routes:
            try:
                routes = fallback_get_routes_for_line(line_name)
            except Exception:
                routes = []
        # 主线信息
        main_count = 0
        try:
            if tools is not None:
                info = tools.get_station_info(line_name, route_name)
                main_count = len(info)
            if main_count == 0:
                info = fallback_get_station_info(line_name, route_name)
                main_count = len(info)
        except Exception:
            main_count = 0
        # 主线完整站序（适配direction）
        main_stations = []
        try:
            main_info = []
            if tools is not None:
                try:
                    main_info = tools.get_station_info(line_name, route_name)
                except Exception:
                    main_info = []
            if not main_info:
                main_info = fallback_get_station_info(line_name, route_name)
            main_stations = [s.get('station_name') for s in main_info]
            if direction == 1:
                main_stations = list(reversed(main_stations))
        except Exception:
            main_stations = []
        route_services.append({
            'name': route_name,
            'is_main': True,
            'start': start_station,
            'end': terminal_station,
            'count': max(2, min(6, main_count)),
            'total': main_count,
            'stations': main_stations
        })
        # 其他服务
        for r in routes:
            if r == route_name:
                continue
            try:
                other_info = []
                if tools is not None:
                    try:
                        other_info = tools.get_station_info(line_name, r)
                    except Exception:
                        other_info = []
                if not other_info:
                    other_info = fallback_get_station_info(line_name, r)
                other_names = [s.get('station_name') for s in other_info]
                if direction == 1:
                    other_names = list(reversed(other_names))
                start_other = other_names[0] if len(other_names) > 0 else ''
                end_other = other_names[-1] if len(other_names) > 0 else ''
                route_services.append({
                    'name': r,
                    'is_main': False,
                    'start': start_other,
                    'end': end_other,
                    'count': max(2, min(6, len(other_names))),
                    'total': len(other_names),
                    'stations': other_names
                })
            except Exception:
                # 忽略单个服务错误，继续
                pass
    except Exception:
        route_services = []

    # 按route后的数字排序（稳定排序，不改变非数字名的相对顺序）
    def _route_num(n):
        try:
            if isinstance(n, str) and n.startswith('route'):
                digits = ''.join([c for c in n[5:] if c.isdigit()])
                if digits:
                    return int(digits)
        except Exception:
            pass
        return 10**9
    route_services.sort(key=lambda s: _route_num(s.get('name', '')))

    return render_template('next_station.html', line_color=line_color, terminal_station=terminal_station, start_station=start_station, route_services=route_services, **current_state)

@app.route('/line_map')
def line_map():
    """线路图页面（基于真实数据渲染）"""
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        
        line_info = None
        line_display_name = line_name
        line_color = None
        if tools is not None:
            try:
                line_info = tools.get_line_map_info(line_name, route_name)
                line_display_name = tools.get_line_display_name(line_name)
                line_color = tools.get_line_color(line_name)
            except Exception as e:
                print(f"从RouteTools获取线路图信息失败: {e}")
        
        # 回退到数据文件
        if line_info is None:
            try:
                line_info = fallback_get_line_map_info(line_name, route_name)
                line_display_name = fallback_get_line_display_name(line_name)
                line_color = fallback_get_line_color(line_name)
            except Exception as e:
                print(f"从数据文件获取线路图信息失败: {e}")
        
        # 子路线检测：若当前route是某一更大route的子集，则展示该大路线，并将非当前route的站点标记为灰色静止
        full_route_mode = False
        try:
            # 当前路线的站序
            current_route_stations = [s.get('station_name') for s in (line_info or [])]
            # 获取该线路所有route名
            routes = []
            if tools is not None:
                try:
                    routes = tools.get_routes_for_line(line_name)
                except Exception:
                    routes = []
            if not routes:
                try:
                    routes = fallback_get_routes_for_line(line_name)
                except Exception:
                    routes = []
            # 工具：拿到指定route的站序（仅名称）
            def _names_for_route(rn):
                info_r = []
                if tools is not None:
                    try:
                        info_r = tools.get_station_info(line_name, rn)
                    except Exception:
                        info_r = []
                if not info_r:
                    info_r = fallback_get_station_info(line_name, rn)
                return [s.get('station_name') for s in info_r]
            # 判断small是否是big的连续子序列（支持与big同向或反向）
            def _is_contiguous_subseq(small, big):
                if not small or not big or len(small) > len(big):
                    return False
                # 正向匹配
                try:
                    idx = big.index(small[0])
                    if big[idx:idx+len(small)] == small:
                        return True
                except ValueError:
                    pass
                # 反向匹配
                small_rev = list(reversed(small))
                try:
                    idx2 = big.index(small_rev[0])
                    if big[idx2:idx2+len(small_rev)] == small_rev:
                        return True
                except ValueError:
                    pass
                return False
            # 选择最长的包含当前route的“大路线”
            candidate_full = None
            candidate_full_len = len(current_route_stations)
            for r in routes:
                if r == route_name:
                    continue
                names_r = _names_for_route(r)
                if len(names_r) > candidate_full_len and _is_contiguous_subseq(current_route_stations, names_r):
                    candidate_full = r
                    candidate_full_len = len(names_r)
            if candidate_full:
                full_route_mode = True
                # 使用“大路线”的富信息作为展示数据
                full_line_info = None
                if tools is not None:
                    try:
                        full_line_info = tools.get_line_map_info(line_name, candidate_full)
                        line_display_name = tools.get_line_display_name(line_name)
                        line_color = tools.get_line_color(line_name)
                    except Exception:
                        full_line_info = None
                if full_line_info is None:
                    try:
                        full_line_info = fallback_get_line_map_info(line_name, candidate_full)
                        line_display_name = fallback_get_line_display_name(line_name)
                        line_color = fallback_get_line_color(line_name)
                    except Exception:
                        full_line_info = None
                if full_line_info:
                    line_info = full_line_info
                # 将当前路线站序注入到模板上下文（用于灰显非当前route站点）
                # 注意：即便未找到大路线也注入当前站序，用于普通模式
        except Exception as e:
            print(f"子路线检测失败: {e}")
        
        # 根据direction控制显示方向：0与数据一致，1反向显示
        is_reversed = False
        try:
            direction = current_state.get('direction', 0)
            if line_info and isinstance(line_info, list) and direction == 1:
                line_info = list(reversed(line_info))
                is_reversed = True
        except Exception as e:
            print(f"整理线路显示方向失败: {e}")
        
        # 线路类型（环线/普通）
        is_loop = False
        try:
            route_data = _get_route_data()
            d = route_data.get(line_name, {})
            is_loop = (d.get('type') == 'loop')
        except Exception:
            is_loop = False

        # 环线终点字段（用于环线有/无终点的不同着色规则）
        loop_has_terminal = False
        loop_terminal_station = ''
        try:
            route_data = _get_route_data()
            d = route_data.get(line_name, {})
            services = d.get('services', [])
            for s in services:
                name = s.get('type') or s.get('service_name')
                if name == route_name:
                    term = (s.get('terminal_station') or '').strip()
                    loop_has_terminal = bool(term)
                    loop_terminal_station = term
                    break
        except Exception:
            loop_has_terminal = False
            loop_terminal_station = ''

        return render_template('line_map.html', 
                                line_info=line_info,
                                line_display_name=line_display_name,
                                line_color=line_color,
                                is_reversed=is_reversed,
                                is_loop=is_loop,
                                loop_has_terminal=loop_has_terminal,
                                loop_terminal_station=loop_terminal_station,
                                current_route_stations=current_route_stations,
                                full_route_mode=full_route_mode,
                                **current_state)
    except Exception as e:
        error_msg = f"获取线路信息失败: {str(e)}"
        print(error_msg)
        return error_msg, 500

@app.route('/station_detail')
def station_detail():
    """站点详情页面（基于真实数据渲染）"""
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        
        # 获取富含英文名与换乘信息的线路数据
        line_info = None
        if tools is not None:
            try:
                line_info = tools.get_line_map_info(line_name, route_name)
            except Exception as e:
                print(f"从RouteTools获取站点详情数据失败: {e}")
        
        # 回退到数据文件
        if line_info is None:
            try:
                line_info = fallback_get_line_map_info(line_name, route_name)
            except Exception as e:
                print(f"从数据文件获取站点详情失败: {e}")
        
        # 当前站与下一站
        current_station_info = None
        next_station_info = None
        
        if line_info:
            for i, station in enumerate(line_info):
                if station.get('station_name') == current_state.get('next_station'):
                    next_station_info = station
                    if i - 1 >= 0:
                        current_station_info = line_info[i - 1]
                    break
        
        # 计算下一站的换乘线路（显示名与徽章），排除当前线路
        transfer_lines_display = []
        transfer_badges = []
        line_color = None
        if tools is not None:
            try:
                line_color = tools.get_line_color(line_name)
            except Exception:
                pass
        if line_color is None:
            line_color = fallback_get_line_color(line_name)
        
        if next_station_info and tools is not None:
            try:
                current_code = tools._line_code_from_key(line_name)
                for code in next_station_info.get('transfer_lines', []):
                    if code != current_code:
                        key = f"line_{int(code)}"
                        transfer_lines_display.append(tools.get_line_display_name(key))
                        transfer_badges.append({'code': str(int(code)), 'color': tools.get_line_color(key)})
            except Exception:
                pass
        elif next_station_info:
            try:
                current_code = _line_code_from_key(line_name)
                for code in next_station_info.get('transfer_lines', []):
                    if code != current_code:
                        key = f"line_{int(code)}"
                        transfer_lines_display.append(fallback_get_line_display_name(key))
                        transfer_badges.append({'code': str(int(code)), 'color': fallback_get_line_color(key)})
            except Exception:
                pass
        
        return render_template('station_detail.html',
                              current_station_info=current_station_info,
                              next_station_info=next_station_info,
                              transfer_lines_display=transfer_lines_display,
                              transfer_badges=transfer_badges,
                              line_color=line_color,
                              **current_state)
    except Exception as e:
        error_msg = f"获取站点信息失败: {str(e)}"
        print(error_msg)
        return error_msg, 500

@app.route('/arrival')
def arrival():
    """到站信息页面（基于真实数据渲染）"""
    try:
        line_name = current_state['line_name']
        route_name = current_state['route_name']
        
        # 获取线路信息（含英文名、换乘信息）
        line_info = None
        if tools is not None:
            try:
                line_info = tools.get_line_map_info(line_name, route_name)
            except Exception as e:
                print(f"从RouteTools获取到站数据失败: {e}")
        
        # 回退到数据文件
        if line_info is None:
            try:
                line_info = fallback_get_line_map_info(line_name, route_name)
            except Exception as e:
                print(f"从数据文件获取到站数据失败: {e}")
        
        current_station_info = None
        next_station_info = None
        
        if line_info:
            for i, station in enumerate(line_info):
                if station.get('station_name') == current_state.get('next_station'):
                    next_station_info = station
                    if i - 1 >= 0:
                        current_station_info = line_info[i - 1]
                    break
        
        # 终点站（真实数据）
        terminal_station = None
        if tools is not None:
            try:
                terminal_station = tools.get_terminal_station(line_name, route_name)
            except Exception:
                pass
        if terminal_station is None:
            terminal_station = fallback_get_terminal_station(line_name, route_name)
        
        # 模拟出口与设施（数据文件未提供）
        exits = ['A口', 'B口', 'C口', 'D口']
        facilities = ['无障碍电梯', '卫生间', '客服中心']

        # 主题色
        line_color = None
        if tools is not None:
            try:
                line_color = tools.get_line_color(line_name)
            except Exception:
                pass
        if line_color is None:
            line_color = fallback_get_line_color(line_name)

        # 计算下一站的换乘线路（显示名与徽章），排除当前线路
        transfer_lines_display = []
        transfer_badges = []
        if next_station_info and tools is not None:
            try:
                current_code = tools._line_code_from_key(line_name)
                for code in next_station_info.get('transfer_lines', []):
                    if code != current_code:
                        key = f"line_{int(code)}"
                        transfer_lines_display.append(tools.get_line_display_name(key))
                        transfer_badges.append({'code': str(int(code)), 'color': tools.get_line_color(key)})
            except Exception:
                pass
        
        return render_template('arrival.html',
                              current_station_info=current_station_info,
                              next_station_info=next_station_info,
                              exits=exits,
                              facilities=facilities,
                              transfer_lines_display=transfer_lines_display,
                              transfer_badges=transfer_badges,
                              line_color=line_color,
                              **current_state)
    except Exception as e:
        error_msg = f"获取到站信息失败: {str(e)}"
        print(error_msg)
        return error_msg, 500

@app.route('/api/get_station_info')
def api_get_station_info():
    """API接口：获取站点信息"""
    try:
        line_name = request.args.get('line_name', current_state['line_name'])
        route_name = request.args.get('route_name', current_state['route_name'])
        
        # 尝试从RouteTools获取数据
        if tools is not None:
            try:
                station_info = tools.get_station_info(line_name, route_name)
                return jsonify({
                    'status': 'success',
                    'data': station_info
                })
            except Exception as e:
                print(f"从RouteTools获取API站点信息失败: {e}")
        
        # 回退到数据文件
        try:
            station_info = fallback_get_station_info(line_name, route_name)
            return jsonify({
                'status': 'success',
                'data': station_info
            })
        except Exception as e:
            print(f"从数据文件获取API站点信息失败: {e}")
        
        return jsonify({
            'status': 'error',
            'message': '无法获取站点信息'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/get_all_lines')
def api_get_all_lines():
    """API接口：获取所有线路"""
    try:
        # 尝试从RouteTools获取数据
        if tools is not None:
            try:
                lines = tools.get_all_lines()
                return jsonify({
                    'status': 'success',
                    'data': lines
                })
            except Exception as e:
                print(f"从RouteTools获取线路列表失败: {e}")
        
        # 回退到数据文件
        try:
            lines = fallback_get_all_lines()
            return jsonify({
                'status': 'success',
                'data': lines
            })
        except Exception as e:
            print(f"从数据文件获取线路列表失败: {e}")
            return jsonify({
                'status': 'error',
                'message': '无法获取线路列表'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/get_routes_for_line')
def api_get_routes_for_line():
    """API接口：获取指定线路的所有路线"""
    try:
        line_name = request.args.get('line_name')
        if not line_name:
            return jsonify({
                'status': 'error',
                'message': '未提供线路名称'
            }), 400
        
        # 尝试从RouteTools获取数据
        if tools is not None:
            try:
                routes = tools.get_routes_for_line(line_name)
                return jsonify({
                    'status': 'success',
                    'data': routes
                })
            except Exception as e:
                print(f"从RouteTools获取路线信息失败: {e}")
        
        # 回退到数据文件
        try:
            routes = fallback_get_routes_for_line(line_name)
            return jsonify({
                'status': 'success',
                'data': routes
            })
        except Exception as e:
            print(f"从数据文件获取路线信息失败: {e}")
            return jsonify({
                'status': 'error',
                'message': '无法获取路线信息'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/update_state', methods=['POST'])
def update_state():
    """API接口：更新当前状态（用于模拟测试）"""
    try:
        data = request.json
        if data:
            for key, value in data.items():
                if key in current_state:
                    current_state[key] = value
        
        return jsonify({
            'status': 'success',
            'data': current_state
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

# 获取线路显示名称（优先使用RouteTools，其次使用数据文件回退）
def get_line_display_name(line):
    try:
        if tools is not None:
            return tools.get_line_display_name(line)
    except Exception:
        pass
    return fallback_get_line_display_name(line)

# 注册模板过滤器
@app.template_filter('line_display')
def line_display_filter(line):
    return get_line_display_name(line)

# 确保目录存在
def ensure_directories():
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    static_css_dir = os.path.join(static_dir, 'css')
    static_js_dir = os.path.join(static_dir, 'js')
    static_images_dir = os.path.join(static_dir, 'images')
    
    for directory in [templates_dir, static_dir, static_css_dir, static_js_dir, static_images_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")

# 数据文件读取与回退工具（代码与数据分离）
_DATA_CACHE = {}

def _data_path(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', name)

def _load_json(name):
    try:
        with open(_data_path(name), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载数据文件失败 {name}: {e}")
        return {}

def _get_route_data():
    if 'route.json' not in _DATA_CACHE:
        _DATA_CACHE['route.json'] = _load_json('route.json')
    return _DATA_CACHE['route.json']

def _get_station_data():
    if 'station.json' not in _DATA_CACHE:
        _DATA_CACHE['station.json'] = _load_json('station.json')
    return _DATA_CACHE['station.json']

def _get_color_data():
    if 'color.json' not in _DATA_CACHE:
        _DATA_CACHE['color.json'] = _load_json('color.json')
    return _DATA_CACHE['color.json']

def _get_trans_data():
    if 'trans_name.json' not in _DATA_CACHE:
        _DATA_CACHE['trans_name.json'] = _load_json('trans_name.json')
    return _DATA_CACHE['trans_name.json']

def _line_code_from_key(line_key):
    try:
        return int(line_key.split('_')[1])
    except Exception:
        return None

def fallback_get_line_display_name(line_key):
    route_data = _get_route_data()
    d = route_data.get(line_key, {})
    return d.get('line_name', line_key)

def fallback_get_line_color(line_key):
    color_data = _get_color_data()
    return color_data.get(line_key)

def fallback_get_routes_for_line(line_key):
    route_data = _get_route_data()
    d = route_data.get(line_key, {})
    services = d.get('services', [])
    names = []
    for s in services:
        name = s.get('type') or s.get('service_name')
        if name:
            names.append(name)
    return names

def fallback_get_terminal_station(line_key, route_name):
    route_data = _get_route_data()
    d = route_data.get(line_key, {})
    services = d.get('services', [])
    for s in services:
        name = s.get('type') or s.get('service_name')
        if name == route_name:
            stations = s.get('stations', [])
            if stations:
                return stations[-1]
    return None

def fallback_get_line_map_info(line_key, route_name):
    route_data = _get_route_data()
    station_data = _get_station_data()
    trans_data = _get_trans_data()
    d = route_data.get(line_key, {})
    services = d.get('services', [])
    target = None
    for s in services:
        name = s.get('type') or s.get('service_name')
        if name == route_name:
            target = s
            break
    if target is None:
        return None
    stations = target.get('stations', [])
    line_code = _line_code_from_key(line_key)
    result = []
    for name in stations:
        entry = {
            'station_name': name,
            'station_name_en': trans_data.get(name, name),
            'station_index': None,
            'is_transfer': False,
            'transfer_lines': [],
            'transfer_count_excl_current': 0,
            'transfer_badges': []
        }
        info = station_data.get(name)
        if isinstance(info, list) and line_code is not None:
            indices = []
            transfer_lines = []
            for rec in info:
                try:
                    code = int(rec[0])
                except Exception:
                    try:
                        code = int(str(rec[0]).lstrip('0'))
                    except Exception:
                        code = None
                idx = rec[1] if len(rec) > 1 else None
                if code is not None:
                    indices.append([code, idx])
                    if code != line_code:
                        transfer_lines.append(code)
            entry['station_index'] = indices
            if transfer_lines:
                entry['is_transfer'] = True
                entry['transfer_lines'] = transfer_lines
                entry['transfer_count_excl_current'] = len(transfer_lines)
        result.append(entry)
    return result

def fallback_get_station_info(line_key, route_name):
    route_data = _get_route_data()
    trans_data = _get_trans_data()
    d = route_data.get(line_key, {})
    services = d.get('services', [])
    target = None
    for s in services:
        name = s.get('type') or s.get('service_name')
        if name == route_name:
            target = s
            break
    if target is None:
        return []
    stations = target.get('stations', [])
    return [{'station_name': n, 'station_name_en': trans_data.get(n, n)} for n in stations]

def fallback_get_all_lines():
    route_data = _get_route_data()
    return list(route_data.keys())


if __name__ == '__main__':
    # 创建必要的目录
    ensure_directories()
    
    # 运行应用
    app.run(host='0.0.0.0', port=8089, debug=True)