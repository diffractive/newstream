CREATE TABLE "user" (
    id VARCHAR(50) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    given_name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    card_number CHAR(16),
    card_expiry DATE,
    card_cvv CHAR(3),
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "payment" (
    id VARCHAR(50) PRIMARY KEY,
    amount VARCHAR(50) NOT NULL,
    currency_code VARCHAR(3) NOT NULL,
    status VARCHAR(255) NOT NULL default 'PENDING',
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "order" (
    id VARCHAR(50) PRIMARY KEY,
    processing_instruction VARCHAR(36) default 'NO_INSTRUCTION',
    purchase_units JSON NOT NULL,
    payment_source JSON NOT NULL,
    intent VARCHAR(50) NOT NULL,
    payer JSON,
    status VARCHAR(255) NOT NULL default 'CREATED',
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "product" (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    type VARCHAR(50) default 'PHYSICAL',
    category VARCHAR(255),
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "plan" (
    id VARCHAR(50) PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL references product(id),
    name VARCHAR(255) NOT NULL,
    billing_cycles JSON NOT NULL,
    payment_preferences JSON NOT NULL,
    status VARCHAR(50) NOT NULL default 'CREATED',
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "subscription" (
    id VARCHAR(50) PRIMARY KEY,
    plan_id VARCHAR(50) NOT NULL references plan(id),
    quantity VARCHAR(50) default '1',
    custom_id VARCHAR(255),
    start_time TIMESTAMP NOT NULL default current_timestamp,
    subscriber JSON,
    billing_info JSON,
    status VARCHAR(255) NOT NULL default 'APPROVAL_PENDING',
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "checkout_session" (
    id VARCHAR(50) PRIMARY KEY,
    subscription_id VARCHAR(50) references subscription(id),
    order_id VARCHAR(50) references "order" (id),
    payment_id VARCHAR(50) references payment(id),
    return_url TEXT NOT NULL,
    cancel_url TEXT NOT NULL,
    status VARCHAR(255) NOT NULL default 'PENDING',
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "webhook" (
    id VARCHAR(50) PRIMARY KEY,
    url TEXT NOT NULL,
    event_types JSON NOT NULL,
    create_time TIMESTAMP NOT NULL default current_timestamp,
    update_time TIMESTAMP NOT NULL
);

CREATE TABLE "oauth_token" (
    id VARCHAR(50) PRIMARY KEY,
    access_token VARCHAR(255) UNIQUE NOT NULL,
    expires_in INTEGER NOT NULL,
    token_type VARCHAR(50) NOT NULL,
    create_time TIMESTAMP NOT NULL default current_timestamp
);
