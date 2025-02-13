create table order_details(
    order_id char(36) not null,
    username varchar(32),
    product_id int,
    itemcount int default 1,
    date_of_order date default now()::date,
    constraint product_id_fk foreign key (product_id) references product(id) 
)
/*
set random_order_id = uuid_generate_v4();
insert into order_details (order_id,username,product_id,itemcount)
values 
(random_order_id,'abc',12,2)
(random_order_id,'def',7,3)
(random_order_id,'xyz',3,1)
(random_order_id,'qwr',1,7)
*/