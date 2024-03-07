from etl import extract, transform, load
from utils.log_config import configure_logger

log = configure_logger("main")  # Configuration du logger



class ETLProcess:
    def __init__(self, extractor, transformer):
        self.extractor = extractor
        self.transformer = transformer
        # self.loader = loader

    def execute_etl(self):
        category_urls = self.extractor.get_all_category()
        all_books_data = []
        for category_url in category_urls[:1]:
            books_urls = self.extractor.get_all_books_in_category(category_url)
            for book_url in books_urls:
                book_info = self.extractor.get_book_info(book_url)
                all_books_data.append(book_info)
        print(all_books_data)


if __name__ == "__main__":
    try:
        extractor = extract.Extract(site_url="https://books.toscrape.com")
        transformer = transform.Transform()

        print(test)

        # etl_process = ETLProcess(extractor, transformer)
        # etl_process.execute_etl()

    except Exception as e:
        print(f"Erreur : {e}")
