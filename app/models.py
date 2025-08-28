from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, TIMESTAMP, Text, ForeignKey, LargeBinary, Enum, Float
from datetime import datetime, timezone, date
from enum import Enum as PyEnum
from datetime import date

class Base(DeclarativeBase):
    pass

class StatusEnum(str,PyEnum):
    do_zrobienia = "Do zrobienia"
    w_trakcie = "W trakcie"
    zakonczono = "Zakończono"
    anulowano = "Anulowano"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    diary_entries: Mapped[list["DiaryEntry"]] = relationship("DiaryEntry", back_populates="user", cascade="all, delete")
    goal_entries: Mapped[list["GoalEntry"]] = relationship("GoalEntry", back_populates="user", cascade="all, delete")
    measure_entries: Mapped[list["MeasurementEntry"]] = relationship("MeasurementEntry", back_populates="user", cascade="all, delete")

class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    entry_date: Mapped[date] = mapped_column(Date,nullable=True)
    folder_name: Mapped[str] = mapped_column(String) 
    description: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="diary_entries")
    images: Mapped[list["EntryImage"]] = relationship("EntryImage", back_populates="diary_entry", cascade="all, delete")


class EntryImage(Base):
    __tablename__ = "entry_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    diary_entry_id: Mapped[int] = mapped_column(ForeignKey("diary_entries.id", ondelete="CASCADE"))
    image_path: Mapped[str] = mapped_column(String)

    diary_entry: Mapped["DiaryEntry"] = relationship("DiaryEntry", back_populates="images")


class GoalEntry(Base):
    __tablename__ = "goals_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    goal: Mapped[str] = mapped_column(Text, nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, default=date.today)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.do_zrobienia,nullable=False)

    user: Mapped["User"] = relationship("User", back_populates='goal_entries')
    def __repr__(self):
        return f"<GoalEntry(id={self.id}, user_id={self.user_id}, goal='{self.goal}', date={self.entry_date}, priority={self.priority})>"

class MeasurementEntry(Base):
    __tablename__ = "measurement_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    waga: Mapped[Float] = mapped_column(Float, nullable=False)
    pas: Mapped[int] = mapped_column(Integer, nullable=False)
    posladek: Mapped[int] = mapped_column(Integer,nullable=False)
    klatka: Mapped[int] = mapped_column(Integer,nullable=False)
    udo_l: Mapped[int] = mapped_column(Integer, nullable=False)
    udo_p: Mapped[int] = mapped_column(Integer, nullable=False)
    lydka_l: Mapped[int] = mapped_column(Integer, nullable=False)
    lydka_p: Mapped[int] = mapped_column(Integer,nullable=False)
    biceps_l: Mapped[int] = mapped_column(Integer, nullable=False)
    biceps_p: Mapped[int] = mapped_column(Integer, nullable=False)
    entry_date: Mapped[date] = mapped_column(Date,)
    folder_name: Mapped[str] = mapped_column(String) 
    user: Mapped['User'] = relationship('User', back_populates='measure_entries')
    measure_image : Mapped[list["MeasurementImage"]] = relationship("MeasurementImage", back_populates="measurement_image", )

class MeasurementImage(Base):
    __tablename__ = "measurement_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    measurement_entry_id: Mapped[int] = mapped_column(ForeignKey("measurement_entries.id", ondelete="CASCADE"))
    image_path: Mapped[str] = mapped_column(String)

    measurement_image: Mapped['MeasurementEntry'] = relationship('MeasurementEntry', back_populates="measure_image",cascade="all, delete")