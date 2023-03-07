DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS user_id_list;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS advice;
DROP TABLE IF EXISTS style;
DROP TABLE IF EXISTS furniture;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS provinces;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS template;

CREATE TABLE user_id_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    val TEXT NOT NULL -- ID值
);

CREATE TABLE user (
    id TEXT PRIMARY KEY, -- 编号，5个英文字母+10个数字，随机生成, 管理员账户前缀为ADMIN
    username TEXT UNIQUE NOT NULL, -- 用户名，最大长度限制10
    headshot TEXT NOT NULL DEFAULT 'images/headshot/default.jpg', -- 用户头像，默认头像未定
    sex TEXT DEFAULT '私密', -- 性别，可以为空
    password TEXT NOT NULL, -- 密码，6-15个字符，必须包含英文大写/小写和数字，特殊字符只能是 . @ $ ! % * # _ ~ ? & ^
    phone INTEGER UNIQUE NOT NULL, -- 手机号，限制11个数字，可以的话检测号码可用性
    email TEXT DEFAULT '', -- 邮箱，需要邮箱格式，并验证邮箱的有效性
    age INTEGER DEFAULT '0', -- 生日，早于当前时间
    status INTEGER NOT NULL, -- 权限，1:管理员；2:普通用户
    creation_date TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')) -- 用户创建时间，默认当前时间
);

CREATE TABLE advice (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    creation_date TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')), -- 用户反馈时间
    content TEXT NOT NULL, -- 反馈内容
    contactWay TEXT -- 联系方式
);

