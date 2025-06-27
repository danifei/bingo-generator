📘 Idiomas dispoñibles: [English](/README.en.md) Galego

<p align="center">
  <img src="/assets/bingo_card_11.png" alt="Image 1" width="30%" style="margin-right: 10px;">
  <img src="/assets/bingo_card_39.png" alt="Image 2" width="30%">
</p>

# Xerador de Bingo
Esto só é un repo pra xerar un xerador de cartóns de bingo. De carallada.


## Instalación

Clona o repositorio

```bash
git clone https://github.com/danifei/bingo-generator.git
```

Só se necesita a librería pillow. Instalaa:

```bash
pip install pillow
```

## Funcionamento

O arquivo principal é [generator.py](/generator.py). Nel poderás atopar as variables a configurar (en maiúsculas).

Na carpeta [/background](/background/), coloca as imaxes de fondo que queres utilizar nos teus cartóns. Logo, no arquivo [events.txt](/events.txt) pon os eventos que queres considerar como casillas dos teus cartóns. Pon un evento por fila.

Feito isto, só tes que correr:

```bash
python generator.py
```

