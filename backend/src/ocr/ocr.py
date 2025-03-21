from abc import ABC, abstractmethod


class Ocr(ABC):
    @abstractmethod
    def extract_raw_text(self, s3_url: str) -> list[str]:
        pass

    @abstractmethod
    def scan(self, s3_url: str, queries: list[str] | None = None) -> dict[str, dict[str, str | float]]:
        pass
