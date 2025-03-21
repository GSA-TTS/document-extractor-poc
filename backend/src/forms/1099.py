from src.forms.form import Form


class TenNinetyNineNec(Form):
    def identifier(self) -> str:
        return "1099-NEC"

    def form_matches(self) -> str:
        return "1099-NEC"

    def queries(self) -> list[str]:
        return []
