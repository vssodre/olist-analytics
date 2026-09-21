with source as (

    select * from {{ source('olist', 'order_items') }}

),

renamed as (

    select
        order_id || '-' || cast(order_item_id as varchar) as order_item_key,
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date as shipping_limit_at,
        cast(price as decimal(18, 2)) as price,
        cast(freight_value as decimal(18, 2)) as freight_value
    from source

)

select * from renamed