-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.moderation_status,
    a.rating,
    a.occurred_at
FROM product_reviews AS a
JOIN reviewed_products AS m ON m.review_entity_id = a.review_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (stars)
CREATE OR REPLACE VIEW vw_review_status_summary AS
SELECT
    moderation_status,
    COUNT(*) AS event_count,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(SUM(rating), 2) AS total_rating
FROM product_reviews
GROUP BY moderation_status;

SELECT * FROM vw_review_status_summary
ORDER BY event_count DESC, moderation_status;
