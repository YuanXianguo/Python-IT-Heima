create database python_test charset=utf8;

create table students(
	id int unsigned primary key not null auto_increment,
	name varchar(20) default "",
	age tinyint unsigned default 0,
	height decimal(5,2) ,
	gender enum("男", "女", "保密", "中性") default "保密",
	cls_id int unsigned default 0,
	is_delete bit default 0
);


create table classes(
	id int unsigned auto_increment primary key not null,
	name varchar(20) not null
);

insert into students values 
	(0, "小明", 18, 180.0, 2, 1, 0),
	(0, "小月月", 18, 180.0, 2, 2, 1),
	(0, "彭于晏", 29, 185.0, 1, 1, 0),
	(0, "刘德华", 59, 175.0, 1, 2, 1),
	(0, "黄蓉", 38, 160.0, 2,1,0),
	(0, "凤姐", 28,150,4,2,1),
	(0,"王祖贤",18,172,2,1,1),
	(0,"周杰伦",36,null,1,1,0),
	(0,"刘亦菲",25,166,2,2,0),
	(0, "金星",33,162,3,3,1),
	(0, "郭靖",12,170,1,4,0),
	(0,"静香",12,180,2,4,0),
	(0,"周杰",34,176,2,5,0);


insert into classes values (0,"python_01期"),(0,"python_02期");

select * from students;
select * from classes;

select id,name from classes;

select name,age from students;

# 字段别名
select name as 姓名, age as 年龄 from students;

# 数据表别名
select s.name,s.age from students as s;

# 数据去重
select distinct gender from students;

select * from students where not age>18 and gender=2;

-- 模糊查询
select name from students where name like "小%";

-- rlike
select name from students where name rlike "^周.*";

select name,height from students where age between 18 and 34 and gender=2 order by height desc,age desc;

-- 分组聚合
select gender,count(*) from students group by gender;
-- 查看分组内容
select gender,group_concat(name,"",age) from students group by gender;


select gender,count(*) from students where gender=1 group by gender;

-- 分页limit (页数-1)*每页,每页 0,2;2,2;4,2;
select * from students where gender=2 order by height desc limit 2,2;


-- 连接
select * from students inner join classes on students.cls_id=classes.id; 
select s.*,c.name from students as s inner join classes as c on s.cls_id=c.id; 

-- 自关联，查询河南省所有市
select * from areas as province inner join areas as city on province.aid=city.pid having province.atitle="河南省";

-- 视图
create view v_goods_info as select g.*,c.name as cate_name,b.name as brand_name from goods as g left join goods_cates as c on g.cate_id=c.id left join goods_brand as b on g.brand_id=b.id;