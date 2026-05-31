def serialize_user(user) -> dict:
    return {
        "_id": user.id,
        "username": user.username,
        "role": user.role,
        "orders": [],
    }


def serialize_product(product) -> dict:
    return {
        "_id": product.id,
        "title": product.title,
        "description": product.description,
        "price": float(product.price),
        "isActive": bool(product.is_active),
        "image": product.image,
        "createdAt": product.created_at.isoformat(),
    }


def serialize_message(message) -> dict:
    return {
        "_id": message.id,
        "user": message.user,
        "message": message.message,
        "createdAt": message.created_at.isoformat(),
    }