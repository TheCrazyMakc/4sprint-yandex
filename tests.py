import pytest
from main import BooksCollector


class TestBooksCollector:

    # Фикстура для создания объекта перед каждым тестом
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # 1. Тест на добавление книги
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.get_books_genre()
        assert collector.get_book_genre("Гарри Поттер") == ""

    # 2. Тест: нельзя добавить книгу с именем > 40 символов
    def test_add_new_book_long_name(self, collector):
        long_name = "А" * 41
        collector.add_new_book(long_name)
        assert long_name not in collector.get_books_genre()

    # 3. Тест: нельзя добавить книгу с пустым именем
    def test_add_new_book_empty_name(self, collector):
        collector.add_new_book("")
        assert "" not in collector.get_books_genre()

    # 4. Параметризованный тест на установку жанра
    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_set_book_genre_valid(self, collector, genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert collector.get_book_genre("Книга") == genre

    # 5. Тест: нельзя установить несуществующий жанр
    def test_set_book_genre_invalid(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Роман")
        assert collector.get_book_genre("Книга") == ""

    # 6. Тест: получение книг по жанру (параметризованный)
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Книга1"]),
        ("Ужасы", ["Книга2"]),
        ("Детективы", []),
    ])
    def test_get_books_with_specific_genre(self, collector, genre, expected_books):
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Ужасы")
        
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected_books

    # 7. Тест: получение книг для детей (без возрастного рейтинга)
    def test_get_books_for_children(self, collector):
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        
        children_books = collector.get_books_for_children()
        assert "Детская книга" in children_books
        assert "Страшная книга" not in children_books

    # 8. Тест: добавление книги в избранное
    def test_add_book_in_favorites(self, collector):
        collector.add_new_book("Любимая книга")
        collector.set_book_genre("Любимая книга", "Фантастика")
        collector.add_book_in_favorites("Любимая книга")
        
        favorites = collector.get_list_of_favorites_books()
        assert "Любимая книга" in favorites

    # 9. Тест: нельзя добавить книгу в избранное, если её нет в словаре
    def test_add_book_in_favorites_not_in_books(self, collector):
        collector.add_book_in_favorites("Несуществующая книга")
        assert collector.get_list_of_favorites_books() == []

    # 10. Тест: удаление книги из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        
        assert "Книга" not in collector.get_list_of_favorites_books()

    # 11. Тест: нельзя добавить книгу в избранное дважды
    def test_add_book_in_favorites_twice(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        
        favorites = collector.get_list_of_favorites_books()
        assert favorites.count("Книга") == 1

    # 12. Дополнительный тест: удаление несуществующей книги из избранного
    def test_delete_book_from_favorites_not_exist(self, collector):
        collector.delete_book_from_favorites("Нет такой")
        assert collector.get_list_of_favorites_books() == []