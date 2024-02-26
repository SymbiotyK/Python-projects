import classes as cl

#Add book to library
LOTR = cl.Book("Lords of the Ring: Team of the Ring","J.R.R. Tolkien",123456,True)
HP = cl.Book("Harry Potter and The Prisoner of Azkaban","J.K. Rolling",123457,True)

#Add users
Tomek = cl.User("Tomek",51,[])
Jola = cl.User("Jola",52,[])

#Actions :P
Tomek.borrow_book(LOTR)
print("---------------------------")
Jola.borrow_book(HP)
print("---------------------------")
Tomek.borrow_book(HP)
print("---------------------------")
Tomek.return_book(HP)
print("---------------------------")
Jola.return_book(HP)
print("---------------------------")
Jola.display_books_borrowed()
print("---------------------------")
Tomek.borrow_book(HP)
print("---------------------------")
Tomek.display_books_borrowed()
print("---------------------------")
Tomek.return_book(HP)
print("---------------------------")
Tomek.return_book(LOTR)
print("---------------------------")
Tomek.display_books_borrowed()

