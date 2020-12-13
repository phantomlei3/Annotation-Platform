import psycopg2
import psycopg2.extras


class database:
    '''
    Mediator Design Pattern
    PostgreSQL class functions as mediator to control all execution function for all tables
    PostgreSQL class rely on one connection from psycogn2
    '''

    def __init__(self):
        self.conn = psycopg2.connect("host='vcm-17659.vm.duke.edu' port='5432' dbname='annotation' user='annotator' password='duke'")
        self.cursor = self.conn.cursor()

    def insert_new_paragraph(self, paragraph_id, article_url, paragraph_content):
        '''
        insert one new paragraph into paragraphs table

        :param paragraph_id: string, hashlib.md5(article_url) ends with paragraph index started from 0
        :param article_url: string, article url
        :param paragraph_content: string, the content of paragraph
        '''
        insert_command = "INSERT INTO paragraphs(paragraph_id, article_url, paragraph_content) VALUES (%s, %s, %s)"

        self.cursor.execute(insert_command, [paragraph_id, article_url, paragraph_content])
        self.conn.commit()

    def get_all_paragraph_ids_in_dict(self):
        '''
        :return: a dict that contains article_url as key and a list of paragraphs IDs as value
                    eg. [www.google.com:[ exampleid1, exampleid2 ]]
        '''
        select_command = "SELECT paragraph_id, article_url FROM paragraphs"

        self.cursor.execute(select_command)
        results = self.cursor.fetchall()

        paragraph_dict = dict()
        # create the dictionary to aggregate the paragraphs
        for paragraph_id, article_url in results:
            if article_url not in paragraph_dict:
                paragraph_dict[article_url] = list()
            paragraph_dict[article_url].append(paragraph_id)

        return paragraph_dict

    def get_paragraph_content_from_paragraph_id(self, paragraph_id):
        '''

        :return: paragraph content according to the paragraph_id
        '''

        select_command = "SELECT paragraph_content FROM paragraphs WHERE paragraph_id = %s"

        self.cursor.execute(select_command, [paragraph_id])
        results = self.cursor.fetchall()

        return results[0][0]


    def insert_annotations(self, batch_id, paragraph_id, answer_time, annotations):
        '''

        :param batch_id: string
        :param paragraph_id: string
        :param answer_time: string, %Y-%m-%d %H:%M:%S
        :param annotations: a list of string
        '''

        insert_command = "INSERT INTO annotations(batch_id, paragraph_id, answer_time, annotations) VALUES (%s, %s, %s, %s)"

        self.cursor.execute(insert_command, [batch_id, paragraph_id, answer_time, annotations])
        self.conn.commit()

    def get_all_annotations(self):
        '''

        :return: a list of annotations in (batch_id, paragraph_id, answer_time, annotations)
        '''

        select_command = "SELECT * FROM annotations"

        self.cursor.execute(select_command)
        results = self.cursor.fetchall()

        return results


    def insert_new_batch(self, batch_id, paragraph_ids):
        '''

        insert new batch into batches table

        '''

        insert_command = "INSERT INTO batches(batch_id, paragraph_ids) VALUES (%s, %s)"

        self.cursor.execute(insert_command, [batch_id, paragraph_ids])
        self.conn.commit()

    def get_batch_paragraph_IDs(self, batch_id):
        '''

        get a list of paragraph IDs from given batch id

        :return: a list of string, paragraph IDs
        '''

        select_command = "SELECT paragraph_ids FROM batches WHERE batch_id = %s"

        self.cursor.execute(select_command, [batch_id])
        results = self.cursor.fetchall()
        print(results)

        return results[0][0]