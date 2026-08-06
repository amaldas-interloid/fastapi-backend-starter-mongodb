from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.associations import role_permissions
from app.models.base_model import BaseModelMixin

if TYPE_CHECKING:
    from app.models.permission import Permission
    from app.models.user import User


class Role(BaseModelMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    ) 

    users: Mapped[list["User"]] = relationship(
    back_populates="role",
    )

    permissions: Mapped[list["Permission"]] = relationship(
    secondary=role_permissions,
    back_populates="roles",
    )
    