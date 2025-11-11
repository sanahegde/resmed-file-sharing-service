from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import String, BigInteger

Base = declarative_base()

class FileMeta(Base):
    __tablename__ = "files"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)     # original filename
    path: Mapped[str] = mapped_column(String, nullable=False)     # disk path
    size: Mapped[int] = mapped_column(BigInteger, nullable=False) # bytes
    uploaded_at: Mapped[int] = mapped_column(BigInteger, nullable=False) # unix seconds