CREATE TABLE article (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    username TEXT NOT NULL, -- 用户名，最大长度限制10
    title TEXT NOT NULL, -- 文章标题
    theme TEXT NOT NULL, -- 文章主题
    content TEXT NOT NULL, -- 文章md文件地址
    creation_time TIMESTAMP NOT NULL DEFAULT (datetime('now', 'localtime')), -- 文章创建时间
    FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE style (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    title TEXT NOT NULL, -- 图片标题
    type TEXT NOT NULL, -- 房间类型
    area REAL NOT NULL, -- 房间面积
    style TEXT NOT NULL, -- 房间风格
    func TEXT NOT NULL, -- 功能分区
    filetype TEXT NOT NULL -- 图片类型
);

CREATE TABLE furniture (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    title TEXT NOT NULL, -- 图片标题
    model TEXT NOT NULL, -- 模型
    color TEXT NOT NULL, -- 色系
    material TEXT NOT NULL, -- 材质
    style TEXT NOT NULL, -- 风格
    price TEXT NOT NULL, -- 价格
    unit TEXT NOT NULL, -- 单位
    size TEXT, -- 尺寸
    filetype TEXT NOT NULL -- 图片类型
);

INSERT INTO style VALUES (1, '美式装修风格样例图', '单层', 36.42, 'Americano', '客厅', 'jpg');
INSERT INTO style VALUES (2, '田园式装修风格样例图', '多层', 49.84, 'Arcadian', '客厅', 'jpg');
INSERT INTO style VALUES (3, '欧式装修风格样例图', '单层', 24.29, 'European', '客厅', 'jpg');
INSERT INTO style VALUES (4, '港式装修风格样例图', '单层', 19.09, 'HongKong', '客厅', 'jpg');
INSERT INTO style VALUES (5, '简欧装修风格样例图', '单层', 46.68, 'JaneEuropean', '客厅', 'jpg');
INSERT INTO style VALUES (6, '日式装修风格样例图', '单层', 71.03, 'Japanese', '客厅', 'jpg');
INSERT INTO style VALUES (7, '地中海式装修风格样例图', '单层', 33.19, 'Mediterranean', '客厅', 'jpg');
INSERT INTO style VALUES (8, '轻奢装修风格样例图', '单层', 45.36, 'MildLuxury', '客厅', 'jpg');
INSERT INTO style VALUES (9, '现代装修风格样例图', '单层', 85.82, 'Modern', '客厅', 'jpg');
INSERT INTO style VALUES (10, '新中式装修风格样例图', '单层', 69.03, 'NeoChinese', '客厅', 'jpg');
INSERT INTO style VALUES (11, '北欧装修风格样例图', '单层', 22.98, 'NorthernEuropean', '客厅', 'jpg');
INSERT INTO style VALUES (12, '后现代装修风格样例图', '单层', 21.13, 'Postmodern', '客厅', 'jpg');

INSERT INTO furniture VALUES (1, '模型样例图：门', '门', '木色', '木质', 'Modern', 500, '扇', '定制', 'jpg');
INSERT INTO furniture VALUES (2, '模型样例图：窗', '窗', '白色', '玻璃', 'Modern', 150, '扇', '1.96*0.47*2.08（m）', 'jpg');
INSERT INTO furniture VALUES (3, '模型样例图：地面', '地面', '米色', '陶瓷', 'European', 70, 'm²', '', 'jpg');
INSERT INTO furniture VALUES (4, '模型样例图：墙面', '墙面', '白色', '木质', 'NeoChinese', 100, '个', '4.68*0.07*2.40（m）', 'jpg');
INSERT INTO furniture VALUES (5, '模型样例图：结构部件', '结构部件', '黄色', '木质', 'JaneEuropean', 110, '个', '50*50*900-1000 110*110*1050-1200（mm）', 'jpg');
INSERT INTO furniture VALUES (6, '模型样例图：沙发', '沙发', '米色', '布料', 'Arcadian', 12277, '个', '3.35*1.70*0.75（m）', 'jpg');
INSERT INTO furniture VALUES (7, '模型样例图：床', '床', '米色', '木质', 'Japanese', 7590, '张', '1.57*2.85*1.00（m）', 'jpg');
INSERT INTO furniture VALUES (8, '模型样例图：桌子', '桌子', '蓝色', '石材', 'NorthernEuropean', 1050, '个', '0.12*0.60*0.75（m）', 'jpg');
INSERT INTO furniture VALUES (9, '模型样例图：椅子|凳子', '椅子|凳子', '灰色', '布料', 'NorthernEuropean', 480, '个', '', 'jpg');
INSERT INTO furniture VALUES (10, '模型样例图：柜架', '柜架', '褐色', '木质', 'Americano', 2900, '个', '0.6米以下宽', 'jpg');
INSERT INTO furniture VALUES (11, '模型样例图：橱柜', '橱柜', '蓝色', '木质', 'Mediterranean', 1400, '个', '4.54*2.25*2.43（m）', 'jpg');
INSERT INTO furniture VALUES (12, '模型样例图：浴室柜', '浴室柜', '灰色', '石材', 'Modern', 800, '个', '1.38*0.51*1.73（m）', 'jpg');
INSERT INTO furniture VALUES (13, '模型样例图：洗手台', '洗手台', '灰色', '石材', 'MildLuxury', 300, '个', '0.40*0.29*0.50（m）', 'jpg');
INSERT INTO furniture VALUES (14, '模型样例图：马桶', '马桶', '白色', '石材', 'Modern', 600, '个', '0.36*0.66*0.79（m）', 'jpg');
INSERT INTO furniture VALUES (15, '模型样例图：浴缸', '浴缸', '黑色', '塑料', 'MildLuxury', 2000, '个', '1.67*0.89*0.86（m）', 'jpg');

CREATE TABLE provinces (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    provinceid INTEGER UNIQUE NOT NULL, -- 省份编号
    province TEXT UNIQUE NOT NULL -- 省份名称
);

INSERT INTO provinces VALUES ('1', '110000', '北京市'); 
INSERT INTO provinces VALUES ('2', '120000', '天津市'); 
INSERT INTO provinces VALUES ('3', '130000', '河北省'); 
INSERT INTO provinces VALUES ('4', '140000', '山西省'); 
INSERT INTO provinces VALUES ('5', '150000', '内蒙古自治区'); 
INSERT INTO provinces VALUES ('6', '210000', '辽宁省'); 
INSERT INTO provinces VALUES ('7', '220000', '吉林省'); 
INSERT INTO provinces VALUES ('8', '230000', '黑龙江省'); 
INSERT INTO provinces VALUES ('9', '310000', '上海市'); 
INSERT INTO provinces VALUES ('10', '320000', '江苏省'); 
INSERT INTO provinces VALUES ('11', '330000', '浙江省'); 
INSERT INTO provinces VALUES ('12', '340000', '安徽省'); 
INSERT INTO provinces VALUES ('13', '350000', '福建省'); 
INSERT INTO provinces VALUES ('14', '360000', '江西省'); 
INSERT INTO provinces VALUES ('15', '370000', '山东省'); 
INSERT INTO provinces VALUES ('16', '410000', '河南省'); 
INSERT INTO provinces VALUES ('17', '420000', '湖北省'); 
INSERT INTO provinces VALUES ('18', '430000', '湖南省'); 
INSERT INTO provinces VALUES ('19', '440000', '广东省'); 
INSERT INTO provinces VALUES ('20', '450000', '广西壮族自治区'); 
INSERT INTO provinces VALUES ('21', '460000', '海南省'); 
INSERT INTO provinces VALUES ('22', '500000', '重庆市'); 
INSERT INTO provinces VALUES ('23', '510000', '四川省'); 
INSERT INTO provinces VALUES ('24', '520000', '贵州省'); 
INSERT INTO provinces VALUES ('25', '530000', '云南省'); 
INSERT INTO provinces VALUES ('26', '540000', '西藏自治区'); 
INSERT INTO provinces VALUES ('27', '610000', '陕西省'); 
INSERT INTO provinces VALUES ('28', '620000', '甘肃省'); 
INSERT INTO provinces VALUES ('29', '630000', '青海省'); 
INSERT INTO provinces VALUES ('30', '640000', '宁夏回族自治区'); 
INSERT INTO provinces VALUES ('31', '650000', '新疆维吾尔自治区'); 
-- INSERT INTO provinces VALUES ('32', '710000', '台湾省'); 
-- INSERT INTO provinces VALUES ('33', '810000', '香港特别行政区'); 
-- INSERT INTO provinces VALUES ('34', '820000', '澳门特别行政区');

CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    cityid INTEGER UNIQUE NOT NULL, -- 城市编号
    city TEXT UNIQUE NOT NULL, -- 城市名称
    provinceid INTEGER NOT NULL, -- 所属省份编号
    lines INTEGER NOT NULL DEFAULT 3, -- 几线城市
    FOREIGN KEY (provinceid) REFERENCES provinces (provinceid)
);

INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('110100', '北京市', '110000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('120100', '天津市', '120000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('130100', '石家庄市', '130000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130200', '唐山市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130300', '秦皇岛市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130400', '邯郸市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130500', '邢台市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130600', '保定市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130700', '张家口市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130800', '承德市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('130900', '沧州市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('131000', '廊坊市', '130000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('131100', '衡水市', '130000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('140100', '太原市', '140000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140200', '大同市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140300', '阳泉市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140400', '长治市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140500', '晋城市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140600', '朔州市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140700', '晋中市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140800', '运城市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('140900', '忻州市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('141000', '临汾市', '140000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('141100', '吕梁市', '140000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('150100', '呼和浩特市', '150000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('150200', '包头市', '150000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150300', '乌海市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150400', '赤峰市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150500', '通辽市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150600', '鄂尔多斯市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150700', '呼伦贝尔市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150800', '巴彦淖尔市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('150900', '乌兰察布市', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('152200', '兴安盟', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('152500', '锡林郭勒盟', '150000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('152900', '阿拉善盟', '150000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('210100', '沈阳市', '210000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('210200', '大连市', '210000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210300', '鞍山市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210400', '抚顺市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210500', '本溪市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210600', '丹东市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210700', '锦州市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210800', '营口市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('210900', '阜新市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('211000', '辽阳市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('211100', '盘锦市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('211200', '铁岭市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('211300', '朝阳市', '210000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('211400', '葫芦岛市', '210000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('220100', '长春市', '220000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220200', '吉林市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220300', '四平市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220400', '辽源市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220500', '通化市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220600', '白山市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220700', '松原市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('220800', '白城市', '220000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('222400', '延边朝鲜族自治州', '220000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('230100', '哈尔滨市', '230000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230200', '齐齐哈尔市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230300', '鸡西市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230400', '鹤岗市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230500', '双鸭山市', '230000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('230600', '大庆市', '230000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230700', '伊春市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230800', '佳木斯市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('230900', '七台河市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('231000', '牡丹江市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('231100', '黑河市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('231200', '绥化市', '230000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('232700', '大兴安岭地区', '230000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('310100', '上海市', '310000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320100', '南京市', '320000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320200', '无锡市', '320000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320300', '徐州市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320400', '常州市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320500', '苏州市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320600', '南通市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('320700', '连云港市', '320000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('320800', '淮安市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('320900', '盐城市', '320000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('321000', '扬州市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('321100', '镇江市', '320000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('321200', '泰州市', '320000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('321300', '宿迁市', '320000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('330100', '杭州市', '330000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('330200', '宁波市', '330000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('330300', '温州市', '330000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('330400', '嘉兴市', '330000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('330500', '湖州市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('330600', '绍兴市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('330700', '金华市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('330800', '衢州市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('330900', '舟山市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('331000', '台州市', '330000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('331100', '丽水市', '330000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('340100', '合肥市', '340000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340200', '芜湖市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340300', '蚌埠市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340400', '淮南市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340500', '马鞍山市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340600', '淮北市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340700', '铜陵市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('340800', '安庆市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341000', '黄山市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341100', '滁州市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341200', '阜阳市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341300', '宿州市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341400', '巢湖市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341500', '六安市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341600', '亳州市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341700', '池州市', '340000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('341800', '宣城市', '340000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('350100', '福州市', '350000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('350200', '厦门市', '350000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350300', '莆田市', '350000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350400', '三明市', '350000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('350500', '泉州市', '350000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350600', '漳州市', '350000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350700', '南平市', '350000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350800', '龙岩市', '350000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('350900', '宁德市', '350000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('360100', '南昌市', '360000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360200', '景德镇市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360300', '萍乡市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360400', '九江市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360500', '新余市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360600', '鹰潭市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360700', '赣州市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360800', '吉安市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('360900', '宜春市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('361000', '抚州市', '360000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('361100', '上饶市', '360000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('370100', '济南市', '370000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('370200', '青岛市', '370000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('370300', '淄博市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('370400', '枣庄市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('370500', '东营市', '370000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('370600', '烟台市', '370000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('370700', '潍坊市', '370000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('370800', '济宁市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('370900', '泰安市', '370000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('371000', '威海市', '370000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371100', '日照市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371200', '莱芜市', '370000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('371300', '临沂市', '370000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371400', '德州市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371500', '聊城市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371600', '滨州市', '370000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('371700', '荷泽市', '370000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('410100', '郑州市', '410000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410200', '开封市', '410000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('410300', '洛阳市', '410000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410400', '平顶山市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410500', '安阳市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410600', '鹤壁市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410700', '新乡市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410800', '焦作市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('410900', '濮阳市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411000', '许昌市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411100', '漯河市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411200', '三门峡市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411300', '南阳市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411400', '商丘市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411500', '信阳市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411600', '周口市', '410000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('411700', '驻马店市', '410000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('420100', '武汉市', '420000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420200', '黄石市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420300', '十堰市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420500', '宜昌市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420600', '襄樊市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420700', '鄂州市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420800', '荆门市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('420900', '孝感市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('421000', '荆州市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('421100', '黄冈市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('421200', '咸宁市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('421300', '随州市', '420000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('422800', '恩施土家族苗族自治州', '420000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('430100', '长沙市', '430000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430200', '株洲市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430300', '湘潭市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430400', '衡阳市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430500', '邵阳市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430600', '岳阳市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430700', '常德市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430800', '张家界市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('430900', '益阳市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('431000', '郴州市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('431100', '永州市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('431200', '怀化市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('431300', '娄底市', '430000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('433100', '湘西土家族苗族自治州', '430000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('440100', '广州市', '440000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('440200', '韶关市', '440000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('440300', '深圳市', '440000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('440400', '珠海市', '440000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('440500', '汕头市', '440000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('440600', '佛山市', '440000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('440700', '江门市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('440800', '湛江市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('440900', '茂名市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441200', '肇庆市', '440000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('441300', '惠州市', '440000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441400', '梅州市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441500', '汕尾市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441600', '河源市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441700', '阳江市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('441800', '清远市', '440000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('441900', '东莞市', '440000', 2); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('442000', '中山市', '440000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('445100', '潮州市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('445200', '揭阳市', '440000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('445300', '云浮市', '440000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('450100', '南宁市', '450000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450200', '柳州市', '450000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('450300', '桂林市', '450000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450400', '梧州市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450500', '北海市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450600', '防城港市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450700', '钦州市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450800', '贵港市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('450900', '玉林市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('451000', '百色市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('451100', '贺州市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('451200', '河池市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('451300', '来宾市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('451400', '崇左市', '450000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('460100', '海口市', '460000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('460200', '三亚市', '460000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('500100', '重庆市', '500000', 1); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('510100', '成都市', '510000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510300', '自贡市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510400', '攀枝花市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510500', '泸州市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510600', '德阳市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510700', '绵阳市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510800', '广元市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('510900', '遂宁市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511000', '内江市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511100', '乐山市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511300', '南充市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511400', '眉山市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511500', '宜宾市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511600', '广安市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511700', '达州市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511800', '雅安市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('511900', '巴中市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('512000', '资阳市', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('513200', '阿坝藏族羌族自治州', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('513300', '甘孜藏族自治州', '510000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('513400', '凉山彝族自治州', '510000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('520100', '贵阳市', '520000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('520200', '六盘水市', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('520300', '遵义市', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('520400', '安顺市', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('522200', '铜仁地区', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('522300', '黔西南布依族苗族自治州', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('522400', '毕节地区', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('522600', '黔东南苗族侗族自治州', '520000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('522700', '黔南布依族苗族自治州', '520000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('530100', '昆明市', '530000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530300', '曲靖市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530400', '玉溪市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530500', '保山市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530600', '昭通市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530700', '丽江市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530800', '思茅市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('530900', '临沧市', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('532300', '楚雄彝族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('532500', '红河哈尼族彝族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('532600', '文山壮族苗族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('532800', '西双版纳傣族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('532900', '大理白族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('533100', '德宏傣族景颇族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('533300', '怒江傈僳族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('533400', '迪庆藏族自治州', '530000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('540100', '拉萨市', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542100', '昌都地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542200', '山南地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542300', '日喀则地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542400', '那曲地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542500', '阿里地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('542600', '林芝地区', '540000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('610100', '西安市', '610000', 1); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610200', '铜川市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610300', '宝鸡市', '610000'); 
INSERT INTO cities(cityid, city, provinceid, lines) VALUES ('610400', '咸阳市', '610000', 2); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610500', '渭南市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610600', '延安市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610700', '汉中市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610800', '榆林市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('610900', '安康市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('611000', '商洛市', '610000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620100', '兰州市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620200', '嘉峪关市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620300', '金昌市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620400', '白银市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620500', '天水市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620600', '武威市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620700', '张掖市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620800', '平凉市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('620900', '酒泉市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('621000', '庆阳市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('621100', '定西市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('621200', '陇南市', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('622900', '临夏回族自治州', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('623000', '甘南藏族自治州', '620000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('630100', '西宁市', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632100', '海东地区', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632200', '海北藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632300', '黄南藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632500', '海南藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632600', '果洛藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632700', '玉树藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('632800', '海西蒙古族藏族自治州', '630000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('640100', '银川市', '640000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('640200', '石嘴山市', '640000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('640300', '吴忠市', '640000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('640400', '固原市', '640000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('640500', '中卫市', '640000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('650100', '乌鲁木齐市', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('650200', '克拉玛依市', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652100', '吐鲁番地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652200', '哈密地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652300', '昌吉回族自治州', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652700', '博尔塔拉蒙古自治州', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652800', '巴音郭楞蒙古自治州', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('652900', '阿克苏地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('653000', '克孜勒苏柯尔克孜自治州', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('653100', '喀什地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('653200', '和田地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('654000', '伊犁哈萨克自治州', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('654200', '塔城地区', '650000'); 
INSERT INTO cities(cityid, city, provinceid) VALUES ('654300', '阿勒泰地区', '650000'); 

CREATE TABLE model (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    name TEXT NOT NULL, -- 模型名称
    type TEXT NOT NULL, -- 模型类别
    minGrow REAL NOT NULL, -- 最小缩放比例
    maxGrow REAL NOT NULL, -- 最大缩放比例
    code TEXT NOT NULL -- svg代码
);

CREATE TABLE template (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 编号
    title TEXT NOT NULL, -- 模板标题
    func TEXT NOT NULL, -- 房间类型
    width REAL NOT NULL, -- 房间宽度
    height REAL NOT NULL, -- 房间长度
    floor TEXT NOT NULL, -- 房间地板
    style TEXT NOT NULL, -- 房间风格
    remark TEXT, -- 模板描述
    locate TEXT, -- 门窗位置
    demand TEXT, -- 一般需求
    near TEXT, -- 临近信息
    scaleRange TEXT, -- 家具尺寸
    svg TEXT -- svg文件名
);

INSERT INTO template VALUES (1, '我的卧室', '卧室', 2.8, 3.8, '木地板', 'Modern', '', '相对', '适中', '柜架与床相近;床与柜架相近;桌子与窗相近;窗与桌子相近', '双人床(2.1m*2m)——尺寸范围(0.8-1.2);方桌(2.8m*0.64m)——尺寸范围(0.8-1.0);坐椅(0.3m*0.42m)——尺寸范围(0.8-1.3);抽屉柜(0.4m*0.37m)——尺寸范围(0.8-1.1);滑动柜(1.8m*0.6m)——尺寸范围(0.8-1.0)', '1');
INSERT INTO template VALUES (2, '父母卧室', '卧室', 2.8, 3.8, '木地板', 'Modern', '', '相对', '宽敞', '柜架与床相近;床与柜架相近;柜架与门相近', '双人床(2.1m*2m)——尺寸范围(0.8-1.3);抽屉柜(0.4m*0.37m)——尺寸范围(0.8-1.2);滑动柜(1.8m*0.6m)——尺寸范围(0.8-1.1)', '2');