import pytest
from src.utils import eleva_quadrado, require_permission
from http import HTTPStatus


@pytest.mark.parametrize("test_input, expected", [(2, 4),(10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)
    assert resultado == expected

@pytest.mark.parametrize("test_input, exc_class, msg", [("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"), (None, TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'")])
def test_eleva_quadrado_falha(test_input, exc_class, msg):  
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
        assert str(exc.value) == msg  



def test_requires_permission_success(mocker):
    #Given 
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    mocker.patch("src.utils.get_jwt_identity") 
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user) 
    decorated_function = require_permission("admin")(lambda: "success")
    
    #When
    result = decorated_function()

    #Then 
    assert result == "success"


def test_requires_permission_failure(mocker):
    #Given - O que é fornecido para o teste: definição das variáveis mocks e funções mocks
    mock_user = mocker.Mock()
    mock_user.role.name = "user"
 
    
    #When - O que é executado 
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user) 
    decorated_function = require_permission("admin")(lambda: "success")
    
    #Then - O que é verificado
    result = decorated_function()
    assert result == ({"message": "User don't have access!"}, HTTPStatus.FORBIDDEN)