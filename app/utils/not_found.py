from fastapi import HTTPException, status
from typing import Optional

def not_found(obj: object, model_class: type, id: Optional[int] = None) -> None:
    """

    Lança uma exceção HTTP 404 (Not Found) caso o objeto buscado no banco de dados não exista.

    ---
    ### **O que faz?**
    - **Valida** se um objeto retornado de uma consulta ao banco existe.
    - Se não existir (`obj is None`), lança uma exceção 404 com mensagem personalizada e amigável.

    ---
    ### **Parâmetros**
    - `id` (`int`): O ID buscado na consulta.
    - `obj` (`object`): Objeto retornado da consulta (ex: resultado de um select).
    - `model_class` (`type`): Classe do modelo relacionada ao objeto.
      - **Obs:** A classe deve possuir o atributo `nome`, para exibir na mensagem de erro.

    ---
    
    ### **Exemplo de uso**
    ```python
        not_found(produto_id, produto, ProductModel)
        not_found(cliente_id, cliente, ClientModel)
    ```

    ---

    ### **Mensagem de erro gerada**
    - `"Produto referente ao ID: 2 não encontrado."`
    - `"Cliente referente ao ID: 5 não encontrado."`

    """
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.nome} referente ao ID: {id} não encontrado."
        )
