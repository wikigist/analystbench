INSERT INTO customers (
    customer_id,
    signup_date,
    region,
    customer_status
)
VALUES
    ('C001', '2025-01-10', 'North West', 'active'),
    ('C002', '2025-03-14', 'London', 'active'),
    ('C003', '2025-06-22', 'Scotland', 'active'),
    ('C004', '2025-08-05', 'Midlands', 'inactive');



INSERT INTO accounts (
    account_id,
    customer_id,
    account_open_date,
    account_status,
    account_type
)
VALUES
    ('A001', 'C001', '2025-01-12', 'active', 'current'),
    ('A002', 'C001', '2025-02-01', 'active', 'savings'),
    ('A003', 'C002', '2025-03-20', 'active', 'current'),
    ('A004', 'C003', '2025-07-01', 'active', 'current');



INSERT INTO payments (
    payment_id,
    account_id,
    payment_date,
    amount,
    payment_status,
    payment_method
)
VALUES
    ('P001', 'A001', '2026-09-03', 120.00, 'successful', 'card'),
    ('P002', 'A001', '2026-09-10', 75.50, 'failed', 'card'),
    ('P003', 'A002', '2026-09-15', 200.00, 'successful', 'bank_transfer'),
    ('P004', 'A003', '2026-09-18', 95.25, 'successful', 'card'),
    ('P005', 'A004', '2026-09-21', 50.00, 'failed', 'direct_debit');



INSERT INTO refunds (
    refund_id,
    payment_id,
    refund_date,
    refund_amount,
    refund_status
)
VALUES
    ('R001', 'P001', '2026-09-05', 60.00, 'completed'),
    ('R002', 'P001', '2026-09-08', 40.00, 'completed'),
    ('R003', 'P004', '2026-09-20', 20.00, 'pending');



INSERT INTO queues (
    queue_id,
    queue_name,
    queue_type
)
VALUES
    ('Q001', 'General Enquiries', 'general'),
    ('Q002', 'Payments', 'specialist'),
    ('Q003', 'Complaints', 'specialist'),
    ('Q004', 'Retentions', 'specialist');



INSERT INTO contact_events (
    contact_id,
    customer_id,
    channel,
    contact_reason,
    started_at,
    ended_at
)
VALUES
    ('CT001', 'C001', 'phone', 'payment issue', '2026-09-10 10:00:00', '2026-09-10 10:18:00'),
    ('CT002', 'C001', 'chat', 'payment issue', '2026-09-11 09:00:00', '2026-09-11 09:12:00'),
    ('CT003', 'C001', 'phone', 'complaint', '2026-09-15 14:00:00', '2026-09-15 14:22:00'),
    ('CT004', 'C002', 'email', 'general enquiry', '2026-09-18 11:00:00', '2026-09-18 11:10:00'),
    ('CT005', 'C003', 'phone', 'payment issue', '2026-09-21 16:00:00', '2026-09-21 16:15:00'),
    ('CT006', 'C003', 'phone', 'complaint', '2026-09-22 13:00:00', '2026-09-22 13:30:00'),
    ('CT007', 'C004', 'chat', 'general enquiry', '2026-09-25 12:00:00', '2026-09-25 12:08:00');



INSERT INTO agent_interactions (
    interaction_id,
    contact_id,
    queue_id,
    agent_id,
    started_at,
    ended_at,
    interaction_outcome
)
VALUES
    ('I001', 'CT001', 'Q001', 'AG001', '2026-09-10 10:00:00', '2026-09-10 10:04:00', 'transferred'),
    ('I002', 'CT001', 'Q002', 'AG002', '2026-09-10 10:04:00', '2026-09-10 10:18:00', 'resolved'),

    ('I003', 'CT002', 'Q002', 'AG003', '2026-09-11 09:00:00', '2026-09-11 09:12:00', 'resolved'),

    ('I004', 'CT003', 'Q001', 'AG004', '2026-09-15 14:00:00', '2026-09-15 14:05:00', 'transferred'),
    ('I005', 'CT003', 'Q003', 'AG005', '2026-09-15 14:05:00', '2026-09-15 14:22:00', 'resolved'),

    ('I006', 'CT004', 'Q001', 'AG001', '2026-09-18 11:00:00', '2026-09-18 11:10:00', 'resolved'),

    ('I007', 'CT005', 'Q002', 'AG002', '2026-09-21 16:00:00', '2026-09-21 16:15:00', 'resolved'),

    ('I008', 'CT006', 'Q001', 'AG004', '2026-09-22 13:00:00', '2026-09-22 13:07:00', 'transferred'),
    ('I009', 'CT006', 'Q003', 'AG005', '2026-09-22 13:07:00', '2026-09-22 13:30:00', 'resolved'),

    ('I010', 'CT007', 'Q001', 'AG006', '2026-09-25 12:00:00', '2026-09-25 12:08:00', 'resolved');