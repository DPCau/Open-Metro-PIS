# 成都地铁PIS车内导视系统

## 项目介绍

本项目基于成都地铁数据实现一个车内乘客信息系统(PIS)，提供实时的线路信息、到站提醒、站点导航等功能。

## 项目结构

```
/Metro/PIS/
├── .venv/                 # 虚拟环境
├── data/                  # 数据文件夹
│   ├── route.json         # 线路数据
│   └── station.json       # 站台数据
├── tools/                 # 工具类
│   └── route_tools.py     # 线路工具类
├── static/                # 静态资源
│   ├── css/               # 样式文件
│   ├── js/                # JavaScript文件
│   └── images/            # 图片资源
├── templates/             # HTML模板
│   ├── base.html          # 基础模板
│   ├── index.html         # 首页/下一站信息页面
│   ├── line_map.html      # 线路图页面
│   ├── station_detail.html # 站点详情页面
│   └── arrival.html       # 到站信息页面
├── app.py                 # 主应用程序
└── requirements.txt       # 依赖文件
```

## 功能特性

1. **下一站信息显示**：展示当前线路、下一站信息、开门方向等
2. **线路图显示**：展示完整线路图和当前位置
3. **站点详情显示**：展示站点的换乘信息、预计到达时间等
4. **到站信息显示**：到站时的出口指引和站点信息

## 技术栈

- **后端**：Python Flask
- **前端**：HTML, CSS, JavaScript
- **数据处理**：基于现有的JSON数据文件

## 使用方法

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 访问系统：
在浏览器中访问 http://localhost:8089

## 数据说明

- **route.json**：包含各线路的名称、类型和服务信息
- **station.json**：包含各站点的索引信息和换乘信息

## 扩展开发

可以通过以下方式扩展系统功能：

1. 添加实时车辆位置数据接口
2. 集成实时客流数据
3. 添加多语言支持
4. 优化移动端显示效果