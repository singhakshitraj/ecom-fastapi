create table user_cart(
    username varchar(32),
    product_id int,
    itemcount int default 1,
    primary key (username,product_id),
    constraint username_fk foreign key (username) references users(username),
    constraint product_id_fk foreign key (product_id) references product(id)
)