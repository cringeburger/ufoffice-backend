from typing import Dict, Optional

from ..middleware.utils import (
    provide_cursor,
    create_dict_from_one_row,
)


@provide_cursor
def get_document_type(document_id: int, cursor=None) -> Optional[Dict]:
    """Получение типа документа"""
    cursor.execute("""
        select dt.document_type_name
          from ufoffice.fct_document d
          join ufoffice.dim_document_type dt on dt.document_type_id = d.document_type_id 
         where d.document_id = %(document_id)s;
    """, dict(document_id=document_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def get_document_path(document_id: int, cursor=None) -> Optional[Dict]:
    """Получение пути документа и содержимого"""
    cursor.execute("""
        select d.document_path || d.document_name filepath, d.inner_document_text, d.document_name
          from ufoffice.fct_document d
         where d.document_id = %(document_id)s;
    """, dict(document_id=document_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)
