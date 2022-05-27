from pygost.gost34112012 import GOST34112012


def pass_hash(password: str) -> str:
    """Хэширование пароля по алгоритму ГОСТ-3411 2012"""
    hash = GOST34112012(
        digest_size=512,
        data=bytes(password, encoding='utf-8')
    )
    return hash


def hash_check(hash: str, password: str) -> bool:
    """Проверка хэша"""
    hash_pass = GOST34112012(
        digest_size=512,
        data=bytes(password, encoding='utf-8')
    )
    
    return hash == hash_pass.hexdigest()
