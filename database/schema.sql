-- 1. FINANCE
CREATE TABLE IF NOT EXISTS finance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    record_type TEXT CHECK(record_type IN ('income', 'expense')) NOT NULL,
    category TEXT,
    comment TEXT,
    date DATETIME DEFAULT (DATETIME('now', 'localtime'))
);

-- 2. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER, 
    item_name TEXT NOT NULL,
    status TEXT DEFAULT 'buy', -- buy, stock, low
    category TEXT,
    last_bought DATETIME
);

-- 3. ROUTINE
CREATE TABLE IF NOT EXISTS routine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    last_done DATETIME,
    frequency_days INTEGER DEFAULT 7,
    comment TEXT
);

-- 4. HABITS
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    habit_name TEXT NOT NULL,
    frequency_per_week INTEGER DEFAULT 3,
    progress_count INTEGER DEFAULT 0,
    last_tracked DATETIME
);

-- 5. EVENTS
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    event_time DATETIME NOT NULL,
    is_shared BOOLEAN DEFAULT 0,
    reminded BOOLEAN DEFAULT 0
);

-- 6. GENERAL_KNOWLEDGE
CREATE TABLE IF NOT EXISTS general_knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    topic TEXT,
    content TEXT,
    is_private BOOLEAN DEFAULT 1,
    updated_at DATETIME DEFAULT (DATETIME('now', 'localtime'))
);

-- 7. LOGS
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER, 
    level TEXT DEFAULT 'INFO', -- INFO, ERROR, WARNING
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT (DATETIME('now', 'localtime'))
);

-- 8. BOT RESOURCES
CREATE TABLE IF NOT EXISTS bot_state (
    user_id INTEGER DEFAULT 0,
    key TEXT NOT NULL,
    value TEXT,
    updated_at DATETIME DEFAULT (DATETIME('now', 'localtime')),
    PRIMARY KEY (user_id, key)
);
