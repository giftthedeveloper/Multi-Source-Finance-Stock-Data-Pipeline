SELECT 
    currency,
    value as fx_rate
    
  from {{ source('stocks', 'raw_fx_rates') }}
  where value is not null
  and currency is not null
