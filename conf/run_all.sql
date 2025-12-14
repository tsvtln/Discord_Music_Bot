-- how to run: mysql -u root -p < run_all.sql

-- Create database and user
SOURCE create_discord_bot_db.sql;

-- Setup and use db
SOURCE sql/00_setup.sql;

-- Schema and data
SOURCE sql/10_config.sql;
SOURCE sql/20_command_prefixes.sql;
SOURCE sql/30_funny_responses.sql;
SOURCE sql/40_gifs.sql;
SOURCE sql/50_presence_states.sql;
SOURCE sql/60_responses.sql;
SOURCE sql/70_fallback_facts.sql;
SOURCE sql/80_keywords.sql;
SOURCE sql/90_allowed_commands.sql;
SOURCE sql/95_list_of_commands.sql;
SOURCE sql/97_lucky_list.sql;
SOURCE sql/98_misc.sql;

