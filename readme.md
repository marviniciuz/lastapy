# Last.fm Mosaic Downloader

Um script simples e eficiente em Python para automatizar a criação e download de mosaicos musicais (álbuns mais ouvidos) do Last.fm utilizando o serviço [Tapmusic](https://tapmusic.net/).

## Funcionalidades

- **Automático:** Gera a imagem baseada no seu perfil do Last.fm.
- **Flexível:** Permite configurar período (semana, mês, ano), tamanho da grade (3x3, 5x5) e legendas.
- **Organizado:** Salva o arquivo com data e nome do usuário para fácil arquivamento.
- **Leve:** Não baixa capas individualmente; consome a imagem pronta gerada pelo Tapmusic.

## Tecnologias e Ferramentas

* **[Python 3](https://www.python.org/)** - Linguagem utilizada.
* **[Requests](https://pypi.org/project/requests/)** - Biblioteca para requisições HTTP e download da imagem.
* **[Last.fm](https://www.last.fm/)** - Fonte dos dados de scrobble.
* **[Tapmusic](https://tapmusic.net/)** - Motor de geração dos mosaicos.

## Pré-requisitos

Necessario ter o python instalado.

## Instalação e Configuração

1. **Clone o repositório** (ou baixe o arquivo `.py`):
   ```bash
   git clone [https://github.com/seu-usuario/lastfm-mosaic.git](https://github.com/seu-usuario/lastfm-mosaic.git)
   cd lastfm-mosaic

   