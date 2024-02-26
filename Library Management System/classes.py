class Book:
    def __init__(self,title, author, ISBN, availability):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.availability = availability
    def check_availability(self):
        if self.availability == True:
            print("Książka jest dostępna mordoooooooo.")
            return True
        else:
            print("Ups! Ktoś wypożyczył "+ self.title +".")
            return False
    def borrow_book(self):
        if self.availability == True:
            self.availability = False
            print("Książka została wypożyczona, miłego czytania :).")
        else:
            print("Ups! Ktoś wypożyczył już tą książkę.")
    def return_book(self):
        self.availability = True
    
class User:
    def __init__(self,name,user_id,books_borrowed):
        self.name = name
        self.user_id = user_id
        self.books_borrowed = books_borrowed
    def borrow_book(self,book):
        if book.check_availability() == True:
            print(self.name+" wypożyczył "+book.title+".")
            book.borrow_book()
            self.books_borrowed.append(book.title)
    def return_book(self, book):
        book.return_book()
        for borrowed_book in self.books_borrowed:
            if borrowed_book == book.title:
                self.books_borrowed.remove(borrowed_book)
                print(book.title + " został oddany przez " + self.name + ".")
                return
        print(book.title + " nie jest na liście wypożyczeń " + self.name)
    def display_books_borrowed(self):
        print(self.name + " ma wypożyczone: "+ str(self.books_borrowed))