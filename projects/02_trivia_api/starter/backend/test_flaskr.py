import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_add_questions(self):
        res = self.client().post('/questions',json={"question": "Test?",
                                                     "answer": "answer_test",
                                                     "category": 1,
                                                     "difficulty": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        # self.assertTrue(data['total_questions'])
        # self.assertTrue(data['categories'])
       
    def test_delete_question(self):
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['deleted'], 6)
        # self.assertTrue(data['total_books'])
        # self.assertTrue(len(data['books']))
        # self.assertEqual(book, None)

    def test_404_if_qustion_does_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')
    
    def test_get_qustion(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
       
    def test_search_questions(self):
        res = self.client().post('/questions/search',json={"search": "Whose"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # def test_category_of_question(self):
    #     res = self.client().

    def test_play(self):
        res = self.client().post('/quizzes', json={"previous_questions": [],
                                                "quiz_category":{"type": "Art", "id":"2"} })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['quiz_category'])

    def test_404_error(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Page Not Found")

    # def test_422_error(self):
    #     res = self.client().get('/questions?page=x')
    #     data = json.loads(res.data)

    #     self.assertEqual(data["error"], 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Unprocessable Entity")

    def test_422_error(self):
        res = self.client().post('/questions',json={"question":"Test","answer":"Test","category":"Test","difficulty":1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable Entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()