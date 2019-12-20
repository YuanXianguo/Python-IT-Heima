-- 新建数据库
CREATE DATABASE `school`;

-- 使用数据库
USE `school`;

-- 新建表
CREATE TABLE `students`(
`id` INT NOT NULL auto_increment PRIMARY KEY,
`name` VARCHAR(20) NOT NULL,
`nick_name` VARCHAR(20),
`gender` CHAR(1),
`in_time` DATETIME
);

-- 按默认字段插入数据
INSERT INTO `students` VALUE(1,'daguo','guojiang','男',now());

-- 按指定字段插入数据
INSERT INTO `students` (`name`,`nick_name`,`gender`,`in_time`) VALUE('daguo','guojiang','男',now());

-- 按指定字段插入多条数据
INSERT INTO `students` (`name`,`nick_name`,`gender`,`in_time`) VALUES
('daguo2','guojiang','男',now()),
('daguo3','guojiang','男',now())
;


-- 查询所有信息
SELECT * FROM `students`;

-- 查询指定字段的所有信息
SELECT `name`,`nick_name` FROM `students`;

-- 查询指定字段指定地方的信息
SELECT `name`,`nick_name` FROM `students` WHERE `gender`='男';

-- 查询并按指定顺序显示信息,DESC：降序，ASC升序
SELECT `name`,`nick_name` FROM `students` WHERE `gender`='男' ORDER BY `id` DESC/ASC;

-- 查询并分页显示信息，指定起始索引和单页数量
SELECT `name`,`nick_name` FROM `students` WHERE `gender`='男' ORDER BY `id` DESC LIMIT 0,2;

-- 修改单个字段数据
UPDATE `students` SET `gender`='神' WHERE `gender`='男';

-- 修改多个字段数据
UPDATE `students` SET `gender`='男',`nick_name`='果酱' WHERE `id`>3;

-- 删除数据
DELETE FROM `students` WHERE `gender`='男';