# Initial Idea

## Project Structure

```txt
project-root/
│
├── pyproject.toml # or requirements.txt
├── README.md
├── .env # DB credentials, Ollama host, etc.
│
├── src/
│ ├── cli/
│ │ ├── main.py # CLI entrypoint
│ │ └── commands/ # Subcommands (parse, rank, etc.)
│ │
│ ├── core/ # Business logic layer
│ │ ├── resume_parser.py
│ │ ├── jd_processor.py
│ │ ├── ranker.py
│ │ ├── star_manager.py
│ │ ├── resume_generator.py
│ │ └── models.py # Pydantic models for structured data
│ │
│ ├── llm/
│ │ ├── ollama_client.py
│ │ ├── prompts/
│ │ │ ├── extract_keywords.txt
│ │ │ ├── summarize_resume.txt
│ │ │ ├── star_selection.txt
│ │ │ ├── star_rewrite.txt
│ │ │ ├── latex_resume_gen.txt
│ │ │ └── rank_resume.txt
│ │ └── embeddings.py
│ │
│ ├── storage/
│ │ ├── db.py # DB connection pool
│ │ ├── repositories/ # CRUD operations
│ │ │ ├── resume_repo.py
│ │ │ ├── jd_repo.py
│ │ │ ├── star_repo.py
│ │ │ └── match_repo.py
│ │ └── migrations/ # Alembic migrations
│ │
│ ├── resume/ # Resume-specific utilities
│ │ ├── pdf_reader.py
│ │ ├── text_cleaner.py
│ │ └── skill_extractor.py
│ │
│ ├── api/ # Future expansion (FastAPI)
│ │ ├── main.py
│ │ └── routes/
│ │
│ └── web/ # Future UI (React, Svelte, etc.)
│
├── resume/
│ │ ├── latex/
│ │ └── output/
│
└── tests/
├── test_resume_parser.py
├── test_llm.py
└── test_ranker.py
```

## Data Entities

```txt
users
  ├── static_section_entries
  ├── star_metadata
  │     └── star_entries
  └── resumes
        └── resume_static_entry_map
        └── resume_sections
            └── resume_section_entries
resume_entry_star_map
  ├── star_entries
  └── resume_section_entries
resume_static_entry_map
  ├── resumes
  └── static_section_entries
job_descriptions
  └── job_parsed
matches (links resumes ↔ job_descriptions)
```

### Example of SQL

```sql

embeddings (
  id,
  source_type (star_entry, jd_parsed, resume_section, static_entry),
  embedding_type TEXT CHECK (embedding_type IN ('semantic', 'skills', 'context'))
  source_id,
  content TEXT,
  embedding vector(1536),  -- OpenAI/Ollama embedding dimension
  model_version TEXT,
  created_at
)

skill_embeddings (
  id,
  skill_name,
  embedding vector(1536),     -- semantic position in skill space
  category TEXT,              -- frontend, cloud, data, etc.
  user_proficiency NUMERIC,   -- inferred from JD matches
  created_at
)

llm_context_cache (
  id,
  user_id,
  context_window TEXT,        -- serialized user's STAR entries + skills
  embedding vector(1536),     -- hash of the context
  prompt_version TEXT,
  created_at
)

CREATE TABLE star_metadata (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    metadata_type TEXT NOT NULL CHECK (metadata_type IN ('experience', 'education', 'project', 'volunteer'))
    title TEXT,                   -- job title, degree, project name
    subtitle TEXT,                -- company, school, etc.
    location TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE star_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    metadata_id INTEGER REFERENCES star_metadata(id) ON DELETE CASCADE, -- Only allow metadata_id for experience-type sections
    title TEXT,  -- oneliner
    situation TEXT NOT NULL,
    task TEXT NOT NULL,
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    skills TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE static_section_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    entry_type TEXT NOT NULL,     -- "education", "certification", "skills", etc.
    content JSONB NOT NULL,       -- structured data
    position INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
-- Education
--{
--  "degree": "BSc Computer Science",
--  "institution": "MIT",
--  "start_date": "2018-09",
--  "end_date": "2022-06",
--  "gpa": "3.8"
--}
-- Certifications
--{
--  "name": "AWS Solutions Architect Associate",
--  "year": 2023
--}

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT,
    raw_latex TEXT,
    raw_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE resume_static_entry_map (
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    static_entry_id INTEGER REFERENCES static_section_entries(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL,   -- "education", "certification", etc.
    position INTEGER,
    PRIMARY KEY (resume_id, static_entry_id)
);


CREATE TABLE resume_sections (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL,   -- "experience", "education", "projects", etc.
    position INTEGER
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE resume_section_entries (
    id SERIAL PRIMARY KEY,
    section_id INTEGER REFERENCES resume_sections(id) ON DELETE CASCADE,
    metadata_id INTEGER REFERENCES star_metadata(id) ON DELETE CASCADE,
    content JSONB,                 -- LLM‑generated or parsed bullet points
    created_at TIMESTAMP DEFAULT NOW()
);
-- content example:
--{
--  "bullets": [
--    "Improved system performance by 40%",
--    "Reduced server load by 25%"
--  ]
--}

CREATE TABLE resume_entry_star_map (
    entry_id INTEGER REFERENCES resume_section_entries(id) ON DELETE CASCADE,
    star_id INTEGER REFERENCES star_entries(id) ON DELETE CASCADE,
    PRIMARY KEY (entry_id, star_id)
    rewritten_star_content JSONB
);


CREATE TABLE job_descriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title TEXT,
    raw_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE job_parsed (
    id SERIAL PRIMARY KEY,
    jd_id INTEGER REFERENCES job_descriptions(id) ON DELETE CASCADE,
    UNIQUE (jd_id)
    embedding_id INTEGER REFERENCES embeddings(id)
    summary TEXT,
    required_skills TEXT[],
    preferred_skills TEXT[],
    responsibilities TEXT[],
    seniority TEXT,
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Match Explanation via RAG
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    jd_id INTEGER REFERENCES job_descriptions(id) ON DELETE CASCADE,
    score NUMERIC(5,2),           -- 0–100
    missing_skills TEXT[],
    llm_analysis TEXT,            -- explanation from LLM
    created_at TIMESTAMP DEFAULT NOW()
    UNIQUE (resume_id, jd_id)
    match_features JSONB
);
-- match_features (make system explainable) example:
--{
--  "cosine similarity":
--  "keyword_overlap": []
--  "skill_coverage":
--  "seniority_match":
--}

```

