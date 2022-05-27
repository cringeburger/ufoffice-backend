create schema ufoffice;

-- Группы достижений
create table ufoffice.dim_achievement_group(
	achievement_group_id serial primary key,
	achievement_group_name varchar(500)
);

-- Достижения
create table ufoffice.dim_achievement(
	achievement_id serial primary key,
	achievement_name varchar(100),
	achievement_desc varchar(250),
	achievement_end_point smallint,
	achievement_group_id int references ufoffice.dim_achievement_group(achievement_group_id),
	achievement_image varchar(500)
);

-- Роли пользователей
create table ufoffice.dim_user_role(
	user_role_id serial primary key,
	user_role_name varchar(100),
	user_role_sysname varchar(100) default 'N/D'
);

-- Профессии
create table ufoffice.dim_profession(
	profession_id serial primary key,
	profession_name varchar(200)
);

-- Пользователи
create table ufoffice.users(
	user_id serial primary key,
	username varchar(100) unique,
	user_sex varchar(1),
	user_birthday date,
	user_password varchar(1000),
	user_fio varchar(300),
	user_mail varchar(100),
	user_vk varchar(100),
	user_tg varchar(100),
	user_facebook varchar(100),
	user_role_id int references ufoffice.dim_user_role(user_role_id),
	user_rating smallint,
	user_image varchar(1000),
	user_status varchar(200),
	profession_id int references ufoffice.dim_profession(profession_id),
	user_phone varchar(100)
);

-- Типы организаций
create table ufoffice.dim_orgatization_type(
	org_type_id serial primary key,
	org_type_name varchar(200)
);

-- Организации
create table ufoffice.organization(
	org_id serial primary key,
	org_type_id int references ufoffice.dim_orgatization_type(org_type_id),
	org_name varchar(100),
	legal_entity varchar(150),
	org_desc varchar(300),
	org_image varchar(1500)
);

-- Команды
create table ufoffice.team(
	team_id serial primary key,
	org_id int references ufoffice.organization(org_id),
	team_name varchar(100),
	team_desc varchar(300),
	team_image varchar(1500)
);

-- Члены команды
create table ufoffice.map_team_participants(
	team_prt_id serial primary key,
	user_id int references ufoffice.users(user_id),
	team_id int references ufoffice.team(team_id)
);


-- Прогресс достижений
create table ufoffice.fct_user_achievement(
	user_achievement_id serial primary key,
	user_id int references ufoffice.users(user_id),
	achievement_id int references ufoffice.dim_achievement(achievement_id),
	progress int,
	ach_status bool default false
);


-- Группы навыков
create table ufoffice.dim_skill_group(
	skill_group_id serial primary key,
	skill_group_name varchar(100)
);

-- Навыки
create table ufoffice.dim_skill(
	skill_id serial primary key,
	skill_group_id int references ufoffice.dim_skill_group(skill_group_id),
	skill_name varchar(100),
	skill_img varchar(1500)
);

-- Навыки пользователя 
create table ufoffice.fct_user_skills(
	user_skill_id serial primary key,
	user_id int references ufoffice.users(user_id),
	skill_id int references ufoffice.dim_skill(skill_id)
);

-- Календарь
create table ufoffice.dim_calendar(
	date_id serial primary key,
	date_value date,
	day_num int,
	month_num int,
	year_num int,
	month_name varchar(20)
);

-- Статусы задач (список)
create table ufoffice.dim_task_status_name(
	task_status_name_id serial primary key,
	task_status_name varchar(100),
	task_status_sysname varchar(100)
);

-- Задачи
create table ufoffice.fct_task(
	task_id serial primary key,
	task_name varchar(200),
	create_dttm timestamp default now(),
	last_upd_dttm timestamp default now(),
	task_desc varchar(1000),
	end_dt date,
    task_status_name_id int references ufoffice.dim_task_status_name(task_status_name_id),
    ach_pts int
);


-- Задачи пользователя
create table ufoffice.map_user_tasks(
	user_task_id serial primary key,
	user_id int references ufoffice.users(user_id),
	task_id int references ufoffice.fct_task(task_id)
);

create sequence ufoffice.new_notes_seq start 1;

-- Заметки
create table ufoffice.fct_notes(
	note_id serial primary key,
	note_header varchar(500) default 'new note '||nextval('ufoffice.new_notes_seq'),
	note_body varchar(15000),
	user_id int references ufoffice.users(user_id),
	updated_dttm timestamp default now()
);

create table ufoffice.dim_item(
	item_id serial primary key,
	item_name varchar(500),
	price int,
	org_id int references ufoffice.organization(org_id),
	image varchar(500)
);

create table ufoffice.fct_item_purchase(
	note_id serial primary key,
	item_id int references ufoffice.dim_item(item_id),
	user_id int references ufoffice.users(user_id),
	purchase_dttm timestamp default now(),
	quantity int default 1
);

create table ufoffice.fct_chat_history(
	note_id serial primary key,
	from_user_id int references ufoffice.users(user_id),
	to_user_id int references ufoffice.users(user_id),
	message_dttm timestamp default now(),
	message_text text
);


-- тип документа
create table ufoffice.dim_document_type(
	document_type_id serial primary key,
	document_type_name varchar(100)
);

-- папки
create table ufoffice.fct_document_folder(
	folder_id serial primary key,
	parent_folder_id int,
	folder_name varchar(100),
	created_dttm timestamp default now(),
	org_id int references ufoffice.organization (org_id)
);

create sequence ufoffice.new_doc_seq start 1;

-- документ
create table ufoffice.fct_document(
	document_id serial primary key,
	document_name varchar(100) default 'New item '||nextval('ufoffice.new_doc_seq'),
	document_path varchar(400),
	document_type_id int references ufoffice.dim_document_type(document_type_id),
	inner_document_text text,
	uploaded_by int references ufoffice.users(user_id)
);


-- документ в папке
create table ufoffice.map_folder_document(
	folder_doc_id serial primary key,
	folder_id int references ufoffice.fct_document_folder(folder_id),
	document_id int references ufoffice.fct_document(document_id)
);

create sequence ufoffice.new_folder_seq start 1 no cycle;

create or replace function ufoffice.leaderboard_update() returns trigger
language plpgsql
    as $$
    begin
        if new.task_status_name_id = 3
        then
            update ufoffice.users
            set user_rating = user_rating + new.ach_pts
            where user_id = (
                select distinct
                    user_id
                from
                    ufoffice.map_user_tasks t
                where
                    t.task_id = new.task_id
                );
        end if;
       RETURN NULL;
    end $$

create trigger leaderboard
after update on ufoffice.fct_task
for each row execute function ufoffice.leaderboard_update();
