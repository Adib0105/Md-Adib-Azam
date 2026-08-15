CREATE TABLE customers (
  customer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(190) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE agents (
  agent_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(190) NOT NULL UNIQUE,
  team VARCHAR(80) NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tickets (
  ticket_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  customer_id BIGINT UNSIGNED NOT NULL,
  agent_id BIGINT UNSIGNED NULL,
  subject VARCHAR(200) NOT NULL,
  category ENUM('billing','account','login','delivery','technical','general') NOT NULL DEFAULT 'general',
  priority ENUM('low','normal','high','urgent') NOT NULL DEFAULT 'normal',
  status ENUM('open','pending','resolved','closed') NOT NULL DEFAULT 'open',
  opened_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  first_response_at TIMESTAMP NULL,
  resolved_at TIMESTAMP NULL,
  sla_due_at TIMESTAMP NOT NULL,
  CONSTRAINT fk_ticket_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  CONSTRAINT fk_ticket_agent FOREIGN KEY (agent_id) REFERENCES agents(agent_id),
  CONSTRAINT chk_resolution_order CHECK (resolved_at IS NULL OR resolved_at >= opened_at),
  INDEX idx_ticket_queue (status, priority, sla_due_at),
  INDEX idx_ticket_agent (agent_id, opened_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ticket_messages (
  message_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ticket_id BIGINT UNSIGNED NOT NULL,
  sender_type ENUM('customer','agent','system') NOT NULL,
  message_body TEXT NOT NULL,
  sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_message_ticket FOREIGN KEY (ticket_id)
    REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  INDEX idx_message_ticket_time (ticket_id, sent_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE tags (
  tag_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tag_name VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ticket_tags (
  ticket_id BIGINT UNSIGNED NOT NULL,
  tag_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (ticket_id, tag_id),
  CONSTRAINT fk_ticket_tag_ticket FOREIGN KEY (ticket_id)
    REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  CONSTRAINT fk_ticket_tag_tag FOREIGN KEY (tag_id)
    REFERENCES tags(tag_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE VIEW ticket_sla_status AS
SELECT
  t.ticket_id,
  t.status,
  t.priority,
  t.sla_due_at,
  CASE
    WHEN t.status IN ('resolved','closed') THEN 'completed'
    WHEN CURRENT_TIMESTAMP > t.sla_due_at THEN 'breached'
    ELSE 'within_sla'
  END AS sla_status,
  TIMESTAMPDIFF(MINUTE, t.opened_at, t.first_response_at) AS first_response_minutes
FROM tickets t;

CREATE VIEW agent_performance AS
SELECT
  a.agent_id,
  a.full_name,
  COUNT(t.ticket_id) AS assigned_tickets,
  SUM(t.status IN ('resolved','closed')) AS completed_tickets,
  ROUND(AVG(TIMESTAMPDIFF(MINUTE, t.opened_at, t.first_response_at)), 1) AS avg_first_response_minutes
FROM agents a
LEFT JOIN tickets t ON t.agent_id = a.agent_id
GROUP BY a.agent_id, a.full_name;
