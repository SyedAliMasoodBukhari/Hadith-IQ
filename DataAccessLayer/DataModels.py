from sqlalchemy import (
    Column, DateTime, Integer, String, ForeignKey, Table, Text, PrimaryKeyConstraint,JSON
)
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association Tables for Many-to-Many Relationships
book_project = Table(
    'book_project', Base.metadata,
    Column('ProjectID', Integer, ForeignKey('projects.ProjectID', ondelete="CASCADE"), primary_key=True),
    Column('BookID', Integer, ForeignKey('books.BookID', ondelete="CASCADE"), primary_key=True),
    # PrimaryKeyConstraint('ProjectID', 'BookID', name='pk_book_project')
)

hadith_book = Table(
    'hadith_book', Base.metadata,
    Column('BookID', Integer, ForeignKey('books.BookID', ondelete="CASCADE"), primary_key=True),
    Column('HadithID', Integer, ForeignKey('hadiths.HadithID', ondelete="CASCADE"), primary_key=True),
    # PrimaryKeyConstraint('BookID', 'HadithID', name='pk_hadith_book')
)

hadith_project = Table(
    'hadith_project', Base.metadata,
    Column('ProjectID', Integer, ForeignKey('projects.ProjectID', ondelete="CASCADE"), primary_key=True),
    Column('HadithID', Integer, ForeignKey('hadiths.HadithID', ondelete="CASCADE"), primary_key=True),
    # PrimaryKeyConstraint('ProjectID', 'HadithID', name='pk_hadith_project')
)

sanad_project = Table(
    'sanad_project', Base.metadata,
    Column('ProjectID', Integer, ForeignKey('projects.ProjectID', ondelete="CASCADE"), primary_key=True),
    Column('SanadID', Integer, ForeignKey('sanad.SanadID', ondelete="CASCADE"), primary_key=True),
    # PrimaryKeyConstraint('ProjectID', 'SanadID', name='pk_sanad_project')
)

hadith_sanad = Table(
    'hadith_sanad', Base.metadata,
    Column('HadithID', Integer, ForeignKey('hadiths.HadithID', ondelete="CASCADE"), primary_key=True),
    Column('SanadID', Integer, ForeignKey('sanad.SanadID', ondelete="CASCADE"), primary_key=True),
    # PrimaryKeyConstraint('HadithID', 'SanadID', name='pk_hadith_sanad')
)

narrator_sanad = Table(
    'narrator_sanad', Base.metadata,
    Column('SanadID', Integer, ForeignKey('sanad.SanadID', ondelete="CASCADE"), primary_key=True),
    Column('NarratorID', Integer, ForeignKey('narrators.NarratorID', ondelete="CASCADE"), primary_key=True),
    Column('Level', Integer, nullable=False),
    # PrimaryKeyConstraint('SanadID', 'NarratorID', name='pk_narrator_sanad')
)

# Models
class Project(Base):
    __tablename__ = 'projects'
    ProjectID = Column(Integer, primary_key=True, autoincrement=True)
    ProjectName = Column(String(100), nullable=False, unique=True)
    LastUpdated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    CreatedAt = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    books = relationship(
        'Book',
        secondary=book_project,
        back_populates='projects',
        cascade="all, delete"
    )
    hadiths = relationship(
        'Hadith',
        secondary=hadith_project,
        back_populates='projects',
        cascade="all, delete"
    )
    sanads = relationship(
        'Sanad',
        secondary=sanad_project,
        back_populates='projects',
        cascade="all, delete"
    )
    project_state = relationship("ProjectState", back_populates="projects")


    def __repr__(self):
        return f"<Project(ProjectID={self.ProjectID}, ProjectName='{self.ProjectName}', LastUpdated={self.LastUpdated}, CreatedAt={self.CreatedAt})>"

class ProjectState(Base):
    __tablename__ = 'project_state'
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID', ondelete="CASCADE"), primary_key=True)
    Query=Column(String(10,000),nullable=False,unique=True)
    StateData = Column(JSON, nullable=False)

    projects = relationship('Project', back_populates='project_state')

    def __repr__(self):
        return f"<ProjectState(ProjectID={self.ProjectID}, Query={self.Query},StateData='{self.StateData}')>"

class Book(Base):
    __tablename__ = 'books'
    BookID = Column(Integer, primary_key=True, autoincrement=True)
    BookName = Column(String(200), nullable=False, unique=True)

    projects = relationship(
        'Project',
        secondary=book_project,
        back_populates='books'
    )
    hadiths = relationship(
        'Hadith',
        secondary=hadith_book,
        back_populates='books'
    )

    def __repr__(self):
        return f"<Book(BookID={self.BookID}, BookName='{self.BookName}')>"


class Hadith(Base):
    __tablename__ = 'hadiths'
    HadithID = Column(Integer, primary_key=True, autoincrement=True)
    Matn = Column(String(5000), nullable=False, unique=True)
    embeddings = Column(Text, nullable=False)
    cleanedMATN = Column(String(5000), nullable=False)

    projects = relationship(
        'Project',
        secondary=hadith_project,
        back_populates='hadiths'
    )
    books = relationship(
        'Book',
        secondary=hadith_book,
        back_populates='hadiths'
    )
    sanads = relationship(
        'Sanad',
        secondary=hadith_sanad,
        back_populates='hadiths'
    )

    def __repr__(self):
        return f"<Hadith(HadithID={self.HadithID}, Matn='{self.Matn}', cleanedMATN='{self.cleanedMATN}')>"


class Sanad(Base):
    __tablename__ = 'sanad'
    SanadID = Column(Integer, primary_key=True, autoincrement=True)
    Sanad = Column(String(5000), nullable=False, unique=True)
    SanadAuthenticity = Column(Integer, nullable=False)

    projects = relationship(
        'Project',
        secondary=sanad_project,
        back_populates='sanads'
    )
    hadiths = relationship(
        'Hadith',
        secondary=hadith_sanad,
        back_populates='sanads'
    )
    narrators = relationship(
        'Narrator',
        secondary=narrator_sanad,
        back_populates='sanads',
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Sanad(SanadID={self.SanadID}, Sanad='{self.Sanad}', SanadAuthenticity={self.SanadAuthenticity})>"


class Narrator(Base):
    __tablename__ = 'narrators'
    NarratorID = Column(Integer, primary_key=True, autoincrement=True)
    NarratorName = Column(String(200), nullable=False, unique=True)
    NarratorAuthenticity = Column(Integer, nullable=False)

    sanads = relationship(
        'Sanad',
        secondary=narrator_sanad,
        back_populates='narrators'
    )

    def __repr__(self):
        return f"<Narrator(NarratorID={self.NarratorID}, NarratorName='{self.NarratorName}', NarratorAuthenticity={self.NarratorAuthenticity})>"


# # Task progress model
# class Progress(Base):
#     def __init__(self, dbConnection: DbConnection):
#         self.__dbConnection = dbConnection
        
#     __tablename__ = "import_progress"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     task_id = Column(String(50), unique=True, nullable=False)
#     project_name = Column(String(100), nullable=False)
#     progress = Column(Float, default=0.0)

#     # Database configuration
#     def init_db():
#         engine = create_engine(self.__dbConnection.getConnectionUrl())
#         Base.metadata.create_all(engine)
#         Session = sessionmaker(bind=engine)
#         return Session