## Ideas

### Problem with creating resume N+1 queries

```sql
CREATE VIEW resume_complete AS
SELECT
  r.*,
  rs.section_type, rs.position as section_pos,
  rse.content as entry_content,
  se.title as star_title, se.situation, se.task, se.action, se.result,
  sm.title as metadata_title, sm.subtitle, sm.start_date, sm.end_date
FROM resumes r
LEFT JOIN resume_sections rs ON r.id = rs.resume_id
LEFT JOIN resume_section_entries rse ON rs.id = rse.section_id
LEFT JOIN resume_entry_star_map resm ON rse.id = resm.entry_id
LEFT JOIN star_entries se ON resm.star_id = se.id
LEFT JOIN star_metadata sm ON se.metadata_id = sm.id;
```

## 20% / 80%

### The 20 % that makes 80 % of the user experience

1. Reliable resume & star data model
   - If users can’t enter/organise their STAR stories and static sections without bugs or loss, nothing else matters.
   - A clear, robust schema (and repository methods) that let you fetch, update and delete resumes and their linked star entries fast.

2. Fast, deterministic ranking pipeline
   - The ranker/match_repo logic that turns a JD + a resume into a score and explanation must work every time and scale to dozens of resumes.
   - Poor performance or inconsistent scores equals “doesn’t work” for real hiring use‑cases.

3. LLM integration & prompt management
   - Calls to ollama_client (or whichever provider) must succeed, handle errors, and respect token/context limits.
   - Having sane default prompts, versioning and a way to cache embeddings or context is key—without that the system is expensive and unpredictable.

4. Embeddings / semantic search (pgvector)
   - Being able to quickly find the relevant STARs for a JD is what separates this from “copy‑paste job”.
   - Without vector support you end up rewriting every bullet for every job, which isn’t usable at scale.

5. Simple CLI/API for core workflows
   - parse-jd, parse-resume, rank – if these commands are flaky or require manual DB hacks, users abandon the tool.
   - Clean error messages and logging here are worth more than fancy UI.

6. Data consistency & migrations
   - If schema changes break existing resumes or embeddings, the whole service is unreliable.
   - A migration strategy that handles new columns (e.g. updated_at, vector indexes) and re‑embeds old data is critical.

### The 80 % that’s “nice to have” but can wait

- Full web UI / React front end
- Advanced resume formatting / LaTeX templates
- Fine‑grained user preferences, themes, “smart defaults”
- Extensive audit logs, soft deletes, version history
- Skill graph analytics, proficiency inference
- RAG‑style match explanations and few‑shot examples
- Support for multiple LLM providers or on‑device models
- FastAPI endpoints for external integrations
- Detailed A/B testing framework for prompts
- Multi‑user collaboration and sharing
- Mobile app, notifications, scheduling
- Complete unit/integration test coverage for every edge case
- Automatic PDF parsing / OCR improvements
- Internationalisation, currency/dates handling
- CI/CD pipelines, deployment scripts
