create table product(
    id bigserial primary key,
    name varchar(32) not null,
    product_category_id bigserial,
    price double precision not null,
    available_items int not null default 0,
    constraint product_category_fk foreign key (product_category_id) references product_category(id)
)