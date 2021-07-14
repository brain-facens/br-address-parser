import logging
import re


def black_list(
    street: str,
    number: str = None,
    complement: str = None,
    neighborhood: str = None,
    city: str = None,
    state: str = None,
) -> bool:
    if re.match(r"df", state, re.I):
        return False
    if re.match(r"^(RUA|R)$", street, re.I):
        return True
    if re.match(r"^(S\/?N)$", neighborhood, re.I):
        return True

    return re.search(r"(apto|bloco|apartamento|casa|ap|bl\s\d+)\b", street, re.I)


def sanitize_address(completeAddress: str) -> str:
    completeAddress = re.sub(r"(,\-|\-,)", "-", completeAddress)
    completeAddress = re.sub(r"(\d)\.(\d{2,})", r"\1\2", completeAddress)
    completeAddress = re.sub(r"\.\s", " ", completeAddress, flags=re.I)
    completeAddress = re.sub(r"(.)([-,])", r"\1 \2", completeAddress, flags=re.I)
    completeAddress = re.sub(r"([-,])(.)", r"\1 \2", completeAddress, flags=re.I)
    completeAddress = re.sub(
        r"(\d+)([a-z]+)(\d+)", r"\1 \2 \3", completeAddress, flags=re.I
    )
    completeAddress = re.sub(
        r"([a-z]+)(\d+)([a-z]+)", r"\1 \2 \3", completeAddress, flags=re.I
    )
    completeAddress = re.sub(r"(\d+)([a-z]+)", r"\1 \2", completeAddress, flags=re.I)
    completeAddress = re.sub(r"([a-z]+)(\d+)", r"\1 \2", completeAddress, flags=re.I)
    completeAddress = re.sub(r"\s\s+", r" ", completeAddress, flags=re.I)
    completeAddress = re.sub(r"\-\s\-", r"-", completeAddress)

    return completeAddress


def format_address(parsed_address: dict) -> dict:
    return {
        **parsed_address,
        "street": re.sub(r"\s,\s", ", ", parsed_address["street"], flags=re.I),
    }


def apply_default(parsed_address: dict, default_fields: dict) -> dict:
    empty_keys = filter(
        lambda x: parsed_address[x].strip() == "", parsed_address.keys()
    )

    for key in empty_keys:
        if key in default_fields.keys():
            parsed_address[key] = default_fields[key]
    return parsed_address


def parse(complete_address: str, default_fields: dict = None) -> dict:
    sanitized_address = sanitize_address(complete_address)
    flags = re.I | re.MULTILINE
    patterns = [
        # LINHA 99 - COMPLEMENT - NEIGHBORHOOD - CITY - DF
        r"(?P<street>LINHA\s\d+)\s[-,]\s(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - COMPLEMENT - NEIGHBORHOOD - CITY - DF
        r"(?P<street>.*)\s[-,]\s(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>DF)",
        # STREET - COMPLEMENT - NUMBER - NEIGHBORHOOD - CITY - GO
        r"(?P<street>.*(?<!\s))(\s[-,]\s|\s?,\s?)((((NR?|CASA|NUMERO)\s?)(?P<number>\d+|S\/?N)))(\s[-/]\s|\s)(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>GO)",
        # STREET - COMPLEMENT - NEIGHBORHOOD - CITY - GO
        r"(?P<street>.*(?<!\s))\s-\s(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>GO)",
        # BR-999 - 10 - NEIGHBORHOOD - CITY - ST
        r"(?P<street>^(\w{2})[\s-]\d+)\s[-,]\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - N99 COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))(\s[-,]\s|\s?,\s?)((((NR?|CASA|NUMERO)\s?)(?P<number>\d+|S\/?N)))(\s[-/]\s|\s)(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - 99 - COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))(\s[-,]\s|\s?,\s?)(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))(\s[-/]\s|\s)(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - 99/COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))(\s[-,]\s|\s?,\s?)(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s?\/\s?(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET 99 COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s(-\s)?(?P<complement>((CASA|APTO|AP)\b\s).*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - 99 X - COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s(?P<complement>\w\s-.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - 99 - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s[-,]\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET 99 - COMPLEMENT - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s-\s(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET 00 COMPLEMENT- COMPLEMENT2 99 - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s(?P<complement>.*-.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # STREET - STREET2 99 - NEIGHBORHOOD - CITY - ST
        r"(?P<street>.*(?<!\s))\s(((NR?|CASA|NUMERO)\s?)?(?P<number>(\d+|S\/?N)))\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # RURAL WITH COMPLEMENT
        r"(?P<street>^(SITIO|FAZENDA|ESTRADA).*)\s[-,]\s(?P<complement>.*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
        # RURAL WITHOUT COMPLEMENT
        r"(?P<street>^(SITIO|FAZENDA|ESTRADA).*)\s[-,]\s(?P<neighborhood>.*)\s[-,]\s(?P<city>.*)\s[-,]\s(?P<state>\w{2})",
    ]
    # Acho que o match n rola aqui
    pattern = next(
        filter(lambda x: re.search(x, sanitized_address, flags), patterns), None
    )
    if not pattern:
        return None
    logging.info("Pattern found: {}".format(pattern))
    # matches = re.match("".join(patterns), sanitized_address, flags).groupdict()
    matches = re.search(pattern, sanitized_address, flags).groupdict()
    import pdb

    # pdb.set_trace()
    if matches:
        black_listed = black_list(**matches)
        if black_listed:
            logging.info(
                "Sentences {} is listed on black list {}".format(
                    complete_address, black_listed
                )
            )
            return None

        parsed_address = format_address(
            {
                "street": matches["street"],
                "number": matches["number"] if "number" in matches.keys() else "",
                "complement": matches["complement"]
                if "complement" in matches.keys()
                else "",
                "neighborhood": matches["neighborhood"]
                if "neighborhood" in matches.keys()
                else "",
                "city": matches["city"],
                "state": matches["state"],
            }
        )
        if default_fields:
            parsed_address = apply_default(parsed_address, default_fields)
        return parsed_address

    return None
