drop database mcinfodb;
create database mcinfodb;

grant usage on monroeminutesdb.* to mcinfouser identified by 'password123%%%';

grant all privileges on mcinfodb.* to mcinfouser;

use mcinfodb;

create table communities(
communityid int not null auto_increment primary key,
name varchar(128) not null,
hrid int not null
);

create table streets(
streetid int not null auto_increment primary key,
rawname varchar(128) not null,
name varchar(128) not null,
streettype varchar(64) not null,
communityid int not null,
foreign key (communityid) references communities(communityid)
);

create table addresses(
addressid int not null auto_increment primary key,
rawaddress varchar(256) not null,
fulladdress varchar(256) not null,
number int not null,
streetname varchar(256) not null,
streettype varchar(64) not null,
zipcode varchar(8) not null
community varchar(256) not null,
communitytype varchar(64),
county varchar(256) not null,
fullstate varchar(256) not null,
stateabiv varchar(8) not null,
lat double not null,
lng double not null,
);
