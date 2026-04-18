from pydoc import describe
from typing import Optional

from fastapi import FastAPI, Body, Path, Query , HTTPException
from starlette import status
from pydantic import BaseModel , Field

app = FastAPI()
from books import BOOKS, Book


@app.get("/books", status_code = status.HTTP_200_OK)
async def readAllBooks():
    return BOOKS

@app.get("/books/publish", status_code = status.HTTP_200_OK)
async def getPublishBook(givenDate: int = Query(gt = 1999, lt = 2035)):
    tmpBook = []
    for book in BOOKS:
        if book.publish_date == givenDate:
            tmpBook.append(book)
    return tmpBook

@app.get("/books/{book_id}", status_code = status.HTTP_200_OK)
async def getBook(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail = "Book not found")

@app.get("/books/", status_code = status.HTTP_200_OK)
async def getBook(book_rating: int = Query(gt = 0, lt = 6)):
    tmpBook = []
    ok = False
    for book in BOOKS:
        if book.rating == book_rating:
            ok = True
            tmpBook.append(book)
    if ok :
       return tmpBook
    else:
        raise HTTPException(status_code=404, detail = "Book not found")



class BookRequest(BaseModel):
    id: Optional[int] = Field(description="No need to insert any id" , default = None)
    tittle : str = Field(min_length = 4 )
    author: str = Field(min_length = 3 )
    description : str = Field(min_length = 3 , max_length= 100)
    rating : int = Field(gt = 1 , lt = 10)
    publish_date: int = Field(gt = 1999 , lt = 2035)

    model_config = { # set the default expected value
        "json_schema_extra":{
            "example":{
                "tittle" :" Sleep baby ",
                "author":"Akbar Ali Sah",
                "description":" Only sleep should be main goal",
                "rating":10,
                "publish_date": 2026
            }
        }
    }

@app.post("/create_book", status_code = status.HTTP_201_CREATED)
async def createBook(get_book : BookRequest):
    newBook = Book(**get_book.model_dump())
    BOOKS.append(book_id(newBook))

def book_id(book : Book):
    if len(BOOKS) > 0 :
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateBook(givenBook : BookRequest):
    addBook = Book(**givenBook.model_dump())
    ok = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == addBook.id :
            ok = True
            BOOKS[i] = addBook
    if not ok :
        raise HTTPException(status_code=404, detail = "Book id not exist")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateBook(book_id : int = Path(gt = 0)):
    ok = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id :
            ok = True
            BOOKS.pop(i)
            break
    if not ok :
        raise HTTPException(status_code=404, detail = "Book id not exist")
