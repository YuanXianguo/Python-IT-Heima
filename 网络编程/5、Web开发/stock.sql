create table info(
id int primary key not null auto_increment,
code varchar(20) not null,
short varchar(20) not null,
chg varchar(20) not null,
turnover varchar(20) not null,
price decimal(4,2) not null,
highs decimal(4,2) not null,
time varchar(20) not null
);

insert into info values 
(0, "000007","全新好","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000036","华联控股","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000039","中集集团","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000050","深天马A","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000056","皇庭国际","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000059","中金岭南","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000060","华锦股份","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000426","兴业矿业","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000488","晨鸣纸业","10.01%","4.40%",16.05,14.60,"2017-07-18"),
(0, "000528","柳工","10.01%","4.40%",16.05,14.60,"2017-07-18");


create table focus(
id int not null primary key auto_increment,
note_info varchar(100),
info_id int not null
);

insert into focus values(0,"你确定么",2),(0,"你好",3);


select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info
from info as i inner join focus as f on i.id=f.info_id; 

select * from info where code=%s;

select * from focus where info_id=%s;
select * from info inner join focus on info.code=focus.info_id where info.code=%s;

insert into focus (info_id) values (2);
insert into focus (info_id) select id from info where code=%s;