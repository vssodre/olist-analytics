with source as (

    select * from {{ source('olist', 'order_payments') }}

),

renamed as (

    select
        order_id || '-' || cast(payment_sequential as varchar) as payment_key,
        order_id,
        payment_sequential,
        payment_type,
        payment_installments as installments,
        cast(payment_value as decimal(18, 2)) as payment_value
    from source

)

select * from renamed