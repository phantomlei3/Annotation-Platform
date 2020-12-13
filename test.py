from PostgreSQL.database import database
import hashlib

def insert_paragraphs_from_one_article(db):

    with open('test.txt', 'r', encoding='utf-8') as file:
        article_url = "https://vaxxter.com/vaccines-2020-big-pharmas-admissions-of-fraud/"
        article_id = hashlib.md5(article_url.encode()).hexdigest()

        article = file.read()
        paragraphs = article.split("\n")
        paragraph_index = 0
        for paragraph in paragraphs:
            if len(paragraph) >= 100:
                db.insert_new_paragraph(str(article_id)+str(paragraph_index), article_url, paragraph)
                paragraph_index += 1

if __name__ == '__main__':
    db=database()
    batch_id = "test"

    insert_paragraphs_from_one_article(db)

    paragraphs_dict = db.get_all_paragraph_ids_in_dict()
    paragraphs = paragraphs_dict["https://vaxxter.com/vaccines-2020-big-pharmas-admissions-of-fraud/"]

    db.insert_new_batch(batch_id, paragraphs)