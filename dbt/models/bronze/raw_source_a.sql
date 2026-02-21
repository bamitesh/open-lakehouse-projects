-- Bronze model: raw source data landed as-is from ingestion.
-- Replace the source() reference with your actual source definition.

{{ config(materialized='table', tags=['bronze']) }}

select *
from {{ source('raw', 'source_a') }}
