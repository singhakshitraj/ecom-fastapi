create table user_details(
    users varchar(32) primary key,
    address_id bigserial,
    name varchar(50),
    phone char(10) not null,
    constraint username_fk foreign key (users) references users(username),
    constraint address_fk foreign key (address_id) references user_address(id)
)