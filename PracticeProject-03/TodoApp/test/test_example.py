import pytest

def test_equal_or_not():
    assert 3 == 3

def test_is_instance():
    assert isinstance('this is a string', str)
    assert isinstance('10', str)
def test_boolean():
    validated = True
    assert validated == True
    assert ('hello' == 'world') is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)
def greater_and_less_than():
    assert 7 > 3
    assert 3 < 7
def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [True, False]
    assert 1 in num_list
    assert 7 not in any_list
    assert all(num_list)
    assert any(any_list)


class Student :
    def __init__(self, first_name : str, last_name : str, major : str, years : int) :
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee () :
    return Student('John' , 'Doe' , 'Computer Science' , 3)

def test_preson_initialization(default_employee):
    assert default_employee.first_name == 'John'
    assert default_employee.last_name == 'Doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3