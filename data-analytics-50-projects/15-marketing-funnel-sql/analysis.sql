-- Marketing Funnel SQL
-- Import ../../datasets/marketing_campaigns.csv as table `marketing_campaigns` before running.

SELECT channel, ROUND(100.0*clicks/impressions,2) ctr_pct, ROUND(100.0*conversions/clicks,2) cvr_pct, ROUND(1.0*spend/conversions,2) cpa, ROUND(1.0*revenue/spend,2) roas FROM marketing_campaigns ORDER BY roas DESC;
