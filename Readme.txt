1. 利用Visual Studio Code打开本文件夹后，选择右上角菜单栏上面的终端->新建终端后打开命令窗口
2. 在命令窗口中输入flaskr文件夹内command.md文本中配置程序的相应代码：
$env:FLASK_APP='flaskr'
$env:FLASK_ENV='development'
3. 若系统首次在本地启动，输入‘flask init-db’指定以初始化数据库。
4. 输入‘flask run’指令后等待以下代码出现：
* Serving Flask app "flaskr" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Restarting with windowsapi reloader
 * Debugger is active!
 * Debugger PIN: 423-096-938
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
以运行本系统。
3. 打开网站http://127.0.0.1:5000/auth/index以访问本系统主页。