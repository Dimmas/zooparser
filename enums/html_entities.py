from enum import Enum


class Tags(str, Enum):
    div = "div"
    p = "p"
    ul = "ul"
    li = "li"
    a = "a"


class Futures(str, Enum):
    id_ = "#"
    class_ = "."
