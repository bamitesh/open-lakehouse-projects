-- Generic dbt test: assert that a column contains only values from an expected list.
{% test accepted_values_list(model, column_name, values) %}
select {{ column_name }}
from {{ model }}
where {{ column_name }} not in ({{ values | join(', ') }})
{% endtest %}
