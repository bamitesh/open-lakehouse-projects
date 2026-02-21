-- Silver model: cleansed and deduplicated view of the Bronze source.

{{ config(materialized='table', tags=['silver']) }}

with source as (
    select * from {{ ref('raw_source_a') }}
),

deduplicated as (
    select *,
        row_number() over (
            partition by id
            order by _ingested_at desc
        ) as _row_num
    from source
)

select
    * exclude (_row_num)
from deduplicated
where _row_num = 1
