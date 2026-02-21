-- Gold model: business-ready aggregated dataset.

{{ config(materialized='table', tags=['gold']) }}

with silver as (
    select * from {{ ref('stg_source_a') }}
)

-- Add your business aggregations here.
select *
from silver
