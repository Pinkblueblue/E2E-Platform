在命令行执行以下命令：

## 创建虚拟环境

1. python3 -m venv backend-env
2. . backend-env/bin/activate

> for window in git bash env: . ./backend-env/Scripts/activate

## 安装依赖

1. pip install -r requirements.txt

## 启动程序

1. flask run

## 测试

1. 测试项目是否启动成功：http://127.0.0.1:5000
2. 测试数据库是否能够访问：http://127.0.0.1:5000/queryAll/kol-profile

## 创建本地表

1. flask createtable

## 插入数据

2. flask initialtable


