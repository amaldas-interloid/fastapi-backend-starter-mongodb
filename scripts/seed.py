
import asyncio

from app.core.config import settings
from app.core.security import hash_password
from app.db.database import close_mongodb_connection, connect_to_mongodb
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole

PERMISSIONS = [
    {
        "name": "users:read",
        "description": "View users",
    },
    {
        "name": "users:create",
        "description": "Create users",
    },
    {
        "name": "users:update",
        "description": "Update users",
    },
    {
        "name": "users:delete",
        "description": "Delete users",
    },
    {
        "name": "roles:read",
        "description": "View roles",
    },
    {
        "name": "roles:create",
        "description": "Create roles",
    },
    {
        "name": "roles:update",
        "description": "Update roles",
    },
    {
        "name": "roles:delete",
        "description": "Delete roles",
    },
    {
        "name": "permissions:read",
        "description": "View permissions",
    },
    {
        "name": "permissions:manage",
        "description": "Manage permissions",
    },
]


ROLES = [
    {
        "name": "admin",
        "description": "Full system access",
    },
    {
        "name": "manager",
        "description": "User management access",
    },
    {
        "name": "user",
        "description": "Standard user access",
    },
]


ROLE_PERMISSIONS = {
    "admin": [
        "users:read",
        "users:create",
        "users:update",
        "users:delete",
        "roles:read",
        "roles:create",
        "roles:update",
        "roles:delete",
        "permissions:read",
        "permissions:manage",
    ],
    "manager": [
        "users:read",
        "users:update",
        "roles:read",
    ],
    "user": [

    ],
}


SEED_USERS = [
    {
        "email": "admin@example.com",
        "username": "amaldas",
        "first_name": "amal",
        "last_name": "das",
        "role": "admin",
        "is_active": True,
        "is_verified": True,
    },
    {
        "email": "manager@example.com",
        "username": "vikram",
        "first_name": "vikram",
        "last_name": "anna",
        "role": "manager",
        "is_active": True,
        "is_verified": True,
    },
    {
        "email": "jeffy@example.com",
        "username": "jeffy",
        "first_name": "jeffy",
        "last_name": "s",
        "role": "user",
        "is_active": True,
        "is_verified": True,
    },
    {
        "email": "mani@example.com",
        "username": "mani",
        "first_name": "mani",
        "last_name": "s",
        "role": "user",
        "is_active": True,
        "is_verified": True,
    },
    {
        "email": "vijay@example.com",
        "username": "vijay",
        "first_name": "vijay",
        "last_name": "o s",
        "role": "user",
        "is_active": True,
        "is_verified": False,
    },
    {
        "email": "sarah@example.com",
        "username": "sarah",
        "first_name": "Sarah",
        "last_name": "Brown",
        "role": "user",
        "is_active": True,
        "is_verified": True,
    },
    {
        "email": "akshay@example.com",
        "username": "akshay",
        "first_name": "akshay",
        "last_name": "c a",
        "role": "user",
        "is_active": True,
        "is_verified": False,
    },
    {
        "email": "naveen@example.com",
        "username": "naveen",
        "first_name": "naveen",
        "last_name": "s",
        "role": "user",
        "is_active": False,
        "is_verified": True,
    },
]


async def seed_permissions() -> dict[str, Permission]:
    permissions: dict[str, Permission] = {}

    for data in PERMISSIONS:
        permission = await Permission.find_one(
            Permission.name == data["name"],
        )

        if permission is None:
            permission = Permission(**data)
            await permission.insert()

            print(
                f"Created permission: {permission.name}"
            )
        else:
            print(
                f"Permission already exists: "
                f"{permission.name}"
            )

        permissions[permission.name] = permission

    return permissions


async def seed_roles() -> dict[str, Role]:
    roles: dict[str, Role] = {}

    for data in ROLES:
        role = await Role.find_one(
            Role.name == data["name"],
        )

        if role is None:
            role = Role(**data)
            await role.insert()

            print(f"Created role: {role.name}")
        else:
            print(
                f"Role already exists: {role.name}"
            )

        roles[role.name] = role

    return roles


async def seed_role_permissions(
    roles: dict[str, Role],
    permissions: dict[str, Permission],
) -> None:
    for role_name, permission_names in ROLE_PERMISSIONS.items():
        role = roles[role_name]

        for permission_name in permission_names:
            permission = permissions[permission_name]

            existing = await RolePermission.find_one(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id,
            )

            if existing is None:
                await RolePermission(
                    role_id=role.id,
                    permission_id=permission.id,
                ).insert()

                print(
                    f"Assigned '{permission_name}' "
                    f"to '{role_name}'"
                )


async def seed_users(
    roles: dict[str, Role],
) -> None:
    hashed_password = hash_password(
        settings.SEED_DEFAULT_PASSWORD
    )

    for data in SEED_USERS:
        user = await User.find_one(
            User.email == data["email"],
        )

        if user is None:
            user = User(
                email=data["email"],
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                hashed_password=hashed_password,
                is_active=data["is_active"],
                is_verified=data["is_verified"],
            )

            await user.insert()

            print(
                f"Created user: {user.email}"
            )
        else:
            print(
                f"User already exists: {user.email}"
            )

        role = roles[data["role"]]

        existing_user_role = await UserRole.find_one(
            UserRole.user_id == user.id,
            UserRole.role_id == role.id,
        )

        if existing_user_role is None:
            await UserRole(
                user_id=user.id,
                role_id=role.id,
            ).insert()

            print(
                f"Assigned '{data['role']}' role "
                f"to '{user.email}'"
            )
        else:
            print(
                f"Role already assigned to "
                f"'{user.email}'"
            )


async def seed() -> None:
    print("Starting database seed...")

    await connect_to_mongodb()

    try:
        permissions = await seed_permissions()

        roles = await seed_roles()

        await seed_role_permissions(
            roles,
            permissions,
        )

        await seed_users(roles)

        print("Database seeding completed successfully.")

    finally:
        await close_mongodb_connection()


if __name__ == "__main__":
    asyncio.run(seed())
