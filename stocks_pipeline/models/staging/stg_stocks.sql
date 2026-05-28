SELECT 
    date,
    ticker,
    close_price
  
  from {{ source('stocks', 'raw_stocks') }}
  where close_price is not null
  and ticker is not null
  and date is not null