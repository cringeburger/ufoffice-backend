from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_dict_from_one_row,
    create_list_from_all_rows,
)
# noinspection PyUnresolvedReferences
from ..organizations.postgres import get_user_organization


@provide_cursor
def get_folder_resource_info(folder_id: int, org_id: int, cursor=None) -> List[Dict]:
    """Получение ресурсов папки"""
    cursor.execute("""
        select 'folder' as resource_type,
               df.folder_id resource_id,
               df.folder_name resource_name
          from ufoffice.fct_document_folder df
         where df.parent_folder_id = %(folder_id)s and df.org_id = %(org_id)s
         union all
        select dt.document_type_name resource_type,
               fd.document_id,
               fd.document_name
          from ufoffice.fct_document fd 
          left join ufoffice.map_folder_document mfd on fd.document_id = mfd.document_id
          left join ufoffice.dim_document_type dt on dt.document_type_id = fd.document_type_id
         where mfd.folder_id = %(folder_id)s;
    """, dict(
            folder_id=folder_id,
            org_id=org_id,
        )
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def create_folder(parent_folder_id: int, org_id: int, folder_name: str, cursor=None) -> Dict:
    """Получение ресурсов папки"""
    cursor.execute("""
        insert into ufoffice.fct_document_folder(parent_folder_id, folder_name, org_id)
	         values (%(parent_folder_id)s, %(folder_name)s, %(org_id)s)
        returning folder_id;
    """, dict(
            parent_folder_id=parent_folder_id,
            folder_name=folder_name,
            org_id=org_id,
        )
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def select_folder_seq_nextval(cursor=None) -> Dict:
    """Получение названия безымянной папки"""
    cursor.execute("""
        select 'Новая папка '|| nextval('ufoffice.new_folder_seq') as folder_name;
    """)

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def add_attachment_info(
    user_id: int,
    document_name: str,
    document_path: str,
    document_type_name: str,
    inner_document_text: str = None,
    cursor=None
) -> Dict:
    """Добавление файла"""
    cursor.execute("""
        insert into ufoffice.fct_document(
            document_name,
            document_path,
            document_type_id,
            inner_document_text,
            uploaded_by)
        values(
            %(document_name)s,
            %(document_path)s,
            (select document_type_id from ufoffice. dim_document_type where document_type_name = %(document_type_name)s),
            %(inner_document_text)s,
            %(user_id)s
            )
        returning document_id;
    """, dict(
            document_name=document_name,
            document_path=document_path,
            document_type_name=document_type_name,
            inner_document_text=inner_document_text,
            user_id=user_id,
        )
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def add_attachment_folder_mapping(
    folder_id: int,
    document_id: int,
    cursor=None
) -> None:
    """Добавление маппигна файл-папка"""
    cursor.execute("""
        insert into ufoffice.map_folder_document (folder_id, document_id)
             values (%(folder_id)s, %(document_id)s);
    """, dict(
            folder_id=folder_id,
            document_id=document_id,
        )
    )


@provide_cursor
def get_folder_path(folder_id: int, org_id: int, cursor=None) -> Dict:
    """Получение пути папки"""
    cursor.execute("""
        with recursive folders as ( 
            select prnt.folder_id, prnt.parent_folder_id, '/' || prnt.folder_name || '/' as folder_path
              from ufoffice.fct_document_folder prnt
             where parent_folder_id = 0 and org_id = %(org_id)s
            union
            select chld.folder_id, chld.parent_folder_id, folders.folder_path || chld.folder_name || '/'
              from ufoffice.fct_document_folder chld
              join folders on chld.parent_folder_id = folders.folder_id
             where org_id = %(org_id)s
        )
        select folder_path from folders
        where folder_id = %(folder_id)s;
    """, dict(
            org_id=org_id,
            folder_id=folder_id,
        )
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)
