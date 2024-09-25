def aplicar_mascara(number: str, mask: str):
    """
    aplica máscaras em geral, com exceção para moeda

    mask: ex 00.000.000/0000-00, todos os "0"s serão substituidos
    """
    number = "".join(filter(str.isdigit, str(number)))
    formatted_number = ""
    number_index = 0
    mask_index = 0
    while mask_index < len(mask) and number_index < len(number):
        if mask[mask_index] == "0":
            formatted_number += number[number_index]
            number_index += 1
        else:
            formatted_number += mask[mask_index]
        mask_index += 1
    if number_index < len(number):
        formatted_number += number[number_index:]
    return formatted_number
