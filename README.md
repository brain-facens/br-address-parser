# br-address-parser
This module is a simple parser for Brazilian addresses. This receives a complete address string and split it in 'street', 'number', 'complement', 'neighborhood', 'city' and 'state'.

This code is a [br-address-parser](https://github.com/Minutrade/br-address-parser) port for Python.
Credits should go to the original implementation contributors.

## How to install

```
pip install br_address_parser
```

## How to use

```py
from br_address_parser import parse

complete_address = "Av. Brasil, 1245 - Bloco 2 Ap 203 - Centro - Belo Horizonte - MG"
parsed_address = parse(complete_address)
```

The above example transforms the string "Av. Brasil, 1245 - Bloco 2 Ap 203 - Centro - Belo Horizonte - MG" into the following object:

```json
{
    "street": "Av. Brasil",
    "number": "1245",
    "complement": "Bloco 2 Ap 203",
    "neighborhood": "Centro",
    "city": "Belo Horizonte",
    "state": "MG"
}
```

If you want to fill some fields with default values when they are empty, then you can use `defaultFields` parameter:

```py
complete_address = "AV ANAVILLE 1-QD 3 LT 4 - RESIDENCIAL ANAVILLE - ANAPOLIS - GO"
parsed_address = parse(complete_address, {"number": "S/N"})
```

The above example transforms will put `S/N` in the `number` field, because parsed address returns empty `number`:

```json
{
   "street": "AV ANAVILLE 1",
   "number": "S/N",
   "complement": "QD 3 LT 4",
   "neighborhood": "RESIDENCIAL ANAVILLE",
   "city": "ANAPOLIS",
   "state": "GO"
}
```

When the address cannot be parsed, the `parse` function returns `None`.

## How to test

```
make test
```

## License

This project is licensed under the terms of the MIT license.
