import unittest


class Textanalyzer:
    '''
    тут докментация к функции analyze_text()

    function analyze_text() is very convenient for analyzing text
    here you can recognize absolutely not obvious functionality:
        use analyze_text(your_text) to get more information about your_text
        and output will be like the following:
            {"words": amount_of_words, "sentences": amount_of_sentences, "letters": amount_of_letters, "avgLettersPerWord": avgerage_Letters_Per_Word}
        in case you put not an acceptable value itll return: 'Exception'
        and that's all functionality
    '''
    def analyze_text(self, text: str):
        try:
            return {"words": len(text.split(' ')),
                    "sentences": text.count('.'),
                    "letters": len(text),
                    "avgLettersPerWord": len(text.replace(' ', '')) / len(text.split(' '))}
        except Exception:
            return 'Exception'


class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Textanalyzer()

    # нормальный тест но короткий
    def test_one(self):
        self.assertEqual(self.analyzer.analyze_text('asdf. test'), {'avgLettersPerWord': 4.5, 'letters': 10, 'sentences': 1, 'words': 2})

    # dare mo kore wo yomu koto wo shitenai soshite nihongo no keyboarudo wo motenai dakara egirisugo dde kaku
    def test_two(self):
        self.assertEqual(self.analyzer.analyze_text('この 文章 は 日本語 だから 誰でも よむ こと を 出来ない'), {'avgLettersPerWord': 2.3, 'letters': 32, 'sentences': 0, 'words': 10})

    # bool
    def test_three(self):
        self.assertEqual(self.analyzer.analyze_text(True), 'Exception')

    # int
    def test_four(self):
        self.assertEqual(self.analyzer.analyze_text(123), 'Exception')

    # лист
    def test_five(self):
        self.assertEqual(self.analyzer.analyze_text(['asdf']), 'Exception')

    # the hardest test
    def test_six(self):
        self.assertEqual(self.analyzer.analyze_text('ъ'), {'avgLettersPerWord': 1.0, 'letters': 1, 'sentences': 0, 'words': 1})

    # ошибка MemoryError жаль
    def test_seven(self):
        self.assertEqual(self.analyzer.analyze_text('a'*1000000), {'avgLettersPerWord': 1000000.0, 'letters': 1000000, 'sentences': 0, 'words': 1})


if __name__ == '__main__':
    unittest.main()
