# 🌌 Project TG AI Asistant (DEPRECATED)

**TG AI Asistant** is an AI-powered command center designed to act as the central nervous system for a homelab by autonomously managing finances, resources, and knowledge. It leverages LLM function calling and RAG to transform a simple assistant into a self-auditing network for total personal and technical management.

**TG AI Asistant** is an evolving intelligent ecosystem...

## Key Features

* The bot understands natural language and distributes data across various tables (finance, products, routine, etc.).
* A single phrase (e.g., "Bought milk for 20 DKK") can simultaneously update expenses and product stock status.
* The AI analyzes the context of a question and finds the required information using dynamic filters.

## Tech Stack

* **Language:** Python 3.10+
* **Framework:** [aiogram 3.x](https://docs.aiogram.dev/)
* **AI Engine:** [Groq Cloud SDK](https://console.groq.com/) (Llama 3.3 70B)
* **Database:** SQLite3


## Project Structure

```text
├── ai/
│   └── manager.py       # AI logic and tool handling (Function Calling)
├── database/
│   ├── database.py      # Universal add_record and get_records methods
│   └── schema.sql       # SQL database schema definitions
├── config.py            # Bot settings, AI client initialization
├── main.py              # Entry point, Telegram message handling
├── instructions.json    # System prompt for AI (logic and table descriptions)
├── .env                 # API tokens and private configurations
└── requirements.txt     # Project dependencies
```

## Database Schema

Currently supported modules:
- Finance: Income and expense tracking.
- Products: Shopping lists and inventory (stock).
- Routine: Tracking recurring household tasks.
- Habits: Habit tracker (progress and frequency).
- Events: Calendar events and reminders.
- General Knowledge: Personal knowledge base and notes.

## Roadmap

### Phase 1:

    [x] Universal Database Schema: Support for Finance, Products, Routine, Habits, Events, and Knowledge.
    [x] AI-Driven Data Entry: Autonomous function calling for data routing.
    [x] Multi-Table Search: Context-aware retrieval across all existing tables.

### Phase 2:

    [ ] RAG (Retrieval-Augmented Generation): Implement search across local files and documents to answer questions based on your private data.

    [ ] Self-Monitoring & Auditing: Track and log changes made to local files into SQLite to maintain a full audit trail of your digital environment.

    [ ] Advanced Resource Accounting: Expand tracking logic to include deep analytics for time management and food/pantry inventory.

### Phase 3:

    [ ] Automated Briefings: Scheduled daily/weekly posts including weather forecasts, pending tasks, and habit progress reports.

    [ ] Proactive Reminders: Background notification system for upcoming events and overdue routine tasks.

    [ ] State Management: Tracking the "Bot Resources" (bot_state table) to maintain session continuity and system health.

Built for the Homelab with ❤️
