SELECT
      s.date,
      s.ticker,
      s.close_price as close_price_usd,
      fx.currency,
      ROUND((s.close_price * fx.fx_rate)::numeric, 4) as close_price_converted
  from {{ ref('stg_stocks') }} s
  cross join {{ ref('stg_fx_rates') }} fx