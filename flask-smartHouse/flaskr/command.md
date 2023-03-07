'''配置程序'''
```powershell
$env:FLASK_APP='flaskr'
$env:FLASK_ENV='development'
```
'''本地启动命令'''
```powershell
flask run
```
'''初始化数据库'''
```powershell
flask init-db
```
'''管理数据库'''
```powershell
flask manage-db
(在光标>>>后输入sqlite数据库查询语句以进行数据库的后台操作，输入exit以退出后台操作界面)
```
'''创建管理员'''
```powershell
flask create-admin
(在光标>后用提示的格式输入用户名和手机号以创建管理员，例如'mxh:18655983159'，得到系统分配密码后输入y/n确认是否生成管理员账号，输入Y或y后管理员账号正式注册，输入exit以退出管理员创建界面)
```