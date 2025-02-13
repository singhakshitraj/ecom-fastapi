create table user_address(
    id bigserial primary key,
    user_id varchar(32),
    address_line1 varchar(50) not null,
    address_line2 varchar(50),
    constraint user_id_fk foreign key (user_id) references users(username)
)
