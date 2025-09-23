from faker import Faker

faker = Faker()


class TestGrades:
    def test_grades_stats_count_is_two(self, prepare_two_grades):
        g1, g2, stats = _prepare_two_grades
        assert stats.count == 2, f"Wrong grades count. Expected '2', Actual: {stats.count}"

    def test_grades_stats_min_correct(self, prepare_two_grades):
        g1, g2, stats = prepare_two_grades
        expected = min(g1.grade, g2.grade)
        assert stats.min == expected, f"Wrong min grades. Expected: {expected}, Actual: {stats.min}"

    def test_grades_stats_max_correct(self, prepare_two_grades):
        g1, g2, stats = prepare_two_grades
        expected = max(g1.grade, g2.grade)
        assert stats.max == expected, f"Wrong max grades. Expected: {expected}, Actual: {stats.max}"

    def test_grades_stats_avg_correct(self, prepare_two_grades):
        g1, g2, stats = prepare_two_grades
        expected = (g1.grade + g2.grade) / 2
        assert stats.avg == expected, f"Wrong avg grades. Expected: {expected}, Actual: {stats.avg}"
