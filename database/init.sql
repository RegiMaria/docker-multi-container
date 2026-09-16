CREATE TABLE IF NOT EXISTS messages(
	id SERIAL PRIMARY KEY,
	author VARCHAR(100) NOT NULL,
	content TEXT NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Adiciona dados iniciais na tabela messages
INSERT INTO messages(author, content) VALUES
('Project Manager', 'Welcome to the docker learning project messages board!'),
('Support', 'Learn about container, dockerfile, images, volumes and netowrks!');
