import pytest

from homoglyphs_fork import (
    Categories,
    Languages,
    Homoglyphs,
    STRATEGY_LOAD,
    STRATEGY_IGNORE,
    STRATEGY_REMOVE,
)


class TestBenchmarkCategories:
    @pytest.mark.benchmark
    def test_detect(self, benchmark):
        def categories_detect():
            return [
                Categories.detect("d"),
                Categories.detect("Д"),
                Categories.detect("?"),
                Categories.detect("ㅡ"),
            ]

        result = benchmark(categories_detect)

        assert result == ["LATIN", "CYRILLIC", "COMMON", "HANGUL"]

    @pytest.mark.benchmark
    def test_alphabet(self, benchmark):
        def categories_alphabet():
            return [
                Categories.get_alphabet(["LATIN"]),
                Categories.get_alphabet(["CYRILLIC"]),
                Categories.get_alphabet(["HANGUL"]),
            ]

        benchmark(categories_alphabet)


class TestBenchmarkLanguages:
    @pytest.mark.benchmark
    def test_detect(self, benchmark):
        def languages_detect():
            Languages.detect("d")
            Languages.detect("Д")
            Languages.detect("?")

        benchmark(languages_detect)

    @pytest.mark.benchmark
    def test_alphabet(self, benchmark):
        def languages_alphabet():
            Languages.get_alphabet({"en"})
            Languages.get_alphabet({"ru"})

        benchmark(languages_alphabet)


class TestBenchmarkHomoglyphs:
    @pytest.mark.benchmark
    def test_get_table(self, benchmark):
        alphabet = Categories.get_alphabet(["LATIN", "CYRILLIC", "HANGUL"])

        def get_table():
            return Homoglyphs.get_table(alphabet)

        benchmark(get_table)

    @pytest.mark.benchmark
    def test_to_ascii_strategy_load(self, benchmark):
        def to_ascii():
            Homoglyphs(strategy=STRATEGY_LOAD).to_ascii("d")
            Homoglyphs(strategy=STRATEGY_LOAD).to_ascii("Д")
            Homoglyphs(strategy=STRATEGY_LOAD).to_ascii("?")

        benchmark(to_ascii)

    @pytest.mark.benchmark
    def test_to_ascii_strategy_ignore(self, benchmark):
        def to_ascii():
            Homoglyphs(strategy=STRATEGY_IGNORE).to_ascii("d")
            Homoglyphs(strategy=STRATEGY_IGNORE).to_ascii("Д")
            Homoglyphs(strategy=STRATEGY_IGNORE).to_ascii("?")

        benchmark(to_ascii)

    @pytest.mark.benchmark
    def test_to_ascii_strategy_remove(self, benchmark):
        def to_ascii():
            Homoglyphs(strategy=STRATEGY_REMOVE).to_ascii(
                "d",
            )
            Homoglyphs(strategy=STRATEGY_REMOVE).to_ascii("Д")
            Homoglyphs(strategy=STRATEGY_REMOVE).to_ascii("?")

        benchmark(to_ascii)
