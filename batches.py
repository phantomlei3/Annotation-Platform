from PostgreSQL.database import database
from datetime import datetime

class Batch:
    '''
    Batch class represents one batch and contains a list of paragraphs id for annotation
    Each batch has a unique batch id corresponding to a random password generated for annotator to enter at the start interface
    '''

    def __init__(self, batch_id):
        self.batch_id = batch_id
        self.db = database()
        self.paragraph_ids_list = self.db.get_batch_paragraph_IDs(batch_id)

    def get_first_paragraph_id(self):
        '''

        :return: string, the first paragraph if in paragraph_ids_list
        '''
        return self.paragraph_ids_list[0]

    def get_next_paragraph_id(self, previous_paragraph_id):
        '''

        get the next paragraph id based on previous_paragraph_id

        :return: string, paragraph_id if there is a next paragraph id
                None, if there is no next paragraph id
        '''

        index = self.paragraph_ids_list.index(previous_paragraph_id)
        if index+1 >= len(self.paragraph_ids_list):
            return None
        return self.paragraph_ids_list[index+1]

    def save_annotation(self, paragraph_id, annotations):
        '''

        :param paragraph_id: string
        :param annotations: a list of string
        '''

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.insert_annotations(self.batch_id, paragraph_id, current_time, annotations)

    def get_paragraph(self, paragraph_id):
        '''

        :return: string, the content of a paragraph given paragraph_id
        '''
        return self.db.get_paragraph_content_from_paragraph_id(paragraph_id)

