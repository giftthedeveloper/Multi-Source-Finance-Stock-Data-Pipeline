with stocks as (
      select * from {{ ref('stg_stocks') }}
  ),

  ngn_rate as (
      select fx_rate
      from {{ ref('stg_fx_rates') }}
      where currency = 'NGN'
  ),

  final as (
      select
          s.ticker,
          s.date,
          s.close_price                                                      as usd_price,
          ROUND((s.close_price * (select fx_rate from ngn_rate))::numeric, 2) as ngn_price,
          ROUND(
              (
                  (s.close_price - LAG(s.close_price) OVER (PARTITION BY s.ticker ORDER BY s.date))
                  / LAG(s.close_price) OVER (PARTITION BY s.ticker ORDER BY s.date)
                  * 100
              )::numeric, 2
          )                                                                   as pct_daily_change
      from stocks s
  )

  select * from final