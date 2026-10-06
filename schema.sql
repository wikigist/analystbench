CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    signup_date DATE,
    region TEXT,
    customer_status TEXT
);


CREATE TABLE accounts (
    account_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    account_open_date DATE,
    account_status TEXT,
    account_type TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE payments (
    payment_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    payment_date DATE,
    amount NUMERIC(10, 2),
    payment_status TEXT,
    payment_method TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)

);



CREATE TABLE refunds (
    refund_id TEXT PRIMARY KEY,
    payment_id TEXT NOT NULL,
    refund_date DATE,
    refund_amount NUMERIC(10, 2),
    refund_status TEXT,
    FOREIGN KEY (payment_id) REFERENCES payments(payment_id)

);



CREATE TABLE contact_events (
    contact_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    channel   TEXT,
    contact_reason TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)

);


CREATE TABLE queues (
    queue_id TEXT PRIMARY KEY,
    queue_name TEXT,
    queue_type TEXT
);



CREATE TABLE agent_interactions (
    interaction_id TEXT PRIMARY KEY,
    contact_id TEXT NOT NULL,
    queue_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    interaction_outcome TEXT,
    FOREIGN KEY (contact_id) REFERENCES contact_events(contact_id),
    FOREIGN KEY (queue_id) REFERENCES queues(queue_id)
);