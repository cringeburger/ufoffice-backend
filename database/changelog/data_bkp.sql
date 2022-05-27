-- liquibase formatted sql

-- changeset ichetverikov:1651911874427-1
INSERT INTO "ufoffice"."dim_user_role" ("user_role_id", "user_role_name", "user_role_sysname") VALUES (1, 'Админ', 'administrator');

-- changeset ichetverikov:1651911874427-2
INSERT INTO "ufoffice"."dim_profession" ("profession_id", "profession_name") VALUES (1, 'Тимлид');

-- changeset ichetverikov:1651911874427-3
INSERT INTO "ufoffice"."users" ("user_id", "username", "user_sex", "user_birthday", "user_password", "user_fio", "user_mail", "user_vk", "user_tg", "user_facebook", "user_role_id", "user_rating", "user_image", "user_status", "profession_id", "user_phone") VALUES (1, 'banan', 'M', '2000-01-01', 'banan', 'banan', 'main@mail.ru', 'vk.com/kek', 't.me/kek', 'fb.com/asdas', 1, 0, 'kekow_keka', 'X', 1, '123321');
INSERT INTO "ufoffice"."users" ("user_id", "username", "user_sex", "user_birthday", "user_password", "user_fio", "user_mail", "user_vk", "user_tg", "user_facebook", "user_role_id", "user_rating", "user_image", "user_status", "profession_id", "user_phone") VALUES (2, 'banan2', 'M', '2000-01-01', 'banan2', 'banan2', 'main@mail.ru', 'vk.com/kek', 't.me/kek', 'fb.com/asdas', 1, 0, 'kekow_keka', 'X', 1, '123321');
INSERT INTO "ufoffice"."users" ("user_id", "username", "user_sex", "user_birthday", "user_password", "user_fio", "user_mail", "user_vk", "user_tg", "user_facebook", "user_role_id", "user_rating", "user_image", "user_status", "profession_id", "user_phone") VALUES (3, 'banan3', 'M', '2000-01-01', 'banan3', 'banan3', 'main@mail.ru', 'vk.com/kek', 't.me/kek', 'fb.com/asdas', 1, 0, 'kekow_keka', 'X', 1, '123321');

-- changeset ichetverikov:1651911874427-4
INSERT INTO "ufoffice"."dim_orgatization_type" ("org_type_id", "org_type_name") VALUES (1, 'IT');

-- changeset ichetverikov:1651911874427-5
INSERT INTO "ufoffice"."organization" ("org_id", "org_type_id", "org_name", "legal_entity", "org_desc", "org_image") VALUES (1, 1, 'ООО "Моя оборона"', 'ООО "Моя оборона"', 'ООО "Моя оборона"', NULL);

-- changeset ichetverikov:1651911874427-6
INSERT INTO "ufoffice"."team" ("team_id", "org_id", "team_name", "team_desc", "team_image") VALUES (1, 1, 'Командлетова', 'Да', NULL);
INSERT INTO "ufoffice"."team" ("team_id", "org_id", "team_name", "team_desc", "team_image") VALUES (2, 1, 'Командлетова2', 'Да', NULL);

-- changeset ichetverikov:1651911874427-7
INSERT INTO "ufoffice"."map_team_participants" ("team_prt_id", "user_id", "team_id") VALUES (1, 1, 1);
INSERT INTO "ufoffice"."map_team_participants" ("team_prt_id", "user_id", "team_id") VALUES (2, 2, 1);
INSERT INTO "ufoffice"."map_team_participants" ("team_prt_id", "user_id", "team_id") VALUES (3, 3, 2);

-- changeset ichetverikov:1651911874427-8
INSERT INTO "ufoffice"."dim_task_status_name" ("task_status_name_id", "task_status_name", "task_status_sysname") VALUES (1, 'Нужно сделать', 'to_do');
INSERT INTO "ufoffice"."dim_task_status_name" ("task_status_name_id", "task_status_name", "task_status_sysname") VALUES (2, 'В работе', 'in_progress');
INSERT INTO "ufoffice"."dim_task_status_name" ("task_status_name_id", "task_status_name", "task_status_sysname") VALUES (3, 'Выполнено', 'done');
INSERT INTO "ufoffice"."dim_task_status_name" ("task_status_name_id", "task_status_name", "task_status_sysname") VALUES (4, 'Просрочено', 'outdate');

-- changeset ichetverikov:1651911874427-9
INSERT INTO "ufoffice"."fct_task" ("task_id", "task_name", "create_dttm", "last_upd_dttm", "task_desc", "end_dt", "task_status_name_id", "ach_pts") VALUES (1, '123', '2022-05-07 09:50:37.472009', '2022-05-07 09:50:37.472009', 'фыв', '2022-07-07', 1, NULL);
INSERT INTO "ufoffice"."fct_task" ("task_id", "task_name", "create_dttm", "last_upd_dttm", "task_desc", "end_dt", "task_status_name_id", "ach_pts") VALUES (2, '321', '2022-05-07 09:50:37.495896', '2022-05-07 09:50:37.495896', 'фыв', '2022-07-07', 1, NULL);
INSERT INTO "ufoffice"."fct_task" ("task_id", "task_name", "create_dttm", "last_upd_dttm", "task_desc", "end_dt", "task_status_name_id", "ach_pts") VALUES (3, 'string', '2022-05-07 11:07:13.655821', '2022-05-07 11:07:13.655821', 'string', '2022-05-07', 1, 10);
INSERT INTO "ufoffice"."fct_task" ("task_id", "task_name", "create_dttm", "last_upd_dttm", "task_desc", "end_dt", "task_status_name_id", "ach_pts") VALUES (4, 'string', '2022-05-07 11:07:32.030544', '2022-05-07 11:07:32.030544', 'string', '2022-05-07', 1, 10);
INSERT INTO "ufoffice"."fct_task" ("task_id", "task_name", "create_dttm", "last_upd_dttm", "task_desc", "end_dt", "task_status_name_id", "ach_pts") VALUES (5, 'string', '2022-05-07 11:10:21.597642', '2022-05-07 11:10:21.597642', 'string', '2022-05-07', 1, 10);

-- changeset ichetverikov:1651911874427-10
INSERT INTO "ufoffice"."map_user_tasks" ("user_task_id", "user_id", "task_id") VALUES (1, 1, 2);
INSERT INTO "ufoffice"."map_user_tasks" ("user_task_id", "user_id", "task_id") VALUES (2, 2, 1);
INSERT INTO "ufoffice"."map_user_tasks" ("user_task_id", "user_id", "task_id") VALUES (3, 2, 4);
INSERT INTO "ufoffice"."map_user_tasks" ("user_task_id", "user_id", "task_id") VALUES (4, 2, 5);

-- changeset ichetverikov:1651911874427-11
INSERT INTO "ufoffice"."fct_notes" ("note_id", "note_header", "note_body", "user_id", "updated_dttm") VALUES (1, 'dad', 'asdsa', 1, '2022-05-05 23:02:32.745685');
INSERT INTO "ufoffice"."fct_notes" ("note_id", "note_header", "note_body", "user_id", "updated_dttm") VALUES (2, 'dada', 'asdas', 1, '2022-05-05 23:02:32.745685');
INSERT INTO "ufoffice"."fct_notes" ("note_id", "note_header", "note_body", "user_id", "updated_dttm") VALUES (4, 'string', 'string', 1, '2022-05-05 23:53:35.021575');

