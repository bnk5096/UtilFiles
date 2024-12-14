.echo on

.load ../libmergestat.so

DROP TABLE IF EXISTS commit_data;
DROP TABLE IF EXISTS blame_data;
DROP TABLE IF EXISTS filepaths_task;

SELECT COUNT(*) FROM filepaths;
SELECT datetime();

CREATE TABLE filepaths_task AS
  SELECT filepath FROM filepaths
  ORDER BY filepath
  LIMIT 50 OFFSET :offset
;

SELECT COUNT(*) FROM filepaths_task;
SELECT filepath FROM filepaths_task LIMIT 1;
SELECT datetime();

CREATE TABLE commit_data AS
  SELECT hash, author_email from commits(:repo);

CREATE UNIQUE INDEX commit_hash_idx ON commit_data(hash);

SELECT COUNT(*) as commit_count FROM commit_data;
SELECT datetime();

CREATE TABLE blame_data AS
SELECT filepaths_task.filepath,
       blame.line_no,
       blame.commit_hash,
       commit_data.author_email
FROM filepaths_task,
     blame(:repo,'HEAD',filepaths_task.filepath) 
     JOIN commit_data ON commit_data.hash = blame.commit_hash
    ;

SELECT COUNT(*) FROM blame_data;
SELECT datetime();
