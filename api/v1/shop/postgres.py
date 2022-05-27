from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_dict_from_one_row,
    create_list_from_all_rows,
)
# noinspection PyUnresolvedReferences
from ..organizations.postgres import get_user_organization
from ..users.postgres import get_user_info, update_user_point


@provide_cursor
def get_shop_items(org_id: int, host: str, port: str, cursor=None) -> List[Dict]:
    """Получение предметов магазина пользователя"""
    cursor.execute(f"""
        select i.item_id,
               i.item_name,
               i.price,
               'http://{host}:{port}/api/v1/files/?resource_id='|| d.document_id ||'&download=false' document_path
          from ufoffice.dim_item i
          join ufoffice.fct_document d on d.document_id = i.document_id
         where org_id = %(org_id)s;
    """, dict(org_id=org_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def create_item_attachment(
    user_id: int,
    document_name: str,
    img_path: str,
    cursor=None
) -> Dict:
    """Создание вложения"""
    cursor.execute("""
        insert into ufoffice.fct_document (document_name, document_path, document_type_id, uploaded_by)
        values (%(document_name)s, %(img_path)s, 1, %(user_id)s) returning document_id;
    """, dict(
            document_name=document_name,
            user_id=user_id,
            img_path=img_path,
        )
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def create_item(
    item_name: str,
    price: int,
    org_id: int,
    document_id: int,
    cursor=None
) -> None:
    """Создание предмета магазина"""
    cursor.execute("""
        insert into ufoffice.dim_item (item_name, price, org_id, document_id)
        values (%(item_name)s, %(price)s, %(org_id)s, %(document_id)s);
    """, dict(
            item_name=item_name,
            price=price,
            org_id=org_id,
            document_id=document_id,
        )
    )


# TODO patch
@provide_cursor
def update_item(
    image: int,
    price: int,
    org_id: int,
    item_name: str,
    cursor=None
) -> None:
    """Обновление предмета"""
    cursor.execute("""
        update ufoffice.dim_item
           set image = %(image)s, price = %(price)s, org_id = %(org_id)s, item_name = %(item_name)s
         where item_id = %(item_id)s;
    """, dict(
        image=image,
        price=price,
        org_id=org_id,
        item_name=item_name,
        )
    )


@provide_cursor
def delete_item(item_id: int, cursor=None) -> None:
    """Удаление предмета"""
    cursor.execute("""
        delete from ufoffice.dim_item
         where item_id = %(item_id)s;
    """, dict(item_id=item_id)
    )


@provide_cursor
def purchase_item(user_id: int, item_id: int, cursor=None) -> None:
    """Покупка предмета"""
    cursor.execute("""
        insert into ufoffice.fct_item_purchase (item_id, user_id)
        values (%(item_id)s, %(user_id)s);
    """, dict(
            item_id=item_id,
            user_id=user_id,
        )
    )


@provide_cursor
def item_price_info(item_id: int, cursor=None) -> None:
    """Цена предмета"""
    cursor.execute("""
        select price from ufoffice.dim_item where item_id = %(item_id)s;
    """, dict(item_id=item_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)
