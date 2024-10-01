# Simulador do Sistema Solar em 3D

Este projeto é um simulador de sistema solar em 3D desenvolvido em Python. Permite a visualização de corpos celestes, controle de um foguete, e utiliza o algoritmo A* para calcular rotas otimizadas entre pontos no espaço.

## Sumário

- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)

## Funcionalidades

- Simulação física realista de corpos celestes e do foguete.
- Controle manual do foguete via teclado.
- Cálculo de rotas otimizadas utilizando o algoritmo A*.
- Modo autônomo para o foguete seguir rotas automaticamente.
- Renderização gráfica em 3D utilizando PyOpenGL e Pygame.

## Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. O projeto depende das seguintes bibliotecas:

- `numpy`
- `pygame`
- `PyOpenGL`
- `pytest` (opcional, para testes)
- `networkx` (opcional, para o algoritmo A*)

## Instalação

### Clonando o Repositório

```
git clone https://github.com/EduardoFockinkSilva/exploracao_espacial.git
cd simulacao
```

### Usando Ambiente Virtual

Crie e ative um ambiente virtual para o projeto:

```
# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate
```

### Instalando as Dependências

Instale as dependências listadas no `requirements.txt`:

```
pip install -r requirements.txt
```

### Instalando o Pacote

Para instalar o simulador como um pacote Python:

```
pip install .
```

Ou, para instalação em modo de desenvolvimento:

```
pip install -e .
```

## Execução

Após a instalação, você pode executar o simulador usando o comando:

```
simulacao
```

Ou, se preferir, execute diretamente o arquivo `main.py`:

```
python simulacao/main.py
```

## Uso

### Controles do Foguete

- **`W`**: Acelerar o foguete para frente.
- **`S`**: Acelerar o foguete para trás.
- **`A`**: Rotacionar o foguete para a esquerda.
- **`D`**: Rotacionar o foguete para a direita.
- **`M`**: Alternar entre modo manual e autônomo.
- **`ESC`**: Sair do simulador.

### Definindo Pontos de Destino

No modo autônomo (a ser implementado), você poderá definir pontos de destino para o foguete seguir rotas otimizadas calculadas pelo algoritmo A*.

## Estrutura do Projeto

```
simulacao/
├── main.py
├── corpo_celeste.py
├── foguete.py
├── motor_fisico.py
├── motor_grafico.py
├── algoritmo_a_estrela.py  # (a ser implementado)
├── testes/
├── requirements.txt
├── setup.py
└── README.md
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório GitHub.

### Passos para Contribuir

1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção de bug: `git checkout -b minha-feature`.
3. Commit suas mudanças: `git commit -m 'Adicionar nova feature'`.
4. Envie para a branch principal: `git push origin minha-feature`.
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

- **Nome:** Eduardo Fockink Silva
- **Email:** eduardo.epublic@gmail.com
- **GitHub:** [EduardoFockinkSilva](https://github.com/EduardoFockinkSilva)

---

## Notas Adicionais

- **Algoritmo A\*:** Atualmente, o módulo `algoritmo_a_estrela.py` está reservado para futura implementação do algoritmo A*.
- **Testes:** Os testes unitários estão localizados na pasta `testes/`. Você pode executá-los usando o `pytest`:

  ```
  pytest testes/
  ```

- **Assets:** As pastas `assets/texturas/` e `assets/modelos/` estão preparadas para futuros recursos gráficos, como texturas e modelos 3D.

## Dúvidas Frequentes

### O simulador não está exibindo nada na tela. O que fazer?

- Verifique se todas as dependências estão corretamente instaladas.
- Certifique-se de que sua placa gráfica suporta OpenGL e que os drivers estão atualizados.

### Como posso ajustar a escala dos corpos celestes?

- Você pode modificar os parâmetros de escala diretamente no arquivo `main.py` ao criar instâncias de `CorpoCeleste` e `Foguete`.

### Posso adicionar mais planetas ao simulador?

- Sim! Basta criar novas instâncias de `CorpoCeleste` com os parâmetros desejados e adicioná-las ao `motor_fisico` e à lista `corpos` para renderização.

---

Espero que este arquivo `README.md` forneça todas as informações necessárias para começar a usar e contribuir com o projeto. Se tiver mais alguma dúvida ou precisar de assistência adicional, não hesite em entrar em contato!
