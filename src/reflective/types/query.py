class RQuery:

    def __init__(self, query: any):
        self.query: any = query

    def __repr__(self) -> str:
        return f"RQuery({self.query})"

    def __str__(self) -> str:
        return f"{self.query}"

    def __eq__(self, other: any) -> bool:
        if isinstance(other, RQuery):
            return self.query == other.query
        return self.query == other

    def __neq__(self, other: any) -> bool:
        if isinstance(other, RQuery):
            return self.query != other.query
        return self.query != other


class RQueryResult:

    def __init__(self, query: any, result: list):
        if not isinstance(query, RQuery):
            query = RQuery(query)
        self.query: RQuery = query
        self.result: list = result
        self._index = 0

    def __repr__(self) -> str:
        return f"RQueryResult({self.query}, {self.result})"

    def __str__(self) -> str:
        return f"{self.query}: {self.result}"

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.result):
            self._index += 1
            return self.result[self._index - 1]
        else:
            raise StopIteration

    def __eq__(self, other: any) -> bool:
        if isinstance(other, RQueryResult):
            return self.query == other.query and self.result == other.result
        return self.query == other and self.result == other

    def __neq__(self, other: any) -> bool:
        if isinstance(other, RQueryResult):
            return self.query != other.query or self.result != other.result
        return self.query != other or self.result != other

    def __len__(self) -> int:
        return len(self.result)

    def __getitem__(self, index: int) -> any:
        return self.result[index]

    def __setitem__(self, index: int, value: any) -> None:
        if isinstance(value, RQueryResult):
            self.result[index] = value.result
        else:
            self.result[index] = value

    def __delitem__(self, index: int) -> None:
        del self.result[index]

    def __contains__(self, item: any) -> bool:
        return item in self.result

    def __add__(self, other: any) -> any:
        if isinstance(other, RQueryResult):
            return self.result + other.result
        return self.result + other
