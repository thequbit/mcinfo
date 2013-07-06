drop database mcinfodb;
create database mcinfodb;

grant usage on monroeminutesdb.* to mcinfouser identified by 'password123%%%';

grant all privileges on mcinfodb.* to mcinfouser;

use mcinfodb;

create table communities(
communityid int not null auto_increment primary key,
name varchar(127) not null,
hrid int not null
);

create table streets(
streetid int not null auto_increment primary key,
rawname varchar(127) not null,
name varchar(127) not null,
streettype varchar(63) not null,
communityid int not null,
foreign key (communityid) references communities(communityid)
);

