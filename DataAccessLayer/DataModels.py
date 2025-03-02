from sqlalchemy import (
    create_engine, Column, Integer, String, Float, ForeignKey, Table, DateTime, Text, JSON
)
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB  # For better JSON support in PostgreSQL

# Base for models
Base = declarative_base()

# Association Tables for Many-to-Many Relationships
book_project = Table(
    'book_project', Base.metadata,
    Column('projectid', Integer, ForeignKey('projects.projectid', ondelete="CASCADE"), primary_key=True),
    Column('bookid', Integer, ForeignKey('books.bookid', ondelete="CASCADE"), primary_key=True),
)

hadith_book = Table(
    'hadith_book', Base.metadata,
    Column('bookid', Integer, ForeignKey('books.bookid', ondelete="CASCADE"), primary_key=True),
    Column('hadithid', Integer, ForeignKey('hadiths.hadithid', ondelete="CASCADE"), primary_key=True),
)

hadith_project = Table(
    'hadith_project', Base.metadata,
    Column('projectid', Integer, ForeignKey('projects.projectid', ondelete="CASCADE"), primary_key=True),
    Column('hadithid', Integer, ForeignKey('hadiths.hadithid', ondelete="CASCADE"), primary_key=True),
)

sanad_project = Table(
    'sanad_project', Base.metadata,
    Column('projectid', Integer, ForeignKey('projects.projectid', ondelete="CASCADE"), primary_key=True),
    Column('sanadid', Integer, ForeignKey('sanad.sanadid', ondelete="CASCADE"), primary_key=True),
)

hadith_sanad = Table(
    'hadith_sanad', Base.metadata,
    Column('hadithid', Integer, ForeignKey('hadiths.hadithid', ondelete="CASCADE"), primary_key=True),
    Column('sanadid', Integer, ForeignKey('sanad.sanadid', ondelete="CASCADE"), primary_key=True),
)

narrator_sanad = Table(
    'narrator_sanad', Base.metadata,
    Column('sanadid', Integer, ForeignKey('sanad.sanadid', ondelete="CASCADE"), primary_key=True),
    Column('narratorid', Integer, ForeignKey('narrators.narratorid', ondelete="CASCADE"), primary_key=True),
    Column('level', Integer, nullable=False),
)

# Models
class Project(Base):
    __tablename__ = 'projects'
    
    projectid = Column(Integer, primary_key=True, autoincrement=True)
    projectname = Column(String(100), nullable=False, unique=True)
    lastupdated = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    createdat = Column(DateTime, default=lambda: datetime.now(timezone.utc))

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
        return f"<Project(projectid={self.projectid}, projectname='{self.projectname}', lastupdated={self.lastupdated}, createdat={self.createdat})>"

class ProjectState(Base):
    __tablename__ = 'project_state'
    
    projectid = Column(Integer, ForeignKey('projects.projectid', ondelete="CASCADE"), primary_key=True)
    query=Column(String(10,000),nullable=False,unique=True)
    statedata = Column(JSONB, nullable=False)

    projects = relationship('Project', back_populates='project_state')

    def __repr__(self):
        return f"<ProjectState(projectid={self.projectid},query='{self.query}', statedata='{self.statedata}')>"

class Book(Base):
    __tablename__ = 'books'
    
    bookid = Column(Integer, primary_key=True, autoincrement=True)
    bookname = Column(String(200), nullable=False, unique=True)

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
        return f"<Book(bookid={self.bookid}, bookname='{self.bookname}')>"

class Hadith(Base):
    __tablename__ = 'hadiths'
    
    hadithid = Column(Integer, primary_key=True, autoincrement=True)
    matn = Column(String(5000), nullable=False, unique=True)
    embeddings = Column(Text, nullable=False)
    cleanedmatn = Column(String(5000), nullable=False)

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
        return f"<Hadith(hadithid={self.hadithid}, matn='{self.matn}', cleanedmatn='{self.cleanedmatn}')>"

class Sanad(Base):
    __tablename__ = 'sanad'
    
    sanadid = Column(Integer, primary_key=True, autoincrement=True)
    sanad = Column(String(5000), nullable=False, unique=True)
    sanadauthenticity = Column(Integer, nullable=False)

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
        return f"<Sanad(sanadid={self.sanadid}, sanad='{self.sanad}', sanadauthenticity={self.sanadauthenticity})>"

class Narrator(Base):
    __tablename__ = 'narrators'
    
    narratorid = Column(Integer, primary_key=True, autoincrement=True)
    narratorname = Column(String(200), nullable=False, unique=True)
    narratorauthenticity = Column(Integer, nullable=False)

    sanads = relationship(
        'Sanad',
        secondary=narrator_sanad,
        back_populates='narrators'
    )

    def __repr__(self):
        return f"<Narrator(narratorid={self.narratorid}, narratorname='{self.narratorname}', narratorauthenticity={self.narratorauthenticity})>"

# Progress model for tracking task progress
class Progress(Base):
    __tablename__ = "import_progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    taskid = Column(String(50), unique=True, nullable=False)
    projectname = Column(String(100), nullable=False)
    progress = Column(Float, default=0.0)

    # Database configuration for PostgreSQL
    @staticmethod
    def init_db(db_url):
        """
        Initialize the database.
        :param db_url: Database URL (PostgreSQL URL)
        """
        engine = create_engine(db_url)  # Replace with your PostgreSQL connection string
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session

# Example Usage:
# PostgreSQL connection URL
# db_url = "postgresql://username:password@localhost:5432/mydatabase"
# session = Progress.init_db(db_url)
