CREATE TABLE applications (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	job_id INTEGER NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	applied_date DATETIME NOT NULL, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (user_id, job_id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(job_id) REFERENCES jobs (id)
);

CREATE TABLE candidate_skills (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	skill_name VARCHAR(100) NOT NULL, 
	proficiency_level VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (user_id, skill_name), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE jobs (
	id INTEGER NOT NULL, 
	source_id VARCHAR(80), 
	job_title VARCHAR(160) NOT NULL, 
	company_name VARCHAR(160) NOT NULL, 
	job_description TEXT NOT NULL, 
	required_skills JSON NOT NULL, 
	preferred_skills JSON NOT NULL, 
	location VARCHAR(100) NOT NULL, 
	state VARCHAR(80), 
	min_salary INTEGER, 
	max_salary INTEGER, 
	experience_min FLOAT NOT NULL, 
	experience_max FLOAT, 
	employment_type VARCHAR(50) NOT NULL, 
	industry VARCHAR(80) NOT NULL, 
	education_required VARCHAR(160), 
	posted_date DATE NOT NULL, 
	application_deadline DATE, 
	company_rating FLOAT, 
	active BOOLEAN NOT NULL, 
	is_synthetic BOOLEAN NOT NULL, 
	views INTEGER NOT NULL, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	CHECK (min_salary IS NULL OR min_salary >= 0), 
	CHECK (max_salary IS NULL OR max_salary >= 0), 
	CHECK (min_salary IS NULL OR max_salary IS NULL OR max_salary >= min_salary), 
	CHECK (experience_min >= 0), 
	CHECK (experience_max IS NULL OR experience_max >= experience_min), 
	UNIQUE (source_id)
);

CREATE TABLE recommendation_runs (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	fingerprint VARCHAR(64) NOT NULL, 
	reason VARCHAR(60), 
	profile_summary JSON NOT NULL, 
	weights JSON NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE recommendations (
	id INTEGER NOT NULL, 
	run_id INTEGER NOT NULL, 
	job_id INTEGER NOT NULL, 
	job_title VARCHAR(160) NOT NULL, 
	company_name VARCHAR(160) NOT NULL, 
	overall_score FLOAT NOT NULL, 
	scores JSON NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (run_id, job_id), 
	FOREIGN KEY(run_id) REFERENCES recommendation_runs (id) ON DELETE CASCADE, 
	FOREIGN KEY(job_id) REFERENCES jobs (id)
);

CREATE TABLE resume_drafts (
	id VARCHAR(36) NOT NULL, 
	user_id INTEGER NOT NULL, 
	filename VARCHAR(200) NOT NULL, 
	extracted JSON NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE saved_jobs (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	job_id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (user_id, job_id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(job_id) REFERENCES jobs (id)
);

CREATE TABLE search_events (
	id INTEGER NOT NULL, 
	"query" VARCHAR(160) NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);

CREATE TABLE users (
	id INTEGER NOT NULL, 
	full_name VARCHAR(100) NOT NULL, 
	email VARCHAR(254) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	is_admin BOOLEAN NOT NULL, 
	phone VARCHAR(30), 
	city VARCHAR(80), 
	state VARCHAR(80), 
	country VARCHAR(80), 
	education VARCHAR(180), 
	experience_years FLOAT, 
	experience_summary TEXT, 
	preferred_role VARCHAR(160), 
	preferred_location VARCHAR(160), 
	expected_salary INTEGER, 
	employment_type VARCHAR(50), 
	willing_to_relocate BOOLEAN, 
	certifications TEXT, 
	projects TEXT, 
	career_interests TEXT, 
	resume_text TEXT, 
	resume_filename VARCHAR(200), 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	CHECK (experience_years IS NULL OR experience_years >= 0), 
	CHECK (expected_salary IS NULL OR expected_salary >= 0)
);

CREATE INDEX ix_applications_user_id ON applications (user_id);

CREATE INDEX ix_candidate_skills_user_id ON candidate_skills (user_id);

CREATE INDEX ix_jobs_active ON jobs (active);

CREATE INDEX ix_jobs_company_name ON jobs (company_name);

CREATE INDEX ix_jobs_job_title ON jobs (job_title);

CREATE INDEX ix_jobs_location ON jobs (location);

CREATE INDEX ix_recommendation_runs_user_id ON recommendation_runs (user_id);

CREATE INDEX ix_recommendations_job_id ON recommendations (job_id);

CREATE INDEX ix_recommendations_run_id ON recommendations (run_id);

CREATE INDEX ix_resume_drafts_user_id ON resume_drafts (user_id);

CREATE INDEX ix_saved_jobs_user_id ON saved_jobs (user_id);

CREATE INDEX ix_search_events_created_at ON search_events (created_at);

CREATE UNIQUE INDEX ix_users_email ON users (email);