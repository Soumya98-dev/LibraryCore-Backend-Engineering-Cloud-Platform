from fastapi import FastAPI, HTTPException, status
from starlette.status import HTTP_201_CREATED
from schemas import AuthorCreate, BookCreate
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Author, Book
from database import Base, engine
from schemas import AuthorResponse, BookResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the personal library API project"}


# Author Endpoints
@app.get("/authors", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.get("/authors/{author_id}", response_model=AuthorResponse)
def get_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )
    return author


# POST /authors → validate request → create SQLAlchemy object → save → return response.
@app.post(
    "/authors", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED
)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(name=author.name, country=author.country)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


# Book Endpoints
@app.get("/books", response_model=list[BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found"
        )
    return book


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    author = db.get(Author, book.author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author {book.author_id} not found",
        )
    # new_book = Book(**book.model_dump())
    # Same as below
    new_book = Book(
        title=book.title,
        pages=book.pages,
        published_year=book.published_year,
        author_id=book.author_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